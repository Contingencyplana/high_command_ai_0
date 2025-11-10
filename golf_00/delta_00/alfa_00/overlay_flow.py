"""Overlay flow orchestrator for a first end-to-end interaction.

Wires narrator + telemetry shells with a shared overlay context and optional
correlation ID, appending JSONL traces for both. This supports Order 045's
Directive 2 and provides a simple, testable entrypoint.

Usage (CLI):
    python -m golf_00.delta_00.alfa_00.overlay_flow \
        --overlay overlay-alpha \
        --trace-id overlay-alpha-0001 \
        --say "Overlay node ready" \
        --comfort-level gentle \
        --narration-trace logs/alfa_02/narration_traces.jsonl \
        --telemetry-trace logs/alfa_03/telemetry.jsonl
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

from golf_00.delta_00.alfa_02 import narrator_shell
from golf_00.delta_00.alfa_03 import telemetry_shell


def emit_overlay_click(
    *,
    overlay: str,
    trace_id: Optional[str],
    say: str = "Overlay interaction",
    comfort_level: str = "standard",
    narration_trace: Optional[Path] = None,
    telemetry_trace: Optional[Path] = None,
) -> None:
    """Emit a single overlay click with correlated narration and telemetry.

    - Narration: tagged with overlay `context` and comfort state.
    - Telemetry: includes overlay, comfort, and optional `trace_id`.
    """

    # Narration
    comfort = narrator_shell.ComfortSettings(True, comfort_level)
    narrator_shell.run(
        say=say,
        layer="comfort",
        context=overlay,
        trace=narration_trace,
        comfort=comfort,
        trace_id=trace_id,
    )

    # Telemetry (mode:level format for comfort state)
    telemetry_shell.run(
        event="overlay.click",
        status="success",
        details=f"Operator selects overlay flow: {say}",
        trace=telemetry_trace,
        overlay=overlay,
        comfort=f"comfort:{comfort_level}",
        trace_id=trace_id,
    )


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Emit a single overlay interaction")
    parser.add_argument("--overlay", required=True, help="Overlay context identifier")
    parser.add_argument("--trace-id", help="Optional correlation ID")
    parser.add_argument("--say", default="Overlay node ready", help="Narration line")
    parser.add_argument(
        "--comfort-level",
        choices=["standard", "gentle", "excited"],
        default="standard",
        help="Comfort intensity level",
    )
    parser.add_argument("--narration-trace", type=Path, help="JSONL for narration events")
    parser.add_argument("--telemetry-trace", type=Path, help="JSONL for telemetry events")
    args = parser.parse_args(argv)

    emit_overlay_click(
        overlay=args.overlay,
        trace_id=args.trace_id,
        say=args.say,
        comfort_level=args.comfort_level,
        narration_trace=args.narration_trace,
        telemetry_trace=args.telemetry_trace,
    )
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI
    raise SystemExit(main())

