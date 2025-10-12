"""Utility filters for Forge templates."""

from __future__ import annotations

from typing import Any


def ensure_lower(value: Any) -> str:
    """Return a lowercase string representation."""
    return str(value).lower()
