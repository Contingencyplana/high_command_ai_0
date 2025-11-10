"""Utilities for overlay trace correlation identifiers."""

from __future__ import annotations

from datetime import datetime, timezone


def generate_trace_id(cell_label: str, overlay: str = "overlay-alpha") -> str:
    """Return a deterministic correlation ID for an overlay dispatch."""

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"{overlay}-{cell_label}-{timestamp}"
