"""
AlphaMind AI - Financial News Engine

Normalizes financial news articles, deduplicates, ranks source reliability,
and extracts entities/topics. Zero sentiment scoring is performed.
"""

from __future__ import annotations

import logging
import uuid
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class NormalizedNewsArticle(BaseModel):
    article_id: str = Field(default_factory=lambda: f"art_{uuid.uuid4().hex[:8]}")
    title: str
    body_snippet: str
    url: str
    source_name: str
    source_reliability_score: float = 0.85  # 0.0 to 1.0 trust score
    published_at_utc: str
    language: str = "en"
    entities_extracted: list[str] = Field(default_factory=list)
    topics_extracted: list[str] = Field(default_factory=list)


class NewsEngine:
    """
    Financial News Engine managing article normalization, entity recognition, and source reliability ranking.
    Excludes sentiment scoring per Milestone 6 instructions.
    """

    def __init__(self) -> None:
        self.seen_urls: set[str] = set()

    async def process_raw_articles(
        self, raw_articles: list[dict[str, Any]]
    ) -> list[NormalizedNewsArticle]:
        """Normalize, deduplicate, and extract entities from news feed items."""
        normalized: list[NormalizedNewsArticle] = []

        for item in raw_articles:
            url = item.get("url", "")
            if not url or url in self.seen_urls:
                continue

            self.seen_urls.add(url)
            title = str(item.get("title", "Untitled Article"))
            source = str(item.get("publisher", "Financial Wire"))

            # Simple keyword entity & topic extraction
            entities = [
                word for word in ["AAPL", "NVDA", "MSFT", "FED", "SEC"] if word in title.upper()
            ]
            topics = [
                topic
                for topic in ["Earnings", "Inflation", "M&A", "Regulatory", "Supply Chain"]
                if topic.lower() in title.lower()
            ]

            article = NormalizedNewsArticle(
                title=title,
                body_snippet=title,
                url=url,
                source_name=source,
                source_reliability_score=(
                    0.90 if "Financial Times" in source or "Bloomberg" in source else 0.75
                ),
                published_at_utc=str(item.get("published_at", "2026-08-04T12:00:00Z")),
                language="en",
                entities_extracted=entities if entities else ["GENERAL_MARKET"],
                topics_extracted=topics if topics else ["Corporate"],
            )
            normalized.append(article)

        logger.info("Processed %d normalized articles (deduplicated).", len(normalized))
        return normalized
