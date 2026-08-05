"""
RAG & Document Embedding Interfaces
"""

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class RAGEngineInterface(Protocol):
    """Interface for RAG ingestion and retrieval."""

    async def ingest_sec_filing(self, ticker: str, filing_text: str, form_type: str) -> bool: ...

    async def query_filings(self, query: str, ticker: str) -> list[dict[str, Any]]: ...
