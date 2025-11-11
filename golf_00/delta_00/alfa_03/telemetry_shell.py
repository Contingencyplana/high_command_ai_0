"""Telemetry shell with overlay instrumentation.

Usage:
    python -m golf_00.delta_00.alfa_03.telemetry_shell \
        --event overlay.click \
        --status success \
        --details "Operator selects forge ritual" \
        --trace logs/alfa_03/telemetry.jsonl \
        --overlay overlay-alpha \
        --comfort-state comfort:on

Prints structured telemetry, appends optional JSONL traces, and enriches
records with overlay context for Order 045 validation.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


def _iso_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _comfort_state(override: Optional[str]) -> dict:
    state = override or os.getenv("TELEMETRY_COMFORT_STATE", "comfort:off")
    mode, _, level = state.partition(":")
    return {"mode": mode, "level": level or "standard"}


def _build_record(
    event: str,
    status: str,
    details: Optional[str],
    overlay: Optional[str],
    comfort_state: dict,
    trace_id: Optional[str],
    overlay_id: Optional[str],
    overlay_layer: Optional[str],
    activation_count: Optional[int],
    active_minutes: Optional[float],
    unique_operators: Optional[int],
) -> dict:
    record = {
        "ts": _iso_now(),
        "event": event,
        "status": status,
        "details": details or "",
        "overlay": overlay or "default",
        "comfort": comfort_state,
        "trace_id": trace_id,
        "source": "alfa_03:telemetry_shell",
    }
    if overlay_id:
        record["overlay_id"] = overlay_id
    if overlay_layer:
        record["overlay_layer"] = overlay_layer
    if activation_count is not None:
        record["activation_count"] = int(activation_count)
    if active_minutes is not None:
        record["active_minutes"] = float(active_minutes)
    if unique_operators is not None:
        record["unique_operators"] = int(unique_operators)
    return record


def run(
    event: str,
    status: str,
    details: Optional[str],
    trace: Optional[Path],
    overlay: Optional[str],
    comfort: Optional[str],
    trace_id: Optional[str],
    overlay_id: Optional[str],
    overlay_layer: Optional[str],
    activation_count: Optional[int],
    active_minutes: Optional[float],
    unique_operators: Optional[int],
) -> None:
    record = _build_record(
        event,
        status,
        details,
        overlay,
        _comfort_state(comfort),
        trace_id,
        overlay_id,
        overlay_layer,
        activation_count,
        active_minutes,
        unique_operators,
    )
    print(json.dumps(record, ensure_ascii=False))
    if trace:
        trace.parent.mkdir(parents=True, exist_ok=True)
        with trace.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Telemetry shell with overlay instrumentation")
    parser.add_argument("--event", required=True, help="Event name, e.g. forge.craft")
    parser.add_argument("--status", required=True, choices=["success", "failure", "warning"], help="Status")
    parser.add_argument("--details", help="Optional details string")
    parser.add_argument("--trace", type=Path, help="Optional JSONL path to append events")
    parser.add_argument(
        "--overlay",
        help="Overlay interaction identifier (e.g. overlay-alpha)",
    )
    parser.add_argument(
        "--comfort-state",
        help="Override comfort mode/level (format mode:level; defaults via env)",
    )
    parser.add_argument(
        "--trace-id",
        help="Optional correlation identifier linking narrator + telemetry records",
    )
    parser.add_argument(
        "--overlay-id",
        help="Optional Outland overlay identifier (e.g. outland-lore-v1)",
    )
    parser.add_argument(
        "--overlay-layer",
        choices=["lore", "music", "ritual", "emergent"],
        help="Overlay layer kind when tagging Outlands metadata",
    )
    parser.add_argument(
        "--activation-count",
        type=int,
        help="Number of activations captured by this event",
    )
    parser.add_argument(
        "--active-minutes",
        type=float,
        help="Active minutes represented by this event",
    )
    parser.add_argument(
        "--unique-operators",
        type=int,
        help="Unique operators observed in this interval",
    )
    args = parser.parse_args(argv)
    run(
        args.event,
        args.status,
        args.details,
        args.trace,
        args.overlay,
        args.comfort_state,
        args.trace_id,
        args.overlay_id,
        args.overlay_layer,
        args.activation_count,
        args.active_minutes,
        args.unique_operators,
    )
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI
    raise SystemExit(main())

