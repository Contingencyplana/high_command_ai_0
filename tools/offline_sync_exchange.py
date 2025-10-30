# offline_sync_exchange.py — offline exchange sync for Genesis Mesh
# Works across any workspace; detects and creates missing folders.

import os
import shutil
from pathlib import Path

# Shared hub path
EXCHANGE = Path(os.getenv("SHAGI_EXCHANGE_PATH", "C:/Users/Admin/high_command_exchange"))

def sync_local(workspace_root: str):
    """
    Synchronize outbox/orders and outbox/reports from the current workspace
    into the shared high_command_exchange hub. Creates target folders if missing.
    """
    ws = Path(workspace_root)

    # Define source folders
    source_folders = {
        "orders": ws / "outbox" / "orders",
        "reports": ws / "outbox" / "reports",
    }

    for name, src in source_folders.items():
        dst = EXCHANGE / name
        if not src.exists():
            print(f"[WARN] No {name} folder found in outbox: {src}")
            continue

        # Ensure destination folder exists
        os.makedirs(dst, exist_ok=True)

        files_copied = 0
        for f in src.glob("**/*.*"):
            if f.is_file():
                rel_path = f.relative_to(src)
                dst_file = dst / rel_path
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dst_file)
                print(f"Copied {f} -> {dst_file}")
                files_copied += 1

        if files_copied == 0:
            print(f"[INFO] No new {name} files to sync from {src}")
        else:
            print(f"[OK] Synced {files_copied} {name} file(s) to {dst}")

    print("✅ Local exchange sync complete.")


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    workspace_root = here.parent
    sync_local(str(workspace_root))
