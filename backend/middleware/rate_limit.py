import re
import time
from collections import defaultdict
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


RATE_LIMITS = {
    "ai": 30,
    "query": 60,
    "schema": 100,
}


class RateLimiter(BaseHTTPMiddleware):
    """
    In-memory per-IP rate limiter using a sliding window.
    Blocks excessive requests with HTTP 429.
    """

    def __init__(self, app):
        super().__init__(app)
        self._requests: dict[str, list[float]] = defaultdict(list)

    def _clean_old(self, ip: str, now: float, window: int) -> None:
        cutoff = now - window
        self._requests[ip] = [t for t in self._requests[ip] if t > cutoff]

    def _limit(self, ip: str, endpoint: str) -> tuple[bool, int]:
        now = time.time()
        window = 60

        self._clean_old(ip, now, window)

        key = "schema"
        if "/ai/" in endpoint:
            key = "ai"
        elif "/query" in endpoint or "/workflow/execute" in endpoint:
            key = "query"

        limit = RATE_LIMITS[key]
        count = len(self._requests[ip])

        if count >= limit:
            return False, limit

        self._requests[ip].append(now)
        return True, limit

    async def dispatch(self, request: Request, call_next):
        ip = request.client.host if request.client else "unknown"
        endpoint = request.url.path

        allowed, limit = self._limit(ip, endpoint)

        if not allowed:
            return JSONResponse(
                status_code=429,
                content={
                    "success": False,
                    "error": f"Rate limit exceeded. Maximum {limit} requests per minute.",
                    "code": "RATE_LIMITED",
                },
                headers={
                    "Retry-After": "60",
                    "X-RateLimit-Limit": str(limit),
                    "X-RateLimit-Remaining": "0",
                },
            )

        response = await call_next(request)

        remaining = limit - len(self._requests.get(ip, []))
        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = str(max(0, remaining))

        return response
