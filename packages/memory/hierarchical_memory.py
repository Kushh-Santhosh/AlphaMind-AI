"""
AlphaMind AI - Hierarchical Long-Term Memory System

Provides Research Memory, Knowledge Memory, Document Memory, and Entity Memory stores.
STRICT RULE: Long-term memory is kept strictly separate from short-term workflow checkpoints.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class MemoryRecord(BaseModel):
    record_id: str
    memory_type: str  # "research", "knowledge", "document", "entity"
    key: str
    value: dict[str, Any]
    timestamp: float = Field(default_factory=time.time)
    version: int = 1


class ResearchMemoryStore:
    """Long-term store for historical research report snapshots."""

    def __init__(self) -> None:
        self._store: dict[str, MemoryRecord] = {}

    def store_research(self, symbol: str, report_payload: dict[str, Any]) -> str:
        rec_id = f"mem_res_{symbol.upper()}_{int(time.time())}"
        rec = MemoryRecord(
            record_id=rec_id,
            memory_type="research",
            key=symbol.upper(),
            value=report_payload,
        )
        self._store[rec_id] = rec
        logger.info("Stored Research Memory record '%s'.", rec_id)
        return rec_id

    def get_research(self, record_id: str) -> MemoryRecord | None:
        return self._store.get(record_id)


class KnowledgeMemoryStore:
    """Long-term store for graph triple associations and entity relationships."""

    def __init__(self) -> None:
        self._store: dict[str, MemoryRecord] = {}

    def store_knowledge_triple(self, subject: str, predicate: str, object_: str) -> str:
        rec_id = f"mem_knw_{subject}_{predicate}_{object_}"
        rec = MemoryRecord(
            record_id=rec_id,
            memory_type="knowledge",
            key=f"{subject}:{predicate}:{object_}",
            value={"subject": subject, "predicate": predicate, "object": object_},
        )
        self._store[rec_id] = rec
        return rec_id


class DocumentMemoryStore:
    """Long-term store for processed SEC filings and document metadata."""

    def __init__(self) -> None:
        self._store: dict[str, MemoryRecord] = {}

    def store_document_metadata(self, doc_id: str, metadata: dict[str, Any]) -> str:
        rec_id = f"mem_doc_{doc_id}"
        rec = MemoryRecord(record_id=rec_id, memory_type="document", key=doc_id, value=metadata)
        self._store[rec_id] = rec
        return rec_id


class EntityMemoryStore:
    """Long-term store for resolved entity alias mappings."""

    def __init__(self) -> None:
        self._store: dict[str, MemoryRecord] = {}

    def store_entity_alias(self, alias: str, canonical_id: str) -> str:
        rec_id = f"mem_ent_{alias.upper()}"
        rec = MemoryRecord(
            record_id=rec_id,
            memory_type="entity",
            key=alias.upper(),
            value={"alias": alias, "canonical_id": canonical_id},
        )
        self._store[rec_id] = rec
        return rec_id


class HierarchicalMemoryManager:
    """Consolidated Long-Term Memory System Manager."""

    def __init__(self) -> None:
        self.research_memory = ResearchMemoryStore()
        self.knowledge_memory = KnowledgeMemoryStore()
        self.document_memory = DocumentMemoryStore()
        self.entity_memory = EntityMemoryStore()
