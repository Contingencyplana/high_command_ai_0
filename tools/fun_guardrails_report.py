from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path


def load_events(path: Path, minutes: int):
    if not path.exists():
        return []
    since = datetime.now(timezone.utc) - timedelta(minutes=minutes)
    events = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            if not isinstance(obj, dict):
                continue
            ts_raw = obj.get("ts")
            try:
                ts = datetime.fromisoformat(str(ts_raw).replace("Z", "+00:00"))
            except Exception:
                continue
            if ts >= since:
                events.append(obj)
    return events


def summarize(events):
    by_trigger = Counter()
    by_flag = Counter()
    samples = defaultdict(int)
    for e in events:
        flags = e.get("fun_flags") if isinstance(e.get("fun_flags"), dict) else {}
        flag_key = ",".join(sorted(k for k, v in flags.items() if v)) or "no_flags"
        triggers = e.get("triggers") if isinstance(e.get("triggers"), list) else []
        for t in triggers:
            ttype = str(t.get("type"))
            by_trigger[ttype] += 1
            by_flag[flag_key] += 1
            samples[flag_key] += 1
    return by_trigger, by_flag, samples


def main():
    ap = argparse.ArgumentParser(description="Summarize FUN guardrail events")
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--minutes", type=int, default=60)
    args = ap.parse_args()

    repo = Path(args.repo_root)
    events_path = repo / "logs" / "fun_guardrails" / "events.jsonl"
    events = load_events(events_path, args.minutes)
    by_trigger, by_flag, samples = summarize(events)

    print(f"Window: last {args.minutes} minutes")
    print("Triggers:")
    for t, c in by_trigger.most_common():
        print(f"  - {t}: {c}")
    print("Flags:")
    for k, c in by_flag.most_common():
        print(f"  - {k}: {c}")
    print(f"Total events: {len(events)}")


if __name__ == "__main__":
    main()

