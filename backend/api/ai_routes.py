from fastapi import APIRouter

from schemas.ai_request import AIQueryRequest
from schemas.ai_response import AIQueryResponse
from services.prompt_builder import build_prompt, detect_injection
from services.llm_service import call_gemini, extract_sql

router = APIRouter(prefix="/api", tags=["ai"])


@router.post("/ai/generate", response_model=AIQueryResponse)
def generate_sql(body: AIQueryRequest):
    """
    Takes a natural language question, sends it to Gemini with schema context,
    and returns a validated SQL query for user review.

    The SQL is NEVER auto-executed — the user must explicitly approve it.
    """
    is_injection, inject_error = detect_injection(body.prompt)
    if is_injection:
        return AIQueryResponse(
            success=False,
            user_prompt=body.prompt,
            generated_sql="",
            error=inject_error,
        )

    prompt = build_prompt(body.prompt)

    raw_response, api_error = call_gemini(prompt)
    if api_error or raw_response is None:
        return AIQueryResponse(
            success=False,
            user_prompt=body.prompt,
            generated_sql="",
            error=api_error or "Empty response from Gemini",
        )

    sql, extract_error = extract_sql(raw_response)
    if extract_error or sql is None:
        return AIQueryResponse(
            success=False,
            user_prompt=body.prompt,
            generated_sql="",
            error=f"AI output could not be parsed: {extract_error}",
        )

    return AIQueryResponse(
        success=True,
        user_prompt=body.prompt,
        generated_sql=sql,
        error=None,
    )