"""Interactive Alfa Zero controller bridging the battlegrid to the emoji translator.

This CLI is a stopgap until the graphical overlay lands. It renders the
16×16 grid from the Alfa Zero spec, allows operators (or scripted callers)
to select cells using hexadecimal coordinates, and dispatches the mapped
emoji chains through the Level-0 translator living in Alfa 04.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from overlay_test_harness import (
    CELL_MAPPINGS,
    cell_label,
    dispatch_cell,
    find_repo_root,
    load_sample_chains,
    load_translator,
    resolve_outbox,
)

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
    translator: object
    sample_chains: Dict[str, str]
    outbox: Path


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


def dispatch(cell: Cell, ctx: ControllerContext) -> str:
    """Invoke the translator for the chosen cell and return the relative payload path."""

    path = dispatch_cell(cell, ctx.translator, ctx.sample_chains, ctx.outbox)
    try:
        relative = path.relative_to(ctx.repo_root)
    except ValueError:
        relative = path
    return str(relative)


def interactive_session(ctx: ControllerContext) -> None:
    """Run the interactive controller loop."""

    print("Alfa Zero Controller — select grid cells to dispatch emoji chains.")
    print("Type '?' for help, 'map' to list wired cells, or 'quit' to exit.\n")
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
            payload_path = dispatch(cell, ctx)
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
            "   (inspect under exchange/orders/outbox/emoji_runtime/)"
        )


def bootstrap_context(outbox_override: Optional[str]) -> ControllerContext:
    """Load translator dependencies and return a controller context."""

    script_dir = Path(__file__).resolve().parent
    repo_root = find_repo_root(script_dir)
    translator = load_translator(repo_root)
    sample_chains = load_sample_chains(repo_root)
    outbox = resolve_outbox(repo_root, outbox_override)
    return ControllerContext(
        repo_root=repo_root,
        translator=translator,
        sample_chains=sample_chains,
        outbox=outbox,
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
    args = parser.parse_args()

    ctx = bootstrap_context(args.outbox)

    if args.list:
        list_mapped_cells()
        return

    if args.cell:
        cell = parse_cell_token(args.cell)
        payload_path = dispatch(cell, ctx)
        print(f"✅ Dispatched {cell_label(cell)} → {payload_path}")
        return

    interactive_session(ctx)


if __name__ == "__main__":
    main()
