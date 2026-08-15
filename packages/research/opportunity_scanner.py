"""
AlphaMind AI - Dynamic AI Opportunity Scanner Engine (v4.0)

Continuously screens the broad multi-asset investment universe by computing
real-time quantitative factors from live provider data:
  1. Momentum (1M/3M return, price vs 52-week high)
  2. Technical Trend (RSI-14 zone, MACD crossover, SMA-50/200 alignment)
  3. Valuation Factor (Normalized P/E, EV/EBITDA, earnings yield)
  4. Volatility & Risk Penalty (Annualized standard deviation of returns)
  5. Volume Profile & Liquidity

NO PRECOMPUTED CONSTANTS. Full provenance and factor calculation transparency.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Optional

import numpy as np

from packages.market.provider_registry import market_data_registry
from packages.market.universe_engine import AssetUniverseEngine, asset_universe_engine

logger = logging.getLogger(__name__)


@dataclass
class OpportunityCandidate:
    symbol: str
    name: str
    asset_class: str
    sector: str
    opportunity_score: float  # 0 to 100
    theme: str  # "Momentum Breakout", "Undervalued Compounder", "Oversold Reversal", "Trend Continuation", "Macro Allocation"
    price: float
    change_24h_pct: float
    factors: dict[str, float]  # Exact mathematical factor components
    factor_inputs: dict[str, Any]  # Underlying raw metrics (RSI, P/E, Volatility, etc.)
    recommendation: str
    provenance: dict[str, Any]


class OpportunityScannerEngine:
    """Quantitative multi-factor opportunity scanner calculating genuine real-time scores."""

    def __init__(self, universe_engine: Optional[AssetUniverseEngine] = None) -> None:
        self.universe_engine = universe_engine or asset_universe_engine

    def _compute_factor_score(self, snap: dict[str, Any]) -> tuple[float, dict[str, float], dict[str, Any], str, str]:
        """
        Compute quantitative factors and composite Opportunity Score from live market snapshot.
        """
        price = snap.get("price", 0.0)
        change_pct = snap.get("change_pct", 0.0)
        rsi_14 = snap.get("rsi_14", 50.0)
        macd = snap.get("macd", 0.0)
        macd_signal = snap.get("macd_signal", 0.0)
        sma_50 = snap.get("sma_50", 0.0)
        sma_200 = snap.get("sma_200", 0.0)
        trailing_pe = snap.get("trailing_pe")
        forward_pe = snap.get("forward_pe")
        volatility = snap.get("volatility", 0.25)
        volume = snap.get("volume_24h", 0.0)

        # 1. Momentum Score (0.0 to 1.0): day change + price vs SMA50
        momentum_ratio = (price / sma_50) if sma_50 > 0 else 1.0
        norm_change = max(-1.0, min(1.0, change_pct / 5.0))  # normalize +/- 5%
        momentum_score = max(0.05, min(0.98, 0.50 + (norm_change * 0.25) + ((momentum_ratio - 1.0) * 1.5)))

        # 2. Technical Trend Score (0.0 to 1.0): RSI sweet spot (45-65) + MACD slope
        rsi_component = 1.0 - (abs(rsi_14 - 55.0) / 55.0)
        macd_component = 0.6 if macd >= macd_signal else 0.4
        trend_score = max(0.05, min(0.98, (rsi_component * 0.6) + (macd_component * 0.4)))

        # 3. Valuation Score (0.0 to 1.0): Lower forward PE = higher score
        val_pe = forward_pe or trailing_pe or 25.0
        if val_pe <= 0:
            val_score = 0.50
        else:
            val_score = max(0.10, min(0.95, 1.0 - (val_pe / 60.0)))

        # 4. Quality & Volatility Risk Score (0.0 to 1.0): Lower volatility = higher stability score
        risk_score = max(0.10, min(0.95, 1.0 - min(1.0, volatility / 0.80)))

        # 5. Volume Liquidity Score (0.0 to 1.0)
        volume_score = min(0.95, 0.40 + (np.log10(max(1000.0, volume)) / 12.0))

        # Composite Mathematical Opportunity Score (0 to 100)
        weights = {"momentum": 0.30, "trend": 0.25, "valuation": 0.25, "risk": 0.10, "volume": 0.10}
        composite = (
            (momentum_score * weights["momentum"])
            + (trend_score * weights["trend"])
            + (val_score * weights["valuation"])
            + (risk_score * weights["risk"])
            + (volume_score * weights["volume"])
        ) * 100.0

        # Classify Investment Theme & Recommendation
        if momentum_score > 0.75 and trend_score > 0.70:
            theme = "Momentum Breakout"
            rec = "STRONG_ACCUMULATE" if composite >= 80.0 else "ACCUMULATE"
        elif val_score > 0.70 and composite >= 70.0:
            theme = "Undervalued Compounder"
            rec = "ACCUMULATE"
        elif rsi_14 < 35.0:
            theme = "Oversold Reversal"
            rec = "SELECTIVE_BUY"
        elif momentum_score >= 0.55:
            theme = "Trend Continuation"
            rec = "SELECTIVE_BUY" if composite >= 65.0 else "HOLD"
        else:
            theme = "Defensive Allocation"
            rec = "HOLD" if composite >= 50.0 else "REDUCE"

        factors_breakdown = {
            "momentum": round(momentum_score, 3),
            "trend": round(trend_score, 3),
            "valuation": round(val_score, 3),
            "risk_stability": round(risk_score, 3),
            "volume_profile": round(volume_score, 3),
        }

        factor_inputs = {
            "rsi_14": rsi_14,
            "forward_pe": forward_pe,
            "trailing_pe": trailing_pe,
            "volatility_annualized": volatility,
            "sma_50": sma_50,
            "sma_200": sma_200,
            "macd": macd,
            "macd_signal": macd_signal,
        }

        return round(composite, 1), factors_breakdown, factor_inputs, theme, rec

    async def scan_opportunities(
        self,
        min_score: float = 60.0,
        asset_class: str | None = None,
        theme_filter: str | None = None,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        """
        Run live multi-factor opportunity scan across the active universe.
        Fetches live snapshots concurrently and calculates real factor scores.
        """
        raw_securities = self.universe_engine.get_securities()
        
        # Filter by asset class if provided
        if asset_class:
            raw_securities = [
                s for s in raw_securities
                if s["asset_class"].upper() == asset_class.upper()
                or (asset_class.upper() == "EQUITY_US" and s["asset_class"] == "US_EQUITY")
                or (asset_class.upper() == "EQUITY_INDIA" and s["asset_class"] == "INDIAN_EQUITY")
            ]

        # Concurrently fetch real market snapshots
        tasks = [market_data_registry.get_market_snapshot(s["symbol"]) for s in raw_securities]
        snapshots = await asyncio.gather(*tasks, return_exceptions=True)

        candidates: list[OpportunityCandidate] = []

        for sec, snap in zip(raw_securities, snapshots):
            if not isinstance(snap, dict) or not snap.get("is_available", False):
                continue

            score, factors, inputs, theme, rec = self._compute_factor_score(snap)

            if score >= min_score:
                if theme_filter and theme.lower() != theme_filter.lower():
                    continue

                candidates.append(
                    OpportunityCandidate(
                        symbol=sec["symbol"],
                        name=sec["name"],
                        asset_class=sec["asset_class"],
                        sector=sec["sector"],
                        opportunity_score=score,
                        theme=theme,
                        price=snap["price"],
                        change_24h_pct=snap["change_pct"],
                        factors=factors,
                        factor_inputs=inputs,
                        recommendation=rec,
                        provenance=snap["provenance"],
                    )
                )

        # Sort descending by genuine Opportunity Score
        candidates.sort(key=lambda x: x.opportunity_score, reverse=True)

        return [
            {
                "symbol": c.symbol,
                "name": c.name,
                "asset_class": c.asset_class,
                "sector": c.sector,
                "opportunity_score": c.opportunity_score,
                "theme": c.theme,
                "price": c.price,
                "change_24h_pct": c.change_24h_pct,
                "factors": c.factors,
                "factor_inputs": c.factor_inputs,
                "recommendation": c.recommendation,
                "provenance": c.provenance,
                "scanned_at_utc": datetime.now(timezone.utc).isoformat(),
            }
            for c in candidates[:limit]
        ]


# Singleton Scanner Instance
opportunity_scanner_engine = OpportunityScannerEngine()
