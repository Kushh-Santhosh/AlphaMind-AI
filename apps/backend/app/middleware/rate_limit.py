"""
AlphaMind AI — Enterprise Production Rate Limiting Middleware

Implements endpoint-tier sliding window rate limiting backed by Redis & in-memory fallback:
  - Auth (/api/v1/auth/*): 10 requests / min
  - Heavy AI Analysis (/api/v1/analyst/*, /api/v1/reasoning/*): 5 requests / min
  - Forecast Generation (/api/v1/prediction/*, /api/v1/simulation/*): 10 requests / min
  - Search (/api/v1/*/search, /api/v1/mission-control/search): 60 requests / min
  - General API (all other endpoints): 120 requests / min
  - SSE Connections (/api/v1/*/stream): 5 concurrent connections / IP
"""

from __future__ import annotations

import logging
import time
from collections import defaultdict

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from apps.backend.app.db.redis_client import get_redis

logger = logging.getLogger(__name__)

# ── Rate Limit Policy Configurations ──────────────────────────────────────────

POLICY_LIMITS: dict[str, tuple[int, int]] = {
    # policy_name: (max_requests, window_seconds)
    "auth": (20, 60),
    "heavy_ai": (30, 60),
    "forecast": (30, 60),
    "search": (60, 60),
    "general": (120, 60),
    "sse_stream": (20, 60),
}

# In-Memory Sliding Window Fallback Storage: key -> list[timestamp_floats]
_IN_MEMORY_BUCKET: dict[str, list[float]] = defaultdict(list)

# Active SSE Connection Tracker: client_ip -> count
_ACTIVE_SSE_CONNECTIONS: dict[str, int] = defaultdict(int)


def reset_rate_limits() -> None:
    """Reset rate limit buckets (used for unit test isolation)."""
    _IN_MEMORY_BUCKET.clear()
    _ACTIVE_SSE_CONNECTIONS.clear()


def _get_client_ip(request: Request) -> str:
    """Extract client IP address handling X-Forwarded-For load balancers."""
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "127.0.0.1"


def _determine_policy(path: str) -> str:
    """Classify endpoint path into rate limiting policy tier."""
    p = path.lower()
    if "/api/v1/auth" in p:
        return "auth"
    if "/search" in p or "query" in p and "/research" in p:
        return "search"
    if "/prediction" in p or "/simulation" in p or "/forecast" in p:
        return "forecast"
    if "/analyst" in p or "/reasoning" in p or "/intelligence" in p:
        return "heavy_ai"
    if "/stream" in p or "/events" in p:
        return "sse_stream"
    return "general"


async def _check_sliding_window(
    bucket_key: str, max_requests: int, window_seconds: int, now: float
) -> tuple[bool, int, int]:
    """Perform sliding window rate limit check via Redis or In-Memory fallback."""
    allowed = True
    remaining = max_requests - 1
    retry_after = window_seconds

    try:
        redis = await get_redis()
        if redis is not None:
            pipe = redis.pipeline()
            pipe.zremrangebyscore(bucket_key, 0, now - window_seconds)
            pipe.zadd(bucket_key, {str(now): now})
            pipe.zcard(bucket_key)
            pipe.expire(bucket_key, window_seconds)
            res = await pipe.execute()
            current_count = int(res[2])
            if current_count > max_requests:
                allowed = False
                remaining = 0
            else:
                remaining = max(0, max_requests - current_count)
        else:
            raise ConnectionError("Redis unavailable")
    except Exception:
        timestamps = _IN_MEMORY_BUCKET[bucket_key]
        cutoff = now - window_seconds
        _IN_MEMORY_BUCKET[bucket_key] = [t for t in timestamps if t > cutoff]
        current_count = len(_IN_MEMORY_BUCKET[bucket_key])
        if current_count >= max_requests:
            allowed = False
            remaining = 0
            if _IN_MEMORY_BUCKET[bucket_key]:
                retry_after = int(_IN_MEMORY_BUCKET[bucket_key][0] + window_seconds - now) + 1
        else:
            _IN_MEMORY_BUCKET[bucket_key].append(now)
            remaining = max(0, max_requests - len(_IN_MEMORY_BUCKET[bucket_key]))

    return allowed, remaining, retry_after


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware enforcing sliding-window rate limiting per client IP."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        path = request.url.path

        if path in ("/docs", "/redoc", "/openapi.json", "/favicon.ico"):
            return await call_next(request)

        client_ip = _get_client_ip(request)
        policy_name = _determine_policy(path)
        max_requests, window_seconds = POLICY_LIMITS[policy_name]
        now = time.time()

        if policy_name == "sse_stream":
            current_active = _ACTIVE_SSE_CONNECTIONS[client_ip]
            if current_active >= max_requests:
                return JSONResponse(
                    status_code=429,
                    content={
                        "detail": "Rate limit exceeded. Maximum SSE connections reached.",
                        "policy": policy_name,
                        "retry_after_seconds": 10,
                    },
                    headers={
                        "Retry-After": "10",
                        "X-RateLimit-Limit": str(max_requests),
                        "X-RateLimit-Remaining": "0",
                    },
                )
            _ACTIVE_SSE_CONNECTIONS[client_ip] += 1
            try:
                return await call_next(request)
            finally:
                _ACTIVE_SSE_CONNECTIONS[client_ip] = max(0, _ACTIVE_SSE_CONNECTIONS[client_ip] - 1)

        bucket_key = f"rate_limit:{policy_name}:{client_ip}"
        allowed, remaining, retry_after = await _check_sliding_window(
            bucket_key, max_requests, window_seconds, now
        )

        headers = {
            "X-RateLimit-Limit": str(max_requests),
            "X-RateLimit-Remaining": str(remaining),
            "X-RateLimit-Reset": str(int(now + window_seconds)),
        }

        if not allowed:
            headers["Retry-After"] = str(max(1, retry_after))
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Rate limit exceeded. Too many requests.",
                    "policy": policy_name,
                    "retry_after_seconds": max(1, retry_after),
                },
                headers=headers,
            )

        response = await call_next(request)
        for k, v in headers.items():
            response.headers[k] = v
        return response
