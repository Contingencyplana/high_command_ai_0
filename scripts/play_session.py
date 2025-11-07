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
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in [here.parent] + list(here.parents):
        if (parent / ".git").exists():
            return parent
    return here.parent


def run_sync_loop(
    root: Path,
    stop: threading.Event,
    *,
    interval_s: int = 30,
    log_path: Optional[Path] = None,
) -> None:
    """Periodically run offline sync to export outbox to the hub.

    The sync output can get very noisy; capture it to a log so the interactive
    overlay remains readable.
    """

    sync_script = root / "tools" / "offline_sync_exchange.py"
    if not sync_script.exists():
        return

    if log_path is None:
        log_path = ensure_logs(root) / "play_session_sync.log"

    while not stop.is_set():
        if stop.wait(interval_s):
            break

        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        try:
            result = subprocess.run(
                [sys.executable, str(sync_script)],
                cwd=str(root),
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            if log_path is not None:
                with log_path.open("a", encoding="utf-8") as handle:
                    handle.write(f"=== {timestamp} offline_sync_exchange.py (exit {result.returncode}) ===\n")
                    if result.stdout:
                        handle.write(result.stdout)
                        if not result.stdout.endswith("\n"):
                            handle.write("\n")
                    handle.write("\n")
            if result.returncode != 0:
                print(
                    "⚠️  Offline sync loop encountered an error; see logs/alfa_zero/play_session_sync.log",
                    file=sys.stderr,
                )
        except Exception as exc:
            if log_path is not None:
                with log_path.open("a", encoding="utf-8") as handle:
                    handle.write(f"=== {timestamp} offline_sync_exchange.py — exception: {exc} ===\n\n")


def ensure_logs(root: Path) -> Path:
    logs = root / "logs" / "alfa_zero"
    logs.mkdir(parents=True, exist_ok=True)
    return logs


def main() -> int:
    root = repo_root()
    logs_dir = ensure_logs(root)

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
    sync_thread = threading.Thread(
        target=run_sync_loop,
        args=(root, stop_evt),
        kwargs={"interval_s": 30, "log_path": logs_dir / "play_session_sync.log"},
        daemon=True,
    )
    sync_thread.start()
    print("↻ Offline sync loop logging to logs/alfa_zero/play_session_sync.log", file=sys.stdout)

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

