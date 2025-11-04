"""Terminal UI controller for the Alfa Zero overlay bridge.

This module offers an interactive loop that mirrors the 16x16 Alfa Zero grid,
allows operators to navigate or target cells, and dispatches the mapped emoji
chains through ``OverlayBridge``. It is intentionally lightweight so it can
run on developer workstations without additional dependencies while leaving
room for future graphical clients to plug into the same bridge.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple, TextIO

from overlay_bridge import CELL_MAPPINGS, OverlayBridge, build_bridge, cell_label

Cell = Tuple[int, int]
HEX_DIGITS = "0123456789ABCDEF"

# 16x16 battlefield layout derived from docs/alfa_zero_spec.md
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
class PayloadSummary:
    path: Path
    chain_name: Optional[str]
    template: Optional[str]
    outcomes: List[str]
    description: Optional[str]
    summary_text: Optional[str]


@dataclass
class UIContext:
    bridge: OverlayBridge
    telemetry_path: Optional[Path]
    emit_events: bool
    event_stream: Optional[TextIO]
    output_stream: TextIO
    selected: Cell = (0, 4)

    @property
    def repo_root(self) -> Path:
        return self.bridge.repo_root


def parse_cell_token(token: str) -> Cell:
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
    except ValueError as exc:
        raise ValueError("Row and column must be hexadecimal digits (0-F)") from exc

    if not (0 <= row <= 15 and 0 <= col <= 15):
        raise ValueError("Row and column must be between 0 and F inclusive")

    return row, col


def render_grid(highlight: Optional[Cell] = None, *, stream: TextIO = sys.stdout) -> None:
    header = "    " + " ".join(HEX_DIGITS)
    print(header, file=stream)
    for row_index, row in enumerate(GRID_LAYOUT):
        rendered: List[str] = []
        for col_index, glyph in enumerate(row):
            cell = (row_index, col_index)
            mark = glyph
            if cell in CELL_MAPPINGS:
                mark = glyph if glyph else "·"
            if highlight == cell:
                mark = f"[{mark}]"
            rendered.append(mark)
        print(f"{HEX_DIGITS[row_index]}   " + " ".join(rendered), file=stream)


def list_mapped_cells(stream: TextIO = sys.stdout) -> None:
    print("Mapped overlay cells:", file=stream)
    for cell, (chain, description) in sorted(CELL_MAPPINGS.items()):
        print(f"  - {cell_label(cell)}: {chain} — {description}", file=stream)


def summarize_payload(path: Path) -> PayloadSummary:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    chain_name = payload.get("chain_name")
    template = payload.get("template")
    description = payload.get("overlay_description")
    summary_text = payload.get("summary")
    outcomes = [str(value) for value in payload.get("outcomes", [])]
    return PayloadSummary(
        path=path,
        chain_name=chain_name,
        template=template,
        outcomes=outcomes,
        description=description,
        summary_text=summary_text,
    )


def compute_sync_state(summary: PayloadSummary) -> str:
    """Minimal narration sync indicator heuristic for demo use."""
    return "green" if summary.outcomes else "amber"


def emit_telemetry(summary: PayloadSummary, telemetry_path: Path) -> None:
    sync_state = compute_sync_state(summary)
    record = {
        "path": str(summary.path),
        "chain_name": summary.chain_name,
        "template": summary.template,
        "outcomes": summary.outcomes,
        "description": summary.description,
        "narration_text": summary.summary_text,
        "sync_state": sync_state,
    }
    with telemetry_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False))
        handle.write("\n")


def display_summary(summary: PayloadSummary, repo_root: Path, *, stream: TextIO = sys.stdout) -> None:
    try:
        relative_path = summary.path.relative_to(repo_root)
    except ValueError:
        relative_path = summary.path

    print(f"✅ Dispatched {summary.chain_name or 'unknown chain'}", file=stream)
    print(f"   Template: {summary.template or 'unknown template'}", file=stream)
    if summary.outcomes:
        print(f"   Outcomes: {', '.join(summary.outcomes)}", file=stream)
    if summary.description:
        print(f"   Description: {summary.description}", file=stream)
    # Minimal sync state indicator for demo runs
    try:
        sync_state = compute_sync_state(summary)
        print(f"   Sync: {sync_state}", file=stream)
    except Exception:
        pass
    print(f"   Payload: {relative_path}", file=stream)


def move_selection(context: UIContext, delta_row: int, delta_col: int) -> None:
    row = max(0, min(15, context.selected[0] + delta_row))
    col = max(0, min(15, context.selected[1] + delta_col))
    context.selected = (row, col)


def select_cell(context: UIContext, cell: Cell) -> None:
    context.selected = cell


def dispatch_selected(context: UIContext) -> None:
    cell = context.selected

    if context.emit_events:
        if context.event_stream is None:
            print("⚠️  Event stream not configured; cannot emit dispatch.", file=context.output_stream)
            return
        event = {
            "cell": cell_label(cell),
            "source": "alfa_zero_ui",
            "ledger_note": "alfa_zero_ui",
        }
        context.event_stream.write(json.dumps(event, ensure_ascii=False))
        context.event_stream.write("\n")
        context.event_stream.flush()
        print(f"🚀 Emitted overlay event for {event['cell']}", file=context.output_stream)
        return

    try:
        destination = context.bridge.dispatch_cell(cell)
    except KeyError as exc:
        print(f"⚠️  {exc}", file=context.output_stream)
        return
    except Exception as exc:  # pragma: no cover - surfaced to operator
        print(f"⚠️  Dispatch failed: {exc}", file=context.output_stream)
        return

    summary = summarize_payload(destination)
    display_summary(summary, context.repo_root, stream=context.output_stream)
    if context.telemetry_path:
        emit_telemetry(summary, context.telemetry_path)


def show_cell_info(cell: Cell, stream: TextIO = sys.stdout) -> None:
    label = cell_label(cell)
    if cell in CELL_MAPPINGS:
        chain, description = CELL_MAPPINGS[cell]
        print(f"{label}: {chain} — {description}", file=stream)
    else:
        print(f"{label}: unmapped cell", file=stream)


HELP_TEXT = """Commands:
  w / up       Move selection up
  s / down     Move selection down
  a / left     Move selection left
  d / right    Move selection right
  dispatch     Run the translator for the selected cell
  info         Show mapping info for the selected cell
  map          List every mapped cell and chain
  <cell>       Jump to a cell (formats: 04, 0,4, 0 4)
  show         Re-render the grid
  help         Show this help text
  quit         Exit the controller
"""


def interactive_loop(context: UIContext) -> None:
    print("Alfa Zero Overlay UI — navigate the grid and dispatch mapped chains.", file=context.output_stream)
    print("Type 'help' for command reference.\n", file=context.output_stream)
    render_grid(context.selected, stream=context.output_stream)

    while True:
        try:
            if context.emit_events:
                if context.output_stream is not sys.stdout:
                    print("command> ", end="", file=context.output_stream, flush=True)
                raw_line = sys.stdin.readline()
                if raw_line == "":
                    print(file=context.output_stream)
                    break
                raw = raw_line.strip()
            else:
                raw = input("command> ").strip()
        except (EOFError, KeyboardInterrupt):  # pragma: no cover - interactive exit
            print(file=context.output_stream)
            break

        if not raw:
            dispatch_selected(context)
            render_grid(context.selected, stream=context.output_stream)
            continue

        command = raw.lower()
        if command in {"quit", "q", "exit"}:
            break
        if command in {"help", "?"}:
            print(HELP_TEXT, file=context.output_stream)
            continue
        if command in {"show", "grid"}:
            render_grid(context.selected, stream=context.output_stream)
            continue
        if command in {"map"}:
            list_mapped_cells(context.output_stream)
            continue
        if command in {"info"}:
            show_cell_info(context.selected, context.output_stream)
            continue
        if command in {"w", "up"}:
            move_selection(context, -1, 0)
            render_grid(context.selected, stream=context.output_stream)
            continue
        if command in {"s", "down"}:
            move_selection(context, 1, 0)
            render_grid(context.selected, stream=context.output_stream)
            continue
        if command in {"a", "left"}:
            move_selection(context, 0, -1)
            render_grid(context.selected, stream=context.output_stream)
            continue
        if command in {"d", "right"}:
            move_selection(context, 0, 1)
            render_grid(context.selected, stream=context.output_stream)
            continue
        if command in {"dispatch", "fire", "send"}:
            dispatch_selected(context)
            render_grid(context.selected, stream=context.output_stream)
            continue

        try:
            cell = parse_cell_token(raw)
        except ValueError as exc:
            print(f"⚠️  {exc}", file=context.output_stream)
            continue

        select_cell(context, cell)
        render_grid(context.selected, stream=context.output_stream)


def run_single_dispatch(context: UIContext, cell: Cell) -> None:
    select_cell(context, cell)
    dispatch_selected(context)


def build_context(
    outbox_override: Optional[str],
    telemetry: Optional[str],
    *,
    emit_events: bool,
    event_stream: Optional[TextIO],
) -> UIContext:
    bridge = build_bridge(outbox_override)
    telemetry_path = Path(telemetry).expanduser().resolve() if telemetry else None
    output_stream = sys.stderr if emit_events and event_stream is sys.stdout else sys.stdout
    return UIContext(
        bridge=bridge,
        telemetry_path=telemetry_path,
        emit_events=emit_events,
        event_stream=event_stream,
        output_stream=output_stream,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Interactive Alfa Zero overlay UI")
    parser.add_argument(
        "--cell",
        help="Dispatch a single cell and exit (formats: 04, 0,4, 0 4).",
    )
    parser.add_argument(
        "--outbox",
        default=None,
        help="Override the emoji runtime outbox path.",
    )
    parser.add_argument(
        "--telemetry",
        default=None,
        help="Optional path to append JSONL telemetry records for each dispatch.",
    )
    parser.add_argument(
        "--emit-events",
        action="store_true",
        help="Emit JSON event lines instead of dispatching directly (pipe into alfa_zero_controller).",
    )
    parser.add_argument(
        "--event-file",
        default=None,
        help="When emitting events, write them to this file instead of stdout.",
    )
    args = parser.parse_args()

    if args.event_file and not args.emit_events:
        parser.error("--event-file requires --emit-events")

    event_stream: Optional[TextIO] = None
    close_stream = False
    if args.emit_events:
        if args.event_file:
            event_path = Path(args.event_file).expanduser().resolve()
            event_path.parent.mkdir(parents=True, exist_ok=True)
            event_stream = event_path.open("a", encoding="utf-8")
            close_stream = True
        else:
            event_stream = sys.stdout

    context = build_context(
        args.outbox,
        args.telemetry,
        emit_events=args.emit_events,
        event_stream=event_stream,
    )

    try:
        if args.cell:
            cell = parse_cell_token(args.cell)
            run_single_dispatch(context, cell)
            return

        interactive_loop(context)
    finally:
        if close_stream and event_stream is not None:
            event_stream.close()


if __name__ == "__main__":  # pragma: no cover - manual entry point
    main()
