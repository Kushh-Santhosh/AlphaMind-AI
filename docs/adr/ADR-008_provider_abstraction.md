# ADR-008: Provider Abstraction & 3-Tier Failover Matrix

## Context
Market data providers (`Polygon.io`, `Alpha Vantage`, `FRED`, `CCXT`, `yfinance`) suffer from periodic rate limits, API key suspensions, network latency spikes, and provider outages. Relying on a single market data vendor introduces single points of failure.

## Decision
We decide to implement an abstract `BaseMarketDataProvider` interface with an automated 3-tier provider failover strategy (`Primary` $\rightarrow$ `Secondary` $\rightarrow$ `Fallback`).

## Alternatives Considered
1. **Single Provider Hardcoding**: Direct `yfinance` or `Polygon` calls in business logic. Rejected due to high risk of service downtime.
2. **Ad-Hoc Try/Except Fallback**: Manual inline try/except blocks in endpoints. Rejected due to code duplication and lack of central health check monitoring.

## Pros
- **High Availability**: Service auto-recovers from provider outages within 3000ms.
- **Provider Agnostic**: Code logic depends on uniform Pydantic schemas, not vendor-specific API structures.
- **Cost Optimization**: Primary provider handles high-volume ticks while free/lower-tier fallbacks handle emergency requests.

## Cons
- Requires mapping data format variances across vendor APIs to normalized schemas.

## Consequences
All data ingestion MUST pass through `packages/research/market_data_engine.py` obeying the 3-tier failover protocol defined in `docs/SYSTEM_BOUNDARIES.md`.
