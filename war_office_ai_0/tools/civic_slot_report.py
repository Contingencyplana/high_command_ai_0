#!/usr/bin/env python3
"""Generate civic slot summaries for war_office_ai_0."""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

def parse_citizen(path: Path) -> dict:
    info: dict[str, str] = {}
    for line in path.read_text(encoding='utf-8').splitlines():
        if ':' not in line:
            continue
        key, value = line.split(':', 1)
        info[key.strip()] = value.strip()
    info['path'] = str(path)
    return info

def main() -> None:
    ap = argparse.ArgumentParser(description="War Office civic slot reporter")
    ap.add_argument('--detail', action='store_true', help='Print each citizen entry')
    ap.add_argument('--export', type=Path, help='Write summary JSON to this path')
    args = ap.parse_args()

    root = Path(__file__).resolve().parents[1] / 'civic_lattice' / 'commonwealth'
    citizens = [parse_citizen(p) for p in root.rglob('citizen_*.md')]

    summary: dict[str, dict[str, object]] = {}
    for entry in citizens:
        guild = entry.get('guild', 'guild_unknown')
        status = entry.get('status', 'unknown')
        aspect = entry.get('aspect', 'unknown')
        bucket = summary.setdefault(guild, {
            'total': 0,
            'active': 0,
            'resting': 0,
            'honored': 0,
            'aspect_counts': defaultdict(int)
        })
        bucket['total'] += 1
        if status in bucket:
            bucket[status] += 1
        if status == 'active':
            bucket['active'] += 0  # already counted, but keeps intent clear
        bucket['aspect_counts'][aspect] += 1

    print(f"Civic lattice contains {len(citizens)} citizens across {len(summary)} guilds.")
    for guild, bucket in sorted(summary.items()):
        aspects = ', '.join(f"{asp}:{count}" for asp, count in sorted(bucket['aspect_counts'].items()))
        print(f"{guild}: total={bucket['total']} resting={bucket['resting']} honored={bucket['honored']} aspects=[{aspects}]")

    if args.detail:
        for entry in citizens:
            print(f"{entry.get('civ_id')} -> {entry.get('guild')} / {entry.get('house')} / {entry.get('cell')} :: {entry.get('status')} :: {entry.get('aspect')} :: {entry.get('paired_workspace')}")

    if args.export:
        serializable = {}
        for guild, bucket in summary.items():
            serializable[guild] = {
                'total': bucket['total'],
                'resting': bucket['resting'],
                'honored': bucket['honored'],
                'aspect_counts': dict(bucket['aspect_counts'])
            }
        args.export.parent.mkdir(parents=True, exist_ok=True)
        args.export.write_text(json.dumps(serializable, indent=2), encoding='utf-8')
        print(f"Summary exported to {args.export}")

if __name__ == '__main__':
    main()
