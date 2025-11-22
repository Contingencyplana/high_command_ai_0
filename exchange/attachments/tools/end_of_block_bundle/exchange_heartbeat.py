"""ASCII-safe heartbeat for the offline exchange hub.

Resolves hub path with precedence:
- env SHAGI_EXCHANGE_PATH
- exchange/config.json.upstream_root
- default C:/Users/Admin/high_command_exchange
"""
from pathlib import Path
import os
import sys
import json


DEFAULT_HUB = Path("C:/Users/Admin/high_command_exchange")


def _load_hub(repo_root: Path) -> Path:
    env = os.getenv("SHAGI_EXCHANGE_PATH")
    if env:
        return Path(env)
    cfg = repo_root / "exchange" / "config.json"
    try:
        data = json.loads(cfg.read_text(encoding="utf-8"))
        upstream = data.get("upstream_root") if isinstance(data, dict) else None
        if isinstance(upstream, str) and upstream.strip():
            return Path(upstream)
    except Exception:
        pass
    return DEFAULT_HUB


def heartbeat() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    exchange = _load_hub(repo_root)
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
