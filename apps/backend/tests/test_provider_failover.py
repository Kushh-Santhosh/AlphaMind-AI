"""
Data Foundation Test Suite — Provider Failover, Resilience & Rate Limiting Tests
"""

import pytest

from apps.backend.app.exceptions import DataProviderException
from apps.backend.app.providers.market_provider import (
    AlphaVantageMarketProvider,
    PolygonMarketProvider,
    YFinanceMarketProvider,
)
from packages.plugins.provider_manager import (
    BaseProvider,
    ProviderFailoverManager,
    TokenBucketRateLimiter,
)


@pytest.mark.asyncio
async def test_token_bucket_rate_limiter() -> None:
    """Test rate limiter acquires tokens properly."""
    limiter = TokenBucketRateLimiter(rate_per_minute=600)  # 10 tokens per sec
    await limiter.acquire()
    assert limiter.tokens >= 0


@pytest.mark.asyncio
async def test_provider_failover_primary_success() -> None:
    """Primary provider succeeds -> tier_used should be 'primary'."""
    primary = PolygonMarketProvider()
    secondary = AlphaVantageMarketProvider()
    fallback = YFinanceMarketProvider()

    manager = ProviderFailoverManager(primary, secondary, fallback)

    async def fetch_op(p: BaseProvider) -> list:
        return await p.fetch_bars("AAPL", "1D", "2026-08-01", "2026-08-04")

    resp = await manager.execute_query(fetch_op)
    assert resp.tier_used == "primary"
    assert resp.provider_id == "polygon_io"
    assert len(resp.data) == 1
    assert resp.data[0]["symbol"] == "AAPL"


@pytest.mark.asyncio
async def test_provider_failover_to_secondary() -> None:
    """Primary fails -> failover manager routes to secondary provider."""
    primary = PolygonMarketProvider()
    primary.metadata.is_healthy = False  # Simulate primary outage

    secondary = AlphaVantageMarketProvider()
    fallback = YFinanceMarketProvider()

    manager = ProviderFailoverManager(primary, secondary, fallback)

    async def fetch_op(p: BaseProvider) -> list:
        return await p.fetch_bars("AAPL", "1D", "2026-08-01", "2026-08-04")

    resp = await manager.execute_query(fetch_op)
    assert resp.tier_used == "secondary"
    assert resp.provider_id == "alpha_vantage"


@pytest.mark.asyncio
async def test_provider_failover_exhaustion_raises_exception() -> None:
    """All 3 providers unhealthy -> raises DataProviderException."""
    primary = PolygonMarketProvider()
    primary.metadata.is_healthy = False
    secondary = AlphaVantageMarketProvider()
    secondary.metadata.is_healthy = False
    fallback = YFinanceMarketProvider()
    fallback.metadata.is_healthy = False

    manager = ProviderFailoverManager(primary, secondary, fallback)

    async def failing_op(p: BaseProvider) -> list:
        raise RuntimeError("Network timeout")

    with pytest.raises(DataProviderException):
        await manager.execute_query(failing_op)
