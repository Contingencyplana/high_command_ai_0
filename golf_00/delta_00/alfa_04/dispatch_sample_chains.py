"""Dispatch sample Level-0 emoji chains into the exchange outbox.

This lightweight harness wires the emoji translator into the
High Command exchange pipeline so we can verify round-trips before
connecting the playable overlay. It consumes the sample chains JSON
and produces payload files under exchange/orders/outbox/emoji_runtime/.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict

from emoji_translator import TranslationError, translate_chain


def find_repo_root(start: Path) -> Path:
    """Locate the repository root by walking upward until .git is found."""

    for parent in [start] + list(start.parents):
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Could not locate repository root (missing .git directory)")


def load_sample_chains(path: Path) -> Dict[str, str]:
    """Load the sample chains JSON file."""

    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("sample chains file must contain an object of name → chain mappings")
    return {str(name): str(chain) for name, chain in data.items()}


def sanitize_name(name: str) -> str:
    """Convert chain names into filesystem-friendly strings."""

    return "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in name)


def write_payload(outbox: Path, name: str, payload: Dict[str, object]) -> Path:
    """Write a payload JSON file to the emoji runtime outbox."""

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    filename = f"{timestamp}_{sanitize_name(name)}.json"
    destination = outbox / filename

    outbox.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return destination


def main() -> None:
    parser = argparse.ArgumentParser(description="Dispatch sample emoji chains to the exchange outbox.")
    parser.add_argument(
        "--input",
        default="sample_chains.json",
        help="Path to the JSON file containing sample chains (default: sample_chains.json next to this script).",
    )
    parser.add_argument(
        "--outbox",
        default=None,
        help="Optional override for the emoji runtime outbox directory.",
    )
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    repo_root = find_repo_root(script_dir)

    sample_path = Path(args.input)
    if not sample_path.is_absolute():
        sample_path = script_dir / sample_path

    if args.outbox:
        outbox_dir = Path(args.outbox)
        if not outbox_dir.is_absolute():
            outbox_dir = repo_root / outbox_dir
    else:
        outbox_dir = repo_root / "exchange" / "orders" / "outbox" / "emoji_runtime"

    chains = load_sample_chains(sample_path)

    successes = []
    failures = []

    for name, chain in chains.items():
        try:
            payload = translate_chain(chain)
            payload.update(
                {
                    "chain_name": name,
                    "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                    "source": "golf_00/delta_00/alfa_04/dispatch_sample_chains.py",
                }
            )
            destination = write_payload(outbox_dir, name, payload)
            successes.append((name, destination))
        except (TranslationError, ValueError) as exc:
            failures.append((name, str(exc)))

    if successes:
        print("✅ Dispatched payloads:")
        for name, path in successes:
            print(f"  - {name}: {path.relative_to(repo_root)}")
    else:
        print("⚠️ No payloads dispatched.")

    if failures:
        print("\n⚠️ Failures:")
        for name, error in failures:
            print(f"  - {name}: {error}")

    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
