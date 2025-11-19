# pyright: reportMissingImports=false

from __future__ import annotations

import importlib
import io
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
MODULE_DIR = ROOT_DIR / "golf_00" / "delta_00" / "alfa_00"
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

alfa_zero_ui = importlib.import_module("golf_00.delta_00.alfa_00.alfa_zero_ui")
storyboard_runner = importlib.import_module("golf_00.delta_00.alfa_00.storyboard_runner")

UIContext = alfa_zero_ui.UIContext
execute_storyboard_run = alfa_zero_ui.execute_storyboard_run
NIGHTLANDS_DUET_STORYBOARD = storyboard_runner.NIGHTLANDS_DUET_STORYBOARD
StoryboardGuardrailError = storyboard_runner.StoryboardGuardrailError
StoryboardRunResult = storyboard_runner.StoryboardRunResult
run_storyboard = storyboard_runner.run_storyboard


class DummyBridge:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.calls: list[dict[str, object]] = []
        self._counter = 0

    def dispatch_cell(self, cell, **kwargs):  # type: ignore[no-untyped-def]
        self._counter += 1
        extra = kwargs.get("extra_payload") or {}
        overlays = kwargs.get("overlays") or []
        payload_dir = self.repo_root / "outbox" / "orders" / "emoji_runtime"
        payload_dir.mkdir(parents=True, exist_ok=True)
        destination = payload_dir / f"payload_{self._counter}.json"
        payload = {
            "chain_name": f"storyboard_{self._counter}",
            "template": "nightlands_duet",
            "outcomes": ["ok"],
            "overlay_id": kwargs.get("overlay_id"),
            "overlay_layer": kwargs.get("layer_kind"),
            "overlays": [
                {"overlay_id": oid, "layer_kind": kind} for oid, kind in overlays
            ],
            "trace_id": kwargs.get("trace_id"),
        }
        if isinstance(extra, dict):
            payload.update(extra)
        with destination.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False)
        self.calls.append({
            "cell": cell,
            "kwargs": kwargs,
            "destination": destination,
        })
        return destination


def test_run_storyboard_writes_metadata(tmp_path: Path):
    bridge = DummyBridge(tmp_path)
    moment = datetime(2025, 11, 12, 9, 0, tzinfo=timezone.utc)

    result = run_storyboard(
        bridge,
        NIGHTLANDS_DUET_STORYBOARD,
        lore_enabled=True,
        music_enabled=True,
        now=moment,
    )

    assert result.storyboard_id == NIGHTLANDS_DUET_STORYBOARD.storyboard_id
    assert len(result.payload_paths) == len(NIGHTLANDS_DUET_STORYBOARD.steps)
    assert result.trace_id
    assert result.force is False

    first_call = bridge.calls[0]
    extra_payload = first_call["kwargs"].get("extra_payload")  # type: ignore[index]
    assert isinstance(extra_payload, dict)
    assert extra_payload["storyboard_sequence"] == 1
    assert extra_payload["storyboard_total_steps"] == len(NIGHTLANDS_DUET_STORYBOARD.steps)

    log_path = tmp_path / "logs" / "alfa_zero" / "storyboards" / "nightlands_duet_v1_runs.jsonl"
    assert log_path.exists()
    record = json.loads(log_path.read_text(encoding="utf-8").strip().splitlines()[-1])
    assert record["storyboard_id"] == NIGHTLANDS_DUET_STORYBOARD.storyboard_id
    assert record["force"] is False
    assert record["cooldown_seconds"] == NIGHTLANDS_DUET_STORYBOARD.cooldown_seconds


def test_run_storyboard_enforces_cooldown(tmp_path: Path):
    bridge = DummyBridge(tmp_path)
    start = datetime(2025, 11, 12, 9, 0, tzinfo=timezone.utc)
    run_storyboard(
        bridge,
        NIGHTLANDS_DUET_STORYBOARD,
        lore_enabled=True,
        music_enabled=True,
        now=start,
    )

    with pytest.raises(StoryboardGuardrailError):
        run_storyboard(
            bridge,
            NIGHTLANDS_DUET_STORYBOARD,
            lore_enabled=True,
            music_enabled=True,
            now=start + timedelta(minutes=5),
        )

    forced = run_storyboard(
        bridge,
        NIGHTLANDS_DUET_STORYBOARD,
        lore_enabled=True,
        music_enabled=True,
        now=start + timedelta(minutes=5),
        force=True,
    )
    assert forced.force is True


def test_execute_storyboard_run_appends_metrics(tmp_path: Path, monkeypatch):
    payload_dir = tmp_path / "outbox" / "orders" / "emoji_runtime"
    payload_dir.mkdir(parents=True, exist_ok=True)
    common_fields = {
        "chain_name": "nightlands_step",
        "template": "nightlands_duet",
        "outcomes": ["ok"],
        "storyboard_id": NIGHTLANDS_DUET_STORYBOARD.storyboard_id,
        "storyboard_total_steps": len(NIGHTLANDS_DUET_STORYBOARD.steps),
    }
    payload_specs = [
        {
            "storyboard_step": "Lore Invocation",
            "storyboard_sequence": 1,
            "overlays": [{"overlay_id": "outland-lore-v1", "layer_kind": "lore"}],
        },
        {
            "storyboard_step": "Duet Crescendo",
            "storyboard_sequence": 2,
            "overlays": [
                {"overlay_id": "outland-lore-v1", "layer_kind": "lore"},
                {"overlay_id": "outland-music-v1", "layer_kind": "music"},
            ],
        },
        {
            "storyboard_step": "Twilight Strategy",
            "storyboard_sequence": 3,
            "overlays": [
                {"overlay_id": "outland-lore-v1", "layer_kind": "lore"},
                {"overlay_id": "outland-music-v1", "layer_kind": "music"},
            ],
        },
        {
            "storyboard_step": "Counter Pulse",
            "storyboard_sequence": 4,
            "overlays": [
                {"overlay_id": "outland-lore-v1", "layer_kind": "lore"},
                {"overlay_id": "outland-music-v1", "layer_kind": "music"},
            ],
        },
    ]
    payload_paths: list[Path] = []
    for index, spec in enumerate(payload_specs, start=1):
        payload_path = payload_dir / f"payload_{index}.json"
        payload_path.write_text(
            json.dumps(
                {
                    **common_fields,
                    "storyboard_step": spec["storyboard_step"],
                    "storyboard_sequence": spec["storyboard_sequence"],
                    "overlay_id": "outland-lore-v1",
                    "overlay_layer": "lore",
                    "overlays": spec["overlays"],
                    "trace_id": "trace-nightlands",
                }
            ),
            encoding="utf-8",
        )
        payload_paths.append(payload_path)

    log_path = tmp_path / "logs" / "alfa_zero" / "storyboards" / "nightlands_duet_v1_runs.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.touch()

    result = StoryboardRunResult(
        storyboard_id=NIGHTLANDS_DUET_STORYBOARD.storyboard_id,
        trace_id="trace-nightlands",
        payload_paths=payload_paths,
        log_path=log_path,
        recorded_at=datetime.now(timezone.utc),
        force=False,
    )

    monkeypatch.setattr(
        "golf_00.delta_00.alfa_00.alfa_zero_ui.run_storyboard_sequence",
        lambda *args, **kwargs: result,
    )

    telemetry_path = tmp_path / "telemetry.jsonl"
    metrics_path = tmp_path / "session_metrics.jsonl"
    action_log_path = tmp_path / "actions.log"
    telemetry_path.parent.mkdir(parents=True, exist_ok=True)

    context = UIContext(
        bridge=DummyBridge(tmp_path),
        telemetry_path=telemetry_path,
        emit_events=False,
        event_stream=None,
        output_stream=io.StringIO(),
    )
    context.metrics_path = metrics_path
    context.action_log_path = action_log_path
    context.session_id = "session-test"
    context.session_start_ts = datetime.now(timezone.utc)
    context.lore_layer_enabled = True
    context.music_layer_enabled = True

    execute_storyboard_run(context)

    assert context.dispatch_count == len(payload_paths)
    assert context.selected == NIGHTLANDS_DUET_STORYBOARD.steps[-1].cell
    assert metrics_path.exists()

    records = [json.loads(line) for line in metrics_path.read_text(encoding="utf-8").splitlines() if line]
    events = {record["event"] for record in records}
    assert "storyboard_run" in events
    dispatch_records = [record for record in records if record["event"] == "dispatch"]
    assert len(dispatch_records) == len(payload_paths)
    expected_sequences = set(range(1, len(payload_paths) + 1))
    for dispatch_record in dispatch_records:
        assert dispatch_record["storyboard_id"] == NIGHTLANDS_DUET_STORYBOARD.storyboard_id
        assert dispatch_record["storyboard_sequence"] in expected_sequences

    storyboard_record = next(record for record in records if record["event"] == "storyboard_run")
    assert storyboard_record["payload_count"] == len(payload_paths)
    assert storyboard_record["force"] is False

    action_log_contents = action_log_path.read_text(encoding="utf-8")
    assert "storyboard nightlands_duet_v1" in action_log_contents
    assert telemetry_path.exists()
