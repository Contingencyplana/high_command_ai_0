# pyright: reportMissingImports=false
from __future__ import annotations

from pathlib import Path
import subprocess
import sys

try:  # pragma: no cover - tooling environment may not resolve pytest for static analysis
    import pytest
except ModuleNotFoundError:  # pragma: no cover
    pytest = None  # type: ignore[assignment]

from tools import offline_sync_exchange
from tools.targeted_sync import run_targeted_sync
from golf_00.delta_00.alfa_00.overlay_bridge import OverlayBridge


@pytest.fixture(autouse=True)
def reset_exchange(tmp_path: Path, monkeypatch):
    destination = tmp_path / "exchange"
    monkeypatch.setattr(offline_sync_exchange, "EXCHANGE", destination)
    return destination


def _seed_workspace(tmp_path: Path) -> Path:
    workspace = tmp_path / "workspace"
    orders = workspace / "outbox" / "orders"
    orders.mkdir(parents=True)
    (orders / "sample.json").write_text("{}", encoding="utf-8")
    return workspace


def test_sync_local_dry_run_skips_copy(tmp_path: Path):
    workspace = _seed_workspace(tmp_path)

    offline_sync_exchange.sync_local(
        str(workspace),
        categories=["orders"],
        latest=1,
        quiet=True,
        dry_run=True,
    )

    destination_file = offline_sync_exchange.EXCHANGE / "orders" / "sample.json"
    assert not destination_file.exists()


def test_targeted_sync_executes_copy_when_confirmed(tmp_path: Path):
    workspace = _seed_workspace(tmp_path)

    run_targeted_sync(
        workspace_root=workspace,
        categories=["orders"],
        orders_subpath=None,
        latest=1,
        quiet=True,
        dry_run=False,
        auto_confirm=True,
    )

    destination_file = offline_sync_exchange.EXCHANGE / "orders" / "sample.json"
    assert destination_file.exists()


def test_targeted_sync_prompt_abort(tmp_path: Path):
    workspace = _seed_workspace(tmp_path)

    def _deny(_: str) -> str:
        return "n"

    result = run_targeted_sync(
        workspace_root=workspace,
        categories=["orders"],
        orders_subpath=None,
        latest=1,
        quiet=True,
        dry_run=False,
        auto_confirm=False,
        input_fn=_deny,
    )

    destination_file = offline_sync_exchange.EXCHANGE / "orders" / "sample.json"
    assert result is False
    assert not destination_file.exists()


def test_overlay_bridge_invokes_targeted_sync(monkeypatch, tmp_path: Path):
    bridge = OverlayBridge(
        repo_root=tmp_path,
        translator=object(),
        sample_chains={},
        outbox=tmp_path,
    )

    recorded: dict[str, object] = {}

    def fake_run(cmd, cwd, capture_output, text):  # type: ignore[no-untyped-def]
        recorded["cmd"] = cmd
        recorded["cwd"] = cwd
        return subprocess.CompletedProcess(cmd, 0, stdout="ok", stderr="")

    monkeypatch.setattr(subprocess, "run", fake_run)

    result = bridge.run_targeted_sync(
        categories=["orders"],
        orders_subpath="emoji_runtime",
        latest=3,
        quiet=False,
        dry_run=True,
        auto_confirm=False,
    )

    assert result.returncode == 0
    cmd = recorded["cmd"]
    assert cmd[:3] == [sys.executable, "-m", "tools.targeted_sync"]
    assert "--category" in cmd
    assert "--orders-subpath" in cmd
    assert "--latest" in cmd
    assert "--no-quiet" in cmd
    assert "--dry-run" in cmd
    assert "--yes" not in cmd
