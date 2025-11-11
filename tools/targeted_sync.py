"""CLI helper for targeted Alfa Zero sync loops with safety prompts."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Callable, Iterable, Sequence

from . import offline_sync_exchange

DEFAULT_CATEGORIES = ["orders"]


def _format_categories(categories: Sequence[str]) -> str:
    if not categories:
        return "(none)"
    return ", ".join(categories)


def run_targeted_sync(
    *,
    workspace_root: Path,
    categories: Sequence[str] | None,
    orders_subpath: str | None,
    latest: int | None,
    quiet: bool,
    dry_run: bool,
    auto_confirm: bool,
    input_fn: Callable[[str], str] = input,
) -> bool:
    """Execute a targeted sync after confirming with the operator."""

    selected_categories = list(categories) if categories else list(DEFAULT_CATEGORIES)
    summary_lines = [
        "Targeted sync configuration:",
        f"  Workspace: {workspace_root}",
        f"  Categories: {_format_categories(selected_categories)}",
        f"  Orders subpath: {orders_subpath or '(none)'}",
        f"  Latest: {latest or 'all'}",
        f"  Quiet mode: {'on' if quiet else 'off'}",
        f"  Dry run: {'yes' if dry_run else 'no'}",
    ]
    for line in summary_lines:
        print(line)

    if not auto_confirm:
        response = input_fn("Proceed with sync? [y/N]: ").strip().lower()
        if response not in {"y", "yes"}:
            print("Aborted. No sync executed.")
            return False

    offline_sync_exchange.sync_local(
        str(workspace_root),
        categories=list(selected_categories),
        orders_subpath=orders_subpath,
        latest=latest,
        quiet=quiet,
        dry_run=dry_run,
    )

    if dry_run:
        print("Dry-run completed; verify plan above.")
    else:
        print("Targeted sync complete.")
    return True


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Targeted sync helper for Alfa Zero overlays",
    )
    parser.add_argument(
        "--workspace-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Workspace root (defaults to repository root)",
    )
    parser.add_argument(
        "--category",
        action="append",
        choices=["orders", "reports"],
        help="Restrict sync to one or more categories (defaults to orders only)",
    )
    parser.add_argument(
        "--orders-subpath",
        help="Limit order sync to a subdirectory, e.g. emoji_runtime",
    )
    parser.add_argument(
        "--latest",
        type=int,
        help="Only sync the N most recent files per category",
    )
    parser.add_argument(
        "--no-quiet",
        action="store_true",
        help="Disable quiet mode (verbose copy logs)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview without copying files",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Skip the confirmation prompt",
    )
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    workspace_root = args.workspace_root
    if not workspace_root.exists():
        print(f"[ERROR] Workspace root {workspace_root} does not exist")
        return 2

    success = run_targeted_sync(
        workspace_root=workspace_root,
        categories=args.category,
        orders_subpath=args.orders_subpath,
        latest=args.latest,
        quiet=not args.no_quiet,
        dry_run=args.dry_run,
        auto_confirm=args.yes,
    )
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
