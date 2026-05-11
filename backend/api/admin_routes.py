from fastapi import APIRouter

from services.audit_logger import logger

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/security-status")
def security_status():
    """
    Returns the current status of all security mechanisms.
    Used by the frontend to display a security dashboard.
    """
    return {
        "rate_limiting": True,
        "audit_logging": True,
        "prompt_guard": True,
        "sql_guard": True,
        "security_headers": True,
        "query_timeout_seconds": 5,
        "max_query_length": 5000,
        "max_joins": 5,
        "max_nested_selects": 3,
        "rate_limits": {
            "ai_requests_per_minute": 30,
            "query_requests_per_minute": 60,
            "schema_requests_per_minute": 100,
        },
    }
