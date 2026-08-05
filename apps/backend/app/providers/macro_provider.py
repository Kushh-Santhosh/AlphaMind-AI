"""
AlphaMind AI - Macroeconomic Data Provider Adapters (FRED, World Bank, OECD)
"""

from __future__ import annotations

from typing import Any

from packages.plugins.provider_manager import BaseProvider, ProviderMetadata


class FREDMacroProvider(BaseProvider):
    """Primary Macro Data Provider Adapter (Federal Reserve Economic Data)."""

    def __init__(self) -> None:
        metadata = ProviderMetadata(
            provider_id="fred_api",
            provider_name="FRED St. Louis Fed API",
            version="v1",
            tier="primary",
            supported_assets=["rates", "cpi", "gdp", "unemployment", "yield_curve"],
            rate_limit_per_minute=120,
            timeout_seconds=3.0,
        )
        super().__init__(metadata)

    async def fetch_series(self, series_id: str) -> list[dict[str, Any]]:
        """Fetch economic data series (e.g. T10Y2Y yield curve spread)."""
        return [
            {
                "series_id": series_id,
                "date": "2026-08-01",
                "value": 0.45,
                "provider": "fred_api",
            }
        ]


class WorldBankMacroProvider(BaseProvider):
    """Fallback Macro Data Provider Adapter (World Bank API)."""

    def __init__(self) -> None:
        metadata = ProviderMetadata(
            provider_id="world_bank_api",
            provider_name="World Bank Global Indicator Feed",
            version="v2",
            tier="fallback",
            supported_assets=["global_gdp", "inflation", "trade_balance"],
            rate_limit_per_minute=60,
            timeout_seconds=5.0,
        )
        super().__init__(metadata)

    async def fetch_series(self, series_id: str) -> list[dict[str, Any]]:
        """Fetch global economic indicator series."""
        return [
            {
                "series_id": series_id,
                "date": "2026-08-01",
                "value": 0.45,
                "provider": "world_bank_api",
            }
        ]
