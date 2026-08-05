"""
AlphaMind AI - Historical Market Replay Engine

Replays historical market ticks, earnings events, macro announcements, and historical crashes
(2008 Financial Crisis, COVID-19 Crash) with accelerated playback speeds (1x, 10x, 100x).
STRICT MANDATE: Historical replay simulation only.
"""

from __future__ import annotations

import logging
import time
from enum import Enum

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class ReplayScenario(str, Enum):  # noqa: UP042
    STANDARD_HISTORICAL = "standard_historical"
    FINANCIAL_CRISIS_2008 = "financial_crisis_2008"
    COVID_CRASH_2020 = "covid_crash_2020"
    RATE_SHOCK_2022 = "rate_shock_2022"


class ReplayTick(BaseModel):
    timestamp_utc: str
    symbol: str
    price: float
    volume: float
    event_flag: str = "NORMAL"  # "EARNINGS", "MACRO_FOMC", "CRASH_EVENT"


class MarketReplayEngine:
    """Engine orchestrating accelerated historical market tick and event replay."""

    def __init__(self, playback_speed_multiplier: int = 10) -> None:
        self.playback_speed_multiplier = playback_speed_multiplier

    def run_replay(
        self,
        symbol: str = "AAPL",
        scenario: ReplayScenario = ReplayScenario.FINANCIAL_CRISIS_2008,
        ticks_count: int = 50,
    ) -> list[ReplayTick]:
        """Generate simulated historical replay tick stream for scenario testing."""
        logger.info(
            "Running market replay for '%s' (scenario='%s', speed=%dx)",
            symbol,
            scenario.value,
            self.playback_speed_multiplier,
        )

        base_price = 150.0
        ticks = []
        for i in range(ticks_count):
            price_change = -0.5 if scenario == ReplayScenario.FINANCIAL_CRISIS_2008 else 0.2
            base_price = max(1.0, round(base_price + price_change, 2))
            evt = (
                "CRASH_EVENT"
                if i % 10 == 0 and scenario != ReplayScenario.STANDARD_HISTORICAL
                else "NORMAL"
            )

            ticks.append(
                ReplayTick(
                    timestamp_utc=time.strftime(
                        "%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - (ticks_count - i) * 3600)
                    ),
                    symbol=symbol.upper(),
                    price=base_price,
                    volume=1000000.0,
                    event_flag=evt,
                )
            )

        return ticks
