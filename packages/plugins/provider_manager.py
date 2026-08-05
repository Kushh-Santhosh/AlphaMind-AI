"""
AlphaMind AI - Provider Framework & Provider Failover Manager

Implements the provider abstraction layer with health checks, exponential retries with jitter,
configurable timeouts, token-bucket rate limiting, automatic 3-tier failover, caching, metadata,
and API versioning.
"""

from __future__ import annotations

import asyncio
import logging
import random
import time
from collections.abc import Callable
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

T = TypeVar("T")


class ProviderMetadata(BaseModel):
    """Metadata describing a data provider's capabilities, versioning, and status."""

    provider_id: str
    provider_name: str
    version: str = "1.0.0"
    tier: str  # "primary", "secondary", "fallback"
    supported_assets: list[str] = Field(default_factory=list)
    rate_limit_per_minute: int = 60
    timeout_seconds: float = 5.0
    is_healthy: bool = True
    consecutive_failures: int = 0
    last_health_check_timestamp: float = Field(default_factory=time.time)
    avg_latency_ms: float = 0.0


class ProviderResponse(BaseModel, Generic[T]):
    """Standardized provider response wrapper carrying data payload and telemetry."""

    data: T
    provider_id: str
    tier_used: str
    latency_ms: float
    cached: bool = False
    timestamp: float = Field(default_factory=time.time)


class TokenBucketRateLimiter:
    """Async Token Bucket Rate Limiter per provider."""

    def __init__(self, rate_per_minute: int) -> None:
        self.capacity = float(rate_per_minute)
        self.tokens = float(rate_per_minute)
        self.fill_rate = float(rate_per_minute) / 60.0  # tokens per second
        self.last_update = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        """Acquire a rate-limit token, sleeping if bucket is empty."""
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_update
            self.last_update = now
            self.tokens = min(self.capacity, self.tokens + elapsed * self.fill_rate)

            if self.tokens < 1.0:
                wait_time = (1.0 - self.tokens) / self.fill_rate
                logger.debug("Rate limit reached. Sleeping for %.2f seconds", wait_time)
                await asyncio.sleep(wait_time)
                self.tokens = 0.0
            else:
                self.tokens -= 1.0


class BaseProvider:
    """Base Provider class with built-in health checks, retries, timeouts, and rate limits."""

    def __init__(self, metadata: ProviderMetadata) -> None:
        self.metadata = metadata
        self.rate_limiter = TokenBucketRateLimiter(metadata.rate_limit_per_minute)

    async def check_health(self) -> bool:
        """
        Execute health check ping on the provider.
        Override in concrete providers to perform actual ping requests.
        """
        self.metadata.last_health_check_timestamp = time.time()
        return self.metadata.is_healthy

    async def execute_with_resilience(
        self,
        func: Callable[..., Any],
        *args: Any,
        max_retries: int = 3,
        **kwargs: Any,
    ) -> Any:
        """
        Execute a provider API call with rate limiting, timeouts, and exponential backoff retry.
        """
        await self.rate_limiter.acquire()
        start_time = time.monotonic()

        for attempt in range(1, max_retries + 1):
            try:
                # Execute with configured timeout
                result = await asyncio.wait_for(
                    func(*args, **kwargs), timeout=self.metadata.timeout_seconds
                )
                latency = (time.monotonic() - start_time) * 1000.0

                # Update operational telemetry
                self.metadata.consecutive_failures = 0
                self.metadata.is_healthy = True
                self.metadata.avg_latency_ms = self.metadata.avg_latency_ms * 0.8 + latency * 0.2
                return result

            except Exception as exc:
                self.metadata.consecutive_failures += 1
                logger.warning(
                    "Provider %s attempt %d/%d failed: %s",
                    self.metadata.provider_id,
                    attempt,
                    max_retries,
                    exc,
                )

                if self.metadata.consecutive_failures >= 3:
                    self.metadata.is_healthy = False

                if attempt == max_retries:
                    raise exc

                # Exponential backoff with jitter
                backoff_time = (2 ** (attempt - 1)) + random.uniform(0.1, 0.5)
                await asyncio.sleep(backoff_time)


class ProviderFailoverManager:
    """
    3-Tier Provider Failover Engine.
    Routes queries to Primary Provider -> Secondary Provider -> Fallback Provider automatically.
    """

    def __init__(
        self,
        primary: BaseProvider,
        secondary: BaseProvider,
        fallback: BaseProvider,
    ) -> None:
        self.primary = primary
        self.secondary = secondary
        self.fallback = fallback
        self.providers = [primary, secondary, fallback]

    async def execute_query(
        self, operation: Callable[[BaseProvider], Any]
    ) -> ProviderResponse[Any]:
        """
        Execute provider query attempting primary first, falling back to secondary and fallback.
        Raises DataProviderException if all 3 tiers fail.
        """
        errors: list[str] = []

        for provider in self.providers:
            # Skip provider if unhealthy (unless fallback)
            if not provider.metadata.is_healthy and provider != self.fallback:
                logger.info(
                    "Skipping unhealthy provider %s (tier: %s)",
                    provider.metadata.provider_id,
                    provider.metadata.tier,
                )
                continue

            start_time = time.monotonic()
            try:
                data = await provider.execute_with_resilience(operation, provider)
                latency_ms = (time.monotonic() - start_time) * 1000.0

                return ProviderResponse(
                    data=data,
                    provider_id=provider.metadata.provider_id,
                    tier_used=provider.metadata.tier,
                    latency_ms=latency_ms,
                )
            except Exception as exc:
                err_msg = f"Tier '{provider.metadata.tier}' ({provider.metadata.provider_id}) failed: {exc}"
                errors.append(err_msg)
                logger.error(err_msg)

        # Import here to avoid circular imports
        from apps.backend.app.exceptions import DataProviderException

        raise DataProviderException(
            provider=" -> ".join([p.metadata.provider_id for p in self.providers]),
            asset="exhausted_all_tiers",
        )
