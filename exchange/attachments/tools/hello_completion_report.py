#!/usr/bin/env python3
"""
hello_completion_report.py

Generate a small factory-report JSON ("hello" report) for a newly seeded Alfa
instance. Writes to outbox/reports by default. Designed to run in any workspace
without external dependencies.

Usage (example):
  python exchange/attachments/tools/hello_completion_report.py \
    --instance-id Alfa-001 \
    --baseline alfa-template@2025-11-13 \
    --order-id order-2025-11-13-054 \
    --readiness logs/ops_readiness.json \
    --smoke logs/contract_tests/smoke_summary.txt \
    --notes "seed OK; next: expand batch"
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List


def _utc_ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _compact_ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _detect_workspace_name() -> str:
    # Prefer explicit env, then folder name
    for key in ("WORKSPACE_NAME", "HC_WORKSPACE_NAME"):
        val = os.environ.get(key)
        if val:
            return val
    return Path.cwd().name


def _path_if_exists(p: str | None) -> str | None:
    if not p:
        return None
    pp = Path(p)
    return str(pp.as_posix()) if pp.exists() else None


def main(argv: List[str]) -> int:
    ap = argparse.ArgumentParser(description="Generate a hello factory-report JSON for a seeded Alfa instance")
    ap.add_argument("--instance-id", required=True, help="Stable ID of the Alfa instance (e.g., Alfa-001)")
    ap.add_argument("--baseline", default="unknown", help="Baseline template/version used for seeding")
    ap.add_argument("--order-id", default="order-2025-11-13-054", help="Related mass seeding order id")
    ap.add_argument("--readiness", default=None, help="Path to readiness output (optional)")
    ap.add_argument("--smoke", nargs="*", default=None, help="Paths to smoke outputs/logs (optional)")
    ap.add_argument("--notes", default=None, help="Optional freeform notes to include in the report")
    ap.add_argument("--outdir", default="outbox/reports", help="Directory to write the report into")
    args = ap.parse_args(argv)

    workspace = _detect_workspace_name()
    ts_iso = _utc_ts()
    ts_compact = _compact_ts()

    readiness_path = _path_if_exists(args.readiness)
    smoke_paths = [p for p in ([_path_if_exists(s) for s in (args.smoke or [])]) if p]

    report = {
        "schema": "factory-report@1.0",
        "report_id": f"hello-{args.instance_id}-{ts_compact}",
        "order_id": args.order_id,
        "reported_by": workspace,
        "receiver": "high_command_ai_0",
        "timestamp_reported": ts_iso,
        "status": "completed",
        "summary": f"Hello from {args.instance_id} seeded from {args.baseline} — readiness and smoke attached where available.",
        "instance": {
            "id": args.instance_id,
            "baseline": args.baseline,
        },
        "evidence": {
            "readiness": readiness_path,
            "smoke": smoke_paths if smoke_paths else None,
        },
        "notes": [args.notes] if args.notes else [],
    }

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    outfile = outdir / f"hello-{args.instance_id}-{ts_compact}.json"
    with outfile.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        f.write("\n")

    print(str(outfile.as_posix()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

