"""Hybrid Communications Adapter (shadow-ready)

Purpose
- Provide a single routing surface to publish exchange artifacts to
  offline (local hub/outbox) and online channels.
- Defaults to safe shadow mode; online is disabled via config.

Public API
- send(kind, payload, trace_id, dry_run=True) -> dict
  kind: 'report' | 'order' | 'ack' | 'note'
  payload: dict that would be written
  trace_id: str used to generate idempotent filenames
  dry_run: when True, only plans paths; no files written

Notes
- Offline sink only writes 'report' artifacts to exchange/reports/outbox.
  Other kinds are planned-only for now to avoid unexpected side-effects.
- Online sink is a noop logger until exchange/config.json[online.enabled] is true.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / "exchange" / "config.json"


def _iso_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _content_hash(payload: Dict[str, Any]) -> str:
    blob = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:12]


@dataclass(frozen=True)
class OnlineConfig:
    enabled: bool
    channel: str
    retries: int
    timeout_ms: int


def _load_config() -> dict:
    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"mode": "local", "online": {"enabled": False}}


class CommAdapter:
    def __init__(self) -> None:
        cfg = _load_config()
        online = cfg.get("online", {}) if isinstance(cfg, dict) else {}
        self.online = OnlineConfig(
            enabled=bool(online.get("enabled", False)),
            channel=str(online.get("channel", "git")),
            retries=int(online.get("retries", 0)),
            timeout_ms=int(online.get("timeout_ms", 2000)),
        )

    # Offline sink planning/writing
    def _offline_plan(self, kind: str, trace_id: str, payload: Dict[str, Any]) -> dict:
        outbox = REPO_ROOT / "exchange" / ("reports" if kind == "report" else "outbox")
        # Orders already have specific outboxes under outbox/orders; keep simple plan here
        if kind == "report":
            out_dir = REPO_ROOT / "exchange" / "reports" / "outbox"
            out_dir.mkdir(parents=True, exist_ok=True)
            h = _content_hash(payload)
            filename = f"hybrid_shadow_{_iso_now()}_{trace_id}_{h}.json"
            return {"dir": str(out_dir), "file": str(out_dir / filename)}
        return {"dir": str(outbox), "file": None}

    def _offline_write(self, planned: dict, payload: Dict[str, Any]) -> bool:
        path_str = planned.get("file")
        if not path_str:
            return False
        path = Path(path_str)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return True

    # Online sink (noop until enabled)
    def _online_plan(self, kind: str, trace_id: str, payload: Dict[str, Any]) -> dict:
        return {
            "enabled": self.online.enabled,
            "channel": self.online.channel,
            "retries": self.online.retries,
            "timeout_ms": self.online.timeout_ms,
        }

    def send(self, *, kind: str, payload: Dict[str, Any], trace_id: str, dry_run: bool = True) -> dict:
        result: dict = {"kind": kind, "trace_id": trace_id}

        # Offline
        offline_plan = self._offline_plan(kind, trace_id, payload)
        result["offline"] = {"planned": offline_plan, "wrote": False}
        if not dry_run and kind == "report":
            wrote = self._offline_write(offline_plan, payload)
            result["offline"]["wrote"] = wrote

        # Online (noop unless enabled)
        online_plan = self._online_plan(kind, trace_id, payload)
        result["online"] = {"planned": online_plan, "wrote": False}
        # Future: implement when enabled, honoring retries/timeout

        return result


def main() -> int:  # pragma: no cover - simple manual check
    adapter = CommAdapter()
    sample = {"schema": "ops-hybrid-shadow@1.0", "generated_at": _iso_now(), "note": "shadow"}
    out = adapter.send(kind="report", payload=sample, trace_id="ops-readiness", dry_run=True)
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

