from fastapi import APIRouter

from schemas.workflow_response import (
    WorkflowPreviewRequest,
    WorkflowPreviewResponse,
    WorkflowExecuteRequest,
    WorkflowExecuteResponse,
)
from services.query_workflow import workflow

router = APIRouter(prefix="/api", tags=["workflow"])


@router.post("/workflow/preview", response_model=WorkflowPreviewResponse)
def preview_query(body: WorkflowPreviewRequest):
    """
    Full AI workflow step 1: generate SQL and explanation from natural language.
    Does NOT execute the query — use /workflow/execute for that.
    """
    result = workflow.preview(body.prompt)
    return WorkflowPreviewResponse(
        success=result["success"],
        user_prompt=result["user_prompt"],
        generated_sql=result["generated_sql"],
        explanation=result["explanation"],
        valid=result["valid"],
        error=result.get("error"),
    )


@router.post("/workflow/execute", response_model=WorkflowExecuteResponse)
def execute_workflow_query(body: WorkflowExecuteRequest):
    """
    Full AI workflow step 2: execute a user-approved SQL query.
    The SQL is always re-validated server-side before execution.
    """
    result = workflow.execute(body.query)
    return WorkflowExecuteResponse(
        success=result["success"],
        columns=result["columns"],
        rows=result["rows"],
        count=result["count"],
        error=result.get("error"),
    )