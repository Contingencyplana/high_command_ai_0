"""Factory order emission bridge for Toyfoundry.

This utility converts translator spike outputs (emoji glyph chains,
intent metadata, telemetry stubs, narration summary) into canonical
``factory-order@1.0`` payloads ready for the exchange.

The script safeguards the shared alignment rules captured in
``quint_synced/payload_alignment.md`` and ``quint_synced/narration_alignment.md``.
It performs lightweight validation to catch schema drift early, and it
ensures the lore-facing ``summary`` matches the narration line so the
War Office can plug in voice assets without further edits.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Sequence

QUINT_SYNCED_DIR = Path("quint_synced")
PAYLOAD_ALIGNMENT_PATH = QUINT_SYNCED_DIR / "payload_alignment.md"
NARRATION_ALIGNMENT_PATH = QUINT_SYNCED_DIR / "narration_alignment.md"

FACTORY_SCHEMA = "factory-order@1.0"


class PayloadValidationError(RuntimeError):
    """Raised when the translator payload cannot be promoted."""


@dataclass
class TranslatorPayload:
    """Normalised view over translator output."""

    summary: str
    glyph_chain: Sequence[str]
    intent: Mapping[str, Any]
    telemetry_stub: Mapping[str, Any]
    narration_line: str | None
    narration_beats: Sequence[str] | None
    raw: Mapping[str, Any]


def _load_json(path: Path) -> MutableMapping[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))  # type: ignore[return-value]
    except json.JSONDecodeError as exc:  # pragma: no cover - IO guard
        raise PayloadValidationError(f"Malformed JSON: {path}: {exc}") from exc


def _ensure_sequence(value: Any, field: str) -> Sequence[Any]:
    if not isinstance(value, list):
        raise PayloadValidationError(f"Translator payload field '{field}' must be an array")
    return value


def _ensure_mapping(value: Any, field: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise PayloadValidationError(f"Translator payload field '{field}' must be an object")
    return value


def _validate_glyph_chain(chain: Sequence[Any]) -> List[str]:
    glyphs: List[str] = []
    for index, item in enumerate(chain):
        if not isinstance(item, str):
            raise PayloadValidationError(f"glyph_chain[{index}] must be a string emoji glyph")
        if not item.strip():
            raise PayloadValidationError(f"glyph_chain[{index}] cannot be empty")
        glyphs.append(item)
    if not glyphs:
        raise PayloadValidationError("glyph_chain cannot be empty")
    return glyphs


def _validate_telemetry_stub(stub: Mapping[str, Any]) -> Mapping[str, Any]:
    required_fields = {
        "batch_id": str,
        "ritual": str,
        "units_processed": int,
        "status": str,
        "duration_ms": int,
    }
    for key, expected_type in required_fields.items():
        if key not in stub:
            raise PayloadValidationError(f"telemetry_stub missing '{key}'")
        value = stub[key]
        if not isinstance(value, expected_type):
            raise PayloadValidationError(
                f"telemetry_stub field '{key}' must be {expected_type.__name__}, found {type(value).__name__}"
            )
        if expected_type is int and value < 0:
            raise PayloadValidationError(f"telemetry_stub field '{key}' must be non-negative")
    return stub


def _normalise_narration(raw_payload: Mapping[str, Any]) -> tuple[str | None, Sequence[str] | None]:
    narration = raw_payload.get("narration")
    if narration is None:
        return None, None
    if isinstance(narration, str):
        return narration, None
    if not isinstance(narration, Mapping):
        raise PayloadValidationError("narration must be either a string or an object")
    # Accept common keys emitted by the spike (line / spoken / beats)
    line = narration.get("line") or narration.get("spoken_line") or narration.get("summary")
    beats = narration.get("beats") or narration.get("spoken")
    if beats is not None and not isinstance(beats, list):
        raise PayloadValidationError("narration.beats must be an array when provided")
    return (line if isinstance(line, str) else None, beats if isinstance(beats, list) else None)


def load_translator_payload(path: Path) -> TranslatorPayload:
    raw = _load_json(path)
    if raw.get("schema") != FACTORY_SCHEMA:
        raise PayloadValidationError(
            f"Translator payload schema must be '{FACTORY_SCHEMA}', found '{raw.get('schema')}'"
        )
    summary = raw.get("summary")
    if not isinstance(summary, str) or not summary.strip():
        raise PayloadValidationError("Translator payload must include non-empty 'summary'")

    glyph_chain = _validate_glyph_chain(_ensure_sequence(raw.get("glyph_chain"), "glyph_chain"))
    intent = _ensure_mapping(raw.get("intent"), "intent")
    telemetry_stub = _validate_telemetry_stub(_ensure_mapping(raw.get("telemetry_stub"), "telemetry_stub"))
    narration_line, narration_beats = _normalise_narration(raw)

    return TranslatorPayload(
        summary=summary.strip(),
        glyph_chain=glyph_chain,
        intent=intent,
        telemetry_stub=telemetry_stub,
        narration_line=narration_line.strip() if narration_line else None,
        narration_beats=narration_beats,
        raw=raw,
    )


def ensure_summary_alignment(payload: TranslatorPayload, override_summary: str | None) -> str:
    summary = override_summary.strip() if override_summary else payload.summary
    if payload.narration_line and payload.narration_line.strip() != summary:
        raise PayloadValidationError(
            "Narration line differs from summary. Update either the translator payload or the override "
            "so the War Office receives a single lore-aligned sentence."
        )
    return summary


def generate_metadata(translator: TranslatorPayload, *, narrator: str | None) -> Dict[str, Any]:
    meta: Dict[str, Any] = {
        "translator_version": translator.raw.get("translator_version", "unknown"),
        "quint_synced_payload_spec": str(PAYLOAD_ALIGNMENT_PATH),
        "quint_synced_narration_spec": str(NARRATION_ALIGNMENT_PATH),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    if narrator:
        meta["narrator_profile"] = narrator
    return meta


def build_factory_order(
    translator: TranslatorPayload,
    *,
    order_id: str,
    issued_by: str,
    target: str,
    priority: str,
    timestamp_issued: str,
    summary_override: str | None,
    narrator: str | None,
    extra_fields: Mapping[str, Any] | None,
) -> Dict[str, Any]:
    summary = ensure_summary_alignment(translator, summary_override)

    payload: Dict[str, Any] = {
        "schema": FACTORY_SCHEMA,
        "order_id": order_id,
        "issued_by": issued_by,
        "target": target,
        "priority": priority,
        "timestamp_issued": timestamp_issued,
        "summary": summary,
        "glyph_chain": list(translator.glyph_chain),
        "intent": dict(translator.intent),
        "telemetry_stub": dict(translator.telemetry_stub),
        "narration": {
            "line": summary,
            "beats": list(translator.narration_beats) if translator.narration_beats else [],
        },
        "attachments": translator.raw.get("attachments", []),
        "metadata": generate_metadata(translator, narrator=narrator),
    }

    if extra_fields:
        for key, value in extra_fields.items():
            if key in payload and payload[key] != value:
                raise PayloadValidationError(f"Cannot override canonical field '{key}' via extra_fields")
            payload[key] = value

    return payload


def write_factory_order(payload: Mapping[str, Any], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Promote translator payloads into factory-order@1.0 documents")
    parser.add_argument("translator_payload", type=Path, help="Path to the translator spike output JSON")
    parser.add_argument("destination", type=Path, help="Where to write the resulting factory-order JSON")
    parser.add_argument("--order-id", required=True, help="Factory order identifier (e.g. order-2025-10-26-001)")
    parser.add_argument("--issued-by", default="toyfoundry_ai_0", help="ID of the issuing workspace")
    parser.add_argument("--target", default="toyfoundry_ai_0", help="Factory order target workspace")
    parser.add_argument("--priority", default="standard", help="Order priority flag")
    parser.add_argument(
        "--timestamp",
        default=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        help="ISO-8601 timestamp for the order (defaults to current UTC time)",
    )
    parser.add_argument(
        "--summary",
        help="Optional override for the lore-facing summary (must match narration if provided)",
    )
    parser.add_argument(
        "--narrator",
        help="Optional War Office narrator persona to embed in metadata",
    )
    parser.add_argument(
        "--extra-field",
        action="append",
        metavar="KEY=VALUE",
        help="Inject additional top-level fields (e.g. --extra-field attachments=[])",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and preview payload without writing the destination file",
    )
    return parser.parse_args(argv)


def _parse_extra_fields(pairs: Iterable[str] | None) -> Dict[str, Any]:
    if not pairs:
        return {}
    extras: Dict[str, Any] = {}
    for pair in pairs:
        if "=" not in pair:
            raise PayloadValidationError(f"Invalid extra-field specification '{pair}'. Expected KEY=JSON_VALUE")
        key, raw_value = pair.split("=", 1)
        try:
            value = json.loads(raw_value)
        except json.JSONDecodeError as exc:
            raise PayloadValidationError(f"extra-field '{key}' must be valid JSON: {exc}") from exc
        extras[key] = value
    return extras


def main(argv: Iterable[str] | None = None) -> int:
    try:
        args = parse_args(argv)
        translator_payload = load_translator_payload(args.translator_payload)
        extras = _parse_extra_fields(args.extra_field)
        payload = build_factory_order(
            translator_payload,
            order_id=args.order_id,
            issued_by=args.issued_by,
            target=args.target,
            priority=args.priority,
            timestamp_issued=args.timestamp,
            summary_override=args.summary,
            narrator=args.narrator,
            extra_fields=extras,
        )
        if args.dry_run:
            print(json.dumps(payload, indent=2))
            print("(dry run) factory-order validated; no file written")
        else:
            write_factory_order(payload, args.destination)
            print(f"factory-order emitted to {args.destination}")
        return 0
    except PayloadValidationError as exc:
        print(f"Emission aborted: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
