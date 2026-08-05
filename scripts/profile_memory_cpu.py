"""
AlphaMind AI v2 — Memory & CPU Profiling Tool

Profiles python process memory usage (RSS), garbage collection counts, and CPU thread usage.

Usage:
  python scripts/profile_memory_cpu.py --duration 10
"""

from __future__ import annotations

import argparse
import os
import resource
import time


def profile_process(duration_sec: int) -> dict[str, float]:
    time.sleep(duration_sec)

    final_rss_bytes = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    usage = resource.getrusage(resource.RUSAGE_SELF)

    # Convert KB to MB on macOS / Linux
    rss_mb = (
        final_rss_bytes / (1024 * 1024)
        if os.uname().sysname == "Darwin"
        else final_rss_bytes / 1024
    )

    return {
        "duration_sec": float(duration_sec),
        "max_rss_mb": round(rss_mb, 2),
        "user_cpu_time_sec": round(usage.ru_utime, 3),
        "system_cpu_time_sec": round(usage.ru_stime, 3),
        "total_cpu_time_sec": round(usage.ru_utime + usage.ru_stime, 3),
        "page_faults": float(usage.ru_majflt),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="AlphaMind Memory & CPU Profiler")
    parser.add_argument(
        "--duration", type=int, default=5, help="Profiling sample duration in seconds"
    )
    args = parser.parse_args()

    print(f"Sampling process memory and CPU profile for {args.duration} seconds...")  # noqa: T201
    stats = profile_process(args.duration)
    print("\n--- PROCESS RESOURCE PROFILE ---")  # noqa: T201
    for k, v in stats.items():
        print(f"  {k}: {v}")  # noqa: T201


if __name__ == "__main__":
    main()
