# AlphaMind AI — Local Development & Engineering Workflow Guide

This guide outlines engineering standards, local testing procedures, linter execution, and quality gates for contributing to **AlphaMind AI**.

---

## 1. Local Architecture & Workspace Layout

```
.
├── apps/
│   ├── backend/         # FastAPI Gateway, Controllers, Security Middleware
│   └── frontend/        # Next.js 14 (App Router), React 18, Mission Control UI
├── packages/
│   ├── agents/          # Autonomous Agents & LangGraph State Graph
│   ├── portfolio/       # Strategy Fund Engine & Risk Calculators
│   ├── prediction/      # ML Model Registry (BSTS, TFT, XGBoost)
│   ├── research/        # Quantitative Factor Engines & SEC Parsers
│   └── shared/          # Shared Pydantic Schemas & Types
├── docker/              # Grafana dashboards & Prometheus scrapers
├── k8s/                 # Kubernetes staging deployment manifests
├── scripts/             # Validation, benchmark, and setup scripts
└── tests/               # End-to-end and integration test suites
```

---

## 2. Mandatory Quality Gates

Before pushing code or creating a pull request, all 7 quality gates MUST pass cleanly:

```bash
# 1. Python Formatting (Black)
.venv/bin/black --check apps/backend packages scripts

# 2. Python Linting (Ruff)
.venv/bin/ruff check apps/backend packages scripts

# 3. Python Static Type Safety (Mypy)
PYTHONPATH=apps/backend:. .venv/bin/mypy apps/backend/app packages scripts --explicit-package-bases

# 4. Backend Unit & Integration Tests (Pytest)
PYTHONPATH=apps/backend:. .venv/bin/pytest apps/backend/tests packages/

# 5. Frontend Code Linting (ESLint)
cd apps/frontend && npx eslint src/

# 6. Frontend Type Safety (TypeScript Compiler)
cd apps/frontend && npx tsc --noEmit

# 7. Frontend Unit Tests (Vitest)
cd apps/frontend && npx vitest run
```

Alternatively, use the project `Makefile`:
```bash
make format    # Auto-format Python code with Black and Ruff
make lint      # Run Ruff, Mypy, and ESLint
make test      # Run Pytest and Vitest test suites
```

---

## 3. Engineering Guidelines & Rules

1. **Strict Topology Rule**: **Zero Direct Agent-to-Agent Method Calls**. Agents publish `SystemEvent` objects to `EventBusManager`.
2. **Probabilistic Forecasting**: Predictive functions MUST return probability distributions (Bull, Base, Bear) and 95% confidence bounds instead of static price targets.
3. **Pydantic v2 Models**: All request bodies, API payloads, and memory entries must conform strictly to Pydantic v2 schemas.
