"""
offline_bridge.py — Bidirectional offline exchange bridge for Genesis Mesh.

Provides push/pull/sync between a workspace's local exchange and a shared hub.

Conventions
- Local workspace layout (this repo):
  - exchange/outbox/**          (things we publish)
  - exchange/reports/inbox/**   (incoming reports/acks)
  - exchange/orders/{pending,dispatched,completed}/
  - exchange/acknowledgements/{pending,logged}/
  - telemetry/emoji_runtime/promoted_samples/**

- Hub layout (shared filesystem):
  - <hub>/<front>/outbox/**     (each front publishes here)

Routing rules (pull)
- Any peer <front>/outbox/reports/**              -> exchange/reports/inbox/**
- Any peer <front>/outbox/orders/<state>/**       -> exchange/orders/<state>/**
- Any peer <front>/outbox/acknowledgements/**     -> exchange/acknowledgements/**
- Any peer <front>/outbox/telemetry/emoji_runtime/promoted_samples/**
                                                -> telemetry/emoji_runtime/promoted_samples/**
- Otherwise                                      -> exchange/inbox/**

Front identity
- SHAGI_FRONT env var, or workspace folder name.

Hub path
- SHAGI_EXCHANGE_PATH env var, or exchange/config.json.upstream_root,
  or default: C:/Users/Admin/high_command_exchange
"""

from __future__ import annotations

import argparse
import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional, Tuple, List, Dict
import json
import fnmatch


DEFAULT_HUB = Path("C:/Users/Admin/high_command_exchange")


@dataclass
class BridgeConfig:
    hub: Path
    front: str
    repo_root: Path


def _load_config(repo_root: Path) -> Dict[str, object]:
    cfg_path = repo_root / "exchange" / "config.json"
    try:
        return json.loads(cfg_path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def load_hub_from_config(repo_root: Path) -> Optional[Path]:
    data = _load_config(repo_root)
    upstream = data.get("upstream_root") if isinstance(data, dict) else None
    if isinstance(upstream, str) and upstream.strip():
        return Path(upstream)
    return None


def resolve_config() -> BridgeConfig:
    repo_root = Path(__file__).resolve().parents[1]
    env_hub = os.getenv("SHAGI_EXCHANGE_PATH")
    hub = Path(env_hub) if env_hub else (load_hub_from_config(repo_root) or DEFAULT_HUB)
    # SHAGI_FRONT precedence: env -> exchange/config.json.front -> repo folder name
    cfg_front: Optional[str] = None
    try:
        data = _load_config(repo_root)
        if isinstance(data, dict):
            v = data.get("front")
            if isinstance(v, str) and v.strip():
                cfg_front = v.strip()
    except Exception:
        cfg_front = None
    front = os.getenv("SHAGI_FRONT") or cfg_front or repo_root.name
    return BridgeConfig(hub=hub, front=front, repo_root=repo_root)


def _iter_files(root: Path) -> Iterable[Path]:
    if not root.exists():
        return []
    for p in root.rglob("*"):
        if p.is_file():
            yield p


def _copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def _move_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dst))


def push(cfg: BridgeConfig) -> int:
    local_outbox = cfg.repo_root / "exchange" / "outbox"
    if not local_outbox.exists():
        print(f"[WARN] Local outbox not found: {local_outbox}")
        return 0

    hub_outbox = cfg.hub / cfg.front / "outbox"
    count = 0
    for f in _iter_files(local_outbox):
        rel = f.relative_to(local_outbox)
        dst = hub_outbox / rel
        _copy_file(f, dst)
        print(f"PUSH {f} -> {dst}")
        count += 1

    print(f"[OK] Pushed {count} file(s) to hub: {hub_outbox}")
    return count


def _route_pull_destination(cfg: BridgeConfig, peer_rel_under_outbox: Path) -> Tuple[Path, str]:
    parts = tuple(part.lower() for part in peer_rel_under_outbox.parts)

    # reports -> exchange/reports/inbox/[rest after 'reports']
    if "reports" in parts:
        idx = parts.index("reports")
        tail = Path(*peer_rel_under_outbox.parts[idx + 1 :])
        dest = cfg.repo_root / "exchange" / "reports" / "inbox" / tail
        return dest, "reports/inbox"

    # acknowledgements -> exchange/acknowledgements/[same structure]
    if "acknowledgements" in parts:
        idx = parts.index("acknowledgements")
        tail = Path(*peer_rel_under_outbox.parts[idx + 1 :])
        dest = cfg.repo_root / "exchange" / "acknowledgements" / tail
        return dest, "acknowledgements"

    # orders/<state> -> exchange/orders/<state>/[rest after state]
    if len(parts) >= 2 and parts[0] == "orders" and parts[1] in {"pending", "dispatched", "completed"}:
        state = parts[1]
        tail = Path(*peer_rel_under_outbox.parts[2:])
        dest = cfg.repo_root / "exchange" / "orders" / state / tail
        return dest, f"orders/{state}"

    # telemetry/emoji_runtime/promoted_samples -> telemetry/emoji_runtime/promoted_samples/[tail]
    if len(parts) >= 3 and parts[0] == "telemetry" and parts[1] == "emoji_runtime" and parts[2] == "promoted_samples":
        tail = Path(*peer_rel_under_outbox.parts[3:])
        dest = cfg.repo_root / "telemetry" / "emoji_runtime" / "promoted_samples" / tail
        return dest, "telemetry/emoji_runtime/promoted_samples"

    # default inbox catch-all under exchange/inbox
    dest = cfg.repo_root / "exchange" / "inbox" / peer_rel_under_outbox
    return dest, "exchange/inbox"


def pull(cfg: BridgeConfig, *, move: bool = False) -> int:
    if not cfg.hub.exists():
        print(f"[WARN] Hub path does not exist: {cfg.hub}")
        return 0

    count = 0
    for peer in sorted(p for p in cfg.hub.iterdir() if p.is_dir() and p.name != cfg.front):
        peer_outbox = peer / "outbox"
        if not peer_outbox.exists():
            continue
        for f in _iter_files(peer_outbox):
            rel = f.relative_to(peer_outbox)
            dst, bucket = _route_pull_destination(cfg, rel)
            _copy_file(f, dst)
            action = "MOVE" if move else "COPY"
            print(f"PULL {action} {peer.name}:{rel} -> {dst} [{bucket}]")
            if move:
                try:
                    f.unlink(missing_ok=True)
                except Exception as e:
                    print(f"[WARN] Failed to remove {f}: {e}")
            count += 1

    print(f"[OK] Pulled {count} file(s) from hub into local inboxes")

    # Post-pull sorter: promote known artifacts from exchange/inbox
    try:
        inbox_root = cfg.repo_root / "exchange" / "inbox"
        promoted = 0
        # Load optional router rules
        def _load_rules() -> List[Dict[str, str]]:
            rules: List[Dict[str, str]] = []
            for candidate in [
                cfg.repo_root / "exchange" / "router_rules.json",
                cfg.repo_root / "tools" / "router_rules.json",
            ]:
                try:
                    if candidate.exists():
                        data = json.loads(candidate.read_text(encoding="utf-8"))
                        if isinstance(data, list):
                            for r in data:
                                if (
                                    isinstance(r, dict)
                                    and isinstance(r.get("glob"), str)
                                    and isinstance(r.get("dest"), str)
                                ):
                                    rules.append({"glob": r["glob"], "dest": r["dest"]})
                except Exception:
                    # Ignore malformed rules files
                    pass
            return rules

        rules = _load_rules()
        if inbox_root.exists():
            for f in inbox_root.rglob("*"):
                if not f.is_file():
                    continue
                name = f.name
                low = name.lower()
                dest: Optional[Path] = None
                # Reports
                if low.startswith("order-") and low.endswith("-report.json"):
                    dest = cfg.repo_root / "exchange" / "reports" / "inbox" / name
                # Acknowledgements
                elif low.startswith("order-") and low.endswith("-ack.json"):
                    dest = cfg.repo_root / "exchange" / "acknowledgements" / "logged" / name
                # TF emoji dryrun samples
                elif name.upper().startswith("TF-EMOJI-DRYRUN") and low.endswith(".json"):
                    dest = cfg.repo_root / "telemetry" / "emoji_runtime" / "promoted_samples" / name
                # Externalizable rules (basename glob -> relative dest dir)
                if dest is None and rules:
                    for r in rules:
                        try:
                            if fnmatch.fnmatch(name, r["glob"]):
                                dest = cfg.repo_root / Path(r["dest"]) / name
                                break
                        except Exception:
                            continue
                if dest is not None:
                    _move_file(f, dest)
                    print(f"SORT MOVE {f} -> {dest}")
                    promoted += 1
        print(f"[OK] Sorted {promoted} inbox file(s)")
    except Exception as e:
        print(f"[WARN] Inbox sorting failed: {e}")

    # Update ledger after ingest
    try:
        try:
            from tools.ledger_update import update_ledger  # type: ignore
        except ModuleNotFoundError:
            import sys as _sys
            root = str(cfg.repo_root)
            if root not in _sys.path:
                _sys.path.insert(0, root)
            from tools.ledger_update import update_ledger  # type: ignore

        changed = update_ledger(cfg.repo_root)
        print(f"[OK] Ledger updated ({changed} change(s))")
    except Exception as e:
        print(f"[WARN] Ledger update failed: {e}")
    return count


def main() -> int:
    cfg = resolve_config()

    parser = argparse.ArgumentParser(description="Bidirectional offline exchange bridge")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("push", help="Push local exchange/outbox to hub/<front>/outbox")

    p_pull = sub.add_parser("pull", help="Pull peers' outboxes into local inboxes")
    p_pull.add_argument("--move", action="store_true", help="Remove files from hub after successful pull")

    p_sync = sub.add_parser("sync", help="Push then pull")
    p_sync.add_argument("--move", action="store_true", help="Remove files from hub after successful pull")

    args = parser.parse_args()

    if args.cmd == "push":
        push(cfg)
    elif args.cmd == "pull":
        pull(cfg, move=bool(getattr(args, "move", False)))
    elif args.cmd == "sync":
        push(cfg)
        pull(cfg, move=bool(getattr(args, "move", False)))
    else:
        parser.print_help()
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
