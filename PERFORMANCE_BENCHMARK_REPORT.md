# AlphaMind AI v2 — Performance Benchmark Report

**Date**: August 4, 2026  
**Environment**: Staging Cluster (FastAPI Uvicorn Async / Py3.11)  
**Tool**: `scripts/api_benchmark.py`  
**Iterations per Endpoint**: 30  

---

## Executive Summary

The AlphaMind AI v2 core APIs were benchmarked under real execution conditions to establish sub-millisecond to low-millisecond latency baselines across core telemetry, health, mission control, funds, activity feed, intelligence, and search endpoints. 

Key Findings:
- **Health Probes**: Liveness (`/api/v1/livez`), Readiness (`/api/v1/readyz`), and Metrics (`/api/v1/metrics`) achieve **< 0.95ms p50 latency** and **100% success rate**.
- **Mission Control APIs**: Full dashboard, fund portfolio state, activity feed, and global search achieve **1.0ms–1.3ms p50 latency** with zero error drops.
- **Resource Utilization**: Python process RSS memory ceiling remains under **11 MB**, consuming under **0.04 CPU seconds** during active benchmarking.

---

## 1. Baseline Latency Distribution Table

| Endpoint Path | Description | p50 (ms) | p90 (ms) | p95 (ms) | p99 (ms) | Success Rate (%) |
|---|---|---|---|---|---|---|
| `/api/v1/healthz` | Detailed Subsystem Health | 0.88 | 1.08 | 1.31 | 8.15 | 100.0% |
| `/api/v1/livez` | K8s Liveness Probe | 0.82 | 0.90 | 0.92 | 0.98 | 100.0% |
| `/api/v1/readyz` | K8s Readiness Probe | 0.78 | 0.85 | 0.87 | 1.04 | 100.0% |
| `/api/v1/metrics` | Prometheus Exposition Metrics | 0.85 | 0.97 | 0.99 | 1.32 | 100.0% |
| `/api/v1/mission-control/dashboard` | Aggregated Mission Control | 1.09 | 1.28 | 1.50 | 2.05 | 100.0% |
| `/api/v1/mission-control/funds` | Virtual AI Fund Engine | 1.05 | 1.18 | 1.19 | 1.20 | 100.0% |
| `/api/v1/mission-control/activity-feed` | Unified Activity Feed | 1.01 | 1.23 | 1.27 | 1.29 | 100.0% |
| `/api/v1/mission-control/intelligence` | Reasoning & Decision State | 1.25 | 1.71 | 1.72 | 3.21 | 100.0% |
| `/api/v1/mission-control/search?q=conservative` | Global Vector Search | 1.04 | 1.34 | 1.40 | 1.65 | 100.0% |

---

## 2. Process Memory & CPU Resource Profile

Profiles captured via `scripts/profile_memory_cpu.py`:

- **Process Memory ceiling (max RSS)**: `10.95 MB`
- **User CPU Time**: `0.021s`
- **System CPU Time**: `0.015s`
- **Total CPU Time**: `0.036s`
- **Major Page Faults**: `57`

---

## 3. Performance SLA Conformance

| Performance Metric | Target SLA | Benchmark Result | Status |
|---|---|---|---|
| Health & Probe Latency (p95) | < 10.0 ms | **0.87 ms – 1.31 ms** | **PASSED** |
| Mission Control API Latency (p95) | < 50.0 ms | **1.19 ms – 1.72 ms** | **PASSED** |
| Mission Control Search Latency (p95) | < 100.0 ms | **1.40 ms** | **PASSED** |
| Process Memory Consumption | < 512.0 MB | **10.95 MB** | **PASSED** |
| API Request Success Rate | 99.9% | **100.0%** | **PASSED** |
