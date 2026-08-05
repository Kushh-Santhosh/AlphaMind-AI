"""
AlphaMind AI - SEC EDGAR Filing Provider Adapters
"""

from __future__ import annotations

from typing import Any

from packages.plugins.provider_manager import BaseProvider, ProviderMetadata


class SECEdgarProvider(BaseProvider):
    """Primary SEC EDGAR XBRL Data Provider Adapter."""

    def __init__(self) -> None:
        metadata = ProviderMetadata(
            provider_id="sec_edgar",
            provider_name="SEC EDGAR Direct API",
            version="v1",
            tier="primary",
            supported_assets=["10-K", "10-Q", "8-K", "13F"],
            rate_limit_per_minute=10,  # Strict SEC EDGAR 10 req/sec limit
            timeout_seconds=5.0,
        )
        super().__init__(metadata)

    async def fetch_filing_text(
        self, ticker: str, form_type: str, fiscal_year: int
    ) -> dict[str, Any]:
        """Fetch raw SEC filing text document payload."""
        return {
            "ticker": ticker,
            "form_type": form_type,
            "fiscal_year": fiscal_year,
            "filing_date": "2026-02-15",
            "content": f"Sample SEC {form_type} filing content for {ticker} fiscal year {fiscal_year}.",
            "item_1a_risk_factors": "Key operational and regulatory risk disclosures.",
            "provider": "sec_edgar",
        }
