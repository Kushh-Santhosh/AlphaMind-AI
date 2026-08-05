"""
AlphaMind AI v2 - Intelligence Reasoning Memory

Durable, structured reasoning memory capturing the full chain of AI thought
behind every allocation, forecast, and risk decision.
Supports parent-child reasoning chains, assumptions, alternatives, and replay snapshots.
Every record is published to the Unified Timeline via the EventBus.
"""

from __future__ import annotations

import logging
import time
import uuid
from typing import Any

from pydantic import BaseModel, Field

from packages.os_core.event_bus import EventBusManager, EventType, SystemEvent

logger = logging.getLogger(__name__)


class ReasoningRecord(BaseModel):
    """Structured AI reasoning object capturing the full decision chain."""

    reasoning_id: str = Field(default_factory=lambda: f"rsn_{uuid.uuid4().hex[:10]}")
    decision_id: str
    parent_reasoning_id: str | None = None  # Chain lineage
    timestamp_utc: str = Field(
        default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    )
    workflow_id: str = Field(default_factory=lambda: f"wf_{uuid.uuid4().hex[:8]}")
    # Evidence
    evidence_references: list[str] = Field(default_factory=list)
    confidence_score: float  # 0.0–1.0
    contradictory_evidence: list[str] = Field(default_factory=list)
    # Reasoning structure
    assumptions: list[str] = Field(default_factory=list)
    alternative_actions_considered: list[dict[str, Any]] = Field(default_factory=list)
    selected_action: str
    # Replay & audit
    replay_snapshot_id: str = Field(default_factory=lambda: f"snap_{uuid.uuid4().hex[:8]}")
    audit_metadata: dict[str, str] = Field(default_factory=dict)


class ConfidenceEvolutionPoint(BaseModel):
    """Single time-series data point for confidence evolution tracking."""

    reasoning_id: str
    timestamp_utc: str
    confidence_score: float
    decision_id: str
    headline: str


class IntelligenceMemoryStore:
    """
    Durable reasoning memory store retaining the full chain of AI decisions.
    Supports parent-child chaining, query by decision or workflow,
    and publishes every record to the Unified Timeline via EventBus.
    """

    def __init__(self, event_bus: EventBusManager | None = None) -> None:
        self.event_bus = event_bus
        self.records: dict[str, ReasoningRecord] = {}
        self.decision_index: dict[str, list[str]] = {}  # decision_id → [reasoning_id]
        self.workflow_index: dict[str, list[str]] = {}  # workflow_id → [reasoning_id]
        self.confidence_timeline: list[ConfidenceEvolutionPoint] = []

    def store_reasoning(self, record: ReasoningRecord) -> ReasoningRecord:
        """
        Persist a structured reasoning record, update indices,
        and publish a SystemEvent to the Unified Timeline.
        """
        self.records[record.reasoning_id] = record

        # Decision index
        self.decision_index.setdefault(record.decision_id, []).append(record.reasoning_id)
        # Workflow index
        self.workflow_index.setdefault(record.workflow_id, []).append(record.reasoning_id)
        # Confidence evolution timeline
        self.confidence_timeline.append(
            ConfidenceEvolutionPoint(
                reasoning_id=record.reasoning_id,
                timestamp_utc=record.timestamp_utc,
                confidence_score=record.confidence_score,
                decision_id=record.decision_id,
                headline=record.selected_action,
            )
        )

        # Publish to Unified Timeline
        if self.event_bus:
            evt = SystemEvent(
                event_type=EventType.FORECAST_UPDATED,
                source_subsystem="intelligence_memory",
                headline=f"Reasoning Stored: {record.selected_action[:80]}",
                details=(
                    f"Decision {record.decision_id} | "
                    f"Confidence {record.confidence_score:.0%} | "
                    f"Evidence: {', '.join(record.evidence_references[:2])}"
                ),
                payload={"reasoning_id": record.reasoning_id},
            )
            self.event_bus.publish(evt)

        logger.info(
            "Intelligence Memory: stored reasoning '%s' (decision=%s, confidence=%.2f)",
            record.reasoning_id,
            record.decision_id,
            record.confidence_score,
        )
        return record

    # ── Retrieval ──────────────────────────────────────────────────────────────

    def get_by_reasoning_id(self, reasoning_id: str) -> ReasoningRecord | None:
        """Fetch reasoning record by its primary ID."""
        return self.records.get(reasoning_id)

    def get_chain_for_decision(self, decision_id: str) -> list[ReasoningRecord]:
        """Fetch the full reasoning chain for a given decision."""
        ids = self.decision_index.get(decision_id, [])
        return [self.records[rid] for rid in ids if rid in self.records]

    def get_chain_for_workflow(self, workflow_id: str) -> list[ReasoningRecord]:
        """Fetch all reasoning steps across a workflow execution."""
        ids = self.workflow_index.get(workflow_id, [])
        return [self.records[rid] for rid in ids if rid in self.records]

    def get_confidence_evolution(
        self, decision_id: str | None = None
    ) -> list[ConfidenceEvolutionPoint]:
        """Return confidence evolution points, optionally filtered by decision."""
        if decision_id:
            return [p for p in self.confidence_timeline if p.decision_id == decision_id]
        return self.confidence_timeline

    def list_all_records(self, limit: int = 50) -> list[ReasoningRecord]:
        """List recent reasoning records."""
        all_records = list(self.records.values())
        return all_records[-limit:]
