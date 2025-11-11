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
    pass  # Placeholder for future Git-based publishing


class HttpChannel(OnlineChannel):
    pass  # Placeholder for future HTTP publishing

