"""Adapters that promote emoji-runtime payloads into factory-order commands.

This bridge lets High Command feed the emoji composer output into the
Toyfoundry/Toysoldiers pipelines that expect the long-lived
``factory-order@1.0`` schema. The adapter keeps the original emoji payload
embedded so downstream fronts can audit provenance while still receiving a
schema-compliant order envelope.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Sequence

EMOJI_RUNTIME_SCHEMA = "emoji-runtime@1.0"
FACTORY_ORDER_SCHEMA = "factory-order@1.0"


class EmojiRuntimeAdapterError(ValueError):
    """Raised when an emoji-runtime payload cannot be promoted."""


def _ensure_timestamp(value: object | None) -> str:
    if isinstance(value, str) and value:
        return value
    now = datetime.now(timezone.utc)
    return now.isoformat().replace("+00:00", "Z")


def _summarise_qualifiers(qualifiers: Sequence[str] | None) -> str:
    if not qualifiers:
        return "none"
    return ", ".join(qualifiers)


def _summarise_outcome(intent: Dict[str, Any]) -> str:
    primary = intent.get("outcome", "pending")
    secondary = intent.get("secondary_outcome")
    if secondary:
        return f"{primary} / {secondary}"
    return str(primary)


def _resolve_glyph_chain(payload: Dict[str, Any]) -> Sequence[str]:
    glyph_chain = payload.get("glyph_chain")
    if isinstance(glyph_chain, Sequence):
        return list(glyph_chain)  # type: ignore[list-item]
    raw = payload.get("raw")
    if isinstance(raw, Sequence):
        return list(raw)  # type: ignore[list-item]
    return []


def emoji_runtime_to_factory_order(
    payload: Dict[str, Any],
    *,
    order_id: str,
    issued_by: str,
    target: str,
    priority: str = "medium",
    requires_ack: bool = False,
) -> Dict[str, Any]:
    """Convert an emoji-runtime payload into a factory-order envelope."""

    if payload.get("schema") != EMOJI_RUNTIME_SCHEMA:
        raise EmojiRuntimeAdapterError("payload does not use emoji-runtime@1.0 schema")

    intent = payload.get("intent")
    if not isinstance(intent, dict):
        raise EmojiRuntimeAdapterError("emoji-runtime payload missing intent block")

    timestamp_issued = _ensure_timestamp(payload.get("created_at"))
    glyph_chain = _resolve_glyph_chain(payload)
    glyph_chain_text = " ".join(glyph_chain)

    actor = intent.get("actor", "unknown")
    action = intent.get("action", "command")
    command_target = intent.get("target") or target
    raw_qualifiers = intent.get("qualifiers")
    qualifiers_list = list(raw_qualifiers) if isinstance(raw_qualifiers, Sequence) else []
    qualifier_text = _summarise_qualifiers(qualifiers_list)
    outcome_text = _summarise_outcome(intent)

    telemetry = payload.get("telemetry_stub") if isinstance(payload.get("telemetry_stub"), dict) else None

    detail_lines = [
        f"Actor {actor} executes {action} targeting {command_target}.",
        f"Qualifiers: {qualifier_text}. Outcome: {outcome_text}.",
    ]
    if glyph_chain_text:
        detail_lines.append(f"Glyph chain: {glyph_chain_text}.")
    if telemetry:
        batch_id = telemetry.get("batch_id", "n/a")
        status = telemetry.get("status", "unknown")
        detail_lines.append(f"Telemetry batch {batch_id} status {status}.")

    directive = {
        "step": 1,
        "action": action,
        "details": " ".join(detail_lines),
    }

    order = {
        "schema": FACTORY_ORDER_SCHEMA,
        "order_id": order_id,
        "issued_by": issued_by,
        "target": target,
        "priority": priority,
        "timestamp_issued": timestamp_issued,
        "summary": payload.get("summary", "Emoji runtime command"),
        "directives": [directive],
        "requires_ack": requires_ack,
        "extensions": {
            "emoji_runtime_payload": payload,
        },
    }

    return order


def derive_order_id(chain_name: str, created_at: str | None) -> str:
    """Generate a reproducible factory-order ID from chain metadata."""

    safe_name = "".join(ch if ch.isalnum() else "-" for ch in chain_name.lower() or "command")
    timestamp = created_at.replace(":", "").replace("-", "") if created_at else None
    if timestamp:
        timestamp = timestamp.replace("T", "").replace("Z", "")
    else:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"emoji-{safe_name}-{timestamp}"
