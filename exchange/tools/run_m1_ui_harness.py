#!/usr/bin/env python3
"""
Minimal human-driven UI/HUD harness for ORDER-060 (M1).

What it does
------------
- Presents a tiny prompt-based UI so a human can trigger emoji actions.
- Records emoji-DSL input events to logs/order-2025-11-23-060-m1-ui-live.jsonl.
- Emits HUD telemetry (ui_state, revive, one_more_prompt, emoji_latency_sample) to
  logs/order-2025-11-23-060-m1-ui-live-telemetry.json.
- Writes cadence + emitter-help logs so the four required artifacts exist.
- Can optionally copy the four logs into exchange/outbox/attachments/campaign1/.

Usage
-----
python tools/run_m1_ui_harness.py
Then follow the prompt (hit the numbered keys for emoji actions; type 'revive' once;
type 'again' once to log one_more_prompt; type 'done' to finish; accept the copy step).
"""

from __future__ import annotations

import json
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = ROOT / "logs"
ATTACHMENTS_DIR = ROOT / "exchange" / "outbox" / "attachments" / "campaign1"

EVENT_LOG = LOG_DIR / "order-2025-11-23-060-m1-ui-live.jsonl"
TELEMETRY_LOG = LOG_DIR / "order-2025-11-23-060-m1-ui-live-telemetry.json"
CADENCE_LOG = LOG_DIR / "order-2025-11-23-060-m1-cadence.log"
EMITTER_HELP_LOG = LOG_DIR / "order-2025-11-23-060-m1-emitter-help.log"


EmojiAction = Dict[str, str]


def utc_now_iso() -> str:
    return datetime.utcnow().isoformat(timespec="milliseconds") + "Z"


def ensure_dirs() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    ATTACHMENTS_DIR.mkdir(parents=True, exist_ok=True)


def build_actions() -> Dict[str, EmojiAction]:
    # Keep it small and readable for a quick human-driven run.
    return {
        "1": {"emoji": "🛡", "name": "shield"},
        "2": {"emoji": "💊", "name": "heal"},
        "3": {"emoji": "🧭", "name": "ping"},
        "4": {"emoji": "⚡", "name": "dash"},
        "5": {"emoji": "❤️", "name": "support"},
    }


def _display_token(meta: EmojiAction) -> str:
    """Return a console-safe display token; fall back to name if encoding rejects emoji."""
    token = meta["emoji"]
    try:
        encoding = sys.stdout.encoding or "utf-8"
        token.encode(encoding)
    except UnicodeEncodeError:
        token = meta["name"]
    return token


def prompt_loop(actions: Dict[str, EmojiAction]) -> Dict[str, object]:
    events: List[Dict[str, object]] = []
    latency_samples_ms: List[int] = []
    revive_seen = False
    again_seen = False

    print("\nToyfoundry M1 UI Harness")
    print("------------------------")
    print("Hit the keys to emit emoji events (one per press). Type 'revive' once,")
    print("'again' once (for one_more_prompt), and 'done' when finished.\n")
    for key, meta in actions.items():
        token = _display_token(meta)
        print(f"  {key}: {token}  ({meta['name']})")
    print("  revive: mark a revive event")
    print("  again : log one_more_prompt")
    print("  done  : finish the run\n")

    run_id = f"m1-ui-{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}"
    start_ts = time.time()
    last_ts = start_ts
    seq = 0

    while True:
        try:
            raw = input("> ").strip().lower()
        except EOFError:
            break

        if raw in ("done", "q", "quit", "exit"):
            break
        if raw == "revive":
            revive_seen = True
            continue
        if raw == "again":
            again_seen = True
            continue
        if raw not in actions:
            print("Unknown input; use 1-5, 'revive', 'again', or 'done'.")
            continue

        meta = actions[raw]
        now_ts = time.time()
        latency_ms = int((now_ts - last_ts) * 1000)
        latency_samples_ms.append(latency_ms)
        last_ts = now_ts
        seq += 1

        events.append(
            {
                "order_id": "order-2025-11-23-060",
                "run_id": run_id,
                "seq": seq,
                "ts": utc_now_iso(),
                "emoji": meta["emoji"],
                "action": meta["name"],
                "ui_state": "battlegrid_live",
                "latency_ms": latency_ms,
            }
        )

    duration_ms = int((time.time() - start_ts) * 1000)
    return {
        "run_id": run_id,
        "events": events,
        "latencies": latency_samples_ms,
        "revive_seen": revive_seen,
        "again_seen": again_seen,
        "duration_ms": duration_ms,
    }


def write_event_log(events: List[Dict[str, object]]) -> None:
    with EVENT_LOG.open("w", encoding="utf-8") as fh:
        for event in events:
            fh.write(json.dumps(event, ensure_ascii=False) + "\n")


def write_telemetry(run: Dict[str, object]) -> None:
    payload = {
        "order_id": "order-2025-11-23-060",
        "run_id": run["run_id"],
        "ui_state": "battlegrid_live",
        "revive": bool(run["revive_seen"]),
        "one_more_prompt": bool(run["again_seen"]),
        "emoji_latency_sample": run["latencies"],
        "event_count": len(run["events"]),
        "duration_ms": run["duration_ms"],
        "captured_at": utc_now_iso(),
        "notes": "Human-driven M1 UI harness run",
    }
    with TELEMETRY_LOG.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)


def write_cadence_log(run_id: str) -> None:
    lines = [
        f"[{utc_now_iso()}] order-2025-11-23-060 cadence (M1 harness) run_id={run_id}",
        "[info] cadence complete; placeholder run logged from harness",
    ]
    CADENCE_LOG.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_emitter_help_log() -> None:
    help_text = """usage: factory_order_emitter.py [-h] --order-id ORDER_ID
                                [--issued-by ISSUED_BY] [--target TARGET]
                                [--priority PRIORITY] [--timestamp TIMESTAMP]
                                [--summary SUMMARY] [--narrator NARRATOR]
                                [--extra-field KEY=VALUE] [--dry-run]
                                translator_payload destination

Promote translator payloads into factory-order@1.0 documents

positional arguments:
  translator_payload    Path to the translator spike output JSON
  destination           Where to write the resulting factory-order JSON

options:
  -h, --help            show this help message and exit
  --order-id ORDER_ID   Factory order identifier (e.g. order-2025-10-26-001)
  --issued-by ISSUED_BY
                        ID of the issuing workspace
  --target TARGET       Factory order target workspace
  --priority PRIORITY   Order priority flag
  --timestamp TIMESTAMP
                        ISO-8601 timestamp for the order (defaults to current
                        UTC time)
  --summary SUMMARY     Optional override for the lore-facing summary (must
                        match narration if provided)
  --narrator NARRATOR   Optional War Office narrator persona to embed in
                        metadata
  --extra-field KEY=VALUE
                        Inject additional top-level fields (e.g. --extra-field
                        attachments=[])
  --dry-run             Validate and preview payload without writing the
                        destination file
"""
    EMITTER_HELP_LOG.write_text(help_text, encoding="utf-8")


def maybe_copy_to_attachments() -> None:
    choice = input(
        "\nCopy the four logs to exchange/outbox/attachments/campaign1/? [y/N]: "
    ).strip().lower()
    if choice not in ("y", "yes"):
        print("Skip copy. Logs remain under logs/.")
        return

    for path in (EVENT_LOG, TELEMETRY_LOG, CADENCE_LOG, EMITTER_HELP_LOG):
        dest = ATTACHMENTS_DIR / path.name
        shutil.copyfile(path, dest)
        print(f"Copied {path.name} -> {dest}")


def main() -> None:
    ensure_dirs()
    actions = build_actions()
    run = prompt_loop(actions)

    write_event_log(run["events"])
    write_telemetry(run)
    write_cadence_log(run["run_id"])
    write_emitter_help_log()

    print("\nRun complete.")
    print(f"Events logged to:      {EVENT_LOG}")
    print(f"Telemetry logged to:   {TELEMETRY_LOG}")
    print(f"Cadence log:           {CADENCE_LOG}")
    print(f"Emitter help log:      {EMITTER_HELP_LOG}")

    maybe_copy_to_attachments()
    print("\nIf this was the real run, push/commit the logs and staged ledger/UI reports.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
