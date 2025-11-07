"""Minimal telemetry shell (stub) for Order 044.

Usage:
    python -m golf_00.delta_00.alfa_03.telemetry_shell --event forge.craft --status success \
        --details "Actor forge executes craft" --out logs/alfa_03/telemetry.jsonl

Prints an event dict and optionally appends a JSONL record when --out is set.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


def _iso_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run(event: str, status: str, details: Optional[str] = None, out: Optional[Path] = None) -> None:
    rec = {
        "ts": _iso_now(),
        "event": event,
        "status": status,
        "details": details or "",
        "source": "alfa_03:telemetry_shell",
    }
    print(json.dumps(rec, ensure_ascii=False))
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(rec, ensure_ascii=False) + "\n")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Telemetry shell stub")
    parser.add_argument("--event", required=True, help="Event name, e.g. forge.craft")
    parser.add_argument("--status", required=True, choices=["success", "failure", "warning"], help="Status")
    parser.add_argument("--details", help="Optional details string")
    parser.add_argument("--out", type=Path, help="Optional JSONL path to append events")
    args = parser.parse_args(argv)
    run(args.event, args.status, args.details, args.out)
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI
    raise SystemExit(main())

