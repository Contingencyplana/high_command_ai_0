"""ASCII-safe heartbeat for the offline exchange hub."""
from pathlib import Path
import os
import sys


def heartbeat() -> int:
    exchange = Path(os.getenv("SHAGI_EXCHANGE_PATH", ""))
    if not exchange or not exchange.exists():
        print("[ERROR] Exchange Offline - SHAGI_EXCHANGE_PATH missing or invalid")
        return 1

    # Test write permission safely
    try:
        test_file = exchange / f"heartbeat_test_{os.getpid()}.tmp"
        test_file.write_text("pulse", encoding="utf-8")
        test_file.unlink(missing_ok=True)
        print(f"[OK] Exchange Online - connected to {exchange}")
        return 0
    except Exception as e:
        print(f"[WARN] Exchange Reachable but Unwritable - {exchange}")
        print(f"       Details: {e}")
        return 2


if __name__ == "__main__":
    sys.exit(heartbeat())

