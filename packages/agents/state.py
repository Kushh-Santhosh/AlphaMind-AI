"""
AlphaMind AI - Shared LangGraph Agent State Definition
Comprehensive state schema supporting 11 specialized analysts, adversarial bull/bear debate,
risk committee deliberations, trader sizing, portfolio allocation, and provenance tracking.
"""

from __future__ import annotations

from typing import Any, TypedDict


class AlphaMindAgentState(TypedDict, total=False):
    """
    Shared LangGraph State Object.
    Agents communicate STRICTLY and EXCLUSIVELY by mutating/appending to this state dictionary.
    Direct agent-to-agent method calls are strictly prohibited.
    """

    session_id: str
    symbol: str
    asset_class: str
    target_horizon_days: int
    user_id: str

    # Data Provenance & Freshness Metadata
    data_provenance: dict[str, Any] | None
    market_data: dict[str, Any] | None
    sec_filings_data: dict[str, Any] | None
    news_sentiment_data: dict[str, Any] | None
    macro_indicators: dict[str, Any] | None
    knowledge_graph_subgraph: dict[str, Any] | None

    # 11 Specialized Analyst Outputs
    technical_analysis: dict[str, Any] | None
    fundamental_analysis: dict[str, Any] | None
    valuation_analysis: dict[str, Any] | None
    news_analysis: dict[str, Any] | None
    sentiment_analysis: dict[str, Any] | None
    macro_analysis: dict[str, Any] | None
    market_regime_analysis: dict[str, Any] | None
    earnings_analysis: dict[str, Any] | None
    quant_factor_analysis: dict[str, Any] | None
    risk_analyst_output: dict[str, Any] | None
    portfolio_analyst_output: dict[str, Any] | None

    # Quantitative & Probability Engine Outputs
    quant_factor_outputs: dict[str, Any] | None
    ml_forecast_distribution: dict[str, Any] | None
    monte_carlo_results: dict[str, Any] | None
    risk_assessment: dict[str, Any] | None

    # Adversarial Research Debate Layer
    bull_thesis: dict[str, Any] | None
    bear_thesis: dict[str, Any] | None
    debate_transcript: list[dict[str, Any]]
    debate_rounds: int
    contradiction_resolution: dict[str, Any] | None
    research_manager_summary: dict[str, Any] | None

    # Action & Execution Layer (Paper Simulation)
    trader_proposal: dict[str, Any] | None
    risk_committee_votes: list[dict[str, Any]]
    risk_committee_decision: dict[str, Any] | None
    portfolio_allocation: dict[str, Any] | None
    paper_execution_result: dict[str, Any] | None

    # Final Output Report & Model Telemetry
    final_report_json: dict[str, Any] | None
    model_metadata: dict[str, Any] | None

    # Orchestration Control Plane Metadata
    completed_agent_nodes: list[str]
    current_node: str
    circuit_breaker_active: bool
    error_logs: list[dict[str, Any]]
