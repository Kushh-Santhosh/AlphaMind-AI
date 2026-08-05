# AlphaMind AI — v1.0 Enterprise Operations Manual

## 1. System Overview & Architectural Topology

AlphaMind AI is an institutional-grade, multi-engine autonomous AI investment research and quantitative analytics platform. 

All analytics are **probabilistic** and generated for educational and research purposes. Live trading is optional and defaults to simulation/paper mode. Live execution requires explicit user confirmation.

### Subsystem Layer Architecture

```
[ Frontend: Next.js 14 App Router (Dark Mode Dashboard, Visualizations, AI Analyst Chat) ]
                                    │
                                 (REST)
                                    ▼
[ FastAPI Gateway (Auth, RBAC, Middleware, Disclaimer, Rate Limiter, Observability) ]
  ├── [ Master Analyst Orchestrator ] ──> [ LangGraph Workflow Runtime ]
  ├── [ Research Intelligence Engine ] ──> SEC 10-K Normalization & Factor Extraction
  ├── [ Knowledge Graph Engine ] ─────> 38,900 Triples & 21 Entity Types
  ├── [ Financial Intelligence ] ─────> Financial Health + Contradiction Auditor
  ├── [ Probabilistic Forecast Engine] ──> Bayesian BSTS + TFT + Monte Carlo
  ├── [ Portfolio & Risk Engine ] ────> VaR, CVaR, Sharpe, MCR, Stress Testing
  ├── [ Continuous Evaluation ] ──────> Brier Calibration + Drift Detection
  ├── [ Execution Simulation ] ──────> Paper Exchange + Market Replay (100x)
  └── [ Broker Integration Layer ] ───> Alpaca / IBKR / CCXT / Binance Adapters
```

---

## 2. Deployment & Cluster Operations

### Prerequisites
- Docker 24.0+
- Kubernetes 1.28+ (Helm 3.0+)
- PostgreSQL 15+ (Encrypted at rest)
- ChromaDB 0.4+ Vector Database

### Deployment Commands

```bash
# 1. Build Production Container
docker build -t alphamind/backend:v1.0.0 -f Dockerfile .

# 2. Deploy to Kubernetes Cluster
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

---

## 3. Security, Secret Management & Role-Based Access Control (RBAC)

### User Roles Matrix
- `ADMIN`: Full administrative control, user management, model retraining approval.
- `QUANT_ANALYST`: Research execution, factor extraction, backtesting, simulation.
- `RESEARCHER`: Research view and report generation.
- `AUDITOR`: Immutable audit log inspection and calculation lineage verification.

### Compliance Rules
1. Zero hardcoded secrets in source code.
2. Mandatory SEC / FINRA probabilistic research disclaimers attached to all reports and API responses.
3. Pre-live risk gates (Max 25% position size, Max 2.0x leverage, Daily loss limits).
4. Pre-live user confirmation requirement for live mode orders.
