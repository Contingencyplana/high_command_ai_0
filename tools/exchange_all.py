"""
exchange_all.py — One smart command to tidy the exchange after a work block.

Workflow (auto):
- Heartbeat (detect hub path and write test)
- Push (only if exchange/outbox has files)
- Pull with --move (ingest peers; clean hub copies)
- Ledger update
- Validator (if available)

Flags:
- --no-move           Disable hub cleanup on pull
- --skip-validator    Skip validator run
- --push-only         Only push (skip pull/update/validate)
- --pull-only         Only pull/update/validate (skip push)
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional
import importlib.util
import sys


def _has_files(p: Path) -> bool:
    return p.exists() and any(child.is_file() for child in p.rglob("*"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Smart exchange tidy: heartbeat → push → pull → update → validate")
    parser.add_argument("--no-move", action="store_true", help="Do not remove files from hub after pull")
    parser.add_argument("--skip-validator", action="store_true", help="Skip validator run")
    parser.add_argument("--push-only", action="store_true", help="Only push local outbox to hub")
    parser.add_argument("--pull-only", action="store_true", help="Only pull from hub and validate")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    def _load_module(mod_name: str, file: Path):
        try:
            spec = importlib.util.spec_from_file_location(mod_name, str(file))
            if not spec or not spec.loader:
                return None
            mod = importlib.util.module_from_spec(spec)
            sys.modules[mod_name] = mod
            spec.loader.exec_module(mod)
            return mod
        except Exception:
            return None

    # Try heartbeat
    hb = 0
    hb_mod = _load_module("exchange_heartbeat", repo_root / "tools" / "exchange_heartbeat.py")
    if hb_mod and hasattr(hb_mod, "heartbeat"):
        try:
            hb = hb_mod.heartbeat()
        except Exception:
            print("[WARN] Heartbeat failed; continuing")
    else:
        print("[WARN] Heartbeat module not available; continuing")

    # Resolve bridge config and helpers
    bridge_mod = _load_module("offline_bridge", repo_root / "tools" / "offline_bridge.py")
    if not bridge_mod or not hasattr(bridge_mod, "resolve_config"):
        print("[ERROR] Bridge not available")
        return 2
    cfg = bridge_mod.resolve_config()

    outbox = repo_root / "exchange" / "outbox"

    # Push phase (unless explicitly pull-only)
    if not args.pull_only:
        if _has_files(outbox):
            try:
                pushed = bridge_mod.push(cfg)
                print(f"[all] Pushed {pushed} file(s)")
            except Exception as e:
                print(f"[WARN] Push failed: {e}")
        else:
            print("[all] No local outbox files to push")
        if args.push_only:
            # Optionally return non-zero on failed heartbeat
            return 0 if hb == 0 else 1

    # Pull phase
    try:
        pulled = bridge_mod.pull(cfg, move=not args.no_move)
        print(f"[all] Pulled {pulled} file(s)")
    except Exception as e:
        print(f"[WARN] Pull failed: {e}")

    # Ledger update
    led_mod = _load_module("ledger_update", repo_root / "tools" / "ledger_update.py")
    if led_mod and hasattr(led_mod, "update_ledger"):
        try:
            changed = led_mod.update_ledger(repo_root)
            print(f"[all] Ledger updated, {changed} change(s)")
        except Exception as e:
            print(f"[WARN] Ledger update failed: {e}")
    else:
        print("[INFO] Ledger updater not available; skipping")

    # Validator (optional)
    if not args.skip_validator:
        val_mod = _load_module("exchange_validator", repo_root / "tools" / "exchange_validator.py")
        if val_mod and hasattr(val_mod, "main"):
            try:
                code = val_mod.main()
                if code == 0:
                    print("[all] Validator OK")
                else:
                    print("[all] Validator reported inconsistencies")
            except Exception:
                print("[WARN] Validator failed")
        else:
            print("[INFO] Validator not available; skipping")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
