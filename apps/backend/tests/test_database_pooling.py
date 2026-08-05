"""
Unit and Stress Tests for HARD-03 Database Connection Pooling & Lifecycle Management
"""

import pytest

from apps.backend.app.core.config import settings
from apps.backend.app.db.postgres import close_db_engine, engine


def test_database_pool_configuration_settings():
    """Verify pool parameters are properly configured from environment settings."""
    assert settings.DB_POOL_SIZE == 20
    assert settings.DB_MAX_OVERFLOW == 10
    assert settings.DB_POOL_TIMEOUT == 30
    assert settings.DB_POOL_RECYCLE == 1800
    assert settings.DB_POOL_PRE_PING is True


def test_engine_pool_initialization():
    """Verify SQLAlchemy engine pool properties match settings."""
    assert engine.pool.size() == settings.DB_POOL_SIZE
    assert engine.pool._max_overflow == settings.DB_MAX_OVERFLOW


@pytest.mark.asyncio
async def test_engine_shutdown_cleanup():
    """Verify engine disposal cleanup helper executes without errors."""
    await close_db_engine()
