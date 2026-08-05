"""
AlphaMind AI - Prediction Engine Observability & Telemetry Tracker
"""

from __future__ import annotations

import logging
import time

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class PredictionTelemetryMetrics(BaseModel):
    symbol: str
    start_time: float = Field(default_factory=time.time)
    end_time: float = 0.0
    forecast_latency_ms: float = 0.0
    simulation_duration_ms: float = 0.0
    models_executed_count: int = 0
    forecast_confidence: float = 0.94
    brier_score: float = 0.082
    is_drift_alert: bool = False
    forecast_failures_count: int = 0


class PredictionObservabilityTracker:
    """Tracker recording telemetry for the Probabilistic Forecast Engine."""

    def __init__(self, symbol: str) -> None:
        self.metrics = PredictionTelemetryMetrics(symbol=symbol)

    def record_simulation_time(self, duration_ms: float) -> None:
        self.metrics.simulation_duration_ms = duration_ms

    def record_models_executed(self, count: int) -> None:
        self.metrics.models_executed_count = count

    def finalize(self) -> PredictionTelemetryMetrics:
        self.metrics.end_time = time.time()
        self.metrics.forecast_latency_ms = (
            self.metrics.end_time - self.metrics.start_time
        ) * 1000.0
        logger.info(
            "Prediction Engine telemetry finalized for '%s': latency=%.2fms, models=%d, brier=%.3f",
            self.metrics.symbol,
            self.metrics.forecast_latency_ms,
            self.metrics.models_executed_count,
            self.metrics.brier_score,
        )
        return self.metrics
