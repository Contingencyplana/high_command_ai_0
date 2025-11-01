"""CLI helper to stamp Alfa Zero Phase 2 telemetry completions.

Cron jobs or Toyfoundry callbacks can invoke this script with a batch_id to
update the latency logs created by the overlay bridge. Example usage:

    python tools/record_phase_two_telemetry.py --batch-id forge-command-20251101T102228Z

Optional flags let you override duration or status if Toyfoundry reports them
explicitly.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone

from golf_00.delta_00.alfa_00.overlay_bridge import record_phase_two_telemetry


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Record telemetry completion for an Alfa Zero batch.")
    parser.add_argument("--batch-id", required=True, help="Batch identifier from the emoji runtime payload.")
    parser.add_argument(
        "--status",
        default="success",
        choices=["success", "failure", "timeout", "pending"],
        help="Telemetry status (default: success).",
    )
    parser.add_argument(
        "--duration-ms",
        type=int,
        default=None,
        help="Optional duration override (milliseconds). When omitted, the script computes elapsed time from dispatch.",
    )
    parser.add_argument(
        "--timestamp",
        default=None,
        help="Optional ISO8601 timestamp for telemetry receipt (default: now, UTC).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    received_at = (
        datetime.fromisoformat(args.timestamp.replace("Z", "+00:00"))
        if args.timestamp
        else datetime.now(timezone.utc)
    )

    record_phase_two_telemetry(
        args.batch_id,
        received_at=received_at,
        duration_ms=args.duration_ms,
        status=args.status,
    )
    print(f"Telemetry recorded for batch {args.batch_id} ({args.status}).")


if __name__ == "__main__":
    main()
