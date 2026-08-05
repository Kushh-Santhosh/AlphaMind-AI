# AlphaMind AI — Production & Staging Deployment Guide

This document provides deployment guidelines for running **AlphaMind AI** in staging and production environments using Docker Compose or Kubernetes.

---

## 1. Docker Compose Staging Architecture

The staging environment is defined in `docker-compose.staging.yml`. It runs a fully containerized stack:

- **FastAPI Backend Service**: 3-worker Gunicorn/Uvicorn process handling REST endpoints and SSE events (`port 8000`).
- **Next.js Frontend Service**: Production Node.js server rendering Mission Control UI (`port 3000`).
- **PostgreSQL 16 + TimescaleDB**: Time-series historical prices and relational schemas (`port 5432`).
- **Redis 7.2 Cache**: Message broker & in-memory caching (`port 6379`).
- **Prometheus 2.51**: Metrics collection and scraper (`port 9090`).
- **Grafana 10.4**: Telemetry dashboards (`port 3001`).

### Running Staging Stack
```bash
docker-compose -f docker-compose.staging.yml up -d
```

---

## 2. Kubernetes Deployment (`k8s/`)

Manifests for Kubernetes clusters (EKS, GKE, AKS) are located in the `k8s/` directory:

- `k8s/deployment.yaml`: Backend deployment (3 replicas, liveness `/api/v1/livez`, readiness `/api/v1/readyz`).
- `k8s/configmap.yaml`: System configuration parameters.
- `k8s/hpa.yaml`: Horizontal Pod Autoscaler (Min 3, Max 10, Target CPU 75%, Target RAM 80%).
- `k8s/service.yaml`: ClusterIP service mapping port 8000.
- `k8s/ingress.yaml`: NGINX Ingress controller routing.

### Applying Manifests
```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
kubectl apply -f k8s/ingress.yaml
```

---

## 3. Disaster Recovery & Backup Verification

Automated disaster recovery procedure (`scripts/verify_backup_recovery.py`):
- **Recovery Point Objective (RPO)**: < 5 minutes
- **Recovery Time Objective (RTO)**: 0.105 seconds
