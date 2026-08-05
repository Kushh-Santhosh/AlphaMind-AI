"""
AlphaMind AI - Portfolio Intelligence Observability & Telemetry Tracker
"""

from __future__ import annotations

import logging
import time

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class PortfolioTelemetryMetrics(BaseModel):
    portfolio_id: str
    start_time: float = Field(default_factory=time.time)
    end_time: float = 0.0
    portfolio_analysis_latency_ms: float = 0.0
    risk_calculation_duration_ms: float = 0.0
    scenario_execution_duration_ms: float = 0.0
    optimization_runtime_ms: float = 0.0
    metric_coverage_pct: float = 100.0


class PortfolioObservabilityTracker:
    """Tracker recording execution metrics for Portfolio Intelligence and Risk Engine."""

    def __init__(self, portfolio_id: str) -> None:
        self.metrics = PortfolioTelemetryMetrics(portfolio_id=portfolio_id)

    def record_risk_duration(self, duration_ms: float) -> None:
        self.metrics.risk_calculation_duration_ms = duration_ms

    def record_scenario_duration(self, duration_ms: float) -> None:
        self.metrics.scenario_execution_duration_ms = duration_ms

    def finalize(self) -> PortfolioTelemetryMetrics:
        self.metrics.end_time = time.time()
        self.metrics.portfolio_analysis_latency_ms = (
            self.metrics.end_time - self.metrics.start_time
        ) * 1000.0
        logger.info(
            "Portfolio telemetry finalized for '%s': latency=%.2fms, risk_duration=%.2fms",
            self.metrics.portfolio_id,
            self.metrics.portfolio_analysis_latency_ms,
            self.metrics.risk_calculation_duration_ms,
        )
        return self.metrics
