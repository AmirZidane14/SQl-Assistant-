from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """
    Request body for executing a SQL query.
    The query is sanitized and validated before execution.
    """
    query: str = Field(..., min_length=1, max_length=5000, description="SQL query to execute")


class ValidationResult(BaseModel):
    """
    Result of SQL validation.
    """
    valid: bool
    error: str | None = None


class QueryResult(BaseModel):
    """
    Result of a successfully executed SQL query.
    """
    success: bool
    columns: list[str] = []
    rows: list[list[object]] = []
    count: int = 0


class QueryResponse(BaseModel):
    """
    Combined response: validation result + execution result.
    """
    valid: bool
    error: str | None = None
    success: bool
    columns: list[str] = []
    rows: list[list[object]] = []
    count: int = 0