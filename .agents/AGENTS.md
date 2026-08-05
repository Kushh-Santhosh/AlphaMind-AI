# AGENTS.md — Permanent Engineering Constitution & Guidelines

This document is the **permanent constitution and engineering guideline** for all AI agents, subagents, software engineers, quantitative analysts, and contributors working on the **AlphaMind AI** codebase.

All development, refactoring, code generation, and architectural edits MUST strictly adhere to the rules set forth in this constitution.

---

## 1. Core Architectural Principles

1. **Clean Architecture & Layer Separation**:
   - `apps/backend/`: Web API controllers, FastAPI routing, security middleware.
   - `apps/frontend/`: Next.js 14 UI components, state management, presentation.
   - `packages/agents/`: Autonomous agent definitions, prompts, LangGraph state graph.
   - `packages/research/`: Pure quantitative algorithms, financial factor models, technical indicators.
   - `packages/prediction/`: ML model definitions (TFT, XGBoost, PyTorch), Monte Carlo simulations, Bayesian inference.
   - `packages/portfolio/`: Risk calculations, portfolio optimization solvers, paper trading engine.
   - `packages/shared/`: Shared Pydantic schemas, TypeScript interfaces, global constants.

2. **Strict Agent Topology Rules**:
   - **Zero Direct Agent-to-Agent Method Calls**: Agents MUST NEVER call another agent directly.
   - **State-Driven Coordination**: Agents communicate **strictly and exclusively** through the shared `LangGraph State` object.
   - **Supervisor Isolation**: The `Supervisor Agent` is the sole orchestrator responsible for evaluating state, selecting the next agent execution node, and declaring task completion.

3. **Probability-Based Forecasting Rules**:
   - **No Deterministic Target Prices**: Code MUST NEVER output static, single-point price targets (e.g. "$250 by Friday").
   - **Mandatory Probabilistic Output**: All predictive functions MUST return a probability distribution (Bull, Base, Bear), confidence interval (95%), data quality score, known unknowns, and contradicting evidence.

---

## 2. Coding Standards & Type Safety

### Python Standards (Backend & Agents & ML)
- **Language Level**: Python 3.11+.
- **Type Annotations**: Mandatory type hints on EVERY function signature, method, and return value (`def calculate_var(returns: np.ndarray, confidence_level: float = 0.95) -> float:`).
- **Validation**: Use **Pydantic v2** for all data schemas, request payloads, response bodies, and agent state definitions.
- **Async First**: Use `async`/`await` for all I/O operations (FastAPI endpoints, database queries via `asyncpg`/SQLAlchemy async, HTTP requests via `httpx`, Redis queries via `redis-py async`).
- **Docstrings**: Google-style docstrings for all classes, methods, and public functions.

### TypeScript / React Standards (Frontend)
- **Language Level**: TypeScript 5.0+ with `strict: true` in `tsconfig.json`.
- **Framework**: Next.js 14+ (App Router), React 18+.
- **Styling**: Vanilla TailwindCSS + `shadcn/ui` UI component primitives.
- **State Management**: React Hooks, TanStack React Query for async state, Zustand for global application UI state.
- **Component Design**: Pure functional components with explicit `interface Props`. Zero `any` types permitted.

---

## 3. Testing & Verification Rules

1. **Test Coverage Threshold**: Minimum 80% line and branch coverage across all backend services, agent tools, and quantitative engines.
2. **Backend Unit Tests**: Written with `pytest` and `pytest-asyncio`. Located in `apps/backend/tests/` and `packages/*/tests/`.
3. **Quantitative Assertions**: Mathematical functions (e.g., Fama-French regressions, Black-Scholes pricing, Sharpe ratio) MUST be verified against known analytical test vectors.
4. **Mocking External APIs**: NEVER invoke live external APIs (yfinance, Polygon, OpenAI) during automated unit test runs. Use `pytest-mock` or `respx` to mock external API responses.
5. **Frontend Testing**: React Testing Library / Jest for UI components, static type-checking via `tsc --noEmit`.

---

## 4. Directory & Naming Conventions

- **Python Files & Functions**: `snake_case` (e.g., `monte_carlo_engine.py`, `def calculate_sharpe_ratio()`).
- **Python Classes & Pydantic Schemas**: `PascalCase` (e.g., `MarketResearchAgent`, `PredictionSafetySchema`).
- **TypeScript Files & React Components**: `PascalCase` for React components (`RiskGauge.tsx`), `camelCase` for utilities (`formatCurrency.ts`).
- **Folder Names**: `lowercase` with hyphens or underscores (`apps/backend/app/services`, `packages/prediction`).

---

## 5. Security & Financial Compliance Rules

1. **Zero Hardcoded Secrets**: Secrets, API keys, database credentials, and private keys MUST NEVER be committed to Git. Load exclusively from environment variables via Pydantic `BaseSettings`.
2. **Role-Based Access Control (RBAC)**: All REST and WebSocket endpoints MUST validate user identity and permissions via JWT middleware.
3. **Financial Disclaimer Injection**: Every generated report or research API payload MUST automatically append the mandatory SEC/FINRA financial research disclaimer.
4. **Data Encryption**: Encrypt sensitive user data in PostgreSQL and encrypt vector embeddings in ChromaDB at rest.

---

## 6. Prompt Engineering & LLM Safety Rules

1. **Structured JSON Output**: All agent prompts MUST require LLMs to output valid, parseable JSON conforming to a Pydantic schema.
2. **System Prompt Isolation**: System prompts MUST define persona, available tools, output schema, constraints, and explicit instructions against hallucination.
3. **Hallucination Countermeasures**: Prompts must instruct agents to cite exact data source IDs and return `"UNKNOWN"` if required data is absent from context.
4. **Cost Control**: Enforce max token generation limits on all LLM completions.

---

## 7. Performance & Observability Rules

1. **Vector & DB Indexing**: PostgreSQL tables must have index coverage on foreign keys, timestamps, and ticker symbols. ChromaDB collections must specify cosine similarity distance metrics.
2. **Structured Logging**: Use `structlog` for structured JSON logging with correlation IDs across FastAPI requests and LangGraph agent runs.
3. **OpenTelemetry & Sentry**: Instrument key workflows for tracing (spans for LLM calls, DB queries, quant calculations) and capture exceptions with Sentry context.

---

## 8. Git Workflow & Refactoring Guidelines

1. **Commit Message Format**: Conventional Commits standard (`feat: add Fama-French 5-factor model`, `fix: handle Polygon API timeout in market data engine`, `docs: update API_DESIGN.md`).
2. **Refactoring Rule**: When modifying existing functions or API contracts, search for and update all invocation sites across `apps/` and `packages/` to ensure zero breaking changes.
3. **Continuous Integration**: Code must pass `black`, `ruff`, `mypy`, and `pytest` checks prior to merging.
