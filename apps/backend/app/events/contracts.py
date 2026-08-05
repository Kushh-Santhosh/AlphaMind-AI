"""
AlphaMind AI - Event Message Contracts & Definitions
"""

from __future__ import annotations

import time
import uuid
from typing import Any

from pydantic import BaseModel, Field


class EventMessage(BaseModel):
    """Standardized Event Message Envelope."""

    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str  # e.g. "market.data.ingested", "sec.filing.processed"
    source: str
    payload: dict[str, Any]
    timestamp: float = Field(default_factory=time.time)
    correlation_id: str | None = None
    retry_count: int = 0
    max_retries: int = 3


class MarketDataIngestedEvent(EventMessage):
    event_type: str = "market.data.ingested"


class SECFilingIngestedEvent(EventMessage):
    event_type: str = "sec.filing.ingested"


class ProviderFailedEvent(EventMessage):
    event_type: str = "provider.failed"
