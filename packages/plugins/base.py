"""
AlphaMind AI - Plugin Architecture Interface Contracts

Defines abstract Protocol interfaces for LLMs, Brokers, Market Feeds, News Feeds,
Embedding Engines, Vector Stores, Knowledge Graphs, Auth Providers, and Notifications.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class LLMProviderPlugin(Protocol):
    """Interface for LLM model providers (OpenAI, Anthropic, Gemini, DeepSeek, Ollama)."""

    async def generate_completion(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.2,
        max_tokens: int = 2048,
    ) -> dict[str, Any]:
        """Generate structured text/JSON completion."""
        ...

    async def generate_structured_json(
        self,
        prompt: str,
        schema: dict[str, Any],
        system_prompt: str | None = None,
    ) -> dict[str, Any]:
        """Generate completion conforming to a specific JSON schema."""
        ...


@runtime_checkable
class MarketProviderPlugin(Protocol):
    """Interface for multi-asset market data feeds (Polygon, yfinance, CCXT, FRED)."""

    async def fetch_bars(
        self,
        symbol: str,
        timeframe: str,
        start_date: str,
        end_date: str,
    ) -> list[dict[str, Any]]:
        """Fetch historical price bars."""
        ...

    async def fetch_latest_quote(self, symbol: str) -> dict[str, Any]:
        """Fetch real-time ticker quote."""
        ...


@runtime_checkable
class BrokerProviderPlugin(Protocol):
    """Interface for paper trading and real-money broker execution (Alpaca, IB, Binance)."""

    async def submit_order(
        self,
        symbol: str,
        side: str,  # 'buy' or 'sell'
        quantity: float,
        order_type: str,  # 'market', 'limit'
        limit_price: float | None = None,
    ) -> dict[str, Any]:
        """Submit paper trading order."""
        ...

    async def get_account_positions(self) -> list[dict[str, Any]]:
        """Fetch current portfolio positions."""
        ...


@runtime_checkable
class NewsProviderPlugin(Protocol):
    """Interface for financial news & NLP feeds (NewsAPI, SerpAPI, Bing)."""

    async def fetch_recent_news(self, query: str, limit: int = 20) -> list[dict[str, Any]]:
        """Fetch recent financial news articles."""
        ...


@runtime_checkable
class EmbeddingProviderPlugin(Protocol):
    """Interface for text embedding models (OpenAI, BGE, SentenceTransformers)."""

    async def embed_text(self, text: str) -> list[float]:
        """Generate vector embedding array for text string."""
        ...


@runtime_checkable
class VectorStorePlugin(Protocol):
    """Interface for vector databases (ChromaDB, Qdrant, Pinecone)."""

    async def upsert_documents(
        self,
        collection_name: str,
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict[str, Any]],
        ids: list[str],
    ) -> bool:
        """Upsert document embeddings to collection."""
        ...

    async def query_similar(
        self,
        collection_name: str,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> list[dict[str, Any]]:
        """Query top-K similar vector documents."""
        ...


@runtime_checkable
class KnowledgeGraphPlugin(Protocol):
    """Interface for Knowledge Graph stores (Neo4j, NetworkX)."""

    async def execute_cypher(
        self, query: str, parameters: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """Execute graph query language command."""
        ...


@runtime_checkable
class AuthProviderPlugin(Protocol):
    """Interface for user identity and RBAC validation."""

    async def authenticate_token(self, token: str) -> dict[str, Any]:
        """Validate JWT or API key token."""
        ...


@runtime_checkable
class NotificationProviderPlugin(Protocol):
    """Interface for multi-channel alert notifications (Email, Webhook, Slack, Telegram)."""

    async def send_alert(self, title: str, message: str, channel: str) -> bool:
        """Send notification alert."""
        ...
