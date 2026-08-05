"""
AlphaMind AI - Observability, OpenTelemetry Tracing & Prometheus Metrics Engine
"""

from __future__ import annotations

import structlog

# Initialize structlog structured JSON logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.PrintLoggerFactory(),
)

logger = structlog.get_logger()


class TelemetryMetricsManager:
    """Prometheus Metrics & Telemetry Exporter Stub."""

    _metrics: dict[str, float] = {
        "alphamind_provider_requests_total": 0.0,
        "alphamind_provider_errors_total": 0.0,
        "alphamind_ingestion_latency_ms": 0.0,
        "alphamind_queue_depth": 0.0,
        "alphamind_dlq_depth": 0.0,
    }

    @classmethod
    def record_provider_request(cls, provider_id: str, success: bool, latency_ms: float) -> None:
        """Record provider request count and latency metric."""
        cls._metrics["alphamind_provider_requests_total"] += 1.0
        if not success:
            cls._metrics["alphamind_provider_errors_total"] += 1.0
        cls._metrics["alphamind_ingestion_latency_ms"] = (
            cls._metrics["alphamind_ingestion_latency_ms"] * 0.8 + latency_ms * 0.2
        )
        logger.info(
            "telemetry_recorded",
            provider_id=provider_id,
            success=success,
            latency_ms=latency_ms,
        )

    @classmethod
    def update_queue_depth(cls, queue_depth: int, dlq_depth: int) -> None:
        """Update background task queue and DLQ metrics."""
        cls._metrics["alphamind_queue_depth"] = float(queue_depth)
        cls._metrics["alphamind_dlq_depth"] = float(dlq_depth)

    @classmethod
    def export_prometheus_metrics(cls) -> str:
        """Format metrics as Prometheus plain text format."""
        lines = [
            "# HELP alphamind_provider_requests_total Total data provider API requests",
            "# TYPE alphamind_provider_requests_total counter",
            f"alphamind_provider_requests_total {cls._metrics['alphamind_provider_requests_total']}",
            "# HELP alphamind_provider_errors_total Total data provider error count",
            "# TYPE alphamind_provider_errors_total counter",
            f"alphamind_provider_errors_total {cls._metrics['alphamind_provider_errors_total']}",
            "# HELP alphamind_ingestion_latency_ms Ingestion pipeline latency in ms",
            "# TYPE alphamind_ingestion_latency_ms gauge",
            f"alphamind_ingestion_latency_ms {cls._metrics['alphamind_ingestion_latency_ms']:.2f}",
            "# HELP alphamind_queue_depth Background task queue size",
            "# TYPE alphamind_queue_depth gauge",
            f"alphamind_queue_depth {cls._metrics['alphamind_queue_depth']}",
            "# HELP alphamind_dlq_depth Dead Letter Queue size",
            "# TYPE alphamind_dlq_depth gauge",
            f"alphamind_dlq_depth {cls._metrics['alphamind_dlq_depth']}",
        ]
        return "\n".join(lines) + "\n"
