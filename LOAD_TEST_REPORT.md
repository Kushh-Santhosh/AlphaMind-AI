# AlphaMind AI v2 — Load & Stress Test Report

**Date**: August 4, 2026  
**Environment**: Staging Cluster (FastAPI Uvicorn Async / Py3.11)  
**Tools**: `scripts/load_test.py`, `scripts/stress_test.py`  

---

## Executive Summary

Load testing and stress concurrency testing were executed against the AlphaMind AI backend gateway to measure throughput capacity (Requests Per Second), latency response under concurrent load, error rates, and system saturation boundaries.

Key Findings:
- **Load Test Throughput**: Sustained **686.77 RPS** at 30 concurrent workers with **0.0% error rate** across 300 total HTTP requests.
- **Peak Saturation Capacity**: Achieved peak throughput of **1,026.5 RPS** at 50 concurrent workers with **0.0% error rate** and **68.00ms p95 latency**.
- **System Stability under High Concurrency**: Handled up to **200 concurrent clients** with 100% request completion rate and **0 drops**.

---

## 1. Load Test Summary (30 Concurrent Workers)

Target endpoints evaluated under round-robin distribution (`/api/v1/mission-control/dashboard`, `activity-feed`, `funds`, `intelligence`, `search`, `healthz`):

| Metric | Target / SLA | Load Test Result | Status |
|---|---|---|---|
| Total HTTP Requests | 300 | **300** | **PASSED** |
| Concurrency Level | 30 workers | **30 workers** | **PASSED** |
| Successful Requests | 100% | **300 (100.0%)** | **PASSED** |
| Failed Requests / Drops | 0 | **0 (0.0% error rate)** | **PASSED** |
| Total Execution Time | < 5.0 s | **0.44 s** | **PASSED** |
| Throughput (RPS) | > 200 RPS | **686.77 RPS** | **PASSED** |
| Latency p50 | < 50.0 ms | **31.97 ms** | **PASSED** |
| Latency p95 | < 200.0 ms | **112.06 ms** | **PASSED** |
| Latency p99 | < 300.0 ms | **119.08 ms** | **PASSED** |

---

## 2. Stress & Saturation Concurrency Tiers

Endpoints tested through stepped concurrency levels (10 -> 50 -> 100 -> 200) to identify capacity limits and response degradation curves:

| Concurrency Level | Total Requests | Successful Requests | Failures | Throughput (RPS) | Latency p95 (ms) | Operational Status |
|---|---|---|---|---|---|---|
| **10 Workers** | 200 | 200 | 0 | **547.8 RPS** | 52.91 ms | Optimal (Nominal load) |
| **50 Workers** | 200 | 200 | 0 | **1,026.5 RPS** | 68.00 ms | **Peak Throughput Tier** |
| **100 Workers** | 200 | 200 | 0 | **752.4 RPS** | 164.52 ms | High Concurrency (Queueing) |
| **200 Workers** | 200 | 200 | 0 | **404.6 RPS** | 442.42 ms | Saturation Knee (Sustained) |

---

## 3. Observations & Recommendations

1. **Optimal Operating Envelope**: Single-node uvicorn backend handles up to **50 concurrent workers** cleanly with **1,026.5 RPS** throughput and **< 68ms p95 latency**.
2. **Kubernetes Auto-scaling Trigger**: Horizontal Pod Autoscaler (`k8s/hpa.yaml`) should trigger pod scale-out when concurrency exceeds **50 clients per pod** or CPU utilization exceeds 75%.
3. **Zero Request Loss**: Across all load and stress test executions (1,100+ requests total), zero requests were dropped or failed with 5xx HTTP codes.
