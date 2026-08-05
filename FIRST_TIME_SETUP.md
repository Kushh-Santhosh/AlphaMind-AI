# AlphaMind AI — First-Time Setup & Verification Guide

This guide ensures a new developer or quantitative engineer can perform a fresh checkout of **AlphaMind AI** and launch the full stack in one command.

---

## 1. Quick-Start (3 Steps)

```bash
# Step 1: Clone Repository
git clone https://github.com/alphamind-ai/alphamind-ai.git
cd alphamind-ai

# Step 2: Initialize Environment File
cp .env.example .env

# Step 3: Launch Local Docker Stack (One Command)
docker-compose up -d
```

---

## 2. Service Verification Checklist

Once `docker-compose up -d` finishes, verify each service status:

| Service | Port | Health Verification URL / Command | Expected Response |
|---|---|---|---|
| **Next.js Web UI** | `3000` | Open `http://localhost:3000/mission-control` | Mission Control Dashboard renders |
| **FastAPI Backend** | `8000` | `curl http://localhost:8000/api/v1/healthz` | `{"status":"HEALTHY",...}` |
| **PostgreSQL 16** | `5432` | `docker exec alphamind-postgres pg_isready` | `accepting connections` |
| **Redis Cache** | `6379` | `docker exec alphamind-redis redis-cli ping` | `PONG` |
| **ChromaDB Vector Store** | `8001` | `curl http://localhost:8001/api/v1/heartbeat` | heartbeat response |
| **Neo4j Knowledge Graph** | `7474` | Open `http://localhost:7474` | Neo4j Browser Login |

---

## 3. Database Migration Execution

Database schemas initialize automatically on FastAPI backend startup. You can also run migrations manually:

```bash
PYTHONPATH=apps/backend:. .venv/bin/python -m apps.backend.app.db.init_db
```

---

## 4. Running Quality Gates

To verify code quality and tests after setup:
```bash
make lint
make test
```
