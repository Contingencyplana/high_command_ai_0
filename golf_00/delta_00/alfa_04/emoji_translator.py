"""Level-0 emoji chain translator for Major Pivot Five.

Converts glyph sequences such as "🛠️ ⚒️ 🤖 ✅" into structured
payloads Toyfoundry can consume. This module focuses on Level-0
templates and is intentionally deterministic so the toddler-facing
composer can provide instant feedback.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List


@dataclass(frozen=True)
class Glyph:
    category: str
    token: str
    prompt: str


EMOJI_INDEX: Dict[str, Glyph] = {
    "🛠️": Glyph("noun", "actor.forge", "forge"),
    "🌾": Glyph("noun", "actor.field", "field"),
    "🌌": Glyph("noun", "actor.dream", "dream"),
    "🌊": Glyph("noun", "actor.river", "river"),
    "🧱": Glyph("noun", "actor.wall", "wall"),
    "🔥": Glyph("noun", "actor.ember", "ember"),
    "🌱": Glyph("noun", "actor.seed", "seed"),
    "🤖": Glyph("noun", "actor.ally", "ally"),
    "⚒️": Glyph("verb", "verb.craft", "craft"),
    "🚀": Glyph("verb", "verb.launch", "launch"),
    "🌿": Glyph("verb", "verb.grow", "grow"),
    "🛡️": Glyph("verb", "verb.shield", "shield"),
    "🧶": Glyph("verb", "verb.weave", "weave"),
    "🔄": Glyph("verb", "verb.loop", "loop"),
    "📦": Glyph("verb", "verb.deliver", "deliver"),
    "🪄": Glyph("verb", "verb.transmute", "transmute"),
    "⏱️": Glyph("qualifier", "qualifier.tempo", "quick"),
    "💡": Glyph("qualifier", "qualifier.idea", "bright"),
    "🛰️": Glyph("qualifier", "qualifier.signal", "signal"),
    "🧭": Glyph("qualifier", "qualifier.direction", "north"),
    "🔍": Glyph("qualifier", "qualifier.inspect", "scan"),
    "☁️": Glyph("qualifier", "qualifier.cloud", "cloud"),
    "🔒": Glyph("qualifier", "qualifier.safe", "safe"),
    "🎯": Glyph("qualifier", "qualifier.target", "focus"),
    "✅": Glyph("outcome", "outcome.success", "victory"),
    "⚠️": Glyph("outcome", "outcome.risk", "warning"),
    "💤": Glyph("outcome", "outcome.pause", "sleep"),
    "📈": Glyph("outcome", "outcome.gain", "rise"),
    "🌀": Glyph("outcome", "outcome.chaos", "storm"),
    "🌈": Glyph("outcome", "outcome.bless", "blessing"),
    "🧊": Glyph("outcome", "outcome.freeze", "freeze"),
    "🔁": Glyph("outcome", "outcome.repeat", "again"),
}


@dataclass(frozen=True)
class Template:
    name: str
    pattern: Sequence[str]


LEVEL0_TEMPLATES: Sequence[Template] = (
    Template("basic_ritual", ("noun", "verb", "noun", "outcome")),
    Template("guarded_delivery", ("noun", "verb", "qualifier", "noun", "outcome")),
    Template("signal_loop", ("noun", "qualifier", "verb", "outcome")),
    Template("conditional_repeat", ("noun", "verb", "outcome", "outcome")),
)


class TranslationError(ValueError):
    """Raised when a glyph chain cannot be translated."""


def split_chain(chain: Sequence[str] | str) -> List[str]:
    """Return a clean list of emojis from a sequence or whitespace string."""

    if isinstance(chain, str):
        tokens = [glyph for glyph in chain.strip().split() if glyph]
    else:
        tokens = [glyph for glyph in chain if glyph]
    if not tokens:
        raise TranslationError("emoji chain is empty")
    return tokens


def lookup_glyphs(tokens: Sequence[str]) -> List[Glyph]:
    """Resolve raw emoji tokens to glyph definitions."""

    resolved = []
    for raw in tokens:
        if raw not in EMOJI_INDEX:
            raise TranslationError(f"unknown glyph: {raw}")
        resolved.append(EMOJI_INDEX[raw])
    return resolved


def match_template(glyphs: Sequence[Glyph]) -> Template:
    """Identify the template that fits the glyph category sequence."""

    categories = tuple(g.category for g in glyphs)
    for template in LEVEL0_TEMPLATES:
        if tuple(template.pattern) == categories:
            return template
    raise TranslationError(f"no Level-0 template matches {categories}")


def _strip_prefix(value: str | None) -> str | None:
    if value is None:
        return None
    return value.split(".", 1)[-1]


def _build_summary(spoken: Sequence[str]) -> str:
    if not spoken:
        return "Emoji command dispatched"
    if len(spoken) == 1:
        return spoken[0].capitalize()
    lead = " ".join(spoken[:-1]).capitalize()
    return f"{lead} -> {spoken[-1]}"


def _build_intent(payload: Dict[str, object]) -> Dict[str, object]:
    actor = _strip_prefix(payload.get("actor"))  # type: ignore[arg-type]
    action = _strip_prefix(payload.get("verb"))  # type: ignore[arg-type]
    raw_target = payload.get("target")  # type: ignore[arg-type]
    target = _strip_prefix(raw_target) if isinstance(raw_target, str) else None
    if target is None:
        target = actor or "self"
    raw_outcomes = payload.get("outcomes", [])  # type: ignore[arg-type]
    if not isinstance(raw_outcomes, Sequence):
        raw_outcomes = []
    outcomes = [_strip_prefix(outcome) for outcome in raw_outcomes if isinstance(outcome, str)]
    outcome = next((item for item in outcomes if item), "pending")
    raw_qualifiers = payload.get("qualifiers", [])  # type: ignore[arg-type]
    if not isinstance(raw_qualifiers, Sequence):
        raw_qualifiers = []
    qualifiers = [stripped for stripped in (_strip_prefix(q) for q in raw_qualifiers if isinstance(q, str)) if stripped]
    return {
        "actor": actor or "unbound",
        "action": action or "command",
        "target": target,
        "qualifiers": qualifiers,
        "outcome": outcome,
    }


def _build_telemetry(timestamp: datetime, glyph_count: int, intent: Dict[str, object]) -> Dict[str, object]:
    actor = str(intent.get("actor") or "unbound")
    action = str(intent.get("action") or "command")
    ts_key = timestamp.strftime("%Y%m%dT%H%M%S%f")[:-3] + "Z"
    return {
        "batch_id": f"{actor}-{action}-{ts_key}",
        "ritual": actor,
        "units_processed": glyph_count,
        "status": "success",
        "duration_ms": 0,
    }


def translate_chain(chain: Sequence[str] | str) -> Dict[str, object]:
    """Translate a Level-0 emoji chain into a structured payload."""

    tokens = split_chain(chain)
    glyphs = lookup_glyphs(tokens)
    template = match_template(glyphs)
    dispatched_at = datetime.now(timezone.utc)

    payload: Dict[str, object] = {
        "template": template.name,
        "actor": None,
        "verb": None,
        "target": None,
        "qualifiers": [],
        "outcomes": [],
        "spoken": [g.prompt for g in glyphs],
        "raw": tokens,
    }

    if template.name == "basic_ritual":
        payload["actor"] = glyphs[0].token
        payload["verb"] = glyphs[1].token
        payload["target"] = glyphs[2].token
        payload["outcomes"] = [glyphs[3].token]
    elif template.name == "guarded_delivery":
        payload["actor"] = glyphs[0].token
        payload["verb"] = glyphs[1].token
        payload["qualifiers"] = [glyphs[2].token]
        payload["target"] = glyphs[3].token
        payload["outcomes"] = [glyphs[4].token]
    elif template.name == "signal_loop":
        payload["actor"] = glyphs[0].token
        payload["qualifiers"] = [glyphs[1].token]
        payload["verb"] = glyphs[2].token
        payload["outcomes"] = [glyphs[3].token]
    elif template.name == "conditional_repeat":
        payload["actor"] = glyphs[0].token
        payload["verb"] = glyphs[1].token
        payload["outcomes"] = [glyphs[2].token, glyphs[3].token]
    else:
        raise TranslationError(f"template handler missing: {template.name}")

    spoken = payload["spoken"]  # type: ignore[assignment]
    summary = _build_summary(spoken)
    intent = _build_intent(payload)
    telemetry = _build_telemetry(dispatched_at, len(tokens), intent)

    payload.update(
        {
            "schema": "emoji-runtime@1.0",
            "glyph_chain": tokens,
            "summary": summary,
            "intent": intent,
            "telemetry_stub": telemetry,
            "created_at": dispatched_at.isoformat().replace("+00:00", "Z"),
        }
    )

    return payload


def main() -> None:
    """Simple CLI for manual testing."""

    import argparse
    import json
    import sys

    parser = argparse.ArgumentParser(description="Translate emoji chains to JSON payloads.")
    parser.add_argument("chain", nargs="*", help="Emoji chain (space separated).")
    args = parser.parse_args()

    if not args.chain:
        print("Usage: python emoji_translator.py 🛠️ ⚒️ 🤖 ✅", file=sys.stderr)
        raise SystemExit(1)

    payload = translate_chain(args.chain)
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
