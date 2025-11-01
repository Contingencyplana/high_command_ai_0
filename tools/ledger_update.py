"""Ledger updater — records receipts and completion after pulls.

Updates exchange/ledger/index.json based on files present on disk:
- Reports under exchange/reports/{inbox,archived}/order-*-report.json
- Acks under exchange/acknowledgements/logged/order-*-ack.json
- Orders under exchange/orders/{completed,dispatched}/order-*.json

Status rules:
- closed: order_path present AND ack_path present AND report_path present
- received: report_path present (but not all of the above)
- acknowledged: ack_path present (but not closed/received)
Leaves existing status otherwise.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Tuple


@dataclass
class Ledger:
    path: Path
    data: Dict[str, dict]

    @property
    def orders(self) -> Dict[str, dict]:
        return self.data.setdefault("orders", {})

    @property
    def reports(self) -> Dict[str, str]:
        return self.data.setdefault("reports", {})

    @property
    def acks(self) -> Dict[str, str]:
        return self.data.setdefault("acks", {})

    def save(self) -> None:
        self.path.write_text(json.dumps(self.data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_ledger(repo_root: Path) -> Ledger:
    ledger_path = repo_root / "exchange" / "ledger" / "index.json"
    data = json.loads(ledger_path.read_text(encoding="utf-8"))
    return Ledger(path=ledger_path, data=data)


def _order_id_from_filename(name: str) -> Optional[str]:
    # Accept patterns: order-YYYY-MM-DD-NNN[-suffix].json
    if not name.startswith("order-") or not name.endswith(".json"):
        return None
    core = name[:-5]  # strip .json
    # drop known suffixes
    for suf in ("-report", "-ack", "-policy-update", "-policy-update-report", "-result"):
        if core.endswith(suf):
            core = core[: -len(suf)]
            break
    return core


def _relpath(repo_root: Path, path: Path) -> str:
    return str(path.relative_to(repo_root / "exchange")).replace("\\", "/") if path.is_relative_to(repo_root / "exchange") else str(path)


def update_ledger(repo_root: Path) -> int:
    ledger = load_ledger(repo_root)
    exchange = repo_root / "exchange"

    changed = 0

    # Index acks
    for f in (exchange / "acknowledgements" / "logged").glob("order-*-ack.json"):
        oid = _order_id_from_filename(f.name)
        if not oid:
            continue
        rel = _relpath(repo_root, f)
        key = f"{oid}-ack"
        if ledger.acks.get(key) != rel:
            ledger.acks[key] = rel
            changed += 1
        entry = ledger.orders.setdefault(oid, {"status": "acknowledged"})
        if entry.get("ack_path") != rel:
            entry["ack_path"] = rel
            changed += 1

    # Index reports (inbox + archived)
    for bucket in ("inbox", "archived"):
        for f in (exchange / "reports" / bucket).glob("order-*-report.json"):
            oid = _order_id_from_filename(f.name)
            if not oid:
                continue
            rel = _relpath(repo_root, f)
            key = f"{oid}-report"
            if ledger.reports.get(key) != rel:
                ledger.reports[key] = rel
                changed += 1
            entry = ledger.orders.setdefault(oid, {"status": "received"})
            if entry.get("report_path") != rel:
                entry["report_path"] = rel
                changed += 1

    # Link orders (completed > dispatched preference)
    for state in ("completed", "dispatched"):
        for f in (exchange / "orders" / state).glob("order-*.json"):
            oid = _order_id_from_filename(f.name)
            if not oid:
                continue
            rel = _relpath(repo_root, f)
            entry = ledger.orders.setdefault(oid, {"status": "received"})
            if entry.get("order_path") != rel:
                entry["order_path"] = rel
                changed += 1

    # Recompute statuses
    for oid, entry in list(ledger.orders.items()):
        order_path = entry.get("order_path")
        ack_path = entry.get("ack_path")
        report_path = entry.get("report_path")

        new_status = entry.get("status")
        if order_path and ack_path and report_path:
            new_status = "closed"
        elif report_path:
            new_status = "received"
        elif ack_path:
            new_status = "acknowledged"
        if new_status != entry.get("status"):
            entry["status"] = new_status
            changed += 1

    if changed:
        ledger.save()
    return changed


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    n = update_ledger(root)
    print(f"[OK] Ledger updated, {n} change(s).")

