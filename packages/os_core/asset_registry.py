"""
AlphaMind AI v2 - Canonical Asset Registry

Single canonical source of truth for all supported asset classes:
Stocks, ETFs, Crypto, Forex, Commodities, Bonds, Mutual Funds, Options, and Futures.
Every asset receives an immutable AssetUUID referenced across all platform subsystems.
"""

from __future__ import annotations

import logging
import uuid
from enum import Enum

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class AssetClass(str, Enum):  # noqa: UP042
    STOCKS = "STOCKS"
    ETFS = "ETFS"
    CRYPTO = "CRYPTO"
    FOREX = "FOREX"
    COMMODITIES = "COMMODITIES"
    BONDS = "BONDS"
    MUTUAL_FUNDS = "MUTUAL_FUNDS"
    OPTIONS = "OPTIONS"
    FUTURES = "FUTURES"


class CanonicalAsset(BaseModel):
    asset_uuid: str = Field(default_factory=lambda: f"asset_{uuid.uuid4().hex[:12]}")
    symbol: str
    canonical_name: str
    asset_class: AssetClass
    exchange: str = "NASDAQ"
    currency: str = "USD"
    sector: str | None = None
    industry: str | None = None
    is_active: bool = True


class CanonicalAssetRegistry:
    """Registry maintaining canonical mapping between symbols, UUIDs, and asset metadata."""

    def __init__(self) -> None:
        self.symbol_map: dict[str, CanonicalAsset] = {}
        self.uuid_map: dict[str, CanonicalAsset] = {}
        self._seed_default_assets()

    def _seed_default_assets(self) -> None:
        """Seed initial canonical assets for equities, ETFs, crypto, forex, and bonds."""
        defaults = [
            CanonicalAsset(
                symbol="AAPL",
                canonical_name="Apple Inc.",
                asset_class=AssetClass.STOCKS,
                sector="Technology",
            ),
            CanonicalAsset(
                symbol="NVDA",
                canonical_name="NVIDIA Corporation",
                asset_class=AssetClass.STOCKS,
                sector="Technology",
            ),
            CanonicalAsset(
                symbol="MSFT",
                canonical_name="Microsoft Corporation",
                asset_class=AssetClass.STOCKS,
                sector="Technology",
            ),
            CanonicalAsset(
                symbol="GOOGL",
                canonical_name="Alphabet Inc.",
                asset_class=AssetClass.STOCKS,
                sector="Communication",
            ),
            CanonicalAsset(
                symbol="SPY",
                canonical_name="SPDR S&P 500 ETF Trust",
                asset_class=AssetClass.ETFS,
                sector="Index ETF",
            ),
            CanonicalAsset(
                symbol="QQQ",
                canonical_name="Invesco QQQ Trust",
                asset_class=AssetClass.ETFS,
                sector="Index ETF",
            ),
            CanonicalAsset(
                symbol="BTC-USD",
                canonical_name="Bitcoin USD",
                asset_class=AssetClass.CRYPTO,
                exchange="BINANCE",
            ),
            CanonicalAsset(
                symbol="ETH-USD",
                canonical_name="Ethereum USD",
                asset_class=AssetClass.CRYPTO,
                exchange="BINANCE",
            ),
            CanonicalAsset(
                symbol="EURUSD",
                canonical_name="Euro / US Dollar",
                asset_class=AssetClass.FOREX,
                exchange="FXCM",
            ),
            CanonicalAsset(
                symbol="TLT",
                canonical_name="iShares 20+ Year Treasury Bond ETF",
                asset_class=AssetClass.BONDS,
                sector="Fixed Income",
            ),
        ]
        for asset in defaults:
            self.register_asset(asset)

    def register_asset(self, asset: CanonicalAsset) -> CanonicalAsset:
        """Register or update asset in canonical registry."""
        sym_clean = asset.symbol.upper()
        self.symbol_map[sym_clean] = asset
        self.uuid_map[asset.asset_uuid] = asset
        logger.info(
            "Registered canonical asset '%s' (%s -> %s)",
            sym_clean,
            asset.asset_class.value,
            asset.asset_uuid,
        )
        return asset

    def get_by_symbol(self, symbol: str) -> CanonicalAsset | None:
        """Fetch asset by symbol."""
        return self.symbol_map.get(symbol.upper())

    def get_by_uuid(self, asset_uuid: str) -> CanonicalAsset | None:
        """Fetch asset by canonical UUID."""
        return self.uuid_map.get(asset_uuid)

    def list_all_assets(self) -> list[CanonicalAsset]:
        """List all canonical assets."""
        return list(self.symbol_map.values())
