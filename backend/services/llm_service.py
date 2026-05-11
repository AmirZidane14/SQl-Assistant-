import json
import re
import urllib.request
import urllib.error
import os

from core.config import settings
from services.sql_validator import validate_query


GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models"


def call_gemini(prompt: str) -> tuple[str | None, str | None]:
    """
    Send a prompt to the Gemini API and return the raw text response.

    Returns:
        (response_text, None) on success
        (None, error_message) on failure
    """
    api_key = settings.GEMINI_API_KEY
    if not api_key or api_key == "your_gemini_api_key_here":
        return None, "GEMINI_API_KEY is not configured"

    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    url = f"{GEMINI_API_URL}/{model}:generateContent?key={api_key}"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 1024,
            "topP": 0.8,
        },
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))

    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        if e.code == 403:
            return None, "Invalid or expired Gemini API key"
        if e.code == 429:
            return None, "Gemini API rate limit exceeded. Please try again later"
        return None, f"Gemini API error ({e.code}): {body[:200]}"

    except urllib.error.URLError as e:
        return None, "Unable to reach Gemini API. Check your internet connection"

    except Exception as e:
        return None, f"Unexpected error calling Gemini API: {str(e)[:100]}"

    try:
        candidate = data["candidates"][0]
        content = candidate["content"]["parts"][0]["text"]
        return content.strip(), None
    except (KeyError, IndexError):
        return None, "Unexpected response format from Gemini API"


def extract_sql(text: str) -> tuple[str | None, str | None]:
    """
    Clean and extract the SQL query from LLM output.
    Removes markdown code fences, backticks, explanations.
    Returns (clean_sql, error_message).
    """
    if not text:
        return None, "Empty response from Gemini"

    sql = text.strip()

    code_block_pattern = re.compile(r"```(?:sql)?\s*([\s\S]+?)\s*```", re.IGNORECASE)
    match = code_block_pattern.search(sql)
    if match:
        sql = match.group(1).strip()
    else:
        sql = sql.strip("`").strip()

    sql = re.sub(r"^sql\s*:?\s*", "", sql, flags=re.IGNORECASE).strip()
    sql = re.sub(r"^\s*(SELECT|WITH)\s+", r"\1 ", sql, flags=re.IGNORECASE)

    lines = sql.split("\n")
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if re.match(r"^(here'?s?|explanation|note|sql|answer|result|query):", line, re.IGNORECASE):
            continue
        cleaned_lines.append(line)
    sql = "\n".join(cleaned_lines).strip()

    sql = re.sub(r"^[^S]*SELECT", "SELECT", sql, flags=re.IGNORECASE)
    sql = re.sub(r"\n[^S]*$", "", sql.strip()).strip()

    if not re.match(r"^\s*(SELECT|WITH)", sql, re.IGNORECASE):
        return None, "Generated output does not appear to be a valid SELECT query"

    is_valid, error = validate_query(sql)
    if not is_valid:
        return None, f"Generated SQL failed safety validation: {error}"

    return sql, None