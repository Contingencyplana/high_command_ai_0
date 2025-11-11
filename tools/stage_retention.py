"""Stage Directory Retention Tool

Prunes old staged "online" mirror files under the configured stage_dir
to prevent unbounded growth during Hybrid staging.

Defaults: dry-run; keep last 200 files by mtime.

Usage:
  python -m tools.stage_retention                            # dry-run
  python -m tools.stage_retention --write                    # apply deletions
  python -m tools.stage_retention --keep 500                 # keep last 500
  python -m tools.stage_retention --dir path/to/stage_dir    # override dir
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple
import json


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = REPO_ROOT / "exchange" / "config.json"


@dataclass(frozen=True)
class Plan:
    stage_dir: Path
    keep: int
    total: int
    delete: List[Path]


def resolve_stage_dir(override: str | None) -> Path:
    if override:
        p = Path(override)
        return p if p.is_absolute() else (REPO_ROOT / p)
    cfg_path = DEFAULT_CONFIG
    stage = None
    try:
        raw = json.loads(cfg_path.read_text(encoding="utf-8"))
        online = raw.get("online", {}) if isinstance(raw, dict) else {}
        if isinstance(online, dict):
            candidate = online.get("stage_dir")
            if isinstance(candidate, str) and candidate.strip():
                stage = candidate
    except Exception:
        stage = None
    if not stage:
        stage = "exchange/outbox/online_stage"
    p = Path(stage)
    return p if p.is_absolute() else (REPO_ROOT / p)


def plan_prune(stage_dir: Path, keep: int) -> Plan:
    files = sorted(
        (p for p in stage_dir.glob("**/*") if p.is_file()),
        key=lambda x: x.stat().st_mtime,
        reverse=True,
    )
    to_delete = files[keep:] if len(files) > keep else []
    return Plan(stage_dir=stage_dir, keep=keep, total=len(files), delete=to_delete)


def apply(plan: Plan, *, write: bool) -> None:
    if not write:
        print(f"[DRY-RUN] Stage retention: {plan.total} files, keeping {plan.keep}, would delete {len(plan.delete)}")
        for p in plan.delete[:10]:
            print(f"  would delete: {p}")
        if len(plan.delete) > 10:
            print(f"  ... and {len(plan.delete) - 10} more")
        return
    deleted = 0
    for p in plan.delete:
        try:
            p.unlink(missing_ok=True)
            deleted += 1
        except Exception as exc:
            print(f"[WARN] could not delete {p}: {exc}")
    print(f"[OK] Stage retention: deleted {deleted} file(s); kept {plan.keep} of {plan.total}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Prune Hybrid staging directory")
    p.add_argument("--dir", help="Stage directory (defaults to exchange/config.json online.stage_dir)")
    p.add_argument("--keep", type=int, default=200, help="Keep last N files by mtime (default: 200)")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--write", dest="write", action="store_true", help="Apply deletions")
    g.add_argument("--dry-run", dest="write", action="store_false", help="Plan deletions only (default)")
    p.set_defaults(write=False)
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:  # pragma: no cover - CLI
    args = parse_args(argv)
    stage_dir = resolve_stage_dir(args.dir)
    if not stage_dir.exists():
        print(f"[INFO] Stage dir missing, nothing to prune: {stage_dir}")
        return 0
    plan = plan_prune(stage_dir, keep=max(0, int(args.keep)))
    apply(plan, write=bool(args.write))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

