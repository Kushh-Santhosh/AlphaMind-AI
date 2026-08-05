"""
AlphaMind AI - Watchlists & Platform Alerting System

Manages user Watchlists and emits alerts for Forecast Updates, Research Updates,
Model Drift, Data Quality, and Portfolio Risk thresholds.
STRICT MANDATE: Zero trade execution alerts or order notifications.
"""

from __future__ import annotations

import logging
import time
import uuid

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class PlatformAlert(BaseModel):
    alert_id: str = Field(default_factory=lambda: f"alt_{uuid.uuid4().hex[:8]}")
    alert_type: str  # "forecast_update", "research_update", "drift_alert", "data_quality_alert", "risk_alert"
    severity: str  # "info", "warning", "critical"
    symbol_or_target: str
    headline: str
    description: str
    timestamp_utc: str = Field(
        default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    )


class Watchlist(BaseModel):
    watchlist_id: str = Field(default_factory=lambda: f"wtch_{uuid.uuid4().hex[:8]}")
    name: str = "Core Research Watchlist"
    symbols: list[str] = Field(default_factory=lambda: ["AAPL", "NVDA", "MSFT", "GOOGL"])
    created_at_utc: str = Field(
        default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    )


class WatchlistAlertsManager:
    """Manager handling asset watchlists and platform notification dispatch."""

    def __init__(self) -> None:
        self.watchlists: dict[str, Watchlist] = {}
        self.alerts: list[PlatformAlert] = []

    def create_watchlist(self, name: str, symbols: list[str]) -> Watchlist:
        """Create new user research watchlist."""
        w = Watchlist(name=name, symbols=[s.upper() for s in symbols])
        self.watchlists[w.watchlist_id] = w
        logger.info("Created research Watchlist '%s' with %d symbols.", w.name, len(symbols))
        return w

    def emit_alert(
        self, alert_type: str, severity: str, symbol: str, headline: str, description: str
    ) -> PlatformAlert:
        """Emit non-trading platform research alert."""
        alt = PlatformAlert(
            alert_type=alert_type,
            severity=severity,
            symbol_or_target=symbol.upper(),
            headline=headline,
            description=description,
        )
        self.alerts.append(alt)
        logger.info("Emitted platform alert [%s] for '%s': %s", alert_type, symbol, headline)
        return alt

    def get_active_alerts(self, symbol: str | None = None) -> list[PlatformAlert]:
        """Fetch active platform alerts."""
        if symbol:
            return [a for a in self.alerts if a.symbol_or_target == symbol.upper()]
        return self.alerts
