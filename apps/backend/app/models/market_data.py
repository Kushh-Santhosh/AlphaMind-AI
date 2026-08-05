"""
TimescaleDB Market Bars Hyper-Table Model
"""

from __future__ import annotations

import uuid

from sqlalchemy import BigInteger, Column, DateTime, Float, String, func
from sqlalchemy.dialects.postgresql import UUID

from apps.backend.app.models.base import Base


class MarketBarModel(Base):
    """
    SQLAlchemy ORM model mapped to TimescaleDB hyper-table 'market_bars_daily'.
    Partitioned by time and symbol.
    """

    __tablename__ = "market_bars_daily"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    time = Column(DateTime(timezone=True), nullable=False, index=True, server_default=func.now())
    symbol = Column(String(20), nullable=False, index=True)
    asset_class = Column(String(30), nullable=False, default="equity")
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(BigInteger, nullable=False)
    vwap = Column(Float, nullable=True)
    provider = Column(String(50), nullable=False, default="polygon_io")
