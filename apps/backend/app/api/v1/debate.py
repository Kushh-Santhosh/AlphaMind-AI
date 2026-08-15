"""
AlphaMind AI - Adversarial Research Debate API Router
Exposes multi-round Bull vs Bear research debate endpoints.
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from packages.agents.graphs.debate_graph import ResearchDebateGraph
from packages.agents.state import AlphaMindAgentState
from packages.market.provider_registry import DataProviderRegistry

router = APIRouter(prefix="/api/v1/debate", tags=["Research Debate"])
logger = logging.getLogger(__name__)


class DebateRequest(BaseModel):
    symbol: str = Field(default="NVDA", description="Ticker symbol for research debate")
    rounds: int = Field(default=2, ge=1, le=5, description="Number of dialectical debate rounds")


@router.post("/run", response_model=dict[str, Any])
async def run_research_debate(payload: DebateRequest) -> dict[str, Any]:
    """Execute an adversarial Bull vs Bear research debate with Research Manager referee synthesis."""
    try:
        registry = DataProviderRegistry()
        market_snap = await registry.get_market_snapshot(payload.symbol)

        initial_state: AlphaMindAgentState = {
            "session_id": f"debate_{payload.symbol.lower()}",
            "symbol": payload.symbol.upper(),
            "asset_class": "equity",
            "market_data": market_snap,
            "completed_agent_nodes": [],
            "error_logs": [],
        }

        debate_graph = ResearchDebateGraph(rounds=payload.rounds)
        final_state = await debate_graph.run_debate(initial_state)

        return {
            "symbol": payload.symbol.upper(),
            "rounds": payload.rounds,
            "bull_thesis": final_state.get("bull_thesis"),
            "bear_thesis": final_state.get("bear_thesis"),
            "manager_synthesis": final_state.get("research_manager_summary"),
            "contradiction_resolution": final_state.get("contradiction_resolution"),
            "transcript": final_state.get("debate_transcript"),
            "disclaimer": "RESEARCH & DEBATE SIMULATION ONLY. NOT FINANCIAL ADVICE.",
        }
    except Exception as exc:
        logger.error("Debate execution failed for %s: %s", payload.symbol, exc)
        raise HTTPException(status_code=500, detail=str(exc))
