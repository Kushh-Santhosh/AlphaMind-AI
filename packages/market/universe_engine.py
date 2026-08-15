"""
AlphaMind AI - Broad Asset Universe Engine
Supports configurable multi-asset discovery across US Equities, Indian Equities (NSE),
Global ETFs, Crypto, and Sectors with lifecycle status tracking (discovered, screened, researched, monitored).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class AssetSecurity:
    symbol: str
    name: str
    asset_class: str  # "US_EQUITY", "INDIAN_EQUITY", "GLOBAL_ETF", "CRYPTO", "COMMODITY"
    sector: str
    market_cap_tier: str  # "MEGA_CAP", "LARGE_CAP", "MID_CAP", "SMALL_CAP"
    status: str = "discovered"  # "discovered", "screened", "researched", "deeply_analyzed", "monitored"
    base_price: float = 100.0
    exchange: str = "NASDAQ"


class AssetUniverseEngine:
    """Discovers, screens, filters, and manages institutional investment universes."""

    def __init__(self) -> None:
        self.universes: dict[str, list[AssetSecurity]] = {
            "US_EQUITIES": [
                AssetSecurity("NVDA", "NVIDIA Corporation", "US_EQUITY", "Semiconductors", "MEGA_CAP", "deeply_analyzed", 132.50, "NASDAQ"),
                AssetSecurity("AAPL", "Apple Inc.", "US_EQUITY", "Consumer Electronics", "MEGA_CAP", "deeply_analyzed", 228.40, "NASDAQ"),
                AssetSecurity("MSFT", "Microsoft Corporation", "US_EQUITY", "Software Infrastructure", "MEGA_CAP", "deeply_analyzed", 418.20, "NASDAQ"),
                AssetSecurity("GOOGL", "Alphabet Inc.", "US_EQUITY", "Internet Content & Information", "MEGA_CAP", "researched", 182.10, "NASDAQ"),
                AssetSecurity("AMZN", "Amazon.com Inc.", "US_EQUITY", "E-Commerce & Cloud", "MEGA_CAP", "researched", 188.60, "NASDAQ"),
                AssetSecurity("TSLA", "Tesla Inc.", "US_EQUITY", "Auto Manufacturers & Clean Tech", "LARGE_CAP", "researched", 218.40, "NASDAQ"),
                AssetSecurity("META", "Meta Platforms Inc.", "US_EQUITY", "Social Media & AI", "MEGA_CAP", "researched", 585.10, "NASDAQ"),
                AssetSecurity("AMD", "Advanced Micro Devices", "US_EQUITY", "Semiconductors", "LARGE_CAP", "screened", 146.20, "NASDAQ"),
                AssetSecurity("PLTR", "Palantir Technologies", "US_EQUITY", "Enterprise Software & AI", "LARGE_CAP", "researched", 62.40, "NYSE"),
                AssetSecurity("JPM", "JPMorgan Chase & Co.", "US_EQUITY", "Diversified Financials", "MEGA_CAP", "monitored", 234.10, "NYSE"),
                AssetSecurity("LLY", "Eli Lilly and Company", "US_EQUITY", "Pharmaceuticals", "MEGA_CAP", "screened", 860.50, "NYSE"),
                AssetSecurity("AVGO", "Broadcom Inc.", "US_EQUITY", "Semiconductors", "MEGA_CAP", "screened", 178.90, "NASDAQ"),
            ],
            "INDIAN_EQUITIES": [
                AssetSecurity("RELIANCE.NS", "Reliance Industries Ltd", "INDIAN_EQUITY", "Energy & Conglomerate", "MEGA_CAP", "deeply_analyzed", 1380.00, "NSE"),
                AssetSecurity("TCS.NS", "Tata Consultancy Services", "INDIAN_EQUITY", "IT Services", "MEGA_CAP", "researched", 4120.00, "NSE"),
                AssetSecurity("INFY.NS", "Infosys Ltd", "INDIAN_EQUITY", "IT Services", "LARGE_CAP", "researched", 1860.00, "NSE"),
                AssetSecurity("HDFCBANK.NS", "HDFC Bank Ltd", "INDIAN_EQUITY", "Banking", "MEGA_CAP", "researched", 1740.00, "NSE"),
                AssetSecurity("ICICIBANK.NS", "ICICI Bank Ltd", "INDIAN_EQUITY", "Banking", "LARGE_CAP", "screened", 1260.00, "NSE"),
                AssetSecurity("BHARTIARTL.NS", "Bharti Airtel Ltd", "INDIAN_EQUITY", "Telecom", "LARGE_CAP", "screened", 1620.00, "NSE"),
                AssetSecurity("TATAMOTORS.NS", "Tata Motors Ltd", "INDIAN_EQUITY", "Automotive", "LARGE_CAP", "screened", 980.00, "NSE"),
                AssetSecurity("LT.NS", "Larsen & Toubro Ltd", "INDIAN_EQUITY", "Infrastructure", "LARGE_CAP", "monitored", 3640.00, "NSE"),
            ],
            "GLOBAL_ETFS": [
                AssetSecurity("SPY", "SPDR S&P 500 ETF Trust", "GLOBAL_ETF", "Broad Market", "MEGA_CAP", "deeply_analyzed", 582.30, "NYSE Arca"),
                AssetSecurity("QQQ", "Invesco QQQ Trust", "GLOBAL_ETF", "Technology", "MEGA_CAP", "deeply_analyzed", 504.20, "NASDAQ"),
                AssetSecurity("SMH", "VanEck Semiconductor ETF", "GLOBAL_ETF", "Semiconductors", "LARGE_CAP", "researched", 248.60, "NASDAQ"),
                AssetSecurity("VTI", "Vanguard Total Stock Market", "GLOBAL_ETF", "Total US Market", "MEGA_CAP", "monitored", 285.40, "NYSE Arca"),
                AssetSecurity("GLD", "SPDR Gold Shares", "GLOBAL_ETF", "Precious Metals", "LARGE_CAP", "researched", 244.10, "NYSE Arca"),
                AssetSecurity("TLT", "iShares 20+ Year Treasury Bond", "GLOBAL_ETF", "Fixed Income", "LARGE_CAP", "researched", 92.40, "NASDAQ"),
            ],
            "CRYPTO": [
                AssetSecurity("BTC", "Bitcoin", "CRYPTO", "Layer 1 Store of Value", "MEGA_CAP", "deeply_analyzed", 92400.00, "Global Crypto"),
                AssetSecurity("ETH", "Ethereum", "CRYPTO", "Smart Contract Platform", "MEGA_CAP", "researched", 2740.00, "Global Crypto"),
                AssetSecurity("SOL", "Solana", "CRYPTO", "High Throughput L1", "LARGE_CAP", "researched", 188.50, "Global Crypto"),
                AssetSecurity("BNB", "BNB", "CRYPTO", "Exchange Ecosystem", "LARGE_CAP", "monitored", 640.00, "Global Crypto"),
            ],
        }

    def list_universes(self) -> list[str]:
        """Return list of available universe categories."""
        return list(self.universes.keys())

    def get_securities(self, universe: str | None = None, status: str | None = None, sector: str | None = None) -> list[dict[str, Any]]:
        """Filter securities across supported asset universes."""
        results: list[AssetSecurity] = []
        if universe and universe in self.universes:
            candidates = self.universes[universe]
        else:
            candidates = [s for sublist in self.universes.values() for s in sublist]

        for s in candidates:
            if status and s.status != status:
                continue
            if sector and s.sector.lower() != sector.lower():
                continue
            results.append(s)

        return [
            {
                "symbol": s.symbol,
                "name": s.name,
                "asset_class": s.asset_class,
                "sector": s.sector,
                "market_cap_tier": s.market_cap_tier,
                "status": s.status,
                "base_price": s.base_price,
                "exchange": s.exchange,
            }
            for s in results
        ]

    def update_security_status(self, symbol: str, new_status: str) -> bool:
        """Update lifecycle status of an asset as it moves through research."""
        for sublist in self.universes.values():
            for s in sublist:
                if s.symbol.upper() == symbol.upper():
                    s.status = new_status
                    return True
        return False
