"""Interactive Alfa Zero controller bridging the battlegrid to the emoji translator.

This CLI is a stopgap until the graphical overlay lands. It renders the
16×16 grid from the Alfa Zero spec, allows operators (or scripted callers)
to select cells using hexadecimal coordinates, and dispatches the mapped
emoji chains through the Level-0 translator living in Alfa 04. By default it
also appends ledger entries and runs the heartbeat → sync loop so every
dispatch propagates across the offline mesh. Event streams (JSON lines) from
`alfa_zero_ui.py --emit-events` can be piped in via ``--event-stream`` to share
the same operational cadence.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Tuple, TextIO

from overlay_bridge import CELL_MAPPINGS, OverlayBridge, build_bridge, cell_label
from fun_flags import FunFlags
from pathlib import Path as _PathForWarnings
import json as _json_for_warnings

Cell = Tuple[int, int]

HEX_DIGITS = "0123456789ABCDEF"

# 16×16 battlefield layout copied from docs/alfa_zero_spec.md
GRID_LAYOUT: List[List[str]] = [
    ["🏔️", "🏔️", "🏔️", "🏔️", "⛏️", "⛏️", "⛏️", "⛏️", "📦", "📦", "📦", "📦", "🏭", "🏭", "🏭", "🏭"],
    ["🏔️", "🏔️", "🏔️", "🏔️", "⛏️", "⛏️", "⛏️", "⛏️", "📦", "📦", "📦", "📦", "🏭", "🏭", "🏭", "🏭"],
    ["🏔️", "🏔️", "🏔️", "🏔️", "⛏️", "⛏️", "⛏️", "⛏️", "📦", "📦", "📦", "📦", "🏭", "🏭", "🏭", "🏭"],
    ["🏔️", "🏔️", "🏔️", "🏔️", "⛏️", "⛏️", "⛏️", "⛏️", "📦", "📦", "📦", "📦", "🏭", "🏭", "🏭", "🏭"],
    ["🌾", "🌾", "🌾", "🌾", "👷", "👷", "👷", "👷", "🔨", "🔨", "🔨", "🔨", "⚔️", "⚔️", "⚔️", "⚔️"],
    ["🌾", "🌾", "🌾", "🌾", "👷", "👷", "👷", "👷", "🔨", "🔨", "🔨", "🔨", "⚔️", "⚔️", "⚔️", "⚔️"],
    ["🌾", "🌾", "🌾", "🌾", "👷", "👷", "👷", "👷", "🔨", "🔨", "🔨", "🔨", "⚔️", "⚔️", "⚔️", "⚔️"],
    ["🌾", "🌾", "🌾", "🌾", "👷", "👷", "👷", "👷", "🔨", "🔨", "🔨", "🔨", "⚔️", "⚔️", "⚔️", "⚔️"],
    ["🚢", "🚢", "🚢", "🚢", "📊", "📊", "📊", "📊", "🎯", "🎯", "🎯", "🎯", "✅", "✅", "✅", "✅"],
    ["🚢", "🚢", "🚢", "🚢", "📊", "📊", "📊", "📊", "🎯", "🎯", "🎯", "🎯", "✅", "✅", "✅", "✅"],
    ["🚢", "🚢", "🚢", "🚢", "📊", "📊", "📊", "📊", "🎯", "🎯", "🎯", "🎯", "✅", "✅", "✅", "✅"],
    ["🚢", "🚢", "🚢", "🚢", "📊", "📊", "📊", "📊", "🎯", "🎯", "🎯", "🎯", "✅", "✅", "✅", "✅"],
    ["🔥", "🔥", "🔥", "🔥", "⚠️", "⚠️", "⚠️", "⚠️", "📉", "📉", "📉", "📉", "❌", "❌", "❌", "❌"],
    ["🔥", "🔥", "🔥", "🔥", "⚠️", "⚠️", "⚠️", "⚠️", "📉", "📉", "📉", "📉", "❌", "❌", "❌", "❌"],
    ["🔥", "🔥", "🔥", "🔥", "⚠️", "⚠️", "⚠️", "⚠️", "📉", "📉", "📉", "📉", "❌", "❌", "❌", "❌"],
    ["🔥", "🔥", "🔥", "🔥", "⚠️", "⚠️", "⚠️", "⚠️", "📉", "📉", "📉", "📉", "❌", "❌", "❌", "❌"],
]


@dataclass
class ControllerContext:
    repo_root: Path
    bridge: OverlayBridge
    auto_sync: bool


def render_grid(highlight: Optional[Cell] = None) -> None:
    """Print the 16×16 battlefield with optional highlight."""

    header = "    " + " ".join(HEX_DIGITS)
    print(header)
    for row_index, row in enumerate(GRID_LAYOUT):
        rendered_cells: List[str] = []
        for col_index, emoji in enumerate(row):
            cell = (row_index, col_index)
            if highlight == cell:
                rendered_cells.append(f"[{emoji}]")
            else:
                rendered_cells.append(emoji)
        print(f"{HEX_DIGITS[row_index]}   " + " ".join(rendered_cells))


def list_mapped_cells() -> None:
    """Display the currently wired grid cells and their chain bindings."""

    print("Mapped overlay cells:")
    for cell, (chain, description) in sorted(CELL_MAPPINGS.items()):
        print(f"  - {cell_label(cell)}: {chain} — {description}")


def parse_cell_token(token: str) -> Cell:
    """Parse a cell in formats like '0,4', '04', or '0 4'."""

    cleaned = token.replace(",", " ").strip().upper()
    parts = [part for part in cleaned.split() if part]
    if len(parts) == 2:
        row_token, col_token = parts
    elif len(parts) == 1 and len(parts[0]) == 2:
        row_token, col_token = parts[0][0], parts[0][1]
    else:
        raise ValueError("Provide cell as ROW,COL or ROWCOL using hexadecimal digits (0-F)")

    try:
        row = int(row_token, 16)
        col = int(col_token, 16)
    except ValueError as exc:  # pragma: no cover - defensive
        raise ValueError("Row and column must be hexadecimal digits (0-F)") from exc

    if not (0 <= row <= 15 and 0 <= col <= 15):
        raise ValueError("Row and column must be between 0 and F inclusive")

    return row, col


def dispatch(cell: Cell, ctx: ControllerContext) -> Tuple[str, str]:
    """Invoke the translator for the chosen cell and return payload path and chain."""

    path = ctx.bridge.dispatch_cell(cell)
    chain_name, _ = CELL_MAPPINGS[cell]
    try:
        relative = path.relative_to(ctx.repo_root)
    except ValueError:
        relative = path
    return str(relative), chain_name


def append_ledger_entry(repo_root: Path, cell: Cell, chain_name: str, *, note: Optional[str] = None) -> Path:
    """Append a ledger entry noting the dispatched cell."""

    now = datetime.now(timezone.utc)
    ledger_dir = repo_root / "exchange" / "ledger"
    ledger_dir.mkdir(parents=True, exist_ok=True)
    ledger_path = ledger_dir / f"{now:%Y-%m}.md"
    timestamp = now.strftime("%Y-%m-%d %H:%M")
    summary = f"Alfa Zero controller dispatched {cell_label(cell)} ({chain_name})"
    if note:
        summary = f"{summary} — {note}"
    entry = f"{timestamp} HighCommand OFFLINE-PLAY {summary}\n"
    with ledger_path.open("a", encoding="utf-8") as handle:
        handle.write(entry)
    return ledger_path


def run_sync_commands(repo_root: Path) -> None:
    """Execute heartbeat and sync scripts so payloads reach the exchange."""

    python = Path(sys.executable)
    commands = [
        [python, "tools/exchange_heartbeat.py"],
        [python, "tools/offline_sync_exchange.py"],
    ]
    env = os.environ.copy()
    env.setdefault("PYTHONIOENCODING", "utf-8")
    errors = []
    for command in commands:
        result = subprocess.run(
            command,
            cwd=repo_root,
            check=False,
            text=True,
            capture_output=True,
            env=env,
        )
        label = command[-1]
        if result.stdout:
            print(result.stdout.rstrip())
        if result.stderr:
            print(result.stderr.rstrip())
        if result.returncode != 0:
            errors.append(f"{label} exited with code {result.returncode}")
    if errors:
        raise RuntimeError("; ".join(errors))


def post_dispatch(
    cell: Cell,
    chain_name: str,
    ctx: ControllerContext,
    *,
    sync_override: Optional[bool] = None,
    note: Optional[str] = None,
    payload_path: Optional[str] = None,
) -> None:
    """Handle ledger logging and sync discipline after dispatch."""

    auto_sync = ctx.auto_sync if sync_override is None else bool(sync_override)
    if not auto_sync:
        return
    ledger_path = append_ledger_entry(ctx.repo_root, cell, chain_name, note=note)
    try:
        relative_ledger = ledger_path.relative_to(ctx.repo_root)
    except ValueError:
        relative_ledger = ledger_path
    print(f"🗒️  Logged dispatch to {relative_ledger}")
    try:
        run_sync_commands(ctx.repo_root)
    except RuntimeError as exc:
        print(f"⚠️  {exc}")


    # Non-enforcing warning: print would-clamp triggers if present for this dispatch
    if payload_path:
        try:
            p = _PathForWarnings(payload_path)
            if not p.is_absolute():
                p = ctx.repo_root / p
            data = _json_for_warnings.loads(p.read_text(encoding="utf-8"))
            stub = data.get("telemetry_stub") if isinstance(data.get("telemetry_stub"), dict) else {}
            batch_id = str(getattr(stub, "get", lambda k, d=None: None)("batch_id") or data.get("batch_id") or "")
            if batch_id:
                by_batch = ctx.repo_root / "logs" / "fun_guardrails" / "by_batch" / f"{batch_id}.json"
                if by_batch.exists():
                    evt = _json_for_warnings.loads(by_batch.read_text(encoding="utf-8"))
                    triggers = evt.get("triggers") if isinstance(evt.get("triggers"), list) else []
                    if triggers:
                        parts = []
                        for t in triggers:
                            ttype = str(t.get("type"))
                            obs = t.get("observed")
                            thr = t.get("threshold")
                            parts.append(f"{ttype} {obs}>{thr}")
                        print(f"!! Guardrail would-clamp: {'; '.join(parts)}")
        except Exception:
            pass

def process_event_stream(ctx: ControllerContext, stream: TextIO) -> None:
    """Consume JSONL events that specify overlay dispatches."""

    print("Listening for overlay events...")
    for index, raw_line in enumerate(stream, start=1):
        cell: Optional[Cell] = None
        payload_path: Optional[str] = None
        line = raw_line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            print(f"⚠️  Event {index}: invalid JSON — {exc}")
            continue
        if not isinstance(event, dict):
            print(f"⚠️  Event {index}: expected JSON object, received {type(event).__name__}")
            continue

        cell_token = event.get("cell")
        if not cell_token:
            print(f"⚠️  Event {index}: missing 'cell' field")
            continue
        try:
            cell = parse_cell_token(str(cell_token))
        except ValueError as exc:
            print(f"⚠️  Event {index}: {exc}")
            continue

        sync_override = event.get("auto_sync")
        ledger_note_raw = event.get("ledger_note")
        if ledger_note_raw is None and "source" in event:
            ledger_note_raw = event.get("source")
        ledger_note = str(ledger_note_raw) if ledger_note_raw is not None else None

        try:
            payload_path, chain_name = dispatch(cell, ctx)
        except KeyError as exc:
            print(f"⚠️  Event {index}: {exc}")
            continue
        except Exception as exc:  # pragma: no cover - surfaced to operator
            print(f"⚠️  Event {index}: dispatch failed — {exc}")
            continue

        print(f"✅ Event {index}: {cell_label(cell)} → {payload_path}")
post_dispatch(cell, chain_name, ctx, sync_override=sync_override, note=ledger_note, payload_path=payload_path)


def interactive_session(ctx: ControllerContext) -> None:
    """Run the interactive controller loop."""

    print("Alfa Zero Controller - select grid cells to dispatch emoji chains.")
    print("Type '?' for help, 'map' to list wired cells, or 'quit' to exit.\n")
    try:
        if isinstance(ctx.bridge, OverlayBridge) and getattr(ctx.bridge, "fun_flags", None):
            flags = ctx.bridge.fun_flags.as_dict()  # type: ignore[attr-defined]
            print(f"Active FUN flags: {json.dumps(flags)}\n")
    except Exception:
        pass
    render_grid()

    last_cell: Optional[Cell] = None

    while True:
        try:
            raw = input("Cell or command> ").strip()
        except (EOFError, KeyboardInterrupt):  # pragma: no cover - interactive exit
            print()
            break

        if not raw:
            continue

        command = raw.lower()
        if command in {"quit", "exit", "q"}:
            break
        if command in {"?", "help"}:
            print("Commands:\n  <cell>      Dispatch cell (formats: 04, 0,4, 0 4)\n  map         Show mapped overlay cells\n  show        Re-render the grid\n  quit        Exit controller")
            continue
        if command == "map":
            list_mapped_cells()
            continue
        if command == "show":
            render_grid(last_cell)
            continue

        try:
            cell = parse_cell_token(raw)
        except ValueError as exc:
            print(f"⚠️  {exc}")
            continue

        try:
            payload_path, chain_name = dispatch(cell, ctx)
        except KeyError as exc:
            print(f"⚠️  {exc}")
            continue
        except Exception as exc:  # pragma: no cover - surfaced to operator
            print(f"⚠️  Dispatch failed: {exc}")
            continue

        last_cell = cell
        render_grid(highlight=cell)
        print(
            f"✅ Dispatched {cell_label(cell)} → {payload_path}\n"
            "   (inspect under outbox/orders/emoji_runtime/)"
        )
post_dispatch(cell, chain_name, ctx, payload_path=payload_path)


def bootstrap_context(outbox_override: Optional[str], auto_sync: bool) -> ControllerContext:
    """Load translator dependencies and return a controller context."""

    bridge = build_bridge(outbox_override)
    return ControllerContext(
        repo_root=bridge.repo_root,
        bridge=bridge,
        auto_sync=auto_sync,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Control the Alfa Zero battlegrid via CLI")
    parser.add_argument(
        "--cell",
        help="Dispatch a single cell (formats: 04, 0,4, 0 4) and exit.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List mapped overlay cells and exit.",
    )
    parser.add_argument(
        "--outbox",
        default=None,
        help="Override the emoji runtime outbox path.",
    )
    parser.add_argument(
        "--event-stream",
        default=None,
        help="Read JSONL dispatch events from a file or '-' for stdin.",
    )
    parser.add_argument(
        "--no-auto-sync",
        action="store_true",
        help="Skip heartbeat, ledger, and sync steps after dispatch.",
    )
    args = parser.parse_args()

    ctx = bootstrap_context(args.outbox, auto_sync=not args.no_auto_sync)

    if args.list:
        list_mapped_cells()
        return

    if args.event_stream:
        if args.event_stream == "-":
            stream: TextIO = sys.stdin
        else:
            stream = open(args.event_stream, "r", encoding="utf-8")
        try:
            process_event_stream(ctx, stream)
        finally:
            if stream is not sys.stdin:
                stream.close()
        return

    if args.cell:
        cell = parse_cell_token(args.cell)
        payload_path, chain_name = dispatch(cell, ctx)
        print(f"✅ Dispatched {cell_label(cell)} → {payload_path}")
post_dispatch(cell, chain_name, ctx, payload_path=payload_path)
        return

    interactive_session(ctx)


if __name__ == "__main__":
    main()
