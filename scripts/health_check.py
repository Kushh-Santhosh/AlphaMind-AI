#!/usr/bin/env python3
"""
AlphaMind AI — Health Check Script.
Verifies connectivity to all infrastructure services.
"""

import asyncio
import sys


async def check_services() -> bool:
    """Ping all required infrastructure services and report their status."""
    services = {
        "PostgreSQL (port 5432)": ("localhost", 5432),
        "Redis (port 6379)": ("localhost", 6379),
        "ChromaDB (port 8001)": ("localhost", 8001),
        "Neo4j (port 7687)": ("localhost", 7687),
        "FastAPI Backend (port 8000)": ("localhost", 8000),
    }

    all_healthy = True
    for _name, (host, port) in services.items():
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port), timeout=2.0
            )
            writer.close()
            await writer.wait_closed()
        except Exception:
            all_healthy = False

    return all_healthy


if __name__ == "__main__":
    healthy = asyncio.run(check_services())
    sys.exit(0 if healthy else 1)
