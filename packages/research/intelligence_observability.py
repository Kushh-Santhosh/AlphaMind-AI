"""
AlphaMind AI - Financial Intelligence Observability & Metrics Tracker
"""

from __future__ import annotations

import logging
import time

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class IntelligenceTelemetryMetrics(BaseModel):
    symbol: str
    start_time: float = Field(default_factory=time.time)
    end_time: float = 0.0
    duration_ms: float = 0.0
    evidence_nodes_created: int = 0
    factors_extracted_count: int = 0
    contradictions_detected_count: int = 0
    data_coverage_pct: float = 95.0
    overall_confidence: float = 0.94


class FinancialIntelligenceObservabilityTracker:
    """Tracker recording telemetry for the Financial Intelligence Layer."""

    def __init__(self, symbol: str) -> None:
        self.metrics = IntelligenceTelemetryMetrics(symbol=symbol)

    def record_factors_extracted(self, count: int) -> None:
        self.metrics.factors_extracted_count += count

    def record_evidence_nodes(self, count: int) -> None:
        self.metrics.evidence_nodes_created += count

    def record_contradictions(self, count: int) -> None:
        self.metrics.contradictions_detected_count = count

    def finalize(self) -> IntelligenceTelemetryMetrics:
        self.metrics.end_time = time.time()
        self.metrics.duration_ms = (self.metrics.end_time - self.metrics.start_time) * 1000.0
        logger.info(
            "Financial Intelligence telemetry finalized for '%s': duration=%.2fms, factors=%d, contradictions=%d",
            self.metrics.symbol,
            self.metrics.duration_ms,
            self.metrics.factors_extracted_count,
            self.metrics.contradictions_detected_count,
        )
        return self.metrics
