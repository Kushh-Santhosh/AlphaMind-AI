"""
AlphaMind AI - Adversarial Research Debate Graph
Orchestrates multi-round dialectical debate between Bullish Researcher, Bearish Researcher,
and Research Manager referee within LangGraph state-driven topology.
"""

from __future__ import annotations

import logging
from typing import Any

from packages.agents.agents.bear_researcher import BearResearcherAgent
from packages.agents.agents.bull_researcher import BullResearcherAgent
from packages.agents.agents.research_manager import ResearchManagerAgent
from packages.agents.registry import GraphBuilder
from packages.agents.state import AlphaMindAgentState

logger = logging.getLogger(__name__)


class ResearchDebateGraph:
    """Orchestrates structured adversarial research debate."""

    def __init__(self, rounds: int = 2) -> None:
        self.rounds = rounds
        self.bull_agent = BullResearcherAgent()
        self.bear_agent = BearResearcherAgent()
        self.manager_agent = ResearchManagerAgent()

    async def run_debate(self, initial_state: AlphaMindAgentState) -> AlphaMindAgentState:
        """Run multi-round debate mutating shared LangGraph state."""
        state = dict(initial_state)
        symbol = state.get("symbol", "UNKNOWN").upper()
        logger.info("Initiating %d-round research debate for %s", self.rounds, symbol)

        debate_transcript: list[dict[str, Any]] = []

        for r in range(1, self.rounds + 1):
            # Bull node execution
            bull_res = await self.bull_agent.execute(state)
            state.update(bull_res)
            debate_transcript.append({
                "round": r,
                "speaker": "BullResearcher",
                "stance": "BULLISH",
                "points": state["bull_thesis"]["primary_catalysts"],
                "summary": state["bull_thesis"]["core_argument"],
            })

            # Bear node execution
            bear_res = await self.bear_agent.execute(state)
            state.update(bear_res)
            debate_transcript.append({
                "round": r,
                "speaker": "BearResearcher",
                "stance": "BEARISH",
                "points": state["bear_thesis"]["primary_vulnerabilities"],
                "summary": state["bear_thesis"]["core_argument"],
            })

        # Research Manager synthesis
        manager_res = await self.manager_agent.execute(state)
        state.update(manager_res)
        state["debate_transcript"] = debate_transcript
        state["debate_rounds"] = self.rounds

        return state
