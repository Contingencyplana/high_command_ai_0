from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


def _ts() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass
class UILoggingSession:
    """Lightweight telemetry sink for Campaign 2 emoji-first UI playtests.

    Collects command events and HUD signals, then writes a playtest JSONL plus a
    telemetry summary JSON. Designed to be called from the live UI handlers.
    """

    repo_root: Path
    run_id: str
    start_ts: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    events: List[Dict[str, object]] = field(default_factory=list)
    first_command_ts: Optional[datetime] = None
    down_ts: Optional[datetime] = None
    revive_ts: Optional[datetime] = None
    one_more_prompt_ts: Optional[datetime] = None
    emoji_latency_samples: List[int] = field(default_factory=list)

    def record_command(
        self,
        *,
        cell: str,
        overlays: Optional[List[str]] = None,
        trace_id: Optional[str] = None,
        label: Optional[str] = None,
        description: Optional[str] = None,
        latency_ms: Optional[int] = None,
    ) -> None:
        now = datetime.now(timezone.utc)
        if self.first_command_ts is None:
            self.first_command_ts = now
        if latency_ms is not None:
            try:
                self.emoji_latency_samples.append(int(latency_ms))
            except Exception:
                pass
        record: Dict[str, object] = {
            "timestamp": _ts(),
            "event": "command",
            "cell": cell,
            "run_id": self.run_id,
        }
        if overlays:
            record["overlays"] = overlays
        if trace_id:
            record["trace_id"] = trace_id
        if label:
            record["label"] = label
        if description:
            record["description"] = description
        if latency_ms is not None:
            record["latency_ms"] = latency_ms
        self.events.append(record)

    def record_ui_state(self, *, state: str) -> None:
        self.events.append(
            {
                "timestamp": _ts(),
                "event": "ui_state",
                "state": state,
                "run_id": self.run_id,
            }
        )

    def record_downed(self) -> None:
        self.down_ts = datetime.now(timezone.utc)
        self.events.append(
            {
                "timestamp": _ts(),
                "event": "downed",
                "run_id": self.run_id,
            }
        )

    def record_revive(self) -> None:
        self.revive_ts = datetime.now(timezone.utc)
        self.events.append(
            {
                "timestamp": _ts(),
                "event": "revive",
                "run_id": self.run_id,
            }
        )

    def record_one_more_prompt(self) -> None:
        self.one_more_prompt_ts = datetime.now(timezone.utc)
        self.events.append(
            {
                "timestamp": _ts(),
                "event": "one_more_prompt",
                "run_id": self.run_id,
            }
        )

    def finalize(
        self,
        *,
        duration_ms: Optional[int] = None,
        log_dir: Optional[Path] = None,
        attachments_dir: Optional[Path] = None,
    ) -> None:
        log_dir = log_dir or (self.repo_root / "logs")
        attachments_dir = attachments_dir or (self.repo_root / "exchange" / "outbox" / "attachments" / "campaign2")
        log_dir.mkdir(parents=True, exist_ok=True)
        attachments_dir.mkdir(parents=True, exist_ok=True)

        playtest_path = log_dir / "order-2025-11-26-061-campaign2-playtest.jsonl"
        telemetry_path = log_dir / "order-2025-11-26-061-campaign2-telemetry.json"

        # Write events
        with playtest_path.open("a", encoding="utf-8") as handle:
            for event in self.events:
                handle.write(json.dumps(event, ensure_ascii=False))
                handle.write("\n")

        # Compute summary metrics
        now = datetime.now(timezone.utc)
        duration_ms = duration_ms if duration_ms is not None else int((now - self.start_ts).total_seconds() * 1000)
        time_to_fun_ms: Optional[int] = None
        if self.first_command_ts is not None:
            time_to_fun_ms = int((self.first_command_ts - self.start_ts).total_seconds() * 1000)
        revive_latency_ms: Optional[int] = None
        if self.down_ts and self.revive_ts:
            revive_latency_ms = int((self.revive_ts - self.down_ts).total_seconds() * 1000)

        telemetry: Dict[str, object] = {
            "run_id": self.run_id,
            "start": self.start_ts.isoformat().replace("+00:00", "Z"),
            "duration_ms": duration_ms,
            "time_to_fun_ms": time_to_fun_ms,
            "revive_latency_ms": revive_latency_ms,
            "emoji_latency_samples": self.emoji_latency_samples,
            "accuracy": None,
            "events_logged": len(self.events),
        }

        with telemetry_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(telemetry, ensure_ascii=False))
            handle.write("\n")

        # Mirror to attachments for hub pickup
        for src in (playtest_path, telemetry_path):
            dest = attachments_dir / src.name
            try:
                dest.write_bytes(src.read_bytes())
            except Exception:
                pass
