"""
AlphaMind AI - Research Intelligence Observability & Telemetry Tracker
"""

from __future__ import annotations

import logging
import time

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ResearchTelemetryMetrics(BaseModel):
    symbol: str
    start_time: float = Field(default_factory=time.time)
    end_time: float = 0.0
    duration_ms: float = 0.0
    documents_processed_count: int = 0
    articles_processed_count: int = 0
    provider_latency_ms: float = 0.0
    provider_failures_count: int = 0
    normalization_quality_score: float = 1.0


class ResearchObservabilityTracker:
    """Tracker recording execution telemetry for the Research Intelligence Engine."""

    def __init__(self, symbol: str) -> None:
        self.metrics = ResearchTelemetryMetrics(symbol=symbol)

    def record_document_processed(self) -> None:
        self.metrics.documents_processed_count += 1

    def record_article_processed(self) -> None:
        self.metrics.articles_processed_count += 1

    def record_provider_latency(self, latency_ms: float, success: bool = True) -> None:
        self.metrics.provider_latency_ms = self.metrics.provider_latency_ms * 0.8 + latency_ms * 0.2
        if not success:
            self.metrics.provider_failures_count += 1

    def finalize(self) -> ResearchTelemetryMetrics:
        self.metrics.end_time = time.time()
        self.metrics.duration_ms = (self.metrics.end_time - self.metrics.start_time) * 1000.0
        logger.info(
            "Research telemetry finalized for '%s': duration=%.2fms, docs=%d, articles=%d",
            self.metrics.symbol,
            self.metrics.duration_ms,
            self.metrics.documents_processed_count,
            self.metrics.articles_processed_count,
        )
        return self.metrics
