from pathlib import Path
import json


def _read_last_jsonl(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8").strip().splitlines()
    assert lines, f"no lines in {path}"
    return json.loads(lines[-1])


def test_emit_overlay_traces(tmp_path: Path):
    # Repo-relative import for the orchestrator
    import importlib.util
    from pathlib import Path as _Path
    here = _Path(__file__).resolve()
    root = next((p for p in [here.parent] + list(here.parents) if (p / ".git").exists()), here.parent)
    flow_path = root / "golf_00" / "delta_00" / "alfa_00" / "overlay_flow.py"
    spec = importlib.util.spec_from_file_location("overlay_flow", flow_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[attr-defined]

    narration_path = tmp_path / "narration.jsonl"
    telemetry_path = tmp_path / "telemetry.jsonl"

    module.emit_overlay_click(
        overlay="overlay-alpha",
        trace_id="test-0001",
        say="Overlay node ready",
        comfort_level="gentle",
        narration_trace=narration_path,
        telemetry_trace=telemetry_path,
    )

    assert narration_path.exists()
    assert telemetry_path.exists()

    narr = _read_last_jsonl(narration_path)
    tele = _read_last_jsonl(telemetry_path)

    # Narration assertions
    assert narr.get("type") == "narration"
    assert narr.get("context") == "overlay-alpha"
    comfort = narr.get("comfort") or {}
    assert comfort.get("enabled") is True
    assert comfort.get("level") == "gentle"

    # Telemetry assertions
    assert tele.get("event") == "overlay.click"
    assert tele.get("status") == "success"
    assert tele.get("overlay") == "overlay-alpha"
    assert tele.get("trace_id") == "test-0001"
    tcomfort = tele.get("comfort") or {}
    assert tcomfort.get("mode") == "comfort"
    assert tcomfort.get("level") == "gentle"

