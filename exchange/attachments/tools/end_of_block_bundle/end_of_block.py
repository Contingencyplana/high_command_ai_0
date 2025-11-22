"""
Convenience runner for the standard end-of-block cadence.

Runs, in order:
- python tools/exchange_heartbeat.py
- python tools/offline_sync_exchange.py
- python -m tools.ops_readiness
- python tools/exchange_all.py

Exit on first failure; prints a concise summary.
"""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> int:
    print(f"[cadence] RUN: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        print(f"[cadence] FAIL ({result.returncode}) on: {' '.join(cmd)}")
    return result.returncode


def main() -> int:
    cmds = [
        ["python", "tools/exchange_heartbeat.py"],
        ["python", "tools/offline_sync_exchange.py"],
        ["python", "-m", "tools.ops_readiness"],
        ["python", "tools/exchange_all.py"],
    ]
    for cmd in cmds:
        code = run(cmd)
        if code != 0:
            return code
    stamp = datetime.now(timezone.utc).isoformat()
    print(f"[cadence] DONE {stamp}Z")
    return 0


if __name__ == "__main__":
    sys.exit(main())
