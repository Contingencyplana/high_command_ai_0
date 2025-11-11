"""Morningate Reflection (stub)

Generates a minimal read-only summary of missions from the ledger:
- Counts by status
- Table of recent orders with ack/report presence

Outputs a Markdown file to logs/reflection/summary-<ts>.md and prints the path.

Usage:
  python -m tools.morningate_reflection
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_INDEX = REPO_ROOT / "exchange" / "ledger" / "index.json"
OUT_DIR = REPO_ROOT / "logs" / "reflection"


def _iso_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_index() -> Dict[str, Any]:
    try:
        return json.loads(LEDGER_INDEX.read_text(encoding="utf-8"))
    except Exception:
        return {"orders": {}}


def render_md(index: Dict[str, Any]) -> str:
    orders: Dict[str, Dict[str, Any]] = index.get("orders", {}) or {}
    by_status: Dict[str, int] = {}
    rows: list[tuple[str, str, str, str]] = []
    for order_id, meta in orders.items():
        status = str(meta.get("status", "unknown"))
        by_status[status] = by_status.get(status, 0) + 1
        ack = "✓" if meta.get("ack_path") else "—"
        rep = "✓" if meta.get("report_path") else "—"
        rows.append((order_id, status, ack, rep))

    rows.sort(key=lambda r: r[0])
    lines: list[str] = []
    lines.append(f"Morningate Reflection — {_iso_now()}")
    lines.append("")
    # Summary
    lines.append("Status Totals:")
    for k in sorted(by_status.keys()):
        lines.append(f"- {k}: {by_status[k]}")
    lines.append("")
    # Table
    lines.append("| Order | Status | Ack | Report |")
    lines.append("|-------|--------|-----|--------|")
    for order_id, status, ack, rep in rows[:50]:
        lines.append(f"| {order_id} | {status} | {ack} | {rep} |")
    if len(rows) > 50:
        lines.append(f"\n(… {len(rows)-50} more orders omitted)\n")
    return "\n".join(lines) + "\n"


def write_output(md: str) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    dest = OUT_DIR / f"summary-{ts}.md"
    dest.write_text(md, encoding="utf-8")
    return dest


def main(argv: list[str] | None = None) -> int:  # pragma: no cover - CLI
    index = load_index()
    md = render_md(index)
    path = write_output(md)
    print(path.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

