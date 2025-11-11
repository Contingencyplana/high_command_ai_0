"""Online channel stubs for Hybrid Communications.

These are scaffolds: they plan actions and provide a consistent interface,
but perform no network I/O unless explicitly implemented later.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class ChannelConfig:
    channel: str = "git"  # or "http"
    retries: int = 0
    timeout_ms: int = 2000
    stage_dir: str | None = None


class OnlineChannel:
    def __init__(self, config: ChannelConfig) -> None:
        self.config = config

    def plan(self, *, kind: str, trace_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:  # noqa: D401
        return {
            "channel": self.config.channel,
            "retries": self.config.retries,
            "timeout_ms": self.config.timeout_ms,
            "kind": kind,
            "trace_id": trace_id,
        }

    def write(self, plan: Dict[str, Any], payload: Dict[str, Any]) -> bool:
        # Stub: no network side effects; returns False to indicate no write performed.
        return False


class GitChannel(OnlineChannel):
    def write(self, plan: Dict[str, Any], payload: Dict[str, Any]) -> bool:
        # Local stage write: mirror an online publish to a staging folder for inspection.
        # This is safe and remains local-only; no git commands or pushes are executed here.
        from pathlib import Path
        import json
        from datetime import datetime, timezone

        if not self.config.stage_dir:
            return False
        try:
            out_dir = Path(self.config.stage_dir)
            if not out_dir.is_absolute():
                # Interpret relative to repository root caller
                from pathlib import Path as _P
                root = _P(__file__).resolve().parents[1]
                out_dir = root / out_dir
            out_dir.mkdir(parents=True, exist_ok=True)
            ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            kind = str(plan.get("kind", "note"))
            trace_id = str(plan.get("trace_id", "trace"))
            dest = out_dir / f"online_{kind}_{trace_id}_{ts}.json"
            dest.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            return True
        except Exception:
            return False


class HttpChannel(OnlineChannel):
    pass  # Placeholder for future HTTP publishing
