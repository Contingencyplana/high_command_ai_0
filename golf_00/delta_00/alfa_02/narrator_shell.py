"""Minimal narrator shell (stub) for Order 044.

Usage:
    python -m golf_00.delta_00.alfa_02.narrator_shell --say "Forge crafts the Ally → Victory"

This stub prints a narration line and optionally appends a JSONL event
when --out is provided. Keep side effects minimal to preserve portability.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


def _iso_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run(say: str, out: Optional[Path] = None) -> None:
    print(say)
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        event = {
            "ts": _iso_now(),
            "type": "narration",
            "line": say,
            "source": "alfa_02:narrator_shell",
        }
        with out.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False) + "\n")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Narrator shell stub")
    parser.add_argument("--say", required=True, help="Narration line to emit")
    parser.add_argument("--out", type=Path, help="Optional JSONL path to append events")
    args = parser.parse_args(argv)
    run(args.say, args.out)
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI
    raise SystemExit(main())

