# AlphaMind AI — Installation & Prerequisites Guide

This guide provides step-by-step instructions for setting up **AlphaMind AI** on macOS, Linux, or Windows (WSL2).

---

## 1. System Requirements & Prerequisites

Before installing AlphaMind AI, ensure your system satisfies the following dependencies:

| Software / Tool | Minimum Version | Recommended | Purpose |
|---|---|---|---|
| **Python** | 3.11+ | 3.11.8 | Backend API, Quantitative Models, ML Engines |
| **Node.js** | 18.0+ | 20.x LTS | Next.js 14 Web Frontend |
| **npm** | 9.0+ | 10.x | Node package manager |
| **Docker** | 24.0+ | Latest Docker Desktop | Local infrastructure services (PostgreSQL, Redis, ChromaDB, Neo4j) |
| **Docker Compose** | 2.20+ | Latest | Multi-container stack orchestration |
| **Git** | 2.34+ | Latest | Version control |

---

## 2. Quick-Start One-Command Installation (Docker Stack)

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/alphamind-ai/alphamind-ai.git
   cd alphamind-ai
   ```

2. **Configure Environment Variables**:
   ```bash
   cp .env.example .env
   ```

3. **Launch Local Services & Stack**:
   ```bash
   make up
   # or
   docker-compose up -d
   ```

4. **Verify Application Health**:
   - Backend Health API: `http://localhost:8000/api/v1/healthz`
   - Frontend Mission Control: `http://localhost:3000/mission-control`

---

## 3. Local Native Development Installation (Non-Docker)

If you prefer running Python and Node natively on your host machine:

### A. Backend & Quantitative Packages Setup
```bash
# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -e ".[dev]"
```

### B. Frontend Setup
```bash
cd apps/frontend
npm install
```

### C. Launch Development Servers
```bash
# Terminal 1: Backend Server (from workspace root)
PYTHONPATH=apps/backend:. uvicorn apps.backend.app.main:app --reload --port 8000

# Terminal 2: Frontend App Router (from apps/frontend)
cd apps/frontend && npm run dev
```

---

## 4. Troubleshooting & Common Setup Gotchas

- **Port Conflicts**: Ensure ports `8000` (Backend), `3000` (Frontend), `5432` (PostgreSQL), `6379` (Redis), `8001` (ChromaDB), and `7474`/`7687` (Neo4j) are free on your host machine.
- **Python Version Mismatch**: Python 3.11+ is strictly required. Verify with `python3 --version`.
