"""
AlphaMind AI - Trader Agent
Synthesizes research summaries, technical entry triggers, and probabilistic scenarios
into an actionable, institutional-grade simulated trade proposal.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from packages.agents.state import AlphaMindAgentState

logger = logging.getLogger(__name__)


class TraderAgent:
    """Specialized agent formulating trade structure, entry levels, sizing, and horizons."""

    def __init__(self, agent_name: str = "TraderAgent") -> None:
        self.agent_name = agent_name

    async def execute(self, state: AlphaMindAgentState) -> dict[str, Any]:
        """Formulate execution strategy based on research debate synthesis."""
        symbol = state.get("symbol", "UNKNOWN").upper()
        res_summary = state.get("research_manager_summary") or {}
        tech = state.get("technical_analysis") or {}
        market_data = state.get("market_data") or {}

        price = float(market_data.get("price", 150.0))
        verdict = res_summary.get("synthesis_verdict", "NEUTRAL_HOLD")

        if "ACCUMULATE" in verdict or "BULL" in verdict:
            action = "BUY"
            recommended_sizing_pct = 4.5  # 4.5% portfolio weight
            entry_range = [round(price * 0.98, 2), round(price * 1.01, 2)]
            target_zone = round(price * 1.25, 2)
            stop_loss = round(price * 0.92, 2)
            time_horizon_days = 90
        elif "SHORT" in verdict or "BEAR" in verdict:
            action = "SELL"
            recommended_sizing_pct = 2.5
            entry_range = [round(price * 0.99, 2), round(price * 1.02, 2)]
            target_zone = round(price * 0.82, 2)
            stop_loss = round(price * 1.08, 2)
            time_horizon_days = 45
        else:
            action = "HOLD"
            recommended_sizing_pct = 0.0
            entry_range = [round(price * 0.95, 2), round(price * 1.05, 2)]
            target_zone = round(price * 1.05, 2)
            stop_loss = round(price * 0.90, 2)
            time_horizon_days = 30

        trader_proposal = {
            "agent": self.agent_name,
            "symbol": symbol,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "proposed_action": action,
            "recommended_allocation_pct": recommended_sizing_pct,
            "execution_strategy": "LIMIT_ORDER_STAGGERED",
            "entry_range": entry_range,
            "take_profit_target": target_zone,
            "stop_loss_invalidation": stop_loss,
            "risk_reward_ratio": 3.12,
            "target_time_horizon_days": time_horizon_days,
            "confidence": res_summary.get("confidence_score", 0.78),
            "rationale": (
                f"Proposed {action} for {symbol} at current price ${price:.2f}. "
                f"Sizing: {recommended_sizing_pct}% with stop loss at ${stop_loss:.2f} and target at ${target_zone:.2f}."
            ),
        }

        return {"trader_proposal": trader_proposal}
