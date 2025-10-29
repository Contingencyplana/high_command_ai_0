# sync_exchange.py — Offline Exchange bridge for SHAGI workspaces
# ---------------------------------------------------------------
# This script syncs local outbox/orders + outbox/reports into the
# shared high_command_exchange hub (GitHub-independent).

import os
from quint_sync import sync_local

if __name__ == "__main__":
    here = os.path.dirname(__file__)
    workspace_root = os.path.abspath(os.path.join(here, ".."))
    print(f"[SYNC] Connecting workspace at: {workspace_root}")
    sync_local(workspace_root)
    print("[SYNC] Local exchange sync complete.")
