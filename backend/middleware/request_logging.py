import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs all incoming HTTP requests with timing information.
    Integrates with the audit logger for security events.
    """

    async def dispatch(self, request: Request, call_next):
        from services.audit_logger import logger

        ip = request.client.host if request.client else "unknown"
        path = request.url.path
        method = request.method
        start = time.time()

        response = await call_next(request)

        duration_ms = int((time.time() - start) * 1000)
        status = response.status_code

        logger.log(
            event="http_request",
            endpoint=f"{method} {path}",
            ip=ip,
            extra={
                "method": method,
                "status_code": status,
                "duration_ms": duration_ms,
                "user_agent": request.headers.get("user-agent", ""),
            },
        )

        return response
