"""Rebuilds exchange/ledger/index.json by scanning the exchange tree.

Derives order status and paths based on folder placement:
- closed: order in completed/, ack in acknowledgements/logged/, report in reports/archived/
- dispatched: ack present (pending/logged) and report in reports/inbox/
- pending: order only in orders/pending/

Outputs structure:
{
  "version": "1.0.0",
  "orders": { order_id: { status, order_path, ack_path, report_path } },
  "reports": { report_id: path },
  "acks": { ack_id: path }
}

Usage:
  python tools/ledger_indexer.py --write
  python tools/ledger_indexer.py --dry-run
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional


EXCHANGE = Path("exchange")


@dataclass
class OrderEntry:
    order_path: Optional[Path] = None
    ack_path: Optional[Path] = None
    report_path: Optional[Path] = None

    def status(self) -> str:
        # Determine status from where ack/report live
        if self.ack_path and "acknowledgements/logged/" in self._posix(self.ack_path) and self.report_path and "reports/archived/" in self._posix(self.report_path):
            return "closed"
        if self.ack_path and (
            "acknowledgements/pending/" in self._posix(self.ack_path)
            or "acknowledgements/logged/" in self._posix(self.ack_path)
        ) and self.report_path and "reports/inbox/" in self._posix(self.report_path):
            return "dispatched"
        return "pending"

    @staticmethod
    def _posix(p: Path) -> str:
        return p.as_posix()


def rel_to_exchange(p: Path) -> str:
    return p.relative_to(EXCHANGE).as_posix()


def find_orders() -> Dict[str, OrderEntry]:
    orders: Dict[str, OrderEntry] = {}
    # Order paths by precedence for display
    order_dirs = [
        EXCHANGE / "orders" / "completed",
        EXCHANGE / "orders" / "dispatched",
        EXCHANGE / "orders" / "pending",
    ]
    for d in order_dirs:
        if not d.exists():
            continue
        for f in d.glob("order-*.json"):
            order_id = f.stem  # e.g., order-2025-10-15-022
            entry = orders.setdefault(order_id, OrderEntry())
            entry.order_path = f

    # ACKs
    for d in [EXCHANGE / "acknowledgements" / "logged", EXCHANGE / "acknowledgements" / "pending"]:
        if not d.exists():
            continue
        for f in d.glob("order-*-ack.json"):
            ack_id = f.stem  # order-...-ack
            # map back to order_id
            order_id = ack_id[:-4]  # strip '-ack'
            entry = orders.setdefault(order_id, OrderEntry())
            entry.ack_path = f

    # Reports
    for d in [EXCHANGE / "reports" / "archived", EXCHANGE / "reports" / "inbox"]:
        if not d.exists():
            continue
        for f in d.glob("order-*-report.json"):
            report_id = f.stem  # order-...-report
            # map back to order_id
            order_id = report_id[:-7]  # strip '-report'
            entry = orders.setdefault(order_id, OrderEntry())
            entry.report_path = f

    return orders


def build_index() -> dict:
    orders = find_orders()

    orders_map: Dict[str, dict] = {}
    reports_map: Dict[str, str] = {}
    acks_map: Dict[str, str] = {}

    for order_id, entry in orders.items():
        orders_map[order_id] = {
            "status": entry.status(),
            "order_path": rel_to_exchange(entry.order_path) if entry.order_path else None,
            "ack_path": rel_to_exchange(entry.ack_path) if entry.ack_path else None,
            "report_path": rel_to_exchange(entry.report_path) if entry.report_path else None,
        }

        if entry.report_path:
            report_id = f"{order_id}-report"
            reports_map[report_id] = rel_to_exchange(entry.report_path)
        if entry.ack_path:
            ack_id = f"{order_id}-ack"
            acks_map[ack_id] = rel_to_exchange(entry.ack_path)

    return {
        "version": "1.0.0",
        "orders": orders_map,
        "reports": reports_map,
        "acks": acks_map,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Rebuild exchange ledger index from filesystem state")
    parser.add_argument("--write", action="store_true", help="Write to exchange/ledger/index.json")
    parser.add_argument("--dry-run", action="store_true", help="Print to stdout only")
    args = parser.parse_args(argv)

    index = build_index()
    if args.dry_run and not args.write:
        print(json.dumps(index, indent=2))
        return 0

    out_path = EXCHANGE / "ledger" / "index.json"
    out_path.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

