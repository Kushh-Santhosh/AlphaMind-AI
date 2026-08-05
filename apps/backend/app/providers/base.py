"""
Data Provider Base Abstract Interface
"""

from typing import Protocol, runtime_checkable


@runtime_checkable
class BaseProviderInterface(Protocol):
    """Base interface for all market and data providers."""

    provider_name: str

    async def is_healthy(self) -> bool: ...
