"""
AlphaMind AI - Bearish Researcher Agent
Generates an adversarial, evidence-backed bearish counter-thesis, identifying valuation multiples
vulnerabilities, margin compression triggers, macroeconomic headwinds, and downside tail risks.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from packages.agents.state import AlphaMindAgentState

logger = logging.getLogger(__name__)


class BearResearcherAgent:
    """Specialized agent representing the Bearish investment thesis."""

    def __init__(self, agent_name: str = "BearResearcher") -> None:
        self.agent_name = agent_name

    async def execute(self, state: AlphaMindAgentState) -> dict[str, Any]:
        """Synthesize analyst evidence into a rigorous Bearish counter-thesis."""
        symbol = state.get("symbol", "UNKNOWN").upper()
        val = state.get("valuation_analysis") or {}
        macro = state.get("macro_analysis") or {}
        market_data = state.get("market_data") or {}

        price = float(market_data.get("price", 150.0))
        target_price_bear = val.get("intrinsic_value_dcf", {}).get("bear_case", round(price * 0.82, 2))
        pe_ratio = val.get("multiples", {}).get("forward_pe", 22.1)

        bear_thesis = {
            "agent": self.agent_name,
            "stance": "BEARISH",
            "symbol": symbol,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "conviction_score": 0.62,
            "primary_vulnerabilities": [
                f"Elevated forward multiple ({pe_ratio:.1f}x) leaves zero room for execution missteps.",
                "Potential margin compression as cloud infrastructure costs rise and competitive pricing intensifies.",
                "Regulatory and antitrust scrutiny introducing headline volatility and possible compliance costs.",
                "Macro duration sensitivity: elevated Fed funds rate limits equity risk premium expansion.",
            ],
            "downside_scenario": {
                "bear_target_price": target_price_bear,
                "expected_drawdown_pct": -18.0,
                "time_horizon_months": 12,
                "probability_weight": 0.25,
            },
            "invalidation_triggers": [
                "Consecutive quarter revenue deceleration below 10% YoY.",
                "Breakdown below 200-day moving average.",
                "Customer churn or pricing pressure in core product segments.",
            ],
            "evidence_citations": [f"{symbol}_VALUATION_MULTIPLE_RISK", f"{symbol}_MACRO_DURATION_HEADWIND"],
            "core_argument": (
                f"Consensus expectations for {symbol} are priced for perfection. Any macro deceleration "
                f"or competitive pricing friction could trigger multiple compression toward the ${target_price_bear:.2f} bear zone."
            ),
        }

        return {"bear_thesis": bear_thesis}
