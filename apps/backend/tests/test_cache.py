"""
Data Foundation Test Suite — Redis Cache Keys & TTL Policy Tests
"""

from apps.backend.app.core.cache import CacheKeyBuilder, RedisCacheManager


def test_cache_key_builder_namespaces() -> None:
    """Verify Redis key namespace formatting."""
    assert CacheKeyBuilder.quote_key("aapl") == "quote:AAPL"
    assert CacheKeyBuilder.bars_key("nvda", "1D") == "bars:NVDA:1D"
    assert CacheKeyBuilder.macro_key("CPI") == "macro:CPI"
    assert CacheKeyBuilder.sec_key("tsla", "10-k", 2025) == "sec:TSLA:10-K:2025"


def test_ttl_policies() -> None:
    """Verify TTL policy lookup values."""
    assert RedisCacheManager.get_ttl("quote") == 60
    assert RedisCacheManager.get_ttl("bars") == 300
    assert RedisCacheManager.get_ttl("macro") == 86400
    assert RedisCacheManager.get_ttl("sec") == 3600
