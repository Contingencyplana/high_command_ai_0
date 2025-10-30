# exchange_heartbeat.py — Genesis Offline Mesh Heartbeat
from pathlib import Path
import os, sys, tempfile

def heartbeat():
    exchange = Path(os.getenv("SHAGI_EXCHANGE_PATH", ""))
    if not exchange or not exchange.exists():
        print("🔴 Exchange Offline — SHAGI_EXCHANGE_PATH missing or invalid")
        sys.exit(1)

    # Test write permission safely
    try:
        test_file = exchange / f"heartbeat_test_{os.getpid()}.tmp"
        test_file.write_text("pulse", encoding="utf-8")
        test_file.unlink(missing_ok=True)
        print(f"🟢 Exchange Online — connected to {exchange}")
    except Exception as e:
        print(f"🟠 Exchange Reachable but Unwritable — {exchange}")
        print(f"   Details: {e}")

if __name__ == "__main__":
    heartbeat()
