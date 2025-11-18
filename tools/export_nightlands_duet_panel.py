"""Generate a lightweight JSON panel for Nightlands duet telemetry.

Reads the append-only feed produced by Alfa Zero (`nightlands_duet_storyboard_sync_feed.jsonl`)
and emits a compact JSON summary combining storyboard runs and targeted sync executions.
This acts as the interim “dashboard panel” while the shared tooling remains offline.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


FEED_PATH = Path("exchange/attachments/telemetry/nightlands_duet/nightlands_duet_storyboard_sync_feed.jsonl")
OUTPUT_PATH = Path("exchange/attachments/telemetry/nightlands_duet/nightlands_duet_storyboard_sync_panel.json")
MAX_ENTRIES = 24


def load_feed(path: Path) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    if not path.exists():
        return records
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records[-MAX_ENTRIES:]


def build_panel(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    panel = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source_feed": FEED_PATH.as_posix(),
        "entries": [],
    }
    for record in records:
        event = record.get("event")
        entry: Dict[str, Any] = {
            "timestamp": record.get("timestamp"),
            "event": event,
            "session_id": record.get("session_id"),
            "operator_id": record.get("operator_id"),
            "trace_id": record.get("trace_id"),
        }
        if event == "storyboard_run":
            entry["storyboard_id"] = record.get("storyboard_id")
            entry["payload_count"] = record.get("payload_count")
            entry["cooldown_seconds"] = record.get("cooldown_seconds")
        else:
            entry["files_copied"] = record.get("files_copied", record.get("copied_count"))
            entry["destination"] = record.get("destination")
            entry["summary_line"] = record.get("summary_line")
        panel["entries"].append(entry)
    return panel


def main() -> None:
    records = load_feed(FEED_PATH)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    panel = build_panel(records)
    OUTPUT_PATH.write_text(json.dumps(panel, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[OK] Panel written to {OUTPUT_PATH.as_posix()} ({len(panel['entries'])} entries)")


if __name__ == "__main__":
    main()
