"""Exchange validator attachment. Copy to tools/ to use in a workspace.

Validates exchange layout vs ledger/index.json:
- pending orders ↔ status=pending and ack in acknowledgements/pending
- dispatched orders ↔ status=dispatched and ack in acknowledgements/logged
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import List


# When copied to <workspace>/tools/, this resolves to the workspace root.
ROOT = Path(__file__).resolve().parents[1]
EXCHANGE = ROOT / "exchange"


def load_index(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"[validator] Missing ledger index at {path}")
        return {}


def check_exists(rel_path: str) -> bool:
    return (EXCHANGE / rel_path).exists()


def main() -> int:
    if not EXCHANGE.exists():
        print(f"[validator] Exchange directory missing at {EXCHANGE}")
        return 2

    index = load_index(EXCHANGE / "ledger" / "index.json")
    orders = index.get("orders", {})
    errors: List[str] = []

    pending_fs = {p.name for p in (EXCHANGE / "orders" / "pending").glob("*.json")}
    dispatched_fs = {p.name for p in (EXCHANGE / "orders" / "dispatched").glob("*.json")}

    for order_id, meta in orders.items():
        status = meta.get("status")
        order_path = meta.get("order_path")
        ack_path = meta.get("ack_path")
        report_path = meta.get("report_path")

        if not order_path or not check_exists(order_path):
            errors.append(f"order {order_id}: order_path missing: {order_path}")
        if report_path and not check_exists(report_path):
            errors.append(f"order {order_id}: report_path missing: {report_path}")
        if ack_path and not check_exists(ack_path):
            errors.append(f"order {order_id}: ack_path missing: {ack_path}")

        filename = Path(order_path or "").name
        if status == "pending" and filename and filename not in pending_fs:
            errors.append(f"order {order_id}: status pending but not in orders/pending")
        if status == "dispatched" and filename and filename not in dispatched_fs:
            errors.append(f"order {order_id}: status dispatched but not in orders/dispatched")

        if status == "pending" and ack_path and "/logged/" in ack_path.replace("\\", "/"):
            errors.append(f"order {order_id}: pending order should not have logged ack path")
        if status == "dispatched" and ack_path and "/pending/" in ack_path.replace("\\", "/"):
            errors.append(f"order {order_id}: dispatched order should not have pending ack path")

    if errors:
        print("[validator] Inconsistencies detected:")
        for e in errors:
            print(f" - {e}")
        return 1
    print("[validator] Exchange looks consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

