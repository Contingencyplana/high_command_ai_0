"""Summarize frontline feedback into a Music vs Ritual ranking note."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INBOX = REPO_ROOT / "exchange" / "reports" / "inbox"
DEFAULT_OUTBOX = REPO_ROOT / "exchange" / "reports" / "outbox"

MUSIC_POSITIVE = {"boosts"}
MUSIC_NEGATIVE = {"conflicts"}
RITUAL_DEPENDENT = {"critical"}
RITUAL_INDEPENDENT = {"independent"}


@dataclass
class AggregatedSignal:
    responses: int
    music_score: float
    ritual_score: float
    music_support: Counter
    ritual_dependency: Counter

    def ranking(self) -> list[dict[str, Any]]:
        ordered = sorted(
            (
                {"layer": "music", "score": self.music_score},
                {"layer": "ritual", "score": self.ritual_score},
            ),
            key=lambda item: item["score"],
            reverse=True,
        )
        return ordered


def _iso_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_feedback(path: Path) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    responses = data.get("responses")
    if not isinstance(responses, dict):
        return None
    return data


def load_feedback_entries(inbox: Path) -> list[dict[str, Any]]:
    if not inbox.exists():
        return []
    entries: list[dict[str, Any]] = []
    for path in sorted(inbox.glob("frontline_feedback_*.json")):
        record = _load_feedback(path)
        if record:
            entries.append(record)
    return entries


def compute_signal(entries: list[dict[str, Any]]) -> AggregatedSignal:
    if not entries:
        return AggregatedSignal(0, 0.0, 0.0, Counter(), Counter())

    total_music = 0.0
    total_ritual = 0.0
    music_counts: Counter = Counter()
    ritual_counts: Counter = Counter()

    for entry in entries:
        responses = entry.get("responses", {})
        rating = float(responses.get("experience_rating", 0))
        layer_focus = responses.get("layer_focus")
        music_support = responses.get("music_support")
        ritual_dependency = responses.get("ritual_dependency")

        music_weight = rating
        ritual_weight = rating

        if layer_focus == "music":
            music_weight += 1.0
        elif layer_focus == "lore":
            ritual_weight += 1.0
        elif layer_focus == "both":
            music_weight += 0.5
            ritual_weight += 0.5

        if music_support in MUSIC_POSITIVE:
            music_weight += 1.0
        elif music_support in MUSIC_NEGATIVE:
            music_weight -= 1.0

        if ritual_dependency in RITUAL_DEPENDENT:
            ritual_weight += 1.0
        elif ritual_dependency in RITUAL_INDEPENDENT:
            ritual_weight -= 1.0

        total_music += max(music_weight, 0.0)
        total_ritual += max(ritual_weight, 0.0)

        if isinstance(music_support, str):
            music_counts[music_support] += 1
        if isinstance(ritual_dependency, str):
            ritual_counts[ritual_dependency] += 1

    responses_total = len(entries)
    music_score = total_music / responses_total
    ritual_score = total_ritual / responses_total
    return AggregatedSignal(responses_total, music_score, ritual_score, music_counts, ritual_counts)


def render_report(signal: AggregatedSignal, entries: list[dict[str, Any]], *, generated_at: str | None = None) -> dict[str, Any]:
    timestamp = generated_at or _iso_now()
    notes: list[str] = []
    for entry in entries:
        responses = entry.get("responses", {})
        note = responses.get("note")
        if isinstance(note, str) and note.strip():
            notes.append(note.strip())

    return {
        "schema": "frontline-feedback-summary@1.0",
        "generated_at": timestamp,
        "responses": signal.responses,
        "ranking": signal.ranking(),
        "music_support": signal.music_support,
        "ritual_dependency": signal.ritual_dependency,
        "sample_notes": notes[:3],
    }


def write_report(report: dict[str, Any], outbox: Path = DEFAULT_OUTBOX) -> Path:
    outbox.mkdir(parents=True, exist_ok=True)
    ts = report.get("generated_at", _iso_now()).replace(":", "").replace("-", "")
    destination = outbox / f"frontline_feedback_summary_{ts}.json"
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return destination


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize frontline feedback notes")
    parser.add_argument("--inbox", type=Path, default=DEFAULT_INBOX, help="Directory with frontline feedback JSON files")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTBOX, help="Directory for summary report")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    entries = load_feedback_entries(args.inbox)
    signal = compute_signal(entries)
    report = render_report(signal, entries)
    destination = write_report(report, args.output)
    print(f"Feedback summary written to {destination}")
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI
    raise SystemExit(main())
