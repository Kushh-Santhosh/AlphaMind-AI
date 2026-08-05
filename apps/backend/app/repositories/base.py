"""
Repository Pattern Base Interface
"""

from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseRepository(Generic[T]):
    """Generic repository pattern interface for database interactions."""

    async def get_by_id(self, entity_id: str) -> T | None:
        raise NotImplementedError

    async def list_all(self) -> list[T]:
        raise NotImplementedError

    async def create(self, entity: T) -> T:
        raise NotImplementedError
