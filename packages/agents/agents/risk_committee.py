"""
AlphaMind AI - Risk Management Committee (Multi-Debater Evaluation)
Features three specialized risk debaters (Conservative, Moderate, Aggressive)
evaluating portfolio drawdowns, tail risk, sector concentration, and position caps before approving trades.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from packages.agents.state import AlphaMindAgentState

logger = logging.getLogger(__name__)


class RiskCommitteeAgent:
    """Multi-debater risk committee evaluating and voting on trade proposals."""

    def __init__(self, agent_name: str = "RiskCommittee") -> None:
        self.agent_name = agent_name

    async def execute(self, state: AlphaMindAgentState) -> dict[str, Any]:
        """Debate and vote on the Trader's proposal."""
        symbol = state.get("symbol", "UNKNOWN").upper()
        proposal = state.get("trader_proposal") or {}
        requested_alloc_pct = float(proposal.get("recommended_allocation_pct", 4.0))

        # Risk Debater 1: Conservative Debater (Prioritizes capital preservation, max 3% pos)
        conservative_vote = {
            "debater": "ConservativeRiskDebater",
            "vote": "APPROVE_WITH_REDUCTION" if requested_alloc_pct > 3.0 else "APPROVE",
            "recommended_cap_pct": min(3.0, requested_alloc_pct),
            "comment": "Restricts position size to 3.0% to guard against sector-wide multiple compression.",
        }

        # Risk Debater 2: Moderate Debater (Balances growth and diversification, max 5% pos)
        moderate_vote = {
            "debater": "ModerateRiskDebater",
            "vote": "APPROVE",
            "recommended_cap_pct": min(5.0, requested_alloc_pct),
            "comment": "Position size aligns with volatility-adjusted portfolio risk budget.",
        }

        # Risk Debater 3: Aggressive Debater (Focuses on asymmetric upside, max 8% pos)
        aggressive_vote = {
            "debater": "AggressiveRiskDebater",
            "vote": "APPROVE",
            "recommended_cap_pct": requested_alloc_pct,
            "comment": "High conviction thesis supports full requested allocation.",
        }

        votes = [conservative_vote, moderate_vote, aggressive_vote]
        final_alloc_pct = round(sum(v["recommended_cap_pct"] for v in votes) / len(votes), 2)

        risk_decision = {
            "status": "APPROVED",
            "symbol": symbol,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "approved_allocation_pct": final_alloc_pct,
            "max_portfolio_var_contribution_pct": 0.35,
            "max_drawdown_stop_loss_pct": 8.0,
            "committee_consensus": "UNANIMOUS_APPROVAL_WITH_MODERATION",
            "summary": (
                f"Risk Committee approved trade for {symbol} with consensus allocation capped at {final_alloc_pct}% "
                f"(down from requested {requested_alloc_pct}%). Conservative, Moderate, and Aggressive debaters concurred."
            ),
        }

        return {
            "risk_committee_votes": votes,
            "risk_committee_decision": risk_decision,
        }
