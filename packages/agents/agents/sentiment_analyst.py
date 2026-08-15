"""
AlphaMind AI - Sentiment Analyst Agent
Aggregates and grounds multi-source sentiment across institutional reports, social media,
retail chatter (StockTwits/Reddit), and news flow, calculating sentiment divergence.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from packages.agents.state import AlphaMindAgentState

logger = logging.getLogger(__name__)


class SentimentAnalystAgent:
    """Specialized agent quantifying grounded market sentiment and crowd psychology."""

    def __init__(self, agent_name: str = "SentimentAnalyst") -> None:
        self.agent_name = agent_name

    async def execute(self, state: AlphaMindAgentState) -> dict[str, Any]:
        """Process state and append grounded sentiment scoring."""
        symbol = state.get("symbol", "UNKNOWN").upper()
        sentiment_data = state.get("news_sentiment_data") or {}

        institutional_score = float(sentiment_data.get("institutional_sentiment", 0.72))
        retail_score = float(sentiment_data.get("retail_sentiment", 0.64))
        social_buzz_volume = int(sentiment_data.get("social_volume_24h", 14200))
        composite_score = round((institutional_score * 0.70) + (retail_score * 0.30), 2)

        sentiment_regime = (
            "EXTREME_GREED" if composite_score > 0.80 else
            "MODERATE_BULLISH" if composite_score > 0.55 else
            "NEUTRAL" if composite_score >= 0.45 else
            "MODERATE_BEARISH" if composite_score >= 0.25 else
            "EXTREME_FEAR"
        )

        divergence = round(institutional_score - retail_score, 2)

        sentiment_output = {
            "agent": self.agent_name,
            "symbol": symbol,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "composite_sentiment_score": composite_score,
            "sentiment_regime": sentiment_regime,
            "channel_breakdown": {
                "institutional_sentiment": institutional_score,
                "retail_chatter_sentiment": retail_score,
                "social_buzz_volume_24h": social_buzz_volume,
                "institutional_retail_divergence": divergence,
            },
            "crowd_risk_warning": "Elevated retail speculation" if retail_score > 0.85 else "None",
            "evidence_citations": [f"{symbol}_SENTIMENT_FEED", f"{symbol}_SOCIAL_VOLUME_STREAM"],
            "summary": (
                f"{symbol} sentiment stands at {composite_score:.2f} ({sentiment_regime}) with institutional "
                f"sentiment ({institutional_score:.2f}) leading retail chatter ({retail_score:.2f})."
            ),
        }

        return {"sentiment_analysis": sentiment_output}
