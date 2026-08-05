"""
AlphaMind AI v2 — API Benchmarking Script

Measures exact p50, p90, p95, p99 latency distributions across all core API endpoints.
"""

# ruff: noqa: T201

from __future__ import annotations

import argparse
import asyncio
import time
from typing import Any

import httpx

BENCHMARK_ENDPOINTS = [
    ("/api/v1/healthz", "Health check"),
    ("/api/v1/livez", "Liveness probe"),
    ("/api/v1/readyz", "Readiness probe"),
    ("/api/v1/metrics", "Prometheus metrics"),
    ("/api/v1/mission-control/dashboard", "Mission Control state"),
    ("/api/v1/mission-control/funds", "Virtual AI funds"),
    ("/api/v1/mission-control/activity-feed", "Unified activity feed"),
    ("/api/v1/mission-control/intelligence", "Intelligence snapshot"),
    ("/api/v1/mission-control/search?q=conservative", "Global search"),
]


async def benchmark_endpoint(
    client: httpx.AsyncClient, target_url: str, path: str, iterations: int = 50
) -> dict[str, Any]:
    durations: list[float] = []
    successes = 0

    for _ in range(iterations):
        t0 = time.perf_counter()
        try:
            resp = await client.get(f"{target_url}{path}")
            if resp.status_code == 200:
                successes += 1
        except Exception:
            pass
        durations.append((time.perf_counter() - t0) * 1000.0)

    durations.sort()
    n = len(durations)
    return {
        "path": path,
        "iterations": iterations,
        "success_rate_pct": round(successes / iterations * 100, 1),
        "min_ms": round(durations[0], 2) if n > 0 else 0,
        "p50_ms": round(durations[int(n * 0.50)], 2) if n > 0 else 0,
        "p90_ms": round(durations[int(n * 0.90)], 2) if n > 0 else 0,
        "p95_ms": round(durations[int(n * 0.95)], 2) if n > 0 else 0,
        "p99_ms": round(durations[int(n * 0.99)], 2) if n > 0 else 0,
        "max_ms": round(durations[-1], 2) if n > 0 else 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="AlphaMind API Benchmark")
    parser.add_argument("--target", default="http://localhost:8000", help="Target API base URL")
    parser.add_argument("--iterations", type=int, default=50, help="Iterations per endpoint")
    args = parser.parse_args()

    print(
        f"Starting API Benchmark on {args.target} ({args.iterations} iterations/endpoint)..."
    )  # noqa: T201
    print(
        f"{'ENDPOINT':<45} | {'p50 (ms)':<8} | {'p90 (ms)':<8} | {'p95 (ms)':<8} | {'p99 (ms)':<8} | {'SUCCESS %':<9}"
    )  # noqa: T201
    print("-" * 100)  # noqa: T201

    async def run_all() -> None:
        async with httpx.AsyncClient(timeout=10.0) as client:
            for path, _name in BENCHMARK_ENDPOINTS:
                res = await benchmark_endpoint(client, args.target, path, args.iterations)
                p = res["path"]
                p50 = res["p50_ms"]
                p90 = res["p90_ms"]
                p95 = res["p95_ms"]
                p99 = res["p99_ms"]
                sr = res["success_rate_pct"]
                print(
                    f"{p:<45} | {p50:<8.2f} | {p90:<8.2f} | {p95:<8.2f} | {p99:<8.2f} | {sr:<9.1f}"
                )  # noqa: T201

    asyncio.run(run_all())


if __name__ == "__main__":
    main()
