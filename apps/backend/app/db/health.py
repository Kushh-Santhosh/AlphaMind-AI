"""
AlphaMind AI - Consolidated Multi-Database Health Monitor
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from sqlalchemy import text

from apps.backend.app.db.chroma_client import ChromaDBClientManager
from apps.backend.app.db.neo4j_client import Neo4jClientManager
from apps.backend.app.db.postgres import async_session_factory
from apps.backend.app.db.redis_client import get_redis

logger = logging.getLogger(__name__)


class DatabaseHealthAggregator:
    """Aggregates health checks across PostgreSQL, TimescaleDB, Redis, ChromaDB, and Neo4j."""

    @staticmethod
    async def check_all_databases() -> dict[str, Any]:
        """Perform health ping on all 5 persistence engines."""
        health_status: dict[str, Any] = {
            "postgres_timescaledb": "unhealthy",
            "redis": "unhealthy",
            "chromadb": "unhealthy",
            "neo4j": "unhealthy",
            "overall_healthy": False,
        }

        # 1. PostgreSQL / TimescaleDB Check
        try:
            async with async_session_factory() as session:
                result = await session.execute(text("SELECT 1"))
                if result.scalar() == 1:
                    health_status["postgres_timescaledb"] = "healthy"
        except Exception as exc:
            logger.warning("PostgreSQL health check failed: %s", exc)

        # 2. Redis Check
        try:
            r = await get_redis()
            ping_res = r.ping()
            if asyncio.iscoroutine(ping_res):
                ping_res = await ping_res
            if ping_res:
                health_status["redis"] = "healthy"
        except Exception as exc:
            logger.warning("Redis health check failed: %s", exc)

        # 3. ChromaDB Check
        try:
            chroma = ChromaDBClientManager()
            ch_res = await chroma.check_health()
            if ch_res.get("status") == "healthy":
                health_status["chromadb"] = "healthy"
        except Exception as exc:
            logger.warning("ChromaDB health check failed: %s", exc)

        # 4. Neo4j Check
        try:
            neo = Neo4jClientManager()
            n_res = await neo.check_health()
            if n_res.get("status") == "healthy":
                health_status["neo4j"] = "healthy"
        except Exception as exc:
            logger.warning("Neo4j health check failed: %s", exc)

        # Evaluate Overall Health
        health_status["overall_healthy"] = all(
            v == "healthy" for k, v in health_status.items() if k != "overall_healthy"
        )
        return health_status
