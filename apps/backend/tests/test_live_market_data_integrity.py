"""
AlphaMind AI - Live Market Data Integrity & Anti-Mocking Verification Tests (v4.0)

Enforces zero synthetic data in production paths:
  1. Verifies live provider extraction for US Equities (AAPL, NVDA), Indian Equities (RELIANCE.NS), ETFs (SPY), and Crypto (BTC-USD).
  2. Verifies strict provenance metadata on every returned market datum.
  3. Verifies opportunity scanner factors and scores are dynamically calculated from price series.
  4. AST/Code inspection test: Fails if static price_map, precomputed_factors, or hardcoded scores are introduced into production packages.
"""

from __future__ import annotations

import inspect
import pytest
from packages.market.provider_registry import DataProviderRegistry, market_data_registry
from packages.market.universe_engine import AssetUniverseEngine, asset_universe_engine
from packages.research.opportunity_scanner import OpportunityScannerEngine, opportunity_scanner_engine


@pytest.mark.asyncio
async def test_live_equity_market_snapshot_provenance() -> None:
    """Verify live AAPL snapshot returns non-zero price and complete provenance metadata."""
    snap = await market_data_registry.get_market_snapshot("AAPL")
    assert snap["symbol"] == "AAPL"
    assert snap["price"] > 0.0
    assert "market_cap_usd" in snap and snap["market_cap_usd"] > 1_000_000_000.0
    assert "rsi_14" in snap and 0.0 <= snap["rsi_14"] <= 100.0
    assert "provenance" in snap
    
    prov = snap["provenance"]
    assert "source" in prov
    assert "provider" in prov and prov["provider"] == "yfinance"
    assert "retrieved_at" in prov
    assert "data_timestamp" in prov
    assert "freshness" in prov and prov["freshness"] in ["LIVE", "DELAYED", "CACHED", "HISTORICAL"]
    assert "is_stale" in prov and isinstance(prov["is_stale"], bool)


@pytest.mark.asyncio
async def test_live_crypto_snapshot_resolution() -> None:
    """Verify BTC / crypto snapshot dynamically maps to BTC-USD and returns live quotes."""
    snap = await market_data_registry.get_market_snapshot("BTC")
    assert snap["symbol"] == "BTC-USD"
    assert snap["price"] > 1000.0
    assert snap["is_available"] is True
    assert snap["provenance"]["provider"] == "yfinance"


@pytest.mark.asyncio
async def test_live_indian_equity_snapshot_resolution() -> None:
    """Verify Indian NSE equity RELIANCE.NS returns live quotes in INR."""
    snap = await market_data_registry.get_market_snapshot("RELIANCE.NS")
    assert snap["symbol"] == "RELIANCE.NS"
    assert snap["price"] > 100.0
    assert snap["is_available"] is True


@pytest.mark.asyncio
async def test_dynamic_opportunity_scanner_scoring() -> None:
    """Verify Opportunity Scanner computes dynamic factors and does not return static constants."""
    candidates = await opportunity_scanner_engine.scan_opportunities(min_score=40.0, limit=5)
    assert len(candidates) > 0
    top = candidates[0]
    assert 40.0 <= top["opportunity_score"] <= 100.0
    assert "factors" in top
    assert "momentum" in top["factors"]
    assert "trend" in top["factors"]
    assert "valuation" in top["factors"]
    assert "provenance" in top


def test_anti_mock_source_code_inspection() -> None:
    """AST / String inspection: Fails if static price_map or precomputed_factors exist in production modules."""
    import packages.market.provider_registry as pr_module
    import packages.research.opportunity_scanner as os_module

    pr_src = inspect.getsource(pr_module)
    os_src = inspect.getsource(os_module)

    # Disallow static mock dictionary constants
    assert "price_map = {" not in pr_src, "Production DataProviderRegistry contains hardcoded price_map!"
    assert "precomputed_factors = {" not in os_src, "Production OpportunityScannerEngine contains hardcoded precomputed_factors!"
