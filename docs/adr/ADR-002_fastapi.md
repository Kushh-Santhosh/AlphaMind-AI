# ADR-002: FastAPI for Backend REST & WebSocket Services

## Context
AlphaMind AI requires an asynchronous, high-performance Python web framework to handle REST API queries, real-time market WebSockets streaming, Server-Sent Events (SSE) for agent log streaming, and seamless integration with quantitative Python libraries (`pandas`, `numpy`, `PyTorch`).

## Decision
We decide to adopt **FastAPI (Python 3.11+)** as the primary backend web framework.

## Alternatives Considered
1. **Django / Django REST Framework**: Rejected due to synchronous ORM overhead, heavier footprint, and less intuitive support for async SSE/WebSocket streaming.
2. **Flask**: Rejected due to lack of native async/await support, missing built-in OpenAPI generation, and manual request validation.
3. **Node.js (Express / NestJS)**: Rejected because quantitative financial libraries (`pandas-ta`, `vectorbt`, `PyTorch`, `scikit-learn`) are natively written in Python.

## Pros
- **Native Async I/O**: Exceptional performance for handling concurrent WebSockets and SSE agent log streams.
- **Pydantic v2 Integration**: Automatic request/response validation with auto-generated OpenAPI 3.0 interactive documentation.
- **Python Ecosystem Compatibility**: Direct import of quantitative factor models and LangGraph agent graphs.

## Cons
- Requires strict async database drivers (`asyncpg`, SQLAlchemy async engine).

## Consequences
All backend endpoints MUST be defined inside `apps/backend/app/api/` using FastAPI APIRouter instances and Pydantic response models.
