"""
AlphaMind AI - Production PostgreSQL & TimescaleDB Async Connection Manager

Configures SQLAlchemy AsyncEngine pool settings via environment variables,
supports PgBouncer transaction pooling mode, and manages session lifecycle.
"""

from __future__ import annotations

import logging
from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from apps.backend.app.core.config import settings

logger = logging.getLogger(__name__)

# Connect Arguments for PgBouncer transaction pooling compatibility
connect_args: dict[str, Any] = {}
if settings.DB_PGBOUNCER_MODE:
    connect_args["statement_cache_size"] = 0

# Async SQLAlchemy Engine initialized from environment configuration
engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_recycle=settings.DB_POOL_RECYCLE,
    pool_pre_ping=settings.DB_POOL_PRE_PING,
    connect_args=connect_args,
)

# Async Session Factory
async_session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency injection yield for FastAPI async DB sessions with automatic cleanup."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def close_db_engine() -> None:
    """Dispose database engine connection pool on application shutdown."""
    logger.info("Closing PostgreSQL database engine connection pool...")
    await engine.dispose()
