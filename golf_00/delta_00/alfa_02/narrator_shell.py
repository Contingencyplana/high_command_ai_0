"""Narrator shell with comfort toggles and overlay hooks.

Usage:
    python -m golf_00.delta_00.alfa_02.narrator_shell \
        --say "Forge crafts the Ally → Victory" \
        --layer comfort \
        --context overlay-alpha \
        --trace logs/alfa_02/narration_traces.jsonl \
        --comfort-on \
        [--trace-id TRACE]

Emits narrator lines to stdout, captures optional JSONL trace events, and
supports comfort toggles plus overlay context metadata for Order 045.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


class ComfortSettings:
    """Capture comfort toggle state for narration output."""

    def __init__(self, comfort_on: bool, comfort_level: Optional[str]) -> None:
        self.enabled = comfort_on
        self.level = comfort_level or os.getenv("NARRATOR_COMFORT_LEVEL")

    def as_dict(self) -> dict:
        if not self.enabled:
            return {"enabled": False}
        return {"enabled": True, "level": self.level or "standard"}


def _iso_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _build_event(
    say: str,
    layer: str,
    context: Optional[str],
    comfort: ComfortSettings,
    *,
    overlay_id: Optional[str],
    overlay_layer: Optional[str],
) -> dict:
    event = {
        "ts": _iso_now(),
        "type": "narration",
        "line": say,
        "layer": layer,
        "context": context or "default",
        "comfort": comfort.as_dict(),
        "source": "alfa_02:narrator_shell",
    }
    if overlay_id:
        event["overlay_id"] = overlay_id
    if overlay_layer:
        event["overlay_layer"] = overlay_layer
    return event


def run(
    say: str,
    layer: str,
    context: Optional[str],
    trace: Optional[Path],
    comfort: ComfortSettings,
    trace_id: Optional[str] = None,
    overlay_id: Optional[str] = None,
    overlay_layer: Optional[str] = None,
) -> None:
    if comfort.enabled and comfort.level:
        print(f"[comfort:{comfort.level}] {say}")
    else:
        print(say)
    if trace:
        trace.parent.mkdir(parents=True, exist_ok=True)
        event = _build_event(
            say,
            layer,
            context,
            comfort,
            overlay_id=overlay_id,
            overlay_layer=overlay_layer,
        )
        if trace_id:
            event["trace_id"] = trace_id
        with trace.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False) + "\n")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Narrator shell with overlay hooks")
    parser.add_argument("--say", required=True, help="Narration line to emit")
    parser.add_argument(
        "--layer",
        default="comfort",
        choices=["comfort", "diagnostic", "debug"],
        help="Narration layer to tag the event",
    )
    parser.add_argument(
        "--context",
        help="Overlay interaction context identifier (e.g. overlay-alpha)",
    )
    parser.add_argument(
        "--trace",
        type=Path,
        help="Optional JSONL path to append enriched narration events",
    )
    parser.add_argument(
        "--comfort-on",
        action="store_true",
        help="Enable comfort narration framing (prefixes output and tags trace)",
    )
    parser.add_argument(
        "--comfort-level",
        choices=["standard", "gentle", "excited"],
        help="Override comfort intensity level (defaults to env or standard)",
    )
    parser.add_argument(
        "--trace-id",
        help="Optional correlation identifier to include in narration traces",
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
    args = parser.parse_args(argv)
    comfort = ComfortSettings(args.comfort_on, args.comfort_level)
    run(
        args.say,
        args.layer,
        args.context,
        args.trace,
        comfort,
        args.trace_id,
        overlay_id=args.overlay_id,
        overlay_layer=args.overlay_layer,
    )
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI
    raise SystemExit(main())

