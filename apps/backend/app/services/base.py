"""
Service Layer Base Interface
"""

from typing import Protocol, runtime_checkable


@runtime_checkable
class BaseServiceInterface(Protocol):
    """Base interface for all backend business service classes."""

    ...
