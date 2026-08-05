# ADR-005: PostgreSQL + TimescaleDB for Relational & Time-Series Data

## Context
The platform must persist user profiles, portfolios, paper trading orders, and investment journals alongside high-frequency daily/intraday financial price bars and technical indicator features.

## Decision
We decide to adopt **PostgreSQL 16 with the TimescaleDB extension**.

## Alternatives Considered
1. **MongoDB / NoSQL**: Rejected due to lack of ACID transactional guarantees for paper trading orders and portfolio equity balances.
2. **ClickHouse**: Excellent for time-series analytics, but rejected as a primary store to avoid operational complexity of maintaining separate relational and time-series DBs.
3. **InfluxDB**: Rejected due to limited SQL join capabilities with relational user and order data.

## Pros
- **Unified Engine**: Relational tables (`users`, `portfolios`, `orders`) and Time-Series Hyper-tables (`market_bars_daily`) co-exist in a single PostgreSQL instance.
- **SQL & ORM Compatibility**: Full compatibility with SQLAlchemy Async, Alembic migrations, and standard SQL queries.
- **Automated Partitioning & Compression**: TimescaleDB automatically partitions hyper-tables by time and symbol while compressing historical bars by up to 90%.

## Cons
- Requires installation of TimescaleDB extension in container image (`timescale/timescaledb:latest-pg16`).

## Consequences
All relational database schemas and migrations MUST be maintained via Alembic inside `apps/backend/app/models/`.
