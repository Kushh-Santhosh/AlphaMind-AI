# AlphaMind AI — Environment Variable Master Reference

**Date**: August 5, 2026  
**Build Version**: `v3.0.0-beta`  
**Configuration Scope**: Core Application, Databases, AI Models, Market Data, and Telemetry  

---

## Environment Variable Reference Table

| Variable Name | Description | Status | Default / Example Value |
|---|---|---|---|
| `ENVIRONMENT` | App execution environment (`development`, `staging`, `production`) | **Required** | `development` |
| `LOG_LEVEL` | Application log verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`) | **Required** | `INFO` |
| `SECRET_KEY` | Secret key used for JWT signing and token generation | **Required** | `change_this_to_a_secure_256bit_random_secret` |
| `ALLOWED_ORIGINS` | Comma-separated CORS allowed origins | **Required** | `http://localhost:3000` |
| `POSTGRES_USER` | PostgreSQL database user | **Required** | `alphamind` |
| `POSTGRES_PASSWORD` | PostgreSQL database password | **Required** | `alphamind_dev_pass` |
| `POSTGRES_DB` | PostgreSQL database name | **Required** | `alphamind_db` |
| `POSTGRES_HOST` | PostgreSQL host | **Required** | `localhost` |
| `POSTGRES_PORT` | PostgreSQL port | **Required** | `5432` |
| `DATABASE_URL` | SQLAlchemy async connection URI | **Required** | `postgresql+asyncpg://alphamind:alphamind_dev_pass@localhost:5432/alphamind_db` |
| `REDIS_HOST` | Redis cache host | **Required** | `localhost` |
| `REDIS_PORT` | Redis cache port | **Required** | `6379` |
| `REDIS_URL` | Redis connection URI | **Required** | `redis://localhost:6379/0` |
| `CHROMADB_HOST` | ChromaDB vector store host | **Required** | `localhost` |
| `CHROMADB_PORT` | ChromaDB vector store port | **Required** | `8001` |
| `NEO4J_URI` | Neo4j knowledge graph Bolt URI | **Required** | `bolt://localhost:7687` |
| `NEO4J_USER` | Neo4j knowledge graph username | **Required** | `neo4j` |
| `NEO4J_PASSWORD` | Neo4j knowledge graph password | **Required** | `alphamind_graph_pass` |
| `POLYGON_API_KEY` | Polygon.io market data API key | Optional | `your_polygon_api_key_here` |
| `FRED_API_KEY` | St. Louis FRED macro API key | Optional | `your_fred_api_key_here` |
| `ALPHA_VANTAGE_API_KEY` | Alpha Vantage market data API key | Optional | `your_alpha_vantage_key_here` |
| `OPENAI_API_KEY` | OpenAI API key for GPT-4o models | Optional | `sk-proj-your_openai_key_here` |
| `ANTHROPIC_API_KEY` | Anthropic Claude API key | Optional | `sk-ant-your_anthropic_key_here` |
| `GEMINI_API_KEY` | Google Gemini API key | Optional | `AIzaSy_your_gemini_key_here` |
| `DEEPSEEK_API_KEY` | DeepSeek AI API key | Optional | `sk-ds-your_deepseek_key_here` |
| `OLLAMA_BASE_URL` | Ollama local model server URL | Optional | `http://localhost:11434` |
| `SENTRY_DSN` | Sentry exception tracking DSN | Optional | `https://...@sentry.io/0` |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | OpenTelemetry OTLP exporter endpoint | Optional | `http://localhost:4317` |
