from pydantic import BaseModel


class AIQueryResponse(BaseModel):
    success: bool
    user_prompt: str = ""
    generated_sql: str = ""
    error: str | None = None