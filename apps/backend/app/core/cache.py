"""
AlphaMind AI - Redis Cache Engine (Read-Through, Write-Through, TTL & Key Namespace)
"""

from __future__ import annotations

import json
import logging
from collections.abc import Callable
from typing import Any, TypeVar, cast

from apps.backend.app.db.redis_client import get_redis

logger = logging.getLogger(__name__)

T = TypeVar("T")


class CacheKeyBuilder:
    """Namespace builder for Redis cache keys."""

    @staticmethod
    def quote_key(symbol: str) -> str:
        return f"quote:{symbol.upper()}"

    @staticmethod
    def bars_key(symbol: str, timeframe: str) -> str:
        return f"bars:{symbol.upper()}:{timeframe}"

    @staticmethod
    def macro_key(series_id: str) -> str:
        return f"macro:{series_id}"

    @staticmethod
    def sec_key(ticker: str, form_type: str, fiscal_year: int) -> str:
        return f"sec:{ticker.upper()}:{form_type.upper()}:{fiscal_year}"


class RedisCacheManager:
    """
    Redis Cache Manager enforcing TTL policies, Cache Invalidation, Read-Through, and Write-Through patterns.
    """

    # TTL Policy Map in Seconds
    TTL_POLICIES: dict[str, int] = {
        "quote": 60,  # 60 seconds hot tick cache
        "bars": 300,  # 5 minutes price bar cache
        "macro": 86400,  # 24 hours macro data cache
        "sec": 3600,  # 1 hour SEC filing cache
        "default": 300,
    }

    @classmethod
    def get_ttl(cls, namespace: str) -> int:
        """Get TTL in seconds for a key namespace."""
        return cls.TTL_POLICIES.get(namespace, cls.TTL_POLICIES["default"])

    @classmethod
    async def get(cls, key: str) -> dict[str, Any] | None:
        """Get deserialized JSON value from Redis."""
        try:
            r = await get_redis()
            val = await r.get(key)
            if val:
                data = json.loads(val)
                return cast(dict[str, Any], data)
        except Exception as exc:
            logger.warning("Redis GET failed for key '%s': %s", key, exc)
        return None

    @classmethod
    async def set(cls, key: str, value: dict[str, Any], namespace: str = "default") -> bool:
        """Set value in Redis with namespace TTL policy."""
        try:
            r = await get_redis()
            ttl = cls.get_ttl(namespace)
            serialized = json.dumps(value)
            await r.set(key, serialized, ex=ttl)
            return True
        except Exception as exc:
            logger.warning("Redis SET failed for key '%s': %s", key, exc)
            return False

    @classmethod
    async def invalidate(cls, key: str) -> bool:
        """Invalidate specific cache key."""
        try:
            r = await get_redis()
            await r.delete(key)
            return True
        except Exception as exc:
            logger.warning("Redis INVALIDATE failed for key '%s': %s", key, exc)
            return False

    @classmethod
    async def read_through(
        cls,
        key: str,
        fetch_func: Callable[[], Any],
        namespace: str = "default",
    ) -> dict[str, Any]:
        """
        Read-Through Cache Pattern:
        Attempts reading from cache first. If cache miss, executes fetch_func and populates cache.
        """
        cached_data = await cls.get(key)
        if cached_data is not None:
            logger.debug("CACHE HIT: Key '%s'", key)
            cached_data["_cached"] = True
            return cached_data

        logger.debug("CACHE MISS: Key '%s'. Executing fetch supplier...", key)
        fresh_data = await fetch_func()
        if fresh_data and isinstance(fresh_data, dict):
            await cls.set(key, fresh_data, namespace=namespace)
            fresh_data["_cached"] = False
            return cast(dict[str, Any], fresh_data)
        return cast(dict[str, Any], fresh_data)

    @classmethod
    async def write_through(
        cls,
        key: str,
        value: dict[str, Any],
        write_db_func: Callable[[dict[str, Any]], Any],
        namespace: str = "default",
    ) -> Any:
        """
        Write-Through Cache Pattern:
        Writes data to database first, then updates cache atomically.
        """
        # Step 1: Write to primary storage
        result = await write_db_func(value)

        # Step 2: Write to cache
        await cls.set(key, value, namespace=namespace)
        return result
