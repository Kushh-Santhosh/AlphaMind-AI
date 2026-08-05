"""
Multi-Asset Market Data Engine Interfaces
"""

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class MarketEngineInterface(Protocol):
    """Interface for multi-asset failover market data ingestion engine."""

    async def get_bars(self, symbol: str, timeframe: str) -> list[dict[str, Any]]: ...

    async def get_quote(self, symbol: str) -> dict[str, Any]: ...
