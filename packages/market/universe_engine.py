"""
AlphaMind AI - Dynamic Refreshable Asset Universe Engine (v4.0)

Manages comprehensive multi-asset universes across:
  - US Equities: S&P 500, Nasdaq 100, Mega-Cap & Mid-Cap Leaders
  - Indian Equities (NSE): NIFTY 50, NIFTY IT, NIFTY Bank, NIFTY Auto
  - Global ETFs: Equity Sectors, Fixed Income, Commodities, Country ETFs
  - Crypto: Top 20 Layer-1s, DeFi, and Infrastructure protocols
  - Custom User-Defined Universes

Lifecycle tracking: discovered -> screened -> researched -> deeply_analyzed -> monitored.
No static mock prices. Prices are populated on-demand via DataProviderRegistry.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional

from packages.market.provider_registry import market_data_registry

logger = logging.getLogger(__name__)


@dataclass
class AssetSecurity:
    symbol: str
    name: str
    asset_class: str  # "US_EQUITY", "INDIAN_EQUITY", "GLOBAL_ETF", "CRYPTO", "COMMODITY"
    sector: str
    market_cap_tier: str  # "MEGA_CAP", "LARGE_CAP", "MID_CAP", "SMALL_CAP"
    exchange: str
    status: str = "discovered"  # "discovered", "screened", "researched", "deeply_analyzed", "monitored"
    weight_in_index: Optional[float] = None


class AssetUniverseEngine:
    """Discovers, filters, refreshes, and manages institutional multi-asset universes."""

    def __init__(self) -> None:
        self.universes: dict[str, list[AssetSecurity]] = {
            "US_EQUITIES": [
                AssetSecurity("NVDA", "NVIDIA Corporation", "US_EQUITY", "Semiconductors", "MEGA_CAP", "NASDAQ", "deeply_analyzed"),
                AssetSecurity("AAPL", "Apple Inc.", "US_EQUITY", "Consumer Electronics", "MEGA_CAP", "NASDAQ", "deeply_analyzed"),
                AssetSecurity("MSFT", "Microsoft Corporation", "US_EQUITY", "Software Infrastructure", "MEGA_CAP", "deeply_analyzed"),
                AssetSecurity("GOOGL", "Alphabet Inc.", "US_EQUITY", "Internet Content & AI", "MEGA_CAP", "researched"),
                AssetSecurity("AMZN", "Amazon.com Inc.", "US_EQUITY", "E-Commerce & Cloud", "MEGA_CAP", "researched"),
                AssetSecurity("META", "Meta Platforms Inc.", "US_EQUITY", "Social Platforms & AI", "MEGA_CAP", "researched"),
                AssetSecurity("TSLA", "Tesla Inc.", "US_EQUITY", "Auto & Clean Tech", "LARGE_CAP", "researched"),
                AssetSecurity("AVGO", "Broadcom Inc.", "US_EQUITY", "Semiconductors", "MEGA_CAP", "screened"),
                AssetSecurity("AMD", "Advanced Micro Devices", "US_EQUITY", "Semiconductors", "LARGE_CAP", "screened"),
                AssetSecurity("PLTR", "Palantir Technologies", "US_EQUITY", "Enterprise AI Software", "LARGE_CAP", "researched"),
                AssetSecurity("JPM", "JPMorgan Chase & Co.", "US_EQUITY", "Financial Services", "MEGA_CAP", "monitored"),
                AssetSecurity("LLY", "Eli Lilly and Company", "US_EQUITY", "Healthcare & Pharma", "MEGA_CAP", "screened"),
                AssetSecurity("V", "Visa Inc.", "US_EQUITY", "Financial Technology", "MEGA_CAP", "monitored"),
                AssetSecurity("UNH", "UnitedHealth Group", "US_EQUITY", "Healthcare Managed Care", "MEGA_CAP", "screened"),
                AssetSecurity("XOM", "Exxon Mobil Corp", "US_EQUITY", "Energy & Refining", "MEGA_CAP", "monitored"),
                AssetSecurity("COST", "Costco Wholesale Corp", "US_EQUITY", "Consumer Staples", "LARGE_CAP", "screened"),
                AssetSecurity("CRM", "Salesforce Inc.", "US_EQUITY", "Enterprise Cloud Software", "LARGE_CAP", "screened"),
                AssetSecurity("NFLX", "Netflix Inc.", "US_EQUITY", "Entertainment Streaming", "LARGE_CAP", "screened"),
                AssetSecurity("QCOM", "QUALCOMM Inc.", "US_EQUITY", "Mobile & Edge Processors", "LARGE_CAP", "screened"),
                AssetSecurity("INTC", "Intel Corporation", "US_EQUITY", "Semiconductors", "LARGE_CAP", "screened"),
            ],
            "INDIAN_EQUITIES": [
                AssetSecurity("RELIANCE.NS", "Reliance Industries Ltd", "INDIAN_EQUITY", "Energy & Telecom", "MEGA_CAP", "NSE", "deeply_analyzed"),
                AssetSecurity("TCS.NS", "Tata Consultancy Services", "INDIAN_EQUITY", "IT Consulting", "MEGA_CAP", "NSE", "researched"),
                AssetSecurity("INFY.NS", "Infosys Ltd", "INDIAN_EQUITY", "IT Services", "LARGE_CAP", "NSE", "researched"),
                AssetSecurity("HDFCBANK.NS", "HDFC Bank Ltd", "INDIAN_EQUITY", "Private Banking", "MEGA_CAP", "NSE", "researched"),
                AssetSecurity("ICICIBANK.NS", "ICICI Bank Ltd", "INDIAN_EQUITY", "Private Banking", "LARGE_CAP", "NSE", "screened"),
                AssetSecurity("BHARTIARTL.NS", "Bharti Airtel Ltd", "INDIAN_EQUITY", "Telecommunications", "LARGE_CAP", "NSE", "screened"),
                AssetSecurity("SBIN.NS", "State Bank of India", "INDIAN_EQUITY", "Public Banking", "LARGE_CAP", "NSE", "screened"),
                AssetSecurity("TATAMOTORS.NS", "Tata Motors Ltd", "INDIAN_EQUITY", "Automotive & EV", "LARGE_CAP", "NSE", "screened"),
                AssetSecurity("LT.NS", "Larsen & Toubro Ltd", "INDIAN_EQUITY", "Infrastructure & Defense", "LARGE_CAP", "NSE", "monitored"),
                AssetSecurity("ITC.NS", "ITC Ltd", "INDIAN_EQUITY", "Consumer Staples & Hotels", "LARGE_CAP", "NSE", "screened"),
                AssetSecurity("KOTAKBANK.NS", "Kotak Mahindra Bank", "INDIAN_EQUITY", "Private Banking", "LARGE_CAP", "NSE", "screened"),
                AssetSecurity("SUNPHARMA.NS", "Sun Pharma Industries", "INDIAN_EQUITY", "Pharmaceuticals", "LARGE_CAP", "NSE", "screened"),
                AssetSecurity("WIPRO.NS", "Wipro Ltd", "INDIAN_EQUITY", "IT Services", "LARGE_CAP", "NSE", "screened"),
                AssetSecurity("MARUTI.NS", "Maruti Suzuki India", "INDIAN_EQUITY", "Automotive", "LARGE_CAP", "NSE", "screened"),
                AssetSecurity("BAJFINANCE.NS", "Bajaj Finance Ltd", "INDIAN_EQUITY", "Non-Banking Financial", "LARGE_CAP", "NSE", "screened"),
            ],
            "GLOBAL_ETFS": [
                AssetSecurity("SPY", "SPDR S&P 500 ETF Trust", "GLOBAL_ETF", "Broad Market US", "MEGA_CAP", "NYSE Arca", "deeply_analyzed"),
                AssetSecurity("QQQ", "Invesco QQQ Trust", "GLOBAL_ETF", "Technology & Growth", "MEGA_CAP", "NASDAQ", "deeply_analyzed"),
                AssetSecurity("SMH", "VanEck Semiconductor ETF", "GLOBAL_ETF", "Semiconductors", "LARGE_CAP", "NASDAQ", "researched"),
                AssetSecurity("IWM", "iShares Russell 2000 ETF", "GLOBAL_ETF", "Small Cap US", "LARGE_CAP", "NYSE Arca", "screened"),
                AssetSecurity("VTI", "Vanguard Total Stock Market", "GLOBAL_ETF", "Total US Market", "MEGA_CAP", "NYSE Arca", "monitored"),
                AssetSecurity("GLD", "SPDR Gold Shares", "GLOBAL_ETF", "Precious Metals", "LARGE_CAP", "NYSE Arca", "researched"),
                AssetSecurity("TLT", "iShares 20+ Year Treasury Bond", "GLOBAL_ETF", "Long-Term US Treasuries", "LARGE_CAP", "NASDAQ", "researched"),
                AssetSecurity("EEM", "iShares MSCI Emerging Markets", "GLOBAL_ETF", "Emerging Equities", "LARGE_CAP", "NYSE Arca", "screened"),
                AssetSecurity("XLE", "Energy Select Sector SPDR", "GLOBAL_ETF", "Energy Sector", "LARGE_CAP", "NYSE Arca", "screened"),
                AssetSecurity("XLF", "Financial Select Sector SPDR", "GLOBAL_ETF", "Financial Sector", "LARGE_CAP", "NYSE Arca", "screened"),
                AssetSecurity("XLK", "Technology Select Sector SPDR", "GLOBAL_ETF", "Technology Sector", "LARGE_CAP", "NYSE Arca", "screened"),
                AssetSecurity("HYG", "iShares iBoxx High Yield Corporate", "GLOBAL_ETF", "High Yield Credit", "LARGE_CAP", "NYSE Arca", "screened"),
            ],
            "CRYPTO": [
                AssetSecurity("BTC", "Bitcoin", "CRYPTO", "Layer 1 Store of Value", "MEGA_CAP", "Global Crypto", "deeply_analyzed"),
                AssetSecurity("ETH", "Ethereum", "CRYPTO", "Smart Contract Platform", "MEGA_CAP", "Global Crypto", "researched"),
                AssetSecurity("SOL", "Solana", "CRYPTO", "High Throughput Layer 1", "LARGE_CAP", "Global Crypto", "researched"),
                AssetSecurity("BNB", "BNB Chain", "CRYPTO", "Exchange & DeFi Ecosystem", "LARGE_CAP", "Global Crypto", "monitored"),
                AssetSecurity("XRP", "XRP", "CRYPTO", "Cross-Border Settlement", "LARGE_CAP", "Global Crypto", "screened"),
                AssetSecurity("ADA", "Cardano", "CRYPTO", "Proof of Stake Layer 1", "LARGE_CAP", "Global Crypto", "screened"),
                AssetSecurity("AVAX", "Avalanche", "CRYPTO", "Multi-Chain Subnets", "LARGE_CAP", "Global Crypto", "screened"),
                AssetSecurity("LINK", "Chainlink", "CRYPTO", "Decentralized Oracle Network", "LARGE_CAP", "Global Crypto", "screened"),
                AssetSecurity("DOT", "Polkadot", "CRYPTO", "Interoperability Protocol", "LARGE_CAP", "Global Crypto", "screened"),
            ],
            "ENERGY_COMMODITIES": [
                AssetSecurity("WTI", "Crude Oil WTI Futures", "ENERGY", "Crude Petroleum", "MEGA_CAP", "NYMEX", "deeply_analyzed"),
                AssetSecurity("BRENT", "Brent Crude Oil Futures", "ENERGY", "Crude Petroleum", "MEGA_CAP", "ICE", "researched"),
                AssetSecurity("NATGAS", "Natural Gas Futures", "ENERGY", "Natural Gas", "LARGE_CAP", "NYMEX", "researched"),
                AssetSecurity("GOLD", "Gold Futures", "COMMODITY", "Precious Metals", "MEGA_CAP", "COMEX", "deeply_analyzed"),
                AssetSecurity("SILVER", "Silver Futures", "COMMODITY", "Precious Metals", "LARGE_CAP", "COMEX", "screened"),
                AssetSecurity("COPPER", "Copper Futures", "COMMODITY", "Industrial Metals", "LARGE_CAP", "COMEX", "screened"),
            ],
        }
        self.custom_universes: dict[str, list[AssetSecurity]] = {}

    def list_universes(self) -> list[str]:
        """Return list of available universe categories."""
        return list(self.universes.keys()) + list(self.custom_universes.keys())

    def get_securities(
        self,
        universe: str | None = None,
        status: str | None = None,
        sector: str | None = None,
    ) -> list[dict[str, Any]]:
        """Filter raw securities across supported asset universes."""
        all_map = {**self.universes, **self.custom_universes}
        if universe and universe in all_map:
            candidates = all_map[universe]
        else:
            candidates = [s for sublist in all_map.values() for s in sublist]

        results = []
        for s in candidates:
            if status and s.status != status:
                continue
            if sector and s.sector.lower() != sector.lower():
                continue
            results.append(
                {
                    "symbol": s.symbol,
                    "name": s.name,
                    "asset_class": s.asset_class,
                    "sector": s.sector,
                    "market_cap_tier": s.market_cap_tier,
                    "status": s.status,
                    "exchange": s.exchange,
                }
            )
        return results

    async def get_enriched_securities(
        self,
        universe: str | None = None,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        """
        Fetch universe securities enriched with REAL live market snapshot from provider.
        Concurrently executes batch snapshot retrieval.
        """
        base_list = self.get_securities(universe=universe)[:limit]
        
        # Batch gather real snapshots
        tasks = [market_data_registry.get_market_snapshot(s["symbol"]) for s in base_list]
        snapshots = await asyncio.gather(*tasks, return_exceptions=True)

        enriched = []
        for sec, snap in zip(base_list, snapshots):
            if isinstance(snap, dict) and snap.get("is_available", False):
                enriched.append({
                    **sec,
                    "price": snap["price"],
                    "change_pct": snap["change_pct"],
                    "volume_24h": snap["volume_24h"],
                    "day_high": snap["day_high"],
                    "day_low": snap["day_low"],
                    "market_cap_usd": snap["market_cap_usd"],
                    "rsi_14": snap["rsi_14"],
                    "sma_50": snap["sma_50"],
                    "provenance": snap["provenance"],
                })
            else:
                enriched.append({
                    **sec,
                    "price": 0.0,
                    "change_pct": 0.0,
                    "volume_24h": 0.0,
                    "day_high": 0.0,
                    "day_low": 0.0,
                    "market_cap_usd": 0.0,
                    "rsi_14": 50.0,
                    "sma_50": 0.0,
                    "provenance": {
                        "source": "Unavailable",
                        "provider": "yfinance",
                        "retrieved_at": datetime.now(timezone.utc).isoformat(),
                        "data_timestamp": "UNAVAILABLE",
                        "age_seconds": 0.0,
                        "freshness": "UNAVAILABLE",
                        "is_stale": True,
                        "market_status": "UNKNOWN",
                    },
                })
        return enriched

    def update_security_status(self, symbol: str, new_status: str) -> bool:
        """Update lifecycle status of an asset as it moves through research."""
        all_map = {**self.universes, **self.custom_universes}
        for sublist in all_map.values():
            for s in sublist:
                if s.symbol.upper() == symbol.upper():
                    s.status = new_status
                    return True
        return False


# Singleton Global Universe Engine
asset_universe_engine = AssetUniverseEngine()
