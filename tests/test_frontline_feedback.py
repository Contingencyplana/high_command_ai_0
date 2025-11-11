from __future__ import annotations

from pathlib import Path

from tools.frontline_feedback import build_response, load_schema, write_response
from tools.frontline_feedback_summary import (
    compute_signal,
    load_feedback_entries,
    render_report,
)


def test_build_and_store_feedback(tmp_path: Path) -> None:
    schema = load_schema()
    response = build_response(
        schema=schema,
        workspace="genesis-alpha",
        operator="operator-01",
        layer_focus="music",
        experience_rating=5,
        music_support="boosts",
        ritual_dependency="independent",
        note="Music helps onboarding.",
        submitted_at="2025-11-11T12:00:00Z",
    )
    destination = write_response(response, tmp_path)
    stored = destination.read_text(encoding="utf-8")
    assert "frontline-feedback@1.0" in stored
    assert "Music helps onboarding." in stored


def test_summary_ranking(tmp_path: Path) -> None:
    schema = load_schema()
    first = build_response(
        schema=schema,
        workspace="genesis-alpha",
        operator="operator-01",
        layer_focus="music",
        experience_rating=5,
        music_support="boosts",
        ritual_dependency="independent",
        note="Music unlocks tempo.",
        submitted_at="2025-11-11T12:00:00Z",
    )
    second = build_response(
        schema=schema,
        workspace="genesis-beta",
        operator="operator-02",
        layer_focus="lore",
        experience_rating=4,
        music_support="neutral",
        ritual_dependency="critical",
        note="Ritual still anchors the line.",
        submitted_at="2025-11-11T12:05:00Z",
    )
    write_response(first, tmp_path)
    write_response(second, tmp_path)

    entries = load_feedback_entries(tmp_path)
    signal = compute_signal(entries)
    assert signal.responses == 2
    assert signal.music_support["boosts"] == 1
    ranking = signal.ranking()
    assert ranking[0]["layer"] == "music"

    report = render_report(signal, entries, generated_at="2025-11-11T12:10:00Z")
    assert report["responses"] == 2
    assert report["sample_notes"]
    assert report["ranking"][0]["score"] >= report["ranking"][1]["score"]
