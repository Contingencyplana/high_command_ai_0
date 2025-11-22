# offline_sync_exchange.py — offline exchange sync for Genesis Mesh
# Works across any workspace; detects and creates missing folders.

import argparse
import os
import shutil
import sys
from pathlib import Path

# Shared hub path
EXCHANGE = Path(os.getenv("SHAGI_EXCHANGE_PATH", "C:/Users/Admin/high_command_exchange"))


def _safe_print(message: str) -> None:
    """Print message, degrading gracefully when stdout encoding rejects emoji."""

    try:
        print(message)
        return
    except UnicodeEncodeError:
        pass

    encoding = getattr(sys.stdout, "encoding", None) or "ascii"
    fallback = message.encode(encoding, errors="ignore").decode(encoding, errors="ignore")
    if fallback.strip():
        print(fallback)
    else:
        ascii_only = message.encode("ascii", errors="replace").decode("ascii")
        print(ascii_only)

QUIET_SAMPLE_LIMIT = 5


def _collect_files(base: Path, *, subpath: str | None) -> tuple[Path, list[Path]]:
    """Return the copy root and list of files to transfer."""

    if subpath:
        candidate = (base / subpath).resolve()
        try:
            candidate.relative_to(base.resolve())
        except ValueError:
            raise ValueError(f"Subpath {subpath!r} escapes the {base} directory")
        if not candidate.exists():
            return base, []
        base_glob_root = candidate
    else:
        base_glob_root = base

    files: list[Path] = []
    for file_path in base_glob_root.glob("**/*"):
        if file_path.is_file():
            files.append(file_path)
    return base, files


def _subset_latest(files: list[Path], *, latest: int | None) -> list[Path]:
    if not files:
        return files
    if latest is None or latest <= 0:
        return sorted(files)
    ranked = sorted(files, key=lambda p: p.stat().st_mtime, reverse=True)
    subset = ranked[:latest]
    return sorted(subset)


def _log_copy(
    *,
    quiet: bool,
    name: str,
    copied: list[tuple[Path, Path]],
    missing: bool,
    dst_root: Path,
    dry_run: bool,
) -> None:
    if missing:
        print(f"[WARN] No {name} folder found in outbox")
        return

    if not copied:
        print(f"[INFO] No new {name} files to sync")
        return

    verb = "Would copy" if dry_run else "Copied"

    entries = copied
    if quiet and len(entries) > QUIET_SAMPLE_LIMIT:
        sample = entries[:QUIET_SAMPLE_LIMIT]
        for src, dst in sample:
            print(f"{verb} {src} -> {dst}")
        remaining = len(entries) - QUIET_SAMPLE_LIMIT
        print(
            f"[QUIET] {remaining} additional {name} file(s) {'planned' if dry_run else 'copied'} (see destination for full list)"
        )
    else:
        for src, dst in entries:
            print(f"{verb} {src} -> {dst}")

    status = "Planned" if dry_run else "Synced"
    print(f"[OK] {status} {len(entries)} {name} file(s) to {dst_root}")


def sync_local(
    workspace_root: str,
    *,
    categories: list[str] | None = None,
    orders_subpath: str | None = None,
    latest: int | None = None,
    quiet: bool = False,
    dry_run: bool = False,
) -> None:
    """Synchronize outbox artifacts into the shared exchange hub."""

    ws = Path(workspace_root)
    selected = categories or ["orders", "reports"]

    source_folders = {
        "orders": ws / "outbox" / "orders",
        "reports": ws / "outbox" / "reports",
    }

    for name, src in source_folders.items():
        if name not in selected:
            continue

        dst = EXCHANGE / name
        if not src.exists():
            _log_copy(
                quiet=quiet,
                name=name,
                copied=[],
                missing=True,
                dst_root=dst,
                dry_run=dry_run,
            )
            continue

        if not dry_run:
            os.makedirs(dst, exist_ok=True)

        subpath = orders_subpath if name == "orders" else None
        try:
            copy_root, files = _collect_files(src, subpath=subpath)
        except ValueError as exc:
            print(f"[ERROR] {exc}")
            continue

        files = _subset_latest(files, latest=latest)
        copied: list[tuple[Path, Path]] = []
        for source_path in files:
            rel_path = source_path.relative_to(copy_root)
            dst_file = dst / rel_path
            if not dry_run:
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_path, dst_file)
            copied.append((source_path, dst_file))

        _log_copy(
            quiet=quiet,
            name=name,
            copied=copied,
            missing=False,
            dst_root=dst,
            dry_run=dry_run,
        )

    _safe_print("✅ Local exchange sync complete.")


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    workspace_root = here.parent
    parser = argparse.ArgumentParser(description="Mirror outbox artifacts into the offline exchange hub")
    parser.add_argument(
        "--category",
        choices=["orders", "reports"],
        action="append",
        help="Restrict sync to specific categories (defaults to both orders and reports)",
    )
    parser.add_argument(
        "--orders-subpath",
        help="Limit orders sync to a relative subdirectory (for example emoji_runtime)",
    )
    parser.add_argument(
        "--latest",
        type=int,
        help="Only sync the N most recent files per category",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress detailed per-file logs after the first few entries",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview the sync without copying files",
    )

    args = parser.parse_args()
    sync_local(
        str(workspace_root),
        categories=args.category,
        orders_subpath=args.orders_subpath,
        latest=args.latest,
        quiet=args.quiet,
        dry_run=args.dry_run,
    )
