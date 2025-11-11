import sys
from pathlib import Path


def test_dispatch_all_mapped_cells(tmp_path: Path, monkeypatch):
    """Smoke test: dispatch all mapped cells into a temp outbox.

    Verifies that the overlay bridge writes emoji payloads for each mapped
    cell. Auto-promotion to factory orders is disabled for isolation.
    """

    # Disable factory promotion for test isolation
    monkeypatch.setenv("OVERLAY_AUTO_PROMOTE_FACTORY_ORDERS", "0")

    # Import bridge lazily (repo-relative import)
    import importlib.util
    from pathlib import Path as _Path

    # Locate repo root by walking up from this file
    here = _Path(__file__).resolve()
    root = next((p for p in [here.parent] + list(here.parents) if (p / ".git").exists()), here.parent)

    bridge_path = root / "golf_00" / "delta_00" / "alfa_00" / "overlay_bridge.py"
    spec = importlib.util.spec_from_file_location("overlay_bridge", bridge_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module

    bridge_module_path = str(bridge_path.parent)
    cleanup_path = False
    if bridge_module_path not in sys.path:
        sys.path.insert(0, bridge_module_path)
        cleanup_path = True

    try:
        spec.loader.exec_module(module)  # type: ignore[attr-defined]
    finally:
        if cleanup_path:
            sys.path.remove(bridge_module_path)
        sys.modules.pop(spec.name, None)

    # Build bridge with a temp outbox directory
    outbox_dir = tmp_path / "emoji_runtime_outbox"
    outbox_dir.mkdir(parents=True, exist_ok=True)
    bridge = module.build_bridge(str(outbox_dir))

    # Dispatch all mapped cells
    assert module.CELL_MAPPINGS, "No mapped cells configured"
    for cell in module.CELL_MAPPINGS.keys():
        destination = bridge.dispatch_cell(cell)
        assert destination.exists(), f"Payload not written for {cell}"
        # Basic JSON sanity
        content = destination.read_text(encoding="utf-8")
        assert content.strip().startswith("{")


def test_ui_stacked_overlays_smoke(tmp_path: Path, monkeypatch):
    """Smoke test: UI path with Lore+Music toggles enabled produces stacked overlays.

    Validates that the UI dispatches with an ordered overlays stack (lore, music),
    primary overlay fields match lore, and the trace_id reflects combined overlays.
    """

    # Disable factory promotion for test isolation
    monkeypatch.setenv("OVERLAY_AUTO_PROMOTE_FACTORY_ORDERS", "0")

    # Repo-relative import for the Alfa Zero UI
    import importlib.util
    from pathlib import Path as _Path

    here = _Path(__file__).resolve()
    root = next((p for p in [here.parent] + list(here.parents) if (p / ".git").exists()), here.parent)

    ui_path = root / "golf_00" / "delta_00" / "alfa_00" / "alfa_zero_ui.py"
    spec = importlib.util.spec_from_file_location("alfa_zero_ui", ui_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    import sys as _sys
    _sys.modules[spec.name] = module
    # Ensure local imports (overlay_bridge, etc.) resolve
    added_path = False
    if str(ui_path.parent) not in _sys.path:
        _sys.path.insert(0, str(ui_path.parent))
        added_path = True
    try:
        spec.loader.exec_module(module)  # type: ignore[attr-defined]
    finally:
        if added_path:
            _sys.path.remove(str(ui_path.parent))
        _sys.modules.pop(spec.name, None)

    # Build UI context with outbox override and both overlays enabled
    outbox_dir = tmp_path / "emoji_runtime_outbox_ui"
    outbox_dir.mkdir(parents=True, exist_ok=True)
    context = module.build_context(
        str(outbox_dir),
        telemetry=None,
        emit_events=False,
        event_stream=None,
        auto_contracts=False,
        lore_enabled=True,
        music_enabled=True,
    )

    # Choose a mapped cell and dispatch via UI helper
    assert module.CELL_MAPPINGS, "No mapped cells configured"
    cell = next(iter(module.CELL_MAPPINGS))
    module.run_single_dispatch(context, cell)

    # Find the most recent payload written to the outbox
    payload_files = sorted(outbox_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    assert payload_files, "UI dispatch did not produce a payload"
    payload_path = payload_files[0]

    # Load and validate overlay metadata
    import json as _json
    payload = _json.loads(payload_path.read_text(encoding="utf-8"))

    overlays = payload.get("overlays")
    assert isinstance(overlays, list) and len(overlays) >= 2, "expected stacked overlays in payload"
    assert overlays[0].get("overlay_id") == "outland-lore-v1"
    assert overlays[0].get("layer_kind") == "lore"
    assert overlays[1].get("overlay_id") == "outland-music-v1"
    assert overlays[1].get("layer_kind") == "music"

    # Primary fields should match the first (lore)
    assert payload.get("overlay_id") == "outland-lore-v1"
    assert payload.get("overlay_layer") == "lore"

    # Trace should reflect combined overlays prefix
    trace_id = payload.get("trace_id") or ""
    assert trace_id.startswith("outland-lore-v1+outland-music-v1-"), f"unexpected trace_id: {trace_id}"
