"""
AlphaMind AI - Execution Simulation Telemetry & Observability Tracker
"""

from __future__ import annotations

import logging
import time

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class SimulationTelemetryMetrics(BaseModel):
    simulation_id: str
    start_time: float = Field(default_factory=time.time)
    end_time: float = 0.0
    simulation_duration_ms: float = 0.0
    total_orders_submitted_count: int = 0
    total_orders_filled_count: int = 0
    fill_rate_pct: float = 100.0
    avg_execution_latency_ms: float = 10.5
    avg_slippage_bps: float = 2.0
    total_commission_paid_usd: float = 0.0


class SimulationObservabilityTracker:
    """Tracker recording performance & telemetry metrics for Execution Simulation Platform."""

    def __init__(self, simulation_id: str) -> None:
        self.metrics = SimulationTelemetryMetrics(simulation_id=simulation_id)

    def record_order(
        self, filled: bool = True, latency_ms: float = 10.0, commission: float = 1.0
    ) -> None:
        self.metrics.total_orders_submitted_count += 1
        if filled:
            self.metrics.total_orders_filled_count += 1
        self.metrics.total_commission_paid_usd += commission
        self.metrics.fill_rate_pct = round(
            (self.metrics.total_orders_filled_count / self.metrics.total_orders_submitted_count)
            * 100.0,
            2,
        )

    def finalize(self) -> SimulationTelemetryMetrics:
        self.metrics.end_time = time.time()
        self.metrics.simulation_duration_ms = round(
            (self.metrics.end_time - self.metrics.start_time) * 1000.0, 2
        )
        logger.info(
            "Simulation telemetry finalized for '%s': duration=%.2fms, orders=%d, fill_rate=%.1f%%",
            self.metrics.simulation_id,
            self.metrics.simulation_duration_ms,
            self.metrics.total_orders_submitted_count,
            self.metrics.fill_rate_pct,
        )
        return self.metrics
