"""Utilities for overlay trace correlation identifiers."""

from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime, timezone

def _segment(value: str) -> str:
    cleaned = value.lower().strip()
    safe = [ch if ch.isalnum() or ch in {"-", "_"} else "-" for ch in cleaned]
    return "".join(safe) or "overlay"


def generate_trace_id(
    cell_label: str,
    overlay: str = "overlay-alpha",
    *,
    overlay_id: str | None = None,
    overlays: Sequence[tuple[str, str]] | None = None,
) -> str:
    """Return a deterministic correlation ID for an overlay dispatch.

    When an Outland layer is active, the overlay_id segment is used so that
    traces remain human-readable while matching the metadata captured in
    payloads and telemetry.
    """

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")

    segments: list[str] = []
    if overlays:
        for spec in overlays:
            if not spec:
                continue
            overlay_spec_id = spec[0]
            if overlay_spec_id:
                segments.append(_segment(overlay_spec_id))
    if not segments and overlay_id:
        segments.append(_segment(overlay_id))
    if not segments:
        segments.append(_segment(overlay))

    prefix = "+".join(segments)
    return f"{prefix}-{cell_label}-{timestamp}"
