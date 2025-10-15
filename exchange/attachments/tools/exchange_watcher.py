"""Utilities for surfacing new exchange artefacts.

This watcher is meant to reduce manual polling of the exchange by
recording the last-seen state and printing deltas for pending orders,
pending acknowledgements, and inbox reports. It relies on the shared
directory layout used by both High Command and field theatres.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional


# Workspace root is the parent of the tools/ folder where this file lives
# Example: C:\Users\Admin\toyfoundry_ai_0\tools\exchange_watcher.py
# parents[1] resolves to C:\Users\Admin\toyfoundry_ai_0
ROOT = Path(__file__).resolve().parents[1]
EXCHANGE_ROOT = ROOT / "exchange"
STATE_PATH = ROOT / "logs" / "exchange_watcher_state.json"


class ExchangeWatcherError(RuntimeError):
    """Raised when the watcher cannot recover from an error."""


@dataclass
class Entry:
    identifier: str
    path: Path
    summary: Optional[str]
    timestamp: Optional[str]

    def to_snapshot(self) -> Mapping[str, str]:
        data = {
            "id": self.identifier,
            "path": str(self.path),
        }
        if self.summary:
            data["summary"] = self.summary
        if self.timestamp:
            data["timestamp"] = self.timestamp
        return data


Snapshot = Dict[str, Dict[str, Mapping[str, str]]]


CATEGORIES = {
    "orders_pending": {
        "path": EXCHANGE_ROOT / "orders" / "pending",
        "id_field": "order_id",
        "summary_field": "summary",
        "timestamp_field": "timestamp_issued",
        "label": "Pending orders",
    },
    "acks_pending": {
        "path": EXCHANGE_ROOT / "acknowledgements" / "pending",
        "id_field": "order_id",
        "summary_field": "workspace",
        "timestamp_field": "timestamp_requested",
        "label": "Pending acknowledgements",
    },
    "reports_inbox": {
        "path": EXCHANGE_ROOT / "reports" / "inbox",
        "id_field": "report_id",
        "summary_field": "summary",
        "timestamp_field": "timestamp_sent",
        "label": "Inbox reports",
    },
}


def load_snapshot(path: Path = STATE_PATH) -> Snapshot:
    if not path.exists():
        return {name: {} for name in CATEGORIES.keys()}
    content = json.loads(path.read_text(encoding="utf-8"))
    snapshot: Snapshot = {name: dict(content.get(name, {})) for name in CATEGORIES.keys()}
    return snapshot


def save_snapshot(snapshot: Snapshot, path: Path = STATE_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload: Dict[str, Dict[str, Mapping[str, str]]] = {
        name: dict(entries) for name, entries in snapshot.items()
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def scan_category(category_name: str) -> Dict[str, Mapping[str, str]]:
    config = CATEGORIES[category_name]
    root = config["path"]
    results: Dict[str, Mapping[str, str]] = {}
    if not root.exists():
        return results
    for candidate in sorted(root.glob("*.json")):
        try:
            data = json.loads(candidate.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            identifier = candidate.stem
            results[identifier] = {
                "id": identifier,
                "path": str(candidate),
                "summary": "<unreadable>",
            }
            continue
        identifier = str(data.get(config["id_field"], candidate.stem))
        summary = data.get(config["summary_field"]) or None
        timestamp = data.get(config["timestamp_field"]) or None
        entry = Entry(identifier=identifier, path=candidate, summary=summary, timestamp=timestamp)
        results[identifier] = dict(entry.to_snapshot())
    return results


def collect_snapshot() -> Snapshot:
    snapshot: Snapshot = {}
    for category in CATEGORIES.keys():
        snapshot[category] = scan_category(category)
    return snapshot


def compute_changes(previous: Snapshot, current: Snapshot) -> Dict[str, Dict[str, List[str]]]:
    changes: Dict[str, Dict[str, List[str]]] = {}
    for category in CATEGORIES.keys():
        before = set(previous.get(category, {}).keys())
        after = set(current.get(category, {}).keys())
        changes[category] = {
            "added": sorted(after - before),
            "removed": sorted(before - after),
        }
    return changes


def format_entry(identifier: str, info: Mapping[str, str]) -> str:
    summary = info.get("summary")
    timestamp = info.get("timestamp")
    details: List[str] = [identifier]
    if summary:
        details.append(f"- {summary}")
    if timestamp:
        details.append(f"[{timestamp}]")
    return " ".join(details)


def render_changes(changes: Dict[str, Dict[str, List[str]]], snapshot: Snapshot, quiet: bool) -> int:
    emitted = 0
    for category, delta in changes.items():
        added = delta["added"]
        removed = delta["removed"]
        label = CATEGORIES[category]["label"]
        if added:
            print(f"[exchange] New {label.lower()} detected:")
            for identifier in added:
                print(f"  - {format_entry(identifier, snapshot[category][identifier])}")
                emitted += 1
        if removed:
            print(f"[exchange] {label} cleared:")
            for identifier in removed:
                print(f"  - {identifier}")
                emitted += 1
    if emitted == 0 and not quiet:
        print("[exchange] No changes since last check.")
    return emitted


def process_once(quiet: bool = False) -> None:
    if not EXCHANGE_ROOT.exists():
        raise ExchangeWatcherError(f"Exchange directory missing at {EXCHANGE_ROOT}")
    previous = load_snapshot() if not args.reset else {name: {} for name in CATEGORIES.keys()}  # type: ignore[name-defined]
    current = collect_snapshot()
    changes = compute_changes(previous, current)
    emitted = render_changes(changes, current, quiet=quiet)
    if emitted == 0 and not STATE_PATH.exists():
        for category, data in current.items():
            if not data:
                continue
            label = CATEGORIES[category]["label"]
            print(f"[exchange] Current {label.lower()}:")
            for identifier, info in data.items():
                print(f"  - {format_entry(identifier, info)}")
    save_snapshot(current)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Surface new exchange artefacts")
    parser.add_argument("--watch", action="store_true", help="Poll continuously for changes")
    parser.add_argument("--interval", type=float, default=30.0, help="Polling interval when --watch is enabled")
    parser.add_argument("--quiet", action="store_true", help="Suppress \"no changes\" messages")
    parser.add_argument("--reset", action="store_true", help="Clear the stored watcher state before running")
    return parser


def main(argv: Optional[Iterable[str]] = None) -> int:
    global args
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.watch:
        import time
        try:
            while True:
                process_once(quiet=args.quiet)
                time.sleep(args.interval)
        except KeyboardInterrupt:
            return 130
    else:
        process_once(quiet=args.quiet)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
