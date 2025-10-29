# offline_sync_exchange.py — High Command offline sync bridge
# Mirrors outbox/orders and outbox/reports into the shared high_command_exchange hub.

import os
import shutil
from pathlib import Path

EXCHANGE = Path(os.getenv("SHAGI_EXCHANGE_PATH", "C:/Users/Admin/high_command_exchange"))

def sync_local(src_workspace: str):
    """
    Copy any files from <workspace>/outbox/orders and /outbox/reports
    into the shared high_command_exchange/ directory.
    """
    for folder in ["orders", "reports"]:
        src = Path(src_workspace) / "outbox" / folder
        dst = EXCHANGE / folder
        if not src.exists():
            print(f"[WARN] No {folder} folder found in outbox: {src}")
            continue

        dst.mkdir(parents=True, exist_ok=True)
        for f in src.glob("*"):
            if f.is_file():
                shutil.copy2(f, dst)
                print(f"Copied {f.name} -> {dst}")
    print("✅ Local exchange sync complete.")


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    workspace_root = here.parent
    sync_local(str(workspace_root))
