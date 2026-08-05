"""
AlphaMind AI v2 — Staging Stress & Saturation Testing Script

Pushes target endpoints through increasing concurrency levels (10 -> 50 -> 100 -> 250)
to locate saturation limits, breaking points, and degradation knees.

Usage:
  python scripts/stress_test.py --target http://localhost:8000
"""

# ruff: noqa: T201

from __future__ import annotations

import argparse
import asyncio
import time
from typing import Any

import httpx

CONCURRENCY_LEVELS = [10, 50, 100, 200]
REQUESTS_PER_LEVEL = 200


async def run_stress_level(
    target_url: str, concurrency: int, requests_count: int
) -> dict[str, Any]:
    start = time.perf_counter()
    success_count = 0
    fail_count = 0
    durations: list[float] = []

    async with httpx.AsyncClient(timeout=15.0) as client:
        sem = asyncio.Semaphore(concurrency)

        async def fetch(i: int) -> None:
            nonlocal success_count, fail_count
            async with sem:
                t0 = time.perf_counter()
                try:
                    resp = await client.get(f"{target_url}/api/v1/mission-control/dashboard")
                    if resp.status_code == 200:
                        success_count += 1
                    else:
                        fail_count += 1
                except Exception:
                    fail_count += 1
                durations.append((time.perf_counter() - t0) * 1000.0)

        tasks = [asyncio.create_task(fetch(i)) for i in range(requests_count)]
        await asyncio.gather(*tasks)

    elapsed = time.perf_counter() - start
    durations.sort()
    p95 = durations[int(len(durations) * 0.95)] if durations else 0.0

    return {
        "concurrency": concurrency,
        "requests": requests_count,
        "success": success_count,
        "failures": fail_count,
        "duration_sec": round(elapsed, 2),
        "rps": round(requests_count / elapsed, 1) if elapsed > 0 else 0,
        "p95_latency_ms": round(p95, 2),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="AlphaMind AI Stress Test")
    parser.add_argument("--target", default="http://localhost:8000", help="Target API base URL")
    args = parser.parse_args()

    print(f"Starting Stress & Saturation Test on {args.target}...")  # noqa: T201
    print(
        f"{'CONCURRENCY':<12} | {'REQUESTS':<10} | {'SUCCESS':<10} | {'FAILURES':<10} | {'RPS':<10} | {'p95 (ms)':<10}"
    )  # noqa: T201
    print("-" * 75)  # noqa: T201

    for c in CONCURRENCY_LEVELS:
        res = asyncio.run(run_stress_level(args.target, c, REQUESTS_PER_LEVEL))
        conc = res["concurrency"]
        reqs = res["requests"]
        succ = res["success"]
        fails = res["failures"]
        rps = res["rps"]
        p95 = res["p95_latency_ms"]
        print(
            f"{conc:<12} | {reqs:<10} | {succ:<10} | {fails:<10} | {rps:<10.1f} | {p95:<10.2f}"
        )  # noqa: T201


if __name__ == "__main__":
    main()
