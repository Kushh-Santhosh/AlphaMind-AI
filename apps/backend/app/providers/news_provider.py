"""
AlphaMind AI - News & Media Feed Provider Adapters
"""

from __future__ import annotations

from typing import Any

from packages.plugins.provider_manager import BaseProvider, ProviderMetadata


class NewsAPIProvider(BaseProvider):
    """Primary Financial News Provider Adapter (NewsAPI / SerpAPI)."""

    def __init__(self) -> None:
        metadata = ProviderMetadata(
            provider_id="news_api",
            provider_name="NewsAPI Financial Feed",
            version="v2",
            tier="primary",
            supported_assets=["equities", "crypto", "macro"],
            rate_limit_per_minute=60,
            timeout_seconds=3.0,
        )
        super().__init__(metadata)

    async def fetch_news(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        """Fetch recent financial news articles."""
        return [
            {
                "title": f"Earnings report analysis for {query}",
                "publisher": "Financial Times",
                "url": "https://example.com/news/1",
                "published_at": "2026-08-04T12:00:00Z",
                "sentiment_polarity": 0.65,
                "provider": "news_api",
            }
        ]
