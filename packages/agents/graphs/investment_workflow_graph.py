"""
AlphaMind AI - Full Investment Workflow Graph
Executes end-to-end institutional workflow:
Data Validation -> 8 Specialized Analysts Parallel Fan-Out -> Adversarial Research Debate ->
Trader Proposal -> Risk Committee Deliberation -> Portfolio Strategy Allocation -> Paper Simulation.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from packages.agents.agents.earnings_analyst import EarningsAnalystAgent
from packages.agents.agents.fundamental_analyst import FundamentalAnalystAgent
from packages.agents.agents.macro_analyst import MacroAnalystAgent
from packages.agents.agents.market_regime_analyst import MarketRegimeAnalystAgent
from packages.agents.agents.news_analyst import NewsAnalystAgent
from packages.agents.agents.risk_committee import RiskCommitteeAgent
from packages.agents.agents.sentiment_analyst import SentimentAnalystAgent
from packages.agents.agents.technical_analyst import TechnicalAnalystAgent
from packages.agents.agents.trader_agent import TraderAgent
from packages.agents.agents.valuation_analyst import ValuationAnalystAgent
from packages.agents.graphs.debate_graph import ResearchDebateGraph
from packages.agents.state import AlphaMindAgentState

logger = logging.getLogger(__name__)


class InstitutionalInvestmentWorkflow:
    """Full institutional multi-agent investment research and decision graph."""

    def __init__(self, debate_rounds: int = 2) -> None:
        self.technical_analyst = TechnicalAnalystAgent()
        self.fundamental_analyst = FundamentalAnalystAgent()
        self.valuation_analyst = ValuationAnalystAgent()
        self.news_analyst = NewsAnalystAgent()
        self.sentiment_analyst = SentimentAnalystAgent()
        self.macro_analyst = MacroAnalystAgent()
        self.market_regime_analyst = MarketRegimeAnalystAgent()
        self.earnings_analyst = EarningsAnalystAgent()

        self.debate_graph = ResearchDebateGraph(rounds=debate_rounds)
        self.trader_agent = TraderAgent()
        self.risk_committee = RiskCommitteeAgent()

    async def execute_workflow(self, initial_state: AlphaMindAgentState) -> AlphaMindAgentState:
        """Run the complete institutional workflow asynchronously."""
        start_t = time.monotonic()
        state = dict(initial_state)
        symbol = state.get("symbol", "UNKNOWN").upper()
        logger.info("Starting Institutional Investment Workflow for %s", symbol)

        # 1. Specialized Analysts Analysis
        tech_res = await self.technical_analyst.execute(state)
        state.update(tech_res)

        fund_res = await self.fundamental_analyst.execute(state)
        state.update(fund_res)

        val_res = await self.valuation_analyst.execute(state)
        state.update(val_res)

        news_res = await self.news_analyst.execute(state)
        state.update(news_res)

        sent_res = await self.sentiment_analyst.execute(state)
        state.update(sent_res)

        macro_res = await self.macro_analyst.execute(state)
        state.update(macro_res)

        regime_res = await self.market_regime_analyst.execute(state)
        state.update(regime_res)

        earn_res = await self.earnings_analyst.execute(state)
        state.update(earn_res)

        # 2. Adversarial Research Debate Layer
        state = await self.debate_graph.run_debate(state)

        # 3. Trader Proposal Formulation
        trader_res = await self.trader_agent.execute(state)
        state.update(trader_res)

        # 4. Risk Management Committee Deliberation
        risk_res = await self.risk_committee.execute(state)
        state.update(risk_res)

        # 5. Portfolio Strategy Allocation
        approved_alloc = state.get("risk_committee_decision", {}).get("approved_allocation_pct", 3.0)
        action = state.get("trader_proposal", {}).get("proposed_action", "HOLD")
        portfolio_alloc = {
            "strategy": "ALPHA_MULTI_FACTOR_EQUITY",
            "symbol": symbol,
            "target_weight_pct": approved_alloc if action == "BUY" else 0.0,
            "rebalance_action": action,
            "execution_status": "READY_FOR_PAPER_SIMULATION",
        }
        state["portfolio_allocation"] = portfolio_alloc

        # 6. Assemble Final Structured Report
        runtime_ms = round((time.monotonic() - start_t) * 1000.0, 2)
        state["completed_agent_nodes"] = [
            "TechnicalAnalyst",
            "FundamentalAnalyst",
            "ValuationAnalyst",
            "NewsAnalyst",
            "SentimentAnalyst",
            "MacroAnalyst",
            "MarketRegimeAnalyst",
            "EarningsAnalyst",
            "BullResearcher",
            "BearResearcher",
            "ResearchManager",
            "TraderAgent",
            "RiskCommittee",
        ]

        state["final_report_json"] = {
            "symbol": symbol,
            "runtime_ms": runtime_ms,
            "technical": state.get("technical_analysis"),
            "fundamental": state.get("fundamental_analysis"),
            "valuation": state.get("valuation_analysis"),
            "macro": state.get("macro_analysis"),
            "regime": state.get("market_regime_analysis"),
            "sentiment": state.get("sentiment_analysis"),
            "earnings": state.get("earnings_analysis"),
            "debate": {
                "bull_thesis": state.get("bull_thesis"),
                "bear_thesis": state.get("bear_thesis"),
                "synthesis": state.get("research_manager_summary"),
                "contradictions": state.get("contradiction_resolution"),
                "transcript": state.get("debate_transcript"),
            },
            "trader_proposal": state.get("trader_proposal"),
            "risk_decision": state.get("risk_committee_decision"),
            "disclaimer": "FOR RESEARCH AND SIMULATION PURPOSES ONLY. NOT FINANCIAL OR INVESTMENT ADVICE.",
        }

        return state
