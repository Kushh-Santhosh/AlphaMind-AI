"""
Market Bar Repository Pattern Implementation
"""

from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.models.market_data import MarketBarModel
from apps.backend.app.repositories.base import BaseRepository


class MarketRepository(BaseRepository[Any]):
    """Async repository for market price bar CRUD and hyper-table queries."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, entity_id: str) -> MarketBarModel | None:
        """Fetch market bar by ID."""
        result = await self.session.execute(
            select(MarketBarModel).where(MarketBarModel.id == entity_id)
        )
        return result.scalar_one_or_none()

    async def get_latest_bars(self, symbol: str, limit: int = 100) -> list[MarketBarModel]:
        """Fetch latest OHLCV market bars for a symbol."""
        stmt = (
            select(MarketBarModel)
            .where(MarketBarModel.symbol == symbol.upper())
            .order_by(MarketBarModel.time.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def save_bars(self, bars: list[dict[str, Any]]) -> int:
        """Batch save cleaned market bars to TimescaleDB."""
        models = [
            MarketBarModel(
                symbol=bar["symbol"],
                open=bar["open"],
                high=bar["high"],
                low=bar["low"],
                close=bar["close"],
                volume=bar["volume"],
                vwap=bar.get("vwap"),
                provider=bar.get("provider", "polygon_io"),
            )
            for bar in bars
        ]
        self.session.add_all(models)
        await self.session.flush()
        return len(models)
