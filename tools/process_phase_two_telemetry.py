"""Process telemetry JSON lines and update Alfa Zero Phase 2 logs.

Accepted payload format per line (extra fields ignored):

    {
      "batch_id": "forge-command-20251101T102228Z",
      "status": "success",
      "duration_ms": 2120,
      "timestamp": "2025-11-01T10:22:30.123Z"
    }

If ``duration_ms`` is omitted, the script computes it from the stored dispatch
time. When ``timestamp`` is missing, it defaults to "now".

Usage examples:

    python tools/process_phase_two_telemetry.py < telemetry_events.jsonl
    some_generator | python tools/process_phase_two_telemetry.py --verbose
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from typing import Iterable, TextIO

from golf_00.delta_00.alfa_00.overlay_bridge import record_phase_two_telemetry


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply telemetry JSON lines to Phase 2 latency logs.")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print a line for each processed record.",
    )
    return parser.parse_args()


def load_events(stream: TextIO) -> Iterable[dict]:
    for raw_line in stream:
        line = raw_line.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON: {line}") from exc
        if not isinstance(payload, dict):
            raise ValueError(f"Expected JSON object per line, got: {line}")
        yield payload


def main() -> None:
    args = parse_args()
    processed = 0

    for event in load_events(sys.stdin):
        batch_id = event.get("batch_id")
        if not isinstance(batch_id, str) or not batch_id:
            raise ValueError(f"Missing batch_id in event: {event}")

        status = event.get("status", "success")
        if not isinstance(status, str):
            status = str(status)

        duration_ms = event.get("duration_ms")
        if duration_ms is not None:
            duration_ms = int(duration_ms)

        timestamp_raw = event.get("timestamp")
        if isinstance(timestamp_raw, str):
            received_at = datetime.fromisoformat(timestamp_raw.replace("Z", "+00:00"))
        else:
            received_at = datetime.now(timezone.utc)

        record_phase_two_telemetry(
            batch_id,
            received_at=received_at,
            duration_ms=duration_ms,
            status=status,
        )
        processed += 1
        if args.verbose:
            print(f"[{status}] {batch_id}")

    if args.verbose:
        print(f"Processed {processed} telemetry events.")


if __name__ == "__main__":
    main()
