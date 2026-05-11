from fastapi import APIRouter, HTTPException

from schemas.query_schema import QueryRequest, QueryResponse
from services.query_executor import executor

router = APIRouter(prefix="/api", tags=["query"])


@router.post("/query", response_model=QueryResponse)
def execute_query(body: QueryRequest):
    """
    Validates and executes a raw SQL query.
    Only SELECT queries are allowed; all others are rejected by the SQL validator.
    """
    result = executor.execute(body.query)

    return QueryResponse(
        valid=result["success"] if "error" not in result else (result["error"] is None),
        error=result.get("error"),
        success=result["success"],
        columns=result["columns"],
        rows=result["rows"],
        count=result["count"],
    )