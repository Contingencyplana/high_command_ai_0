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


def test_dispatch_includes_trace_id(tmp_path: Path, monkeypatch):
    import importlib.util
    from pathlib import Path as _Path
    import sys

    monkeypatch.setenv("OVERLAY_AUTO_PROMOTE_FACTORY_ORDERS", "0")

    here = _Path(__file__).resolve()
    root = next((p for p in [here.parent] + list(here.parents) if (p / ".git").exists()), here.parent)
    bridge_path = root / "golf_00" / "delta_00" / "alfa_00" / "overlay_bridge.py"
    spec = importlib.util.spec_from_file_location("overlay_bridge", bridge_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    bridge_module_path = str(bridge_path.parent)
    cleanup_path = False
    if bridge_module_path not in sys.path:
        sys.path.insert(0, bridge_module_path)
        cleanup_path = True
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)  # type: ignore[attr-defined]
    finally:
        if cleanup_path:
            sys.path.remove(bridge_module_path)
        sys.modules.pop(spec.name, None)

    outbox_dir = tmp_path / "emoji_payloads"
    outbox_dir.mkdir(parents=True, exist_ok=True)
    bridge = module.build_bridge(str(outbox_dir))

    cell = next(iter(module.CELL_MAPPINGS))
    trace_id = "trace-test-0001"
    destination = bridge.dispatch_cell(cell, trace_id=trace_id)

    payload = json.loads(destination.read_text(encoding="utf-8"))
    assert payload.get("trace_id") == trace_id
    stub = payload.get("telemetry_stub") or {}
    assert stub.get("trace_id") == trace_id


def test_factory_order_receives_trace_id():
    from golf_00.delta_00.alfa_04 import emoji_translator, factory_adapter

    chain = ("🛠️", "⚒️", "🤖", "✅")
    payload = emoji_translator.translate_chain(chain)
    trace_id = "trace-factory-77"
    payload["trace_id"] = trace_id
    stub = payload.get("telemetry_stub")
    if isinstance(stub, dict):
        stub["trace_id"] = trace_id

    order = factory_adapter.emoji_runtime_to_factory_order(
        payload,
        order_id="emoji-basic-0001",
        issued_by="test",
        target="toyfoundry_ai_0",
        priority="standard",
        requires_ack=False,
    )

    directives = order.get("directives") or []
    assert directives, "expected directives in factory order"
    details = directives[0].get("details", "")
    assert f"Correlation trace_id: {trace_id}." in details
    extensions = order.get("extensions") or {}
    assert extensions.get("correlation_trace_id") == trace_id

