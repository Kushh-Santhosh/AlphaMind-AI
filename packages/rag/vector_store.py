"""
AlphaMind AI - ChromaDB Multi-Collection Vector Architecture

Defines 5 domain document collections: News, SEC Filings, Research Reports, Company Documents, and Macro Reports.
No retrieval execution or reasoning logic included.
"""

from __future__ import annotations

import logging
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class VectorCollectionName(str, Enum):  # noqa: UP042
    NEWS = "news_embeddings"
    SEC_FILINGS = "sec_filings_embeddings"
    RESEARCH_REPORTS = "research_reports_embeddings"
    COMPANY_DOCUMENTS = "company_documents_embeddings"
    MACRO_REPORTS = "macro_reports_embeddings"


class VectorDocumentRecord(BaseModel):
    doc_id: str
    collection_name: VectorCollectionName
    embedding_vector: list[float] = Field(default_factory=list)
    document_text: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class VectorStoreManager:
    """
    Multi-collection vector store architecture manager.
    Stores documents and embedding vectors across 5 domain collections.
    """

    def __init__(self) -> None:
        self._collections: dict[str, list[VectorDocumentRecord]] = {
            col.value: [] for col in VectorCollectionName
        }

    def add_document(self, record: VectorDocumentRecord) -> bool:
        """Store document record in specified collection."""
        col_key = record.collection_name.value
        self._collections[col_key].append(record)
        logger.info(
            "Stored document '%s' in collection '%s'. Total: %d",
            record.doc_id,
            col_key,
            len(self._collections[col_key]),
        )
        return True

    def get_collection_size(self, collection_name: VectorCollectionName) -> int:
        """Get document count for a collection."""
        return len(self._collections.get(collection_name.value, []))

    def get_total_vector_count(self) -> int:
        """Get total stored vector documents across all collections."""
        return sum(len(docs) for docs in self._collections.values())
