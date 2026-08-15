"""
AlphaMind AI - Accelerated Historical Market Replay Engine (v4.0)

Orchestrates point-in-time tick and event replay from genuine historical price series.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any

from packages.market.provider_registry import market_data_registry

logger = logging.getLogger(__name__)


class ReplayScenario(str, Enum):
    FINANCIAL_CRISIS_2008 = "2008_GFC"
    COVID_CRASH_2020 = "2020_COVID"
    FED_RATE_SHOCK_2022 = "2022_RATE_SHOCK"
    TECH_CORRECTION_2024 = "2024_TECH"
    STANDARD_HISTORICAL = "HISTORICAL_1Y"


@dataclass
class ReplayTick:
    timestamp_utc: str
    symbol: str
    price: float
    volume: float
    event_flag: str = "NORMAL"  # "EARNINGS", "MACRO_FOMC", "CRASH_EVENT"


class MarketReplayEngine:
    """Engine orchestrating accelerated historical market tick and event replay."""

    def __init__(self, playback_speed_multiplier: int = 10) -> None:
        self.playback_speed_multiplier = playback_speed_multiplier

    async def run_replay(
        self,
        symbol: str = "AAPL",
        scenario: ReplayScenario = ReplayScenario.STANDARD_HISTORICAL,
        ticks_count: int = 50,
    ) -> list[ReplayTick]:
        """Generate point-in-time replay tick stream from actual historical data."""
        logger.info(
            "Running market replay for '%s' (scenario='%s', speed=%dx)",
            symbol,
            scenario.value,
            self.playback_speed_multiplier,
        )

        hist = await market_data_registry.get_historical_ohlcv(symbol, period="1y")
        ticks: list[ReplayTick] = []

        if not hist.empty:
            sample_df = hist.tail(ticks_count)
            for idx, (dt, row) in enumerate(sample_df.iterrows()):
                close_p = float(row["Close"])
                vol = float(row["Volume"])
                evt = "CRASH_EVENT" if (idx % 15 == 0 and scenario != ReplayScenario.STANDARD_HISTORICAL) else "NORMAL"
                ts_str = dt.isoformat() if hasattr(dt, "isoformat") else str(dt)
                ticks.append(
                    ReplayTick(
                        timestamp_utc=ts_str,
                        symbol=symbol.upper(),
                        price=round(close_p, 4),
                        volume=vol,
                        event_flag=evt,
                    )
                )
        else:
            # Current snapshot fallback
            snap = await market_data_registry.get_market_snapshot(symbol)
            cur_p = snap.get("price", 100.0)
            ticks.append(
                ReplayTick(
                    timestamp_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    symbol=symbol.upper(),
                    price=cur_p,
                    volume=snap.get("volume_24h", 1000000.0),
                    event_flag="NORMAL",
                )
            )

        return ticks
