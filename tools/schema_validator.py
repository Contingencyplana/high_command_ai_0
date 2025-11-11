"""Schema validation utilities for SHAGI message payloads.

Notes
- Not all JSON files under `exchange/` are payloads (e.g., `ledger/index.json`,
  example configs, attachment snippets). These may legitimately lack a
  top‑level `schema` field. The validator skips such files rather than failing
  the validation run, while still enforcing schemas for real payloads.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Mapping

SCHEMAS: Dict[str, Dict[str, type]] = {
    "high-command-order@1.0": {
        "order_id": str,
        "issued_by": str,
        "target": str,
        "priority": str,
        "timestamp_issued": str,
        "summary": str,
        "directives": list,
        "requires_ack": bool,
    },
    "factory-order@1.0": {
        "order_id": str,
        "issued_by": str,
        "target": str,
        "priority": str,
        "timestamp_issued": str,
        "summary": str,
        "directives": list,
        "requires_ack": bool,
    },
    "field-report@1.0": {
        "report_id": str,
        "origin": str,
        "relates_to": str,
        "timestamp_submitted": str,
        "status": str,
        "summary": str,
    },
    "signal-ack@1.0": {
        "ack_id": str,
        "referenced_id": str,
        "sender": str,
        "receiver": str,
        "timestamp_sent": str,
        "status": str,
    },
}

# Toyfoundry/HC factory reports: shared minimal fields; summary/details optional.
SCHEMAS["factory-report@1.0"] = {
    "order_id": str,
    "reported_by": str,
    "timestamp_reported": str,
    "status": str,
}

SCHEMAS["emoji-runtime@1.0"] = {
    "schema": str,
    "summary": str,
    "glyph_chain": list,
    "spoken": list,
    "raw": list,
    "intent": dict,
    "telemetry_stub": dict,
    "created_at": str,
}

# Frontline feedback payloads
SCHEMAS["frontline-feedback@1.0"] = {
    # top-level 'schema' is already required by validate_payload
    "submitted_at": str,
    "workspace": str,
    "operator": str,
    "responses": dict,
}

SCHEMAS["frontline-feedback-summary@1.0"] = {
    # summary artifact generated from multiple frontline-feedback entries
    "generated_at": str,
    "responses": int,
    "ranking": list,
    "music_support": dict,
    "ritual_dependency": dict,
    "sample_notes": list,
}

# Factory acknowledgement for orders
SCHEMAS["factory-ack@1.0"] = {
    "order_id": str,
    "workspace": str,
    "acknowledged_by": str,
    "owner": str,
    "timestamp_ack": str,
    "status": str,
}

# Safety multi-approver approval record
SCHEMAS["safety-approval@1.0"] = {
    "approval_id": str,
    "referenced_id": str,
    "sender": str,
    "receiver": str,
    "timestamp_sent": str,
    "approvers": list,
    "notes": list,
}


class SchemaValidationError(RuntimeError):
    """Raised when a payload fails schema validation."""


def _validate_fields(payload: Mapping[str, object], schema: Mapping[str, type]) -> None:
    for field, expected in schema.items():
        if field not in payload:
            raise SchemaValidationError(f"Missing required field '{field}'")
        value = payload[field]
        if not isinstance(value, expected):
            raise SchemaValidationError(
                f"Field '{field}' expected {expected.__name__}, got {type(value).__name__}"
            )


def validate_payload(payload: Mapping[str, object]) -> None:
    schema_name = payload.get("schema")
    if not schema_name:
        # Non‑payload JSON (e.g., index/config/attachments) — skip validation
        raise SchemaValidationError("__SKIP__: no 'schema' field (non-payload)")
    schema = SCHEMAS.get(schema_name)
    if schema is None:
        raise SchemaValidationError(f"Unsupported schema '{schema_name}'")
    _validate_fields(payload, schema)
    # Factory report may include either 'summary' or 'details'. Accept either.
    if schema_name == "factory-report@1.0":
        if "summary" not in payload and "details" not in payload:
            raise SchemaValidationError("Factory report requires 'summary' or 'details'")


def validate_file(path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    try:
        validate_payload(data)
    except SchemaValidationError as exc:
        msg = str(exc)
        if msg.startswith("__SKIP__"):
            return "skip"
        raise
    return "ok"


def main(file_paths: list[str]) -> int:
    errors = 0
    for file_path in file_paths:
        path = Path(file_path)
        try:
            result = validate_file(path)
        except SchemaValidationError as exc:
            errors += 1
            print(f"[schema] validation error: {file_path}: {exc}")
        else:
            if result == "ok":
                print(f"[schema] {file_path} valid")
            else:
                print(f"[schema] {file_path} skipped (no schema)")
    return 0 if errors == 0 else 1


if __name__ == "__main__":  # pragma: no cover - manual invocation
    import sys

    sys.exit(main(sys.argv[1:]))
