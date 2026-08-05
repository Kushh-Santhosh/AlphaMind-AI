"""
API v1 — Daily Automated Briefings Router
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from packages.agents.daily_briefing_engine import BriefingType, DailyBriefingEngine
from packages.os_core.event_bus import EventBusManager, EventType
from packages.os_core.intelligence_memory import IntelligenceMemoryStore
from packages.os_core.unified_timeline import UnifiedImmutableTimeline
from packages.portfolio.multi_strategy_funds import MultiStrategyFundEngine

router = APIRouter(prefix="/api/v1/briefings", tags=["Daily Automated Briefings"])

# Singleton composition — reuse upstream engines, zero duplicate logic
_event_bus = EventBusManager()
_timeline = UnifiedImmutableTimeline()
_event_bus.subscribe(EventType.BRIEFING_GENERATED, _timeline.append_event)

_fund_engine = MultiStrategyFundEngine(event_bus=_event_bus)
_fund_engine._initialize_5_funds()

_memory_store = IntelligenceMemoryStore(event_bus=_event_bus)

_briefing_engine = DailyBriefingEngine(
    timeline=_timeline,
    memory_store=_memory_store,
    fund_engine=_fund_engine,
    event_bus=_event_bus,
)


@router.post("/generate/{briefing_type}")
async def generate_briefing(
    briefing_type: BriefingType,
    period_label: str | None = None,
) -> dict[str, Any]:
    """Generate a fresh briefing document from live engine data."""
    doc = _briefing_engine.generate_briefing(briefing_type, period_label=period_label)
    return doc.model_dump()


@router.get("/list")
async def list_briefings(
    briefing_type: BriefingType | None = None,
) -> list[dict[str, Any]]:
    """List all previously generated briefings, optionally filtered by type."""
    docs = _briefing_engine.list_briefings(briefing_type=briefing_type)
    return [d.model_dump() for d in docs]


@router.get("/{briefing_id}")
async def get_briefing(briefing_id: str) -> dict[str, Any]:
    """Fetch a specific briefing document by ID."""
    doc = _briefing_engine.get_briefing(briefing_id)
    if not doc:
        raise HTTPException(status_code=404, detail=f"Briefing '{briefing_id}' not found.")
    return doc.model_dump()
