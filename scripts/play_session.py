"""Play Session launcher for Alfa Zero overlay.

Runs the interactive overlay UI with telemetry logging enabled and a
background sync loop to push outbox artifacts to the exchange hub.

Usage:
  python scripts/play_session.py

Environment:
  OVERLAY_AUTO_PROMOTE_FACTORY_ORDERS=1 (default)
  SHAGI_EXCHANGE_PATH can point to the shared exchange hub.
"""

from __future__ import annotations

import os
import subprocess
import sys
import threading
import time
from pathlib import Path


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in [here.parent] + list(here.parents):
        if (parent / ".git").exists():
            return parent
    return here.parent


def run_sync_loop(root: Path, stop: threading.Event, interval_s: int = 15) -> None:
    """Periodically run offline sync to export outbox to the hub."""

    sync_script = root / "tools" / "offline_sync_exchange.py"
    if not sync_script.exists():
        return
    while not stop.is_set():
        try:
            subprocess.run([sys.executable, str(sync_script)], cwd=str(root), check=False)
        except Exception:
            pass
        stop.wait(interval_s)


def ensure_logs(root: Path) -> Path:
    logs = root / "logs" / "alfa_zero"
    logs.mkdir(parents=True, exist_ok=True)
    return logs


def main() -> int:
    root = repo_root()
    ensure_logs(root)

    # Heartbeat (best effort)
    heartbeat = root / "tools" / "exchange_heartbeat.py"
    if heartbeat.exists():
        try:
            subprocess.run([sys.executable, str(heartbeat)], cwd=str(root), check=False)
        except Exception:
            pass

    # Telemetry file for overlay UI
    telemetry_path = root / "logs" / "alfa_zero" / "overlay_events.jsonl"

    # Default-on factory promotion
    env = os.environ.copy()
    env.setdefault("OVERLAY_AUTO_PROMOTE_FACTORY_ORDERS", "1")

    # Start background sync loop
    stop_evt = threading.Event()
    sync_thread = threading.Thread(target=run_sync_loop, args=(root, stop_evt), daemon=True)
    sync_thread.start()

    # Launch interactive overlay UI in foreground
    ui = root / "golf_00" / "delta_00" / "alfa_00" / "alfa_zero_ui.py"
    if not ui.exists():
        print("Overlay UI not found:", ui, file=sys.stderr)
        stop_evt.set()
        return 1

    try:
        cmd = [sys.executable, str(ui), "--telemetry", str(telemetry_path)]
        return subprocess.call(cmd, cwd=str(ui.parent), env=env)
    finally:
        stop_evt.set()
        # Give thread a moment to exit
        time.sleep(0.2)


if __name__ == "__main__":
    raise SystemExit(main())

