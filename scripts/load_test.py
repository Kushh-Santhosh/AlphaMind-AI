"""
AlphaMind AI v2 — Staging Load Testing Script

Simulates concurrent HTTP user requests against Mission Control APIs:
  - GET /api/v1/mission-control/dashboard
  - GET /api/v1/mission-control/activity-feed
  - GET /api/v1/mission-control/funds
  - GET /api/v1/mission-control/intelligence
  - GET /api/v1/mission-control/search?q=conservative
  - GET /api/v1/healthz

Usage:
  python scripts/load_test.py --concurrency 50 --requests 500 --target http://localhost:8000
"""

# ruff: noqa: T201

from __future__ import annotations

import argparse
import asyncio
import time
from typing import Any

import httpx

ENDPOINTS = [
    "/api/v1/mission-control/dashboard",
    "/api/v1/mission-control/activity-feed?limit=20",
    "/api/v1/mission-control/funds",
    "/api/v1/mission-control/intelligence",
    "/api/v1/mission-control/search?q=conservative",
    "/api/v1/healthz",
]


async def worker(
    target_url: str,
    queue: asyncio.Queue[str],
    results: list[dict[str, Any]],
    client: httpx.AsyncClient,
) -> None:
    while not queue.empty():
        path = await queue.get()
        start = time.perf_counter()
        status_code = 0
        success = False
        try:
            resp = await client.get(f"{target_url}{path}", timeout=10.0)
            status_code = resp.status_code
            success = resp.status_code == 200
        except Exception:
            status_code = 500
        duration_ms = (time.perf_counter() - start) * 1000.0
        results.append(
            {
                "path": path,
                "status_code": status_code,
                "duration_ms": duration_ms,
                "success": success,
            }
        )
        queue.task_done()


async def run_load_test(target_url: str, total_requests: int, concurrency: int) -> dict[str, Any]:
    queue: asyncio.Queue[str] = asyncio.Queue()
    for i in range(total_requests):
        path = ENDPOINTS[i % len(ENDPOINTS)]
        queue.put_nowait(path)

    results: list[dict[str, Any]] = []
    start_total = time.perf_counter()

    async with httpx.AsyncClient() as client:
        workers = [
            asyncio.create_task(worker(target_url, queue, results, client))
            for _ in range(concurrency)
        ]
        await queue.join()
        for w in workers:
            w.cancel()

    total_time = time.perf_counter() - start_total
    successful = [r for r in results if r["success"]]
    durations = [r["duration_ms"] for r in results]
    durations.sort()

    p50 = durations[int(len(durations) * 0.50)] if durations else 0.0
    p95 = durations[int(len(durations) * 0.95)] if durations else 0.0
    p99 = durations[int(len(durations) * 0.99)] if durations else 0.0
    rps = len(results) / total_time if total_time > 0 else 0.0

    report = {
        "target_url": target_url,
        "total_requests": total_requests,
        "concurrency": concurrency,
        "successful_requests": len(successful),
        "failed_requests": total_requests - len(successful),
        "error_rate_pct": round((total_requests - len(successful)) / total_requests * 100, 2),
        "total_duration_sec": round(total_time, 2),
        "requests_per_second": round(rps, 2),
        "latency_p50_ms": round(p50, 2),
        "latency_p95_ms": round(p95, 2),
        "latency_p99_ms": round(p99, 2),
    }
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="AlphaMind AI Load Test")
    parser.add_argument("--target", default="http://localhost:8000", help="Target API base URL")
    parser.add_argument("--requests", type=int, default=300, help="Total requests to execute")
    parser.add_argument("--concurrency", type=int, default=30, help="Concurrent workers")
    args = parser.parse_args()

    print(
        f"Running Load Test on {args.target} ({args.requests} requests, concurrency={args.concurrency})..."
    )  # noqa: T201
    report = asyncio.run(run_load_test(args.target, args.requests, args.concurrency))
    print("\n--- LOAD TEST SUMMARY ---")  # noqa: T201
    for k, v in report.items():
        print(f"  {k:<22}: {v}")  # noqa: T201


if __name__ == "__main__":
    main()
