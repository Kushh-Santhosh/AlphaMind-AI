"""
AlphaMind AI - Broker Integration Telemetry & Observability Tracker
"""

from __future__ import annotations

import logging
import time

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class BrokerTelemetryMetrics(BaseModel):
    broker_name: str = "alpaca"
    connection_health: str = "CONNECTED"  # "CONNECTED", "DEGRADED", "DISCONNECTED"
    broker_latency_ms: float = 12.5
    api_failures_count: int = 0
    rejected_orders_count: int = 0
    retries_count: int = 0
    rate_limits_hit_count: int = 0
    last_ping_utc: str = Field(
        default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    )


class BrokerObservabilityTracker:
    """Tracker recording execution metrics and connectivity health for Broker Integration Layer."""

    def __init__(self, broker_name: str = "alpaca") -> None:
        self.metrics = BrokerTelemetryMetrics(broker_name=broker_name)

    def record_latency(self, duration_ms: float) -> None:
        self.metrics.broker_latency_ms = round(duration_ms, 2)

    def record_rejection(self) -> None:
        self.metrics.rejected_orders_count += 1

    def record_api_failure(self) -> None:
        self.metrics.api_failures_count += 1
        if self.metrics.api_failures_count > 3:
            self.metrics.connection_health = "DEGRADED"

    def get_health_snapshot(self) -> BrokerTelemetryMetrics:
        self.metrics.last_ping_utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        return self.metrics
