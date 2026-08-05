# ADR-001: Monorepo Architecture Decision

## Context
AlphaMind AI comprises frontend presentation, backend API routing, autonomous agent graphs, quantitative factor libraries, machine learning prediction models, portfolio optimization solvers, and shared data schemas. We needed a repository architecture that facilitates shared type definitions, simplified cross-package refactoring, and atomic deployments.

## Decision
We decide to adopt a **Monorepo Directory Structure** separating applications (`apps/backend`, `apps/frontend`) and reusable packages (`packages/agents`, `packages/research`, `packages/prediction`, `packages/portfolio`, `packages/shared`).

## Alternatives Considered
1. **Multi-Repo Architecture**: Separate Git repositories for frontend, backend, agents, and quant engines. Rejected due to high overhead in cross-repo schema synchronization and breaking change management.
2. **Monolithic Single-Folder App**: Combining Python backend and agents into a single unstructured folder. Rejected due to lack of modularity and breach of Clean Architecture principles.

## Pros
- **Atomic Refactoring**: Changes to shared Pydantic/TypeScript data schemas can be updated across backend and frontend in a single commit.
- **Shared Code Reuse**: Core quantitative libraries in `packages/research` can be imported by both backend REST endpoints and LangGraph agent tools.
- **Unified CI/CD**: Single GitHub Actions pipeline executing linting, type-checking, and pytest suites.

## Cons
- Slightly larger Git clone footprint.
- Requires clear internal dependency rules to prevent circular dependencies.

## Consequences
All new features and packages MUST be created inside either `apps/` or `packages/` following the layout rules defined in [`AGENTS.md`](file:///Users/kushal/Desktop/AlphaMind%20AI/AGENTS.md).
