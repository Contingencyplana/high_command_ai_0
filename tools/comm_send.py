"""Ad-hoc Hybrid Send CLI (shadow by default)

Examples:
- python -m tools.comm_send --kind report --payload-file path/to/payload.json
- python -m tools.comm_send --kind ack --payload-inline '{"schema":"signal-ack@1.0",...}' --dry-run
- python -m tools.comm_send --kind ack --payload-file ack.json --write   # writes only if config allows
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from tools.comm_adapter import CommAdapter

try:
    # Optional: validate payloads if requested
    from tools.schema_validator import validate_payload, SchemaValidationError  # type: ignore
except Exception:  # pragma: no cover - validator not critical for CLI availability
    validate_payload = None  # type: ignore
    SchemaValidationError = RuntimeError  # type: ignore


def _iso_now_compact() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def load_payload(args: argparse.Namespace) -> Dict[str, Any]:
    if args.payload_file:
        path = Path(args.payload_file)
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("Payload JSON must be an object at top level")
        return data
    if args.payload_inline:
        data = json.loads(args.payload_inline)
        if not isinstance(data, dict):
            raise ValueError("Inline payload JSON must be an object at top level")
        return data
    raise ValueError("Provide --payload-file or --payload-inline")


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Ad-hoc hybrid send (shadow by default)")
    p.add_argument("--kind", choices=["report", "ack", "order", "note"], default="report")
    p.add_argument("--payload-file", help="Path to a JSON payload file")
    p.add_argument("--payload-inline", help="Inline JSON string for the payload")
    p.add_argument("--trace-id", default=None, help="Trace identifier (default: timestamp)")
    p.add_argument("--validate", action="store_true", help="Validate payload against known schemas before sending")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--dry-run", dest="dry_run", action="store_true", help="Plan only; do not write (default)")
    g.add_argument("--write", dest="dry_run", action="store_false", help="Allow offline write if config permits")
    p.set_defaults(dry_run=True)
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    payload = load_payload(args)

    if args.validate and validate_payload is not None:
        try:
            validate_payload(payload)  # type: ignore[arg-type]
        except SchemaValidationError as exc:  # type: ignore[misc]
            print(f"[schema] validation error: {exc}")
            return 2
        else:
            print("[schema] payload valid")

    trace_id = args.trace_id or _iso_now_compact()
    adapter = CommAdapter()
    out = adapter.send(kind=args.kind, payload=payload, trace_id=trace_id, dry_run=args.dry_run)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    if not args.dry_run and not out.get("offline", {}).get("wrote"):
        print("[info] write not performed (kind not permitted by config or safety)")
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI
    raise SystemExit(main())

