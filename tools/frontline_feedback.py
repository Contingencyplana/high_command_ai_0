"""Frontline feedback collector for Lore vs Music rollout.

Writes structured survey responses into the exchange inbox so downstream
summaries can rank Music vs Ritual sentiment.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA_PATH = REPO_ROOT / "exchange" / "attachments" / "schemas" / "frontline_feedback.schema.json"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "exchange" / "reports" / "inbox"


@dataclass
class SurveySchema:
    raw: dict[str, Any]

    @property
    def version(self) -> str:
        return str(self.raw.get("schema", "frontline-feedback@1.0"))


class ValidationError(Exception):
    """Raised when CLI input fails schema validation."""


def _iso_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_schema(path: Path = DEFAULT_SCHEMA_PATH) -> SurveySchema:
    if not path.exists():
        raise FileNotFoundError(f"Feedback schema missing at {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "questions" not in data:
        raise ValueError("Feedback schema must define a questions list")
    return SurveySchema(data)


def _validate_choice(value: str, *, options: list[str], field: str) -> str:
    if value not in options:
        allowed = ", ".join(options)
        raise ValidationError(f"{field} must be one of: {allowed}")
    return value


def _validate_rating(value: int, *, lower: int, upper: int, field: str) -> int:
    if value < lower or value > upper:
        raise ValidationError(f"{field} must be between {lower} and {upper}")
    return value


def build_response(
    *,
    schema: SurveySchema,
    workspace: str,
    operator: str,
    layer_focus: str,
    experience_rating: int,
    music_support: str,
    ritual_dependency: str,
    note: str | None,
    submitted_at: str | None = None,
) -> dict[str, Any]:
    questions = {q["id"]: q for q in schema.raw.get("questions", [])}
    layer_q = questions.get("layer_focus", {})
    rating_q = questions.get("experience_rating", {})
    music_q = questions.get("music_support", {})
    ritual_q = questions.get("ritual_dependency", {})
    note_q = questions.get("note", {})

    layer = _validate_choice(layer_focus, options=list(layer_q.get("options", [])), field="layer_focus")
    rating = _validate_rating(
        experience_rating,
        lower=int(rating_q.get("range", [1, 5])[0]),
        upper=int(rating_q.get("range", [1, 5])[1]),
        field="experience_rating",
    )
    music = _validate_choice(music_support, options=list(music_q.get("options", [])), field="music_support")
    ritual = _validate_choice(ritual_dependency, options=list(ritual_q.get("options", [])), field="ritual_dependency")

    if note:
        max_len = int(note_q.get("max_length", 512))
        if len(note) > max_len:
            raise ValidationError(f"note must be <= {max_len} characters")

    timestamp = submitted_at or _iso_now()
    responses: dict[str, Any] = {
        "layer_focus": layer,
        "experience_rating": rating,
        "music_support": music,
        "ritual_dependency": ritual,
    }
    if note:
        responses["note"] = note

    return {
        "schema": schema.version,
        "submitted_at": timestamp,
        "workspace": workspace,
        "operator": operator,
        "responses": responses,
    }


def write_response(payload: dict[str, Any], output_dir: Path = DEFAULT_OUTPUT_DIR) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = payload.get("submitted_at", _iso_now()).replace(":", "").replace("-", "")
    workspace = str(payload.get("workspace", "unknown")).lower().replace(" ", "-")
    filename = f"frontline_feedback_{ts}_{workspace}.json"
    destination = output_dir / filename
    destination.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # Hybrid shadow: plan dual-sink publish without writing online
    try:
        from tools.comm_adapter import CommAdapter

        adapter = CommAdapter()
        trace_id = f"frontline-feedback-{ts}"
        adapter.send(kind="report", payload=payload, trace_id=trace_id, dry_run=True)
    except Exception:
        pass  # shadow is best-effort and must not affect writing
    return destination


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect frontline feedback notes")
    parser.add_argument("--workspace", required=True, help="Workspace or theatre submitting feedback")
    parser.add_argument("--operator", required=True, help="Operator callsign")
    parser.add_argument("--layer-focus", choices=["lore", "music", "both"], required=True)
    parser.add_argument("--experience-rating", type=int, choices=[1, 2, 3, 4, 5], required=True)
    parser.add_argument(
        "--music-support",
        choices=["boosts", "neutral", "conflicts"],
        required=True,
        help="How Music impacts the workflow",
    )
    parser.add_argument(
        "--ritual-dependency",
        choices=["critical", "supportive", "independent"],
        required=True,
        help="How dependent the workflow is on Ritual cadence",
    )
    parser.add_argument("--note", help="Optional 280-character note")
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA_PATH, help="Override path to survey schema")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Where to write the feedback JSON")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    schema = load_schema(args.schema)
    response = build_response(
        schema=schema,
        workspace=args.workspace,
        operator=args.operator,
        layer_focus=args.layer_focus,
        experience_rating=args.experience_rating,
        music_support=args.music_support,
        ritual_dependency=args.ritual_dependency,
        note=args.note,
    )
    destination = write_response(response, args.output_dir)
    print(f"Feedback written to {destination}")
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI
    raise SystemExit(main())
