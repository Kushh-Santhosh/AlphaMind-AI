"""
AlphaMind AI - Shared LangGraph Agent State Definition
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

    # Raw & Engineered Financial Payloads
    market_data: dict[str, Any] | None
    sec_filings_data: dict[str, Any] | None
    news_sentiment_data: dict[str, Any] | None
    technical_indicators: dict[str, Any] | None
    fundamental_metrics: dict[str, Any] | None
    macro_indicators: dict[str, Any] | None
    knowledge_graph_subgraph: dict[str, Any] | None

    # Quantitative & Probability Outputs
    quant_factor_outputs: dict[str, Any] | None
    ml_forecast_distribution: dict[str, Any] | None
    monte_carlo_results: dict[str, Any] | None
    risk_assessment: dict[str, Any] | None

    # Final Output Report
    final_report_json: dict[str, Any] | None

    # Orchestration Control Plane Metadata
    completed_agent_nodes: list[str]
    current_node: str
    circuit_breaker_active: bool
    error_logs: list[dict[str, Any]]
