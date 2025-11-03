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
from factory_adapter import derive_order_id, emoji_runtime_to_factory_order


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
    """Write a payload JSON file to the emoji runtime outbox.

    The default outbox mirrors Offline Continuity Mode expectations by writing
    to ``outbox/orders/emoji_runtime`` within the repository. This ensures the
    standard heartbeat → ledger → sync loop can pick up the files before they
    travel across the shared mesh.
    """

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
    parser.add_argument(
        "--emit-factory-orders",
        action="store_true",
        help="Also promote emoji-runtime payloads to factory-order@1.0 and write them to the factory outbox.",
    )
    parser.add_argument(
        "--factory-outbox",
        default=None,
        help="Override directory for generated factory orders (default: outbox/orders/factory_orders).",
    )
    parser.add_argument(
        "--factory-issued-by",
        default="high_command_ai_0",
        help="Value for the issued_by field in factory orders (default: high_command_ai_0).",
    )
    parser.add_argument(
        "--factory-target",
        default="toyfoundry_ai_0",
        help="Value for the target field in factory orders (default: toyfoundry_ai_0).",
    )
    parser.add_argument(
        "--factory-priority",
        default="medium",
        help="Priority to set on emitted factory orders (default: medium).",
    )
    parser.add_argument(
        "--factory-requires-ack",
        action="store_true",
        help="Set requires_ack=true on emitted factory orders.",
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
        outbox_dir = repo_root / "outbox" / "orders" / "emoji_runtime"

    if args.emit_factory_orders:
        if args.factory_outbox:
            factory_outbox = Path(args.factory_outbox)
            if not factory_outbox.is_absolute():
                factory_outbox = repo_root / factory_outbox
        else:
            factory_outbox = repo_root / "outbox" / "orders" / "factory_orders"
    else:
        factory_outbox = None

    chains = load_sample_chains(sample_path)

    successes = []
    failures = []

    for name, chain in chains.items():
        try:
            payload = translate_chain(chain)
            payload["chain_name"] = name
            payload["source"] = "golf_00/delta_00/alfa_04/dispatch_sample_chains.py"
            destination = write_payload(outbox_dir, name, payload)
            successes.append((name, destination))

            if factory_outbox is not None:
                order_id = derive_order_id(name, payload.get("created_at"))
                factory_order = emoji_runtime_to_factory_order(
                    payload,
                    order_id=order_id,
                    issued_by=args.factory_issued_by,
                    target=args.factory_target,
                    priority=args.factory_priority,
                    requires_ack=args.factory_requires_ack,
                )
                factory_path = write_payload(factory_outbox, order_id, factory_order)
                successes.append((f"{name} [factory-order]", factory_path))
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
