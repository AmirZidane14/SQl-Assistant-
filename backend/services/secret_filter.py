import re
import os

SECRET_PATTERNS = [
    (re.compile(r"API[_\s]?KEY\s*[=:]\s*['\"]?([A-Za-z0-9_\-]{8,})['\"]?", re.IGNORECASE), r"API_KEY=********"),
    (re.compile(r"(api[_\s]?key|secret|token|password)\s*[=:]\s*['\"]?([^\s'\"]{8,})['\"]?", re.IGNORECASE), r"\1=********"),
    (re.compile(r"Bearer\s+[A-Za-z0-9_\-]{16,}", re.IGNORECASE), "Bearer ********"),
    (re.compile(r"sk-[A-Za-z0-9_\-]{32,}"), "sk-********************************"),
    (re.compile(r"AIza[A-Za-z0-9_\-]{20,}"), "AIza************************************"),
    (re.compile(r"eyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}"), "JWT_TOKEN ********"),
    (re.compile(r"[A-Za-z0-9+/]{40,}==?"), "BASE64_SECRET ********"),
    (re.compile(r"GEMINI_API_KEY\s*[=:]\s*['\"]?([^\s'\"]{8,})['\"]?", re.IGNORECASE), r"GEMINI_API_KEY=********"),
]


def filter_secrets(text: str) -> str:
    """
    Replace any detected secrets in text with masked placeholders.
    Safe to use on log lines, error messages, and API responses.
    """
    if not text:
        return text

    result = text

    for pattern, replacement in SECRET_PATTERNS:
        result = pattern.sub(replacement, result)

    # Also filter environment variable values from error traces
    env_file = os.getenv("ENV_FILE", "")
    if env_file and env_file in result:
        result = result.replace(env_file, "********")

    return result


def safe_error_message(error: str | Exception) -> str:
    """
    Convert an exception or raw error string into a safe user-facing message.
    Never leaks internal paths, secrets, or stack traces.
    """
    if isinstance(error, Exception):
        message = str(error)
    else:
        message = error

    # Filter any secrets that might have leaked
    message = filter_secrets(message)

    # Truncate very long messages
    if len(message) > 300:
        message = message[:300] + "..."

    return message
