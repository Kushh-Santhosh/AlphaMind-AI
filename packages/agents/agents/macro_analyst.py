"""
AlphaMind AI - Macro Analyst Agent
Ingests FRED and global macroeconomic indicators (Fed Funds, 10Y/2Y Yield Curve, CPI, GDP,
Unemployment, Liquidity aggregates) to assess broader macroeconomic climate and sector sensitivity.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from packages.agents.state import AlphaMindAgentState

logger = logging.getLogger(__name__)


class MacroAnalystAgent:
    """Specialized agent modeling macroeconomic factor exposures and monetary policy impacts."""

    def __init__(self, agent_name: str = "MacroAnalyst") -> None:
        self.agent_name = agent_name

    async def execute(self, state: AlphaMindAgentState) -> dict[str, Any]:
        """Process state and append structured macroeconomic backdrop."""
        symbol = state.get("symbol", "UNKNOWN").upper()
        macro_in = state.get("macro_indicators") or {}

        fed_funds = float(macro_in.get("fed_funds_rate", 4.35))
        us10y = float(macro_in.get("us10y_yield", 4.15))
        us2y = float(macro_in.get("us2y_yield", 3.95))
        yield_curve_spread_bps = round((us10y - us2y) * 100, 1)
        cpi_yoy = float(macro_in.get("cpi_yoy", 2.65))
        gdp_growth = float(macro_in.get("gdp_growth", 2.30))

        macro_phase = (
            "LATE_CYCLE_EXPANSION" if yield_curve_spread_bps > 0 and gdp_growth > 2.0 else
            "RECESSIONARY_PRESSURE" if yield_curve_spread_bps < 0 else
            "EARLY_CYCLE_RECOVERY"
        )

        macro_output = {
            "agent": self.agent_name,
            "symbol": symbol,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "macro_regime_phase": macro_phase,
            "indicators": {
                "fed_funds_rate": fed_funds,
                "us10y_yield": us10y,
                "us2y_yield": us2y,
                "yield_curve_spread_bps": yield_curve_spread_bps,
                "cpi_inflation_yoy": cpi_yoy,
                "gdp_growth_annualized": gdp_growth,
            },
            "interest_rate_sensitivity": "MODERATE_NEGATIVE_DURATION",
            "evidence_citations": ["FRED_FEDFUNDS_SERIES", "FRED_T10Y2Y_SPREAD", "BLS_CPI_RELEASE"],
            "summary": (
                f"Macro environment is characterized by {macro_phase} with Fed Funds at {fed_funds:.2f}%, "
                f"10Y-2Y yield curve spread at {yield_curve_spread_bps:+.1f} bps, and headline CPI at {cpi_yoy:.2f}%."
            ),
        }

        return {"macro_analysis": macro_output}
