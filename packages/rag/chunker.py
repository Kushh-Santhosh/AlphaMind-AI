"""
AlphaMind AI - Hierarchical Document Chunking Engine

Splits documents into parent and child text chunks with section hierarchy tracking,
chunk metadata, citation references, and versioning.
STRICT RULE: No search or retrieval execution in Milestone 7.
"""

from __future__ import annotations

import logging
import uuid
from typing import Any

from pydantic import BaseModel, Field

from packages.research.document_processor import ProcessedDocument

logger = logging.getLogger(__name__)


class DocumentChunk(BaseModel):
    chunk_id: str = Field(default_factory=lambda: f"chk_{uuid.uuid4().hex[:8]}")
    parent_chunk_id: str | None = None
    doc_id: str
    symbol: str
    section_title: str
    chunk_text: str
    character_count: int
    chunk_index: int
    version: int = 1
    metadata: dict[str, Any] = Field(default_factory=dict)
    source_reference: str = ""


class HierarchicalDocumentChunker:
    """
    Document Chunking Engine implementing parent-child section-aware chunking.
    """

    def __init__(self, target_chunk_size: int = 500) -> None:
        self.target_chunk_size = target_chunk_size

    def chunk_document(self, document: ProcessedDocument) -> list[DocumentChunk]:
        """Chunk a ProcessedDocument into parent and child DocumentChunk objects."""
        chunks: list[DocumentChunk] = []
        chunk_idx = 0

        for sec in document.sections:
            text = sec.content_text
            # Create Parent Chunk
            parent_id = f"chk_parent_{uuid.uuid4().hex[:6]}"
            parent_chunk = DocumentChunk(
                chunk_id=parent_id,
                doc_id=document.doc_id,
                symbol=document.symbol,
                section_title=sec.section_title,
                chunk_text=text[: self.target_chunk_size],
                character_count=min(len(text), self.target_chunk_size),
                chunk_index=chunk_idx,
                source_reference=f"{document.title} - {sec.section_title}",
            )
            chunks.append(parent_chunk)
            chunk_idx += 1

            # Create Child Chunks if text exceeds target_chunk_size
            if len(text) > self.target_chunk_size:
                child_text = text[self.target_chunk_size : self.target_chunk_size * 2]
                child_chunk = DocumentChunk(
                    parent_chunk_id=parent_id,
                    doc_id=document.doc_id,
                    symbol=document.symbol,
                    section_title=f"{sec.section_title} (Child)",
                    chunk_text=child_text,
                    character_count=len(child_text),
                    chunk_index=chunk_idx,
                    source_reference=f"{document.title} - {sec.section_title} - Subpart",
                )
                chunks.append(child_chunk)
                chunk_idx += 1

        logger.info(
            "Chunked document '%s' (%s) into %d parent-child chunks.",
            document.doc_id,
            document.symbol,
            len(chunks),
        )
        return chunks
