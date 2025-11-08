"""Rank metadata validator for SHAGI payloads/manifests.

Validates presence and shape of `coords` and `rank_path` fields in JSON files.

Usage:
    python tools/rank_validator.py <file1.json> [file2.json ...]
Exit codes:
    0 = all inputs valid or skipped (no rank metadata present)
    1 = one or more files failed validation
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Mapping


RANK_KEYS = {
    # Officers J–A
    "alfa",
    "bravo",
    "charlie",
    "delta",
    "echo",
    "foxtrot",
    "golf",
    "hotel",
    "india",
    "juliett",
    # Generals P–K
    "kilo",
    "lima",
    "mike",
    "november",
    "oscar",
    "papa",
    # Workspace anchor
    "workspace",
}


def _fail(path: Path, msg: str) -> str:
    return f"[rank] {path}: {msg}"


def _validate_coords(data: Mapping[str, Any]) -> str | None:
    if "coords" not in data:
        return None  # Not all payloads need coords
    coords = data["coords"]
    if not (isinstance(coords, list) and len(coords) == 2 and all(isinstance(n, int) for n in coords)):
        return "coords must be a 2-element list of integers [x, y]"
    x, y = coords
    if x < 0 or y < 0:
        return "coords values must be non-negative"
    return None


def _validate_rank_path(data: Mapping[str, Any]) -> str | None:
    if "rank_path" not in data:
        return None  # Allow files without rank_path
    rp = data["rank_path"]
    if not isinstance(rp, Mapping):
        return "rank_path must be an object"
    for key, value in rp.items():
        if key not in RANK_KEYS:
            return f"rank_path contains unsupported key '{key}'"
        if not isinstance(value, str) or not value.strip():
            return f"rank_path['{key}'] must be a non-empty string"
    return None


def validate_file(path: Path) -> list[str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [_fail(path, f"invalid JSON: {exc}")]

    errors: list[str] = []
    msg = _validate_coords(data)
    if msg:
        errors.append(_fail(path, msg))
    msg = _validate_rank_path(data)
    if msg:
        errors.append(_fail(path, msg))
    return errors


def main(argv: list[str]) -> int:
    if not argv:
        print("Usage: python tools/rank_validator.py <file1.json> [file2.json ...]")
        return 2
    errors: list[str] = []
    for arg in argv:
        path = Path(arg)
        if not path.exists():
            errors.append(_fail(path, "file not found"))
            continue
        if path.suffix.lower() != ".json":
            # Skip non-JSON files quietly
            continue
        errors.extend(validate_file(path))
    if errors:
        print("\n".join(errors))
        return 1
    print("[rank] all inputs valid or skipped")
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI
    raise SystemExit(main(sys.argv[1:]))

