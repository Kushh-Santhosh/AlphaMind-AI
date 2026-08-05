# Document 19: Coding Standards & Engineering Guidelines

## Purpose
The **CODING_STANDARDS.md** document specifies the explicit coding conventions, type safety requirements, language style guides, and Clean Architecture constraints for all Python backend, TypeScript frontend, and LangGraph agent code in AlphaMind AI.

## Responsibilities
- Mandate Python 3.11+, Pydantic v2, and explicit type hints on all backend signatures.
- Mandate TypeScript 5.0+ with strict mode in Next.js 14 frontend.
- Enforce SOLID design principles, Clean Architecture layer separation, and Google-style docstrings.
- Detail forbidden coding antipatterns (e.g. silent try/except, hardcoded secrets, deterministic target prices).

## Clean Architecture Layering Constraints

```
apps/backend (API & Routing)
   ↓ (depends on)
packages/agents (LangGraph Workflows)
   ↓ (depends on)
packages/research & prediction & portfolio (Core Quant Engines)
   ↓ (depends on)
packages/shared (Pydantic Schemas & Types)
```

- **Dependency Inversion Rule**: Higher-level policy modules must never depend on lower-level detail modules. Dependencies point inward toward `packages/shared`.

---

## 1. Python Backend & Agent Standards

- **Python Version**: 3.11+.
- **Type Annotations**: Mandatory type hints on every function parameter and return type:
  ```python
  def compute_var(returns: np.ndarray, confidence_level: float = 0.95) -> float:
      ...
  ```
- **Data Validation**: Pydantic v2 schemas for all request payloads, responses, and agent state definitions.
- **Async I/O**: `async`/`await` for all I/O bound operations (`httpx`, `asyncpg`, `redis-py async`).
- **Formatting & Linting**: Enforced via `black` (line length 100), `ruff`, and `mypy --strict`.

---

## 2. TypeScript / React Frontend Standards

- **TypeScript Version**: 5.0+ with `"strict": true` in `tsconfig.json`.
- **Framework**: Next.js 14 (App Router), React 18 functional components with explicit `interface Props`.
- **Zero `any` Types**: Using `any` is strictly prohibited. Use explicit interfaces or generics.
- **Styling**: Vanilla TailwindCSS + `shadcn/ui` UI component primitives.

---

## 3. Forbidden Antipatterns

1. **Deterministic Target Prices**: Never return static target prices (e.g. "$250 by Friday").
2. **Direct Agent-to-Agent Method Invocations**: Agents must communicate exclusively via shared `LangGraph State`.
3. **Superficial Exception Swallowing**: Silent `try: ... except: pass` blocks are strictly forbidden.
4. **Hardcoded Secrets**: API keys or credentials committed to Git cause immediate CI build failure.

## Dependencies & Sub-System References
- [08. Development Plan](file:///Users/kushal/Desktop/AlphaMind%20AI/docs/08_DEVELOPMENT_PLAN.md)
- [10. Testing Strategy](file:///Users/kushal/Desktop/AlphaMind%20AI/docs/10_TESTING_STRATEGY.md)
- [AGENTS.md Permanent Constitution](file:///Users/kushal/Desktop/AlphaMind%20AI/AGENTS.md)
