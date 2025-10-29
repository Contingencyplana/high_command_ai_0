# offline_sync_exchange.py  —  auto-detects deep exchange tree
from pathlib import Path
import os, shutil

EXCHANGE = Path(os.getenv("SHAGI_EXCHANGE_PATH", "C:/Users/Admin/high_command_exchange"))

def sync_local(workspace_root: str):
    ws = Path(workspace_root)
    # Candidate source roots in order of preference
    roots = [
        ws / "exchange" / "orders" / "outbox",
        ws / "exchange" / "outbox",
    ]
    src_root = next((r for r in roots if r.exists()), None)
    if not src_root:
        print(f"[WARN] No outbox found under {ws}")
        return

    for folder in ["orders", "reports"]:
        src = src_root if folder == "orders" else ws / "exchange" / "reports"
        dst = EXCHANGE / folder
        dst.mkdir(parents=True, exist_ok=True)
        if not src.exists():
            print(f"[WARN] {src} missing; skipping")
            continue
        for f in src.glob("**/*.*"):
            if f.is_file():
                rel = f.relative_to(src)
                shutil.copy2(f, dst / rel)
    print("✅ Local exchange sync complete.")
