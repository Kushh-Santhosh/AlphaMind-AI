# AlphaMind AI v2 — Staging Deployment Guide

**Target Environment**: Staging  
**Architecture**: 7-Layer Autonomous AI Operating System  
**Orchestration**: Docker Compose Staging & Kubernetes (`k8s/`)  
**Observability**: Prometheus Metrics + Grafana Telemetry Dashboards  
**Disaster Recovery Target**: RPO < 5 minutes, RTO < 300 seconds  

---

## 1. Staging Architecture Overview

The AlphaMind AI staging environment deploys the complete 24×7 continuously running AI Investment Operating System with full telemetry, automated background workers, persistent reasoning memory, virtual AI funds, and zero-downtime health probing.

```
                  ┌────────────────────────┐
                  │   Kubernetes Ingress   │
                  │     (Port 80/443)      │
                  └───────────┬────────────┘
                              │
            ┌─────────────────┴─────────────────┐
            │                                   │
┌───────────▼───────────┐           ┌───────────▼───────────┐
│   Next.js Frontend    │           │    FastAPI Backend    │
│  (Port 3000 / RSC)    │           │ (Port 8000 / REST+SSE)│
└───────────────────────┘           └───────────┬───────────┘
                                                │
       ┌───────────────────┬────────────────────┼───────────────────┐
       │                   │                    │                   │
┌──────▼──────┐     ┌──────▼──────┐      ┌──────▼──────┐     ┌──────▼──────┐
│ PostgreSQL  │     │    Redis    │      │  Prometheus │     │   Grafana   │
│ (Port 5432) │     │ (Port 6379) │      │ (Port 9090) │     │ (Port 3001) │
└─────────────┘     └─────────────┘      └─────────────┘     └─────────────┘
```

---

## 2. Docker Compose Staging Deployment

### Prerequisites
- Docker Engine 24.0+
- Docker Compose v2.20+

### Step-by-Step Launch
1. Clone the repository and navigate to root:
   ```bash
   cd "AlphaMind AI"
   ```

2. Start the complete staging stack in background:
   ```bash
   docker-compose -f docker-compose.staging.yml up -d --build
   ```

3. Verify container health status:
   ```bash
   docker-compose -f docker-compose.staging.yml ps
   ```

4. Verify backend health endpoint:
   ```bash
   curl http://localhost:8000/api/v1/healthz
   ```

5. Access Services:
   - **Mission Control Terminal**: `http://localhost:3000/mission-control`
   - **FastAPI API Documentation**: `http://localhost:8000/docs`
   - **Prometheus Metrics**: `http://localhost:9090`
   - **Grafana Dashboard**: `http://localhost:3001` (User: `admin`, Pass: `staging_admin`)

---

## 3. Kubernetes Staging Deployment (`k8s/`)

### Manifest Structure
- `k8s/deployment.yaml`: Replicas (3), Liveness probe (`/api/v1/livez`), Readiness probe (`/api/v1/readyz`), resource limits (2Gi RAM, 2000m CPU), Prometheus annotations.
- `k8s/configmap.yaml`: Environment settings (`ENVIRONMENT=staging`, `LOG_LEVEL=INFO`).
- `k8s/hpa.yaml`: Horizontal Pod Autoscaler (min 3, max 10 replicas based on 75% CPU / 80% RAM utilization).
- `k8s/service.yaml`: ClusterIP service mapping port 8000.
- `k8s/ingress.yaml`: NGINX Ingress controller configuration.

### Deploying to Kubernetes Cluster
1. Create namespace:
   ```bash
   kubectl create namespace alphamind-staging
   ```

2. Apply configmap, secrets, and services:
   ```bash
   kubectl apply -f k8s/configmap.yaml -n alphamind-staging
   kubectl apply -f k8s/service.yaml -n alphamind-staging
   ```

3. Apply deployment, ingress, and HPA:
   ```bash
   kubectl apply -f k8s/deployment.yaml -n alphamind-staging
   kubectl apply -f k8s/ingress.yaml -n alphamind-staging
   kubectl apply -f k8s/hpa.yaml -n alphamind-staging
   ```

4. Verify pod readiness:
   ```bash
   kubectl get pods -n alphamind-staging -l app=alphamind-backend
   ```

---

## 4. Telemetry & Observability Setup

### Prometheus Scrape Exporter
The Prometheus server automatically scrapes backend metrics every 10 seconds via:
- Endpoint: `GET /api/v1/metrics`
- Exported Metrics:
  - `alphamind_uptime_seconds` (gauge)
  - `alphamind_timeline_events_total` (counter)
  - `alphamind_reasoning_records_total` (counter)
  - `alphamind_active_funds_total` (gauge)
  - `alphamind_total_aum_usd` (gauge)
  - `alphamind_fund_aum_usd{fund_id="..."}` (gauge)
  - `alphamind_fund_cagr_pct{fund_id="..."}` (gauge)
  - `alphamind_fund_sharpe_ratio{fund_id="..."}` (gauge)
  - `alphamind_event_bus_subscribers` (gauge)
  - `alphamind_briefings_generated_total` (counter)

### Grafana Dashboard
Import pre-configured Grafana JSON dashboard from `docker/grafana/dashboards/alphamind_dashboard.json`.
Provides real-time visualization for System Uptime, Total AUM, Timeline Event Count, AI Reasoning Record Count, Fund AUM Evolution, and Sharpe Ratios.

---

## 5. Probes & Health Checks

- **Liveness Probe**: `GET /api/v1/livez` -> Returns `200 OK` `{"status":"ALIVE"}`.
- **Readiness Probe**: `GET /api/v1/readyz` -> Returns `200 OK` `{"status":"READY"}` when funds and subsystems are initialized.
- **Detailed Subsystem Health**: `GET /api/v1/healthz` -> Detailed state of Event Bus, Timeline, Reasoning Memory, Funds, Briefings, Workspaces.

---

## 6. Disaster Recovery & Database Backup

Run the automated backup and recovery verification suite:
```bash
PYTHONPATH=apps/backend:. .venv/bin/python scripts/verify_backup_recovery.py
```
- **Recovery Point Objective (RPO)**: < 5 minutes data loss limit
- **Recovery Time Objective (RTO)**: < 300 seconds total restoration time (Simulated: ~0.10s)

---

## 7. Cloud Deployment Cost Estimation (AWS / Staging Tier)

Estimated monthly infrastructure operational costs for Staging:

| Service Component | Cloud Instance / Resource | Estimated Monthly Cost (USD) |
|---|---|---|
| EKS Cluster / Kubernetes Control Plane | Managed Kubernetes Cluster | $73.00 |
| Compute (Backend Workers & API) | 3x t3.large EC2 nodes (8GB RAM, 2 vCPU) | $180.00 |
| Relational DB (PostgreSQL 16) | AWS RDS db.t4g.medium (Multi-AZ) | $85.00 |
| In-Memory Cache (Redis 7.2) | AWS ElastiCache cache.t4g.small | $32.00 |
| Networking & Ingress Load Balancer | AWS Application Load Balancer (ALB) | $25.00 |
| Storage & Backup Snapshots | EBS Volumes (100GB gp3) + S3 Backups | $20.00 |
| Telemetry & Monitoring | Managed Grafana / CloudWatch | $15.00 |
| **Total Estimated Staging Cost** | | **$430.00 / month** |

---

## 8. Quality Gate Verification Suite

All staging deployments must pass the 7 mandatory quality gates prior to promotion:

```bash
# 1. Code Formatting
.venv/bin/black --check apps/backend packages scripts

# 2. Python Linting
.venv/bin/ruff check apps/backend packages scripts

# 3. Static Type Checking
PYTHONPATH=apps/backend:. .venv/bin/mypy apps/backend/app packages scripts --explicit-package-bases

# 4. Backend Unit & Integration Tests
PYTHONPATH=apps/backend:. .venv/bin/pytest apps/backend/tests packages/

# 5. Frontend ESLint
cd apps/frontend && npx eslint src/

# 6. Frontend TypeScript Compilation
cd apps/frontend && npx tsc --noEmit

# 7. Frontend Vitest Unit Tests
cd apps/frontend && npx vitest run
```
