"""CLI harness for dispatching Alfa Zero emoji chains via the overlay bridge."""

from __future__ import annotations

import argparse
from typing import Iterable, Tuple

from overlay_bridge import CELL_MAPPINGS, build_bridge, cell_label

Cell = Tuple[int, int]


def parse_cell_argument(argument: str) -> Cell:
    """Parse a row,col argument using hexadecimal coordinates (0-F)."""

    parts = [part.strip().upper() for part in argument.split(",") if part.strip()]
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("Cell must be provided as ROW,COL (hex 0-F)")
    try:
        row = int(parts[0], 16)
        col = int(parts[1], 16)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Row and column must be hexadecimal digits (0-F)") from exc
    if not (0 <= row <= 15 and 0 <= col <= 15):
        raise argparse.ArgumentTypeError("Row and column must be within 0-F")
    return row, col


def iter_cells_to_dispatch(args, available_cells: Iterable[Cell]) -> Iterable[Cell]:
    """Return the collection of cells the user requested to dispatch."""

    if args.all_cells:
        return sorted(available_cells)
    if args.cell:
        return [args.cell]
    raise SystemExit(
        "No cell specified. Pass --cell ROW,COL (hex) or --all-cells to dispatch the mapped set."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Dispatch mapped Alfa Zero emoji chains.")
    parser.add_argument(
        "--cell",
        type=parse_cell_argument,
        help="Grid cell to dispatch (ROW,COL using hexadecimal digits, e.g. 0,4 or C,0).",
    )
    parser.add_argument(
        "--all-cells",
        action="store_true",
        help="Dispatch every mapped cell once (useful for smoke tests).",
    )
    parser.add_argument(
        "--outbox",
        default=None,
        help="Optional override for the emoji runtime outbox location.",
    )
    args = parser.parse_args()

    bridge = build_bridge(args.outbox)

    cells = iter_cells_to_dispatch(args, CELL_MAPPINGS.keys())
    successes = []
    failures = []

    for cell in cells:
        try:
            destination = bridge.dispatch_cell(cell)
            successes.append((cell_label(cell), destination.relative_to(bridge.repo_root)))
        except Exception as exc:  # pylint: disable=broad-except
            failures.append((cell_label(cell), str(exc)))

    if successes:
        print("✅ Overlay dispatch complete:")
        for label, path in successes:
            print(f"  - {label}: {path}")
    else:
        print("⚠️ No payloads dispatched.")

    if failures:
        print("\n⚠️ Failures:")
        for label, error in failures:
            print(f"  - {label}: {error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
