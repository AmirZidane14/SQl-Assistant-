from pydantic import BaseModel


class WorkflowPreviewRequest(BaseModel):
    prompt: str


class WorkflowPreviewResponse(BaseModel):
    success: bool
    user_prompt: str
    generated_sql: str
    explanation: str
    valid: bool
    error: str | None = None


class WorkflowExecuteRequest(BaseModel):
    query: str


class WorkflowExecuteResponse(BaseModel):
    success: bool
    columns: list[str]
    rows: list[list[object]]
    count: int
    error: str | None = None