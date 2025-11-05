import os
from pathlib import Path
from tempfile import TemporaryDirectory


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
    spec.loader.exec_module(module)  # type: ignore[attr-defined]

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

