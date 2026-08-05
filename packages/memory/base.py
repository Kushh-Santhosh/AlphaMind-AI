"""
Hierarchical AI Memory System Interfaces
"""

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class MemorySystemInterface(Protocol):
    """Interface for Working, Episodic, Semantic, and Investment Journal memory."""

    async def record_journal_forecast(self, forecast_data: dict[str, Any]) -> str: ...

    async def retrieve_semantic_context(self, query: str, top_k: int = 5) -> dict[str, Any]: ...
