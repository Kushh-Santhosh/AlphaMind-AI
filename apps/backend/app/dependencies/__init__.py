"""
Backend Dependencies — FastAPI Dependency Injection Stubs.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Async SQLAlchemy session dependency for FastAPI routes.
    Full implementation pending Milestone 4 (database engine wiring).
    """
    raise NotImplementedError("Database session implementation pending Milestone 4.")
    yield  # type: ignore[misc]
