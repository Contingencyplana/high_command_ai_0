"""Utility to log supervised toddler/AI co-play sessions for emoji Level-0.

This script standardizes the reports expected by the Pivot Five readiness
signals. Each invocation writes a JSON file into
`exchange/reports/emoji_level_0/` capturing who participated, which emoji
chains were used, and any observational notes that help future audits.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List


def _find_repo_root(script_path: Path) -> Path:
    for parent in [script_path] + list(script_path.parents):
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Unable to locate repository root (missing .git)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Log a supervised toddler/AI co-play session for emoji Level-0."
    )
    parser.add_argument("--session-id", required=True, help="Readable session identifier (e.g., beta-flight-001).")
    parser.add_argument(
        "--participants",
        nargs="+",
        required=True,
        help="List of participants (e.g., adult-alfa, toddler-beta, agent-shagi-01).",
    )
    parser.add_argument(
        "--glyph-chain",
        action="append",
        default=[],
        help="Emoji chain observed during the session (repeatable).",
    )
    parser.add_argument(
        "--notes",
        default="",
        help="Optional free-form notes capturing narration, accessibility observations, etc.",
    )
    parser.add_argument(
        "--outcome",
        default="pending",
        choices=["success", "partial", "failure", "pending"],
        help="Overall session outcome from facilitator perspective.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    script_path = Path(__file__).resolve()
    repo_root = _find_repo_root(script_path.parent)
    report_dir = repo_root / "exchange" / "reports" / "emoji_level_0"
    report_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc)
    stamp = timestamp.strftime("%Y%m%dT%H%M%SZ")
    filename = f"{stamp}_{args.session_id}.json"
    destination = report_dir / filename

    glyph_chains: List[str] = [glyph.strip() for glyph in args.glyph_chain if glyph.strip()]

    report = {
        "session_id": args.session_id,
        "recorded_at": timestamp.isoformat().replace("+00:00", "Z"),
        "participants": args.participants,
        "glyph_chains": glyph_chains,
        "notes": args.notes,
        "outcome": args.outcome,
        "schema": "emoji-level-0-coplay@1.0",
    }

    with destination.open("w", encoding="utf-8") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    try:
        relative = destination.relative_to(repo_root)
    except ValueError:
        relative = destination
    print(f"Logged co-play session to {relative}")


if __name__ == "__main__":
    main()
