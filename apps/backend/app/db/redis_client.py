"""
AlphaMind AI - Redis Connection Manager & Async Pool
"""

from __future__ import annotations

import logging

import redis.asyncio as aioredis

from apps.backend.app.core.config import settings

logger = logging.getLogger(__name__)

redis_pool: aioredis.Redis | None = None


async def get_redis() -> aioredis.Redis:
    """Get initialized Redis async connection instance."""
    global redis_pool
    if redis_pool is None:
        redis_pool = aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
        )
    return redis_pool


async def close_redis() -> None:
    """Close Redis pool connection."""
    global redis_pool
    if redis_pool is not None:
        await redis_pool.close()
        redis_pool = None
