"""Utilities for synchronizing the quint_synced alignment folder across workspaces.

Run from any workspace root:
    python tools/quint_sync.py
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

CONFIG_FILENAME = "quint_sync_config.json"
DEFAULT_LOG_HEADER = "# Quint Sync Log\n\n"


@dataclass(frozen=True)
class Workspace:
    name: str
    path: Path


def load_config(config_path: Path) -> Tuple[List[Workspace], Path]:
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    raw = json.loads(config_path.read_text(encoding="utf-8"))
    if "workspaces" not in raw or not isinstance(raw["workspaces"], list):
        raise ValueError("Config must contain a 'workspaces' list")

    workspaces: List[Workspace] = []
    for entry in raw["workspaces"]:
        try:
            name = entry["name"]
            path = Path(entry["path"]).expanduser().resolve()
        except KeyError as exc:
            raise ValueError("Each workspace entry requires 'name' and 'path'") from exc
        workspaces.append(Workspace(name=name, path=path))

    log_file = Path(raw.get("log_file", "")).expanduser().resolve()
    if not log_file:
        raise ValueError("Config must define 'log_file'")

    return workspaces, log_file


def is_relative_to(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def detect_source_workspace(
    cwd: Path, workspaces: List[Workspace], explicit_source: str | None
) -> Workspace:
    if explicit_source:
        for ws in workspaces:
            if ws.name == explicit_source:
                return ws
        raise ValueError(f"Workspace '{explicit_source}' is not defined in the config")

    for ws in workspaces:
        if cwd == ws.path or is_relative_to(cwd, ws.path):
            return ws
    raise ValueError(
        "Unable to determine current workspace. Specify with --source or run from a configured path."
    )


def copy_quint_synced(src_ws: Workspace, dest_ws: Workspace, dry_run: bool) -> None:
    src_folder = src_ws.path / "quint_synced"
    dest_folder = dest_ws.path / "quint_synced"

    if not src_folder.exists():
        raise FileNotFoundError(f"Source folder missing: {src_folder}")

    if dry_run:
        print(f"[DRY-RUN] Would copy {src_folder} -> {dest_folder}")
        return

    if dest_folder.exists():
        shutil.rmtree(dest_folder)
    shutil.copytree(src_folder, dest_folder)
    print(f"Copied {src_folder} -> {dest_folder}")


def prompt_statuses(workspaces: List[Workspace]) -> Dict[str, str]:
    print("\nEnter ACK/TODO notes for each workspace (leave blank for ACK).")
    statuses: Dict[str, str] = {}
    for ws in workspaces:
        response = input(f"  {ws.name}: ").strip()
        statuses[ws.name] = response or "ACK"
    print()
    return statuses


def append_log(
    log_path: Path,
    source: Workspace,
    destinations: List[Workspace],
    note: str,
    statuses: Dict[str, str],
) -> None:
    if log_path.parent and not log_path.parent.exists():
        log_path.parent.mkdir(parents=True, exist_ok=True)

    if not log_path.exists():
        log_path.write_text(DEFAULT_LOG_HEADER, encoding="utf-8")

    timestamp = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")
    dest_list = ", ".join(ws.name for ws in destinations) or "(none)"

    lines = [
        f"## {timestamp}\n",
        f"- source: {source.name}\n",
        f"- destinations: {dest_list}\n",
    ]
    if note:
        lines.append(f"- note: {note}\n")
    lines.append("\n### Workspace Status\n")
    for ws_name, status in statuses.items():
        lines.append(f"- {ws_name}: {status}\n")
    lines.append("\n")

    with log_path.open("a", encoding="utf-8") as handle:
        handle.writelines(lines)

    print(f"Logged sync details to {log_path}")


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Sync the quint_synced folder across workspaces.")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(__file__).resolve().parent / CONFIG_FILENAME,
        help="Path to the quint sync config file.",
    )
    parser.add_argument(
        "--source",
        help="Workspace name to use as the sync source (defaults to current working directory).",
    )
    parser.add_argument(
        "--note",
        default="",
        help="Optional summary note to include in the sync log.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned actions without copying files or updating the log.",
    )
    parser.add_argument(
        "--skip-status",
        action="store_true",
        help="Skip ACK/TODO prompts and log all workspaces as ACK.",
    )
    return parser


def main(argv: List[str]) -> int:
    parser = build_argument_parser()
    args = parser.parse_args(argv)

    workspaces, log_file = load_config(args.config.resolve())
    cwd = Path.cwd().resolve()
    source_ws = detect_source_workspace(cwd, workspaces, args.source)

    destinations = [ws for ws in workspaces if ws != source_ws]

    print(f"Source workspace: {source_ws.name} -> {source_ws.path}")
    print("Destinations:")
    for ws in destinations:
        print(f"  - {ws.name}: {ws.path}")

    for target in destinations:
        copy_quint_synced(source_ws, target, args.dry_run)

    if args.dry_run:
        print("Dry run complete; no log entry recorded.")
        return 0

    statuses = {ws.name: "ACK" for ws in workspaces}
    if not args.skip_status:
        statuses = prompt_statuses(workspaces)

    append_log(log_file, source_ws, destinations, args.note.strip(), statuses)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
