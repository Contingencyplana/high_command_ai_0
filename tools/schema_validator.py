 """Schema validation utilities for SHAGI message payloads."""

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

# Toyfoundry currently emits factory reports that follow the same shape as field reports.
SCHEMAS["factory-report@1.0"] = {
    "order_id": str,
    "reported_by": str,
    "timestamp_reported": str,
    "status": str,
    "details": str,
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
        raise SchemaValidationError("Payload missing 'schema' attribute")
    schema = SCHEMAS.get(schema_name)
    if schema is None:
        raise SchemaValidationError(f"Unsupported schema '{schema_name}'")
    _validate_fields(payload, schema)


def validate_file(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    validate_payload(data)


def main(file_paths: list[str]) -> int:
    try:
        for file_path in file_paths:
            validate_file(Path(file_path))
            print(f"[schema] {file_path} valid")
    except SchemaValidationError as exc:
        print(f"[schema] validation error: {exc}")
        return 1
    return 0


if __name__ == "__main__":  # pragma: no cover - manual invocation
    import sys

    sys.exit(main(sys.argv[1:]))
