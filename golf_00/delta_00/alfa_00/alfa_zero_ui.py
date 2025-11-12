# pyright: reportMissingImports=false
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
from datetime import datetime, timedelta, timezone
import os
from pathlib import Path
import subprocess
from typing import Dict, List, Optional, Sequence, TextIO, Tuple

from overlay_bridge import CELL_MAPPINGS, OverlayBridge, build_bridge, cell_label
from trace_utils import generate_trace_id
from storyboard_runner import (
    NIGHTLANDS_DUET_STORYBOARD,
    StoryboardGuardrailError,
    cooldown_remaining,
    format_storyboard_preview,
    load_storyboard_status,
    StoryboardRunResult,
    run_storyboard as run_storyboard_sequence,
)

Cell = Tuple[int, int]
HEX_DIGITS = "0123456789ABCDEF"
DEFAULT_OVERLAY = "overlay-alpha"
LORE_OVERLAY_ID = "outland-lore-v1"
LORE_LAYER_KIND = "lore"
MUSIC_OVERLAY_ID = "outland-music-v1"
MUSIC_LAYER_KIND = "music"

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
    overlay_id: Optional[str]
    overlay_layer: Optional[str]
    overlays: Optional[List[Dict[str, str]]]
    trace_id: Optional[str]
    storyboard_id: Optional[str]
    storyboard_step: Optional[str]
    storyboard_sequence: Optional[int]
    storyboard_total_steps: Optional[int]


@dataclass
class UIContext:
    bridge: OverlayBridge
    telemetry_path: Optional[Path]
    emit_events: bool
    event_stream: Optional[TextIO]
    output_stream: TextIO
    metrics_path: Optional[Path] = None
    action_log_path: Optional[Path] = None
    session_id: str = ""
    session_start_ts: Optional[datetime] = None
    dispatch_count: int = 0
    selected: Cell = (0, 4)
    auto_contracts: bool = False
    lore_layer_enabled: bool = False
    music_layer_enabled: bool = False

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


def render_grid(highlight: Optional[Cell] = None, *, stream: TextIO = sys.stdout, overlay: Optional[Dict[Cell, str]] = None) -> None:
    header = "    " + " ".join(HEX_DIGITS)
    print(header, file=stream)
    for row_index, row in enumerate(GRID_LAYOUT):
        rendered: List[str] = []
        for col_index, glyph in enumerate(row):
            cell = (row_index, col_index)
            mark = overlay.get(cell, glyph) if overlay else glyph
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
    overlay_stack = None
    overlays_field = payload.get("overlays")
    if isinstance(overlays_field, list):
        overlay_stack = []
        for entry in overlays_field:
            if not isinstance(entry, dict):
                continue
            overlay_id_value = entry.get("overlay_id")
            layer_kind_value = entry.get("layer_kind")
            if not overlay_id_value or not layer_kind_value:
                continue
            overlay_stack.append({
                "overlay_id": str(overlay_id_value),
                "layer_kind": str(layer_kind_value),
            })
        if not overlay_stack:
            overlay_stack = None
    trace_id_value = payload.get("trace_id")
    trace_id = str(trace_id_value) if isinstance(trace_id_value, str) else None
    storyboard_id_value = payload.get("storyboard_id")
    storyboard_id = str(storyboard_id_value) if isinstance(storyboard_id_value, str) else None
    storyboard_step_value = payload.get("storyboard_step")
    storyboard_step = str(storyboard_step_value) if isinstance(storyboard_step_value, str) else None
    storyboard_sequence_value = payload.get("storyboard_sequence")
    storyboard_sequence = (
        int(storyboard_sequence_value)
        if isinstance(storyboard_sequence_value, int)
        else None
    )
    storyboard_total_value = payload.get("storyboard_total_steps")
    storyboard_total_steps = (
        int(storyboard_total_value)
        if isinstance(storyboard_total_value, int)
        else None
    )
    return PayloadSummary(
        path=path,
        chain_name=chain_name,
        template=template,
        outcomes=outcomes,
        description=description,
        summary_text=summary_text,
        overlay_id=payload.get("overlay_id"),
        overlay_layer=payload.get("overlay_layer"),
        overlays=overlay_stack,
        trace_id=trace_id,
        storyboard_id=storyboard_id,
        storyboard_step=storyboard_step,
        storyboard_sequence=storyboard_sequence,
        storyboard_total_steps=storyboard_total_steps,
    )


def compute_sync_state(summary: PayloadSummary) -> str:
    """Minimal narration sync indicator heuristic for demo use."""
    return "green" if summary.outcomes else "amber"


def emit_telemetry(
    summary: PayloadSummary,
    telemetry_path: Path,
    *,
    trace_id: Optional[str] = None,
    overlay_id: Optional[str] = None,
    overlay_layer: Optional[str] = None,
    overlays: Optional[List[Dict[str, str]]] = None,
) -> None:
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
    if trace_id:
        record["trace_id"] = trace_id
    if overlay_id:
        record["overlay_id"] = overlay_id
        record["overlay_layer"] = overlay_layer
    if overlays:
        record["overlays"] = overlays
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
    if summary.overlay_id:
        print(f"   Primary Layer: {summary.overlay_layer or 'unknown'} ({summary.overlay_id})", file=stream)
    if summary.overlays:
        layer_text = ", ".join(
            f"{item.get('layer_kind', '?') or '?'} ({item.get('overlay_id', '') or 'unknown'})"
            for item in summary.overlays
        )
        print(f"   Outlands Layers: {layer_text}", file=stream)
    if summary.storyboard_id:
        total = summary.storyboard_total_steps or "?"
        sequence = summary.storyboard_sequence or "?"
        step_label = summary.storyboard_step or "unknown"
        print(
            f"   Storyboard: {summary.storyboard_id} step {sequence}/{total} — {step_label}",
            file=stream,
        )
    # Minimal sync state indicator for demo runs
    try:
        sync_state = compute_sync_state(summary)
        print(f"   Sync: {sync_state}", file=stream)
    except Exception:
        pass
    print(f"   Payload: {relative_path}", file=stream)


def _ensure_action_log(context: UIContext) -> Path:
    if context.action_log_path is None:
        log_dir = context.repo_root / "logs" / "alfa_zero"
        log_dir.mkdir(parents=True, exist_ok=True)
        context.action_log_path = log_dir / "play_session_actions.log"
    else:
        context.action_log_path.parent.mkdir(parents=True, exist_ok=True)
    return context.action_log_path


def _append_action_log(
    context: UIContext,
    label: str,
    result: subprocess.CompletedProcess[str],
) -> Path:
    log_path = _ensure_action_log(context)
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    command_line = ""
    if isinstance(result.args, Sequence):
        command_line = " ".join(str(part) for part in result.args)
    elif result.args:
        command_line = str(result.args)

    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(f"=== {timestamp} {label} exit={result.returncode} ===\n")
        if command_line:
            handle.write(f"$ {command_line}\n")
        if result.stdout:
            handle.write(result.stdout)
            if not result.stdout.endswith("\n"):
                handle.write("\n")
        if result.stderr and result.stderr != result.stdout:
            handle.write("--- stderr ---\n")
            handle.write(result.stderr)
            if not result.stderr.endswith("\n"):
                handle.write("\n")
        handle.write("\n")
    return log_path


def _render_command_result(
    context: UIContext,
    label: str,
    result: subprocess.CompletedProcess[str],
    *,
    log_path: Optional[Path],
    quiet: bool = False,
) -> None:
    status = "✅" if result.returncode == 0 else "⚠️"
    if quiet:
        detail = f" (details: {log_path.name})" if log_path else ""
        print(f"{status} {label} — exit {result.returncode}{detail}", file=context.output_stream)
        return

    print(f"{status} {label} (exit {result.returncode})", file=context.output_stream)
    lines: List[str] = []
    if result.stdout:
        lines = result.stdout.strip().splitlines()
    trimmed = False
    if len(lines) > 20:
        trimmed = True
        head = lines[:8]
        tail = lines[-8:]
        lines = head + ["⋯"] + tail
    for line in lines:
        print(f"   {line}", file=context.output_stream)
    if not lines and result.returncode == 0:
        print("   (no output)", file=context.output_stream)
    if trimmed and log_path:
        print(f"   ⋯ output truncated; see {log_path.name}", file=context.output_stream)
    if result.stderr and result.stderr.strip() and result.stderr != result.stdout:
        stderr_lines = result.stderr.strip().splitlines()
        limit = min(8, len(stderr_lines))
        print("   stderr:", file=context.output_stream)
        for line in stderr_lines[:limit]:
            print(f"     {line}", file=context.output_stream)
        if len(stderr_lines) > limit and log_path:
            print(f"     ⋯ (see {log_path.name})", file=context.output_stream)


def _relative_to_repo(repo_root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def _log_storyboard_result(context: UIContext, result: "StoryboardRunResult") -> Path:
    log_path = _ensure_action_log(context)
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(f"=== {timestamp} storyboard {result.storyboard_id} ===\n")
        handle.write(f"trace_id: {result.trace_id}\n")
        handle.write(f"force: {result.force}\n")
        handle.write(f"payload_count: {len(result.payload_paths)}\n")
        for payload in result.payload_paths:
            handle.write(f"payload: {_relative_to_repo(context.repo_root, payload)}\n")
        handle.write(f"storyboard_log: {_relative_to_repo(context.repo_root, result.log_path)}\n\n")
    return log_path


def render_storyboard_status(context: UIContext) -> None:
    status = load_storyboard_status(context.repo_root, NIGHTLANDS_DUET_STORYBOARD)
    last_run_display = "never"
    eligible_display = "now"
    now = datetime.now(timezone.utc)
    if status.last_run_at is not None:
        last_run_display = status.last_run_at.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
        eligible_at = status.last_run_at + timedelta(seconds=status.cooldown_seconds)
        eligible_display = eligible_at.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    remaining = cooldown_remaining(status, now=now)
    print(
        f"Storyboard {NIGHTLANDS_DUET_STORYBOARD.title} ({NIGHTLANDS_DUET_STORYBOARD.storyboard_id})",
        file=context.output_stream,
    )
    print(f"   Cooldown: {NIGHTLANDS_DUET_STORYBOARD.cooldown_seconds // 60} minutes", file=context.output_stream)
    print(f"   Last run: {last_run_display}", file=context.output_stream)
    print(f"   Next eligible: {eligible_display}", file=context.output_stream)
    if remaining is None or remaining == 0:
        print("   Cooldown remaining: ready", file=context.output_stream)
    else:
        minutes, seconds = divmod(remaining, 60)
        print(
            f"   Cooldown remaining: {minutes}m {seconds}s (use 'storyboard run force' to override)",
            file=context.output_stream,
        )
    print(
        f"   Lore toggle: {'ON' if context.lore_layer_enabled else 'off — enable before run'}",
        file=context.output_stream,
    )
    print(
        f"   Music toggle: {'ON' if context.music_layer_enabled else 'off — enable before run'}",
        file=context.output_stream,
    )
    print(f"   Log: {_relative_to_repo(context.repo_root, status.log_path)}", file=context.output_stream)


def render_storyboard_preview(context: UIContext) -> None:
    for line in format_storyboard_preview(NIGHTLANDS_DUET_STORYBOARD):
        print(line, file=context.output_stream)


def execute_storyboard_run(context: UIContext, *, force: bool = False) -> None:
    print("🎭 Running Nightlands duet storyboard…", file=context.output_stream)
    try:
        result = run_storyboard_sequence(
            context.bridge,
            NIGHTLANDS_DUET_STORYBOARD,
            lore_enabled=context.lore_layer_enabled,
            music_enabled=context.music_layer_enabled,
            force=force,
        )
    except StoryboardGuardrailError as exc:
        print(f"⚠️  {exc}", file=context.output_stream)
        _log_session_event(
            context,
            event="storyboard_guardrail",
            extra={
                "storyboard_id": NIGHTLANDS_DUET_STORYBOARD.storyboard_id,
                "cooldown_seconds": NIGHTLANDS_DUET_STORYBOARD.cooldown_seconds,
                "force": force,
                "message": str(exc),
            },
        )
        return
    except Exception as exc:  # pragma: no cover - surfaced to operator
        print(f"⚠️  Storyboard execution failed: {exc}", file=context.output_stream)
        _log_session_event(
            context,
            event="storyboard_error",
            extra={
                "storyboard_id": NIGHTLANDS_DUET_STORYBOARD.storyboard_id,
                "force": force,
                "message": str(exc),
            },
        )
        return

    if NIGHTLANDS_DUET_STORYBOARD.steps:
        context.selected = NIGHTLANDS_DUET_STORYBOARD.steps[-1].cell

    for payload_path in result.payload_paths:
        summary = summarize_payload(payload_path)
        display_summary(summary, context.repo_root, stream=context.output_stream)
        trace_output = summary.trace_id or result.trace_id
        if trace_output:
            print(f"   Trace: {trace_output}", file=context.output_stream)
        if context.telemetry_path:
            emit_telemetry(
                summary,
                context.telemetry_path,
                trace_id=trace_output,
                overlay_id=summary.overlay_id,
                overlay_layer=summary.overlay_layer,
                overlays=summary.overlays,
            )
        _log_session_event(
            context,
            event="dispatch",
            extra={
                "storyboard_id": summary.storyboard_id,
                "storyboard_step": summary.storyboard_step,
                "storyboard_sequence": summary.storyboard_sequence,
                "storyboard_total_steps": summary.storyboard_total_steps,
                "trace_id": trace_output,
            },
        )

    story_log_path = _log_storyboard_result(context, result)
    print(
        f"   Storyboard log: {_relative_to_repo(context.repo_root, result.log_path)}",
        file=context.output_stream,
    )
    print(
        f"   Action log updated: {_relative_to_repo(context.repo_root, story_log_path)}",
        file=context.output_stream,
    )
    relative_payloads = [_relative_to_repo(context.repo_root, path) for path in result.payload_paths]
    _log_session_event(
        context,
        event="storyboard_run",
        extra={
            "storyboard_id": result.storyboard_id,
            "trace_id": result.trace_id,
            "payload_count": len(result.payload_paths),
            "cooldown_seconds": NIGHTLANDS_DUET_STORYBOARD.cooldown_seconds,
            "force": result.force,
            "payloads": relative_payloads,
            "storyboard_log": _relative_to_repo(context.repo_root, result.log_path),
        },
    )


def run_contract_suite(
    context: UIContext,
    *,
    cases: Optional[Sequence[str]] = None,
    quiet: bool = False,
) -> None:
    message = "🧪 Auto-running contract test suite…" if quiet else "🧪 Running contract test suite…"
    print(message, file=context.output_stream)
    try:
        result = context.bridge.run_contract_tests(cases=cases)
    except FileNotFoundError as exc:
        print(f"⚠️  {exc}", file=context.output_stream)
        return
    log_path = _append_action_log(context, "contract_tests", result)
    _render_command_result(context, "Contract tests", result, log_path=log_path, quiet=quiet)
    _log_session_event(context, event="contract_tests")


def run_manual_sync(
    context: UIContext,
    *,
    categories: Optional[Sequence[str]] = None,
    orders_subpath: Optional[str] = None,
    latest: Optional[int] = None,
    quiet: bool = False,
    label: str = "offline_sync",
    event: str = "offline_sync",
    announce: Optional[str] = None,
) -> None:
    message = announce or "🔄 Running offline sync…"
    print(message, file=context.output_stream)
    try:
        result = context.bridge.run_offline_sync(
            categories=categories,
            orders_subpath=orders_subpath,
            latest=latest,
            quiet=quiet,
        )
    except FileNotFoundError as exc:
        print(f"⚠️  {exc}", file=context.output_stream)
        return
    log_path = _append_action_log(context, label, result)
    _render_command_result(context, "Offline sync", result, log_path=log_path, quiet=quiet)
    _log_session_event(context, event=event)


def run_targeted_sync(
    context: UIContext,
    *,
    categories: Optional[Sequence[str]] = None,
    orders_subpath: Optional[str] = None,
    latest: Optional[int] = None,
    quiet: bool = True,
    dry_run: bool = False,
    label: str = "targeted_sync",
    event: str = "targeted_sync",
    announce: Optional[str] = None,
) -> None:
    message = announce or "🔄 Running targeted sync…"
    print(message, file=context.output_stream)
    try:
        result = context.bridge.run_targeted_sync(
            categories=categories,
            orders_subpath=orders_subpath,
            latest=latest,
            quiet=quiet,
            dry_run=dry_run,
            auto_confirm=True,
        )
    except FileNotFoundError as exc:
        print(f"⚠️  {exc}", file=context.output_stream)
        return
    log_path = _append_action_log(context, label, result)
    _render_command_result(context, "Targeted sync", result, log_path=log_path, quiet=quiet)
    _log_session_event(context, event=event)


def move_selection(context: UIContext, delta_row: int, delta_col: int) -> None:
    row = max(0, min(15, context.selected[0] + delta_row))
    col = max(0, min(15, context.selected[1] + delta_col))
    context.selected = (row, col)


def select_cell(context: UIContext, cell: Cell) -> None:
    context.selected = cell


def dispatch_selected(context: UIContext) -> None:
    cell = context.selected
    overlay_stack: List[Tuple[str, str]] = []
    if context.lore_layer_enabled:
        overlay_stack.append((LORE_OVERLAY_ID, LORE_LAYER_KIND))
    if context.music_layer_enabled:
        overlay_stack.append((MUSIC_OVERLAY_ID, MUSIC_LAYER_KIND))

    overlay_id = overlay_stack[0][0] if overlay_stack else None
    layer_kind = overlay_stack[0][1] if overlay_stack else None
    trace_id = generate_trace_id(
        cell_label(cell),
        DEFAULT_OVERLAY,
        overlay_id=overlay_id,
        overlays=overlay_stack,
    )

    if context.emit_events:
        if context.event_stream is None:
            print("⚠️  Event stream not configured; cannot emit dispatch.", file=context.output_stream)
            return
        event = {
            "cell": cell_label(cell),
            "source": "alfa_zero_ui",
            "ledger_note": "alfa_zero_ui",
            "overlay": DEFAULT_OVERLAY,
            "trace_id": trace_id,
        }
        if overlay_id:
            event["overlay_id"] = overlay_id
            event["overlay_layer"] = layer_kind
        if overlay_stack:
            event["overlays"] = [
                {"overlay_id": oid, "layer_kind": kind} for oid, kind in overlay_stack
            ]
        context.event_stream.write(json.dumps(event, ensure_ascii=False))
        context.event_stream.write("\n")
        context.event_stream.flush()
        print(f"🚀 Emitted overlay event for {event['cell']} (trace_id={trace_id})", file=context.output_stream)
        return

    try:
        destination = context.bridge.dispatch_cell(
            cell,
            trace_id=trace_id,
            overlay_id=overlay_id,
            layer_kind=layer_kind,
            overlays=overlay_stack,
        )
    except KeyError as exc:
        print(f"⚠️  {exc}", file=context.output_stream)
        return
    except Exception as exc:  # pragma: no cover - surfaced to operator
        print(f"⚠️  Dispatch failed: {exc}", file=context.output_stream)
        return

    summary = summarize_payload(destination)
    display_summary(summary, context.repo_root, stream=context.output_stream)
    # Show the correlation trace for operator visibility (non-event mode)
    if trace_id:
        print(f"   Trace: {trace_id}", file=context.output_stream)
    if context.telemetry_path:
        emit_telemetry(
            summary,
            context.telemetry_path,
            trace_id=trace_id,
            overlay_id=summary.overlay_id,
            overlay_layer=summary.overlay_layer,
            overlays=summary.overlays,
        )
    _log_session_event(context, event="dispatch")
    if context.auto_contracts:
        run_contract_suite(context, quiet=True)


def show_cell_info(cell: Cell, stream: TextIO = sys.stdout) -> None:
    label = cell_label(cell)
    if cell in CELL_MAPPINGS:
        chain, description = CELL_MAPPINGS[cell]
        print(f"{label}: {chain} — {description}", file=stream)
    else:
        print(f"{label}: unmapped cell", file=stream)


HELP_TEXT = """Commands:
    w / up         Move selection up
    s / down       Move selection down
    a / left       Move selection left
    d / right      Move selection right
    dispatch       Run the translator for the selected cell
        contracts      Run the contract test suite
    sync           Trigger a full offline exchange sync
    sync latest    Sync the most recent orders payload (optional count, add 'preview' for dry-run)
    sync orders X  Sync orders subdirectory X (for example emoji_runtime; add 'preview' to dry-run)
    info           Show mapping info for the selected cell
    map            List every mapped cell and chain
    lore           Lore overlay controls (lore status | lore enable | lore disable)
    music          Music overlay controls (music status | music enable | music disable)
    storyboard     Nightlands duet (storyboard status | storyboard preview | storyboard run [force])
    <cell>         Jump to a cell (formats: 04, 0,4, 0 4)
    show           Re-render the grid
    help           Show this help text
    quit           Exit the controller
"""


def interactive_loop(context: UIContext) -> None:
    print("Alfa Zero Overlay UI — navigate the grid and dispatch mapped chains.", file=context.output_stream)
    print("Type 'help' for command reference.\n", file=context.output_stream)
    overlay = compute_quilt_overlay(context.repo_root)
    render_grid(context.selected, stream=context.output_stream, overlay=overlay)
    render_footer(context, stream=context.output_stream)
    _log_session_event(context, event="session_start")

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
            overlay = compute_quilt_overlay(context.repo_root)
            render_grid(context.selected, stream=context.output_stream, overlay=overlay)
            render_footer(context, stream=context.output_stream)
            continue

        tokens = raw.split()
        if not tokens:
            continue
        command = tokens[0].lower()

        if command in {"quit", "q", "exit"}:
            break
        if command in {"help", "?"}:
            print(HELP_TEXT, file=context.output_stream)
            continue
        if command in {"show", "grid"}:
            overlay = compute_quilt_overlay(context.repo_root)
            render_grid(context.selected, stream=context.output_stream, overlay=overlay)
            render_footer(context, stream=context.output_stream)
            continue
        if command == "lore":
            if len(tokens) == 1 or tokens[1].lower() == "status":
                state = "enabled" if context.lore_layer_enabled else "disabled"
                print(
                    f"Lore overlay is currently {state}. Use 'lore enable' to opt-in or 'lore disable' to exit.",
                    file=context.output_stream,
                )
                continue
            action = tokens[1].lower()
            if action in {"enable", "on"}:
                if context.lore_layer_enabled:
                    print("Lore overlay already enabled.", file=context.output_stream)
                else:
                    context.lore_layer_enabled = True
                    print(
                        "Lore overlay enabled — overlay payloads will include outland-lore metadata after next dispatch.",
                        file=context.output_stream,
                    )
                continue
            if action in {"disable", "off"}:
                if not context.lore_layer_enabled:
                    print("Lore overlay already disabled.", file=context.output_stream)
                else:
                    context.lore_layer_enabled = False
                    print("Lore overlay disabled — returning to inland-only dispatches.", file=context.output_stream)
                continue
            print("⚠️  Usage: lore status | lore enable | lore disable", file=context.output_stream)
            continue
        if command == "music":
            if len(tokens) == 1 or tokens[1].lower() == "status":
                state = "enabled" if context.music_layer_enabled else "disabled"
                print(
                    f"Music overlay is currently {state}. Use 'music enable' to opt-in or 'music disable' to exit.",
                    file=context.output_stream,
                )
                continue
            action = tokens[1].lower()
            if action in {"enable", "on"}:
                if context.music_layer_enabled:
                    print("Music overlay already enabled.", file=context.output_stream)
                else:
                    context.music_layer_enabled = True
                    print(
                        "Music overlay enabled — payloads will include outland-music metadata after next dispatch.",
                        file=context.output_stream,
                    )
                continue
            if action in {"disable", "off"}:
                if not context.music_layer_enabled:
                    print("Music overlay already disabled.", file=context.output_stream)
                else:
                    context.music_layer_enabled = False
                    print("Music overlay disabled — returning to base cadence.", file=context.output_stream)
                continue
            print("⚠️  Usage: music status | music enable | music disable", file=context.output_stream)
            continue
        if command == "storyboard":
            option = tokens[1].lower() if len(tokens) > 1 else "status"
            if option == "status":
                render_storyboard_status(context)
                continue
            if option == "preview":
                render_storyboard_preview(context)
                continue
            if option == "run":
                force = any(token.lower() == "force" for token in tokens[2:])
                execute_storyboard_run(context, force=force)
                overlay = compute_quilt_overlay(context.repo_root)
                render_grid(context.selected, stream=context.output_stream, overlay=overlay)
                render_footer(context, stream=context.output_stream)
                continue
            print(
                "⚠️  Usage: storyboard status | storyboard preview | storyboard run [force]",
                file=context.output_stream,
            )
            continue
        if command in {"map"}:
            list_mapped_cells(context.output_stream)
            continue
        if command in {"contracts", "contract", "tests"}:
            run_contract_suite(context)
            overlay = compute_quilt_overlay(context.repo_root)
            render_grid(context.selected, stream=context.output_stream, overlay=overlay)
            render_footer(context, stream=context.output_stream)
            continue
        if command in {"sync", "resync"}:
            if len(tokens) == 1:
                run_manual_sync(context)
            elif tokens[1].lower() == "latest":
                count = 1
                dry_run = False
                for token in tokens[2:]:
                    lowered = token.lower()
                    if lowered in {"preview", "dry", "dry-run"}:
                        dry_run = True
                        continue
                    try:
                        count = max(1, int(token))
                    except ValueError:
                        print("⚠️  Provide a numeric count for 'sync latest'", file=context.output_stream)
                        break
                else:  # only executes if loop didn't break
                    label_suffix = "preview" if dry_run else "run"
                    run_targeted_sync(
                        context,
                        categories=["orders"],
                        latest=count,
                        quiet=True,
                        dry_run=dry_run,
                        label=f"targeted_sync_latest_{label_suffix}",
                        event=f"targeted_sync_latest_{label_suffix}",
                        announce=(
                            f"🔄 Previewing latest {count} orders payload(s)…" if dry_run
                            else f"🔄 Syncing latest {count} orders payload(s)…"
                        ),
                    )
                    overlay = compute_quilt_overlay(context.repo_root)
                    render_grid(context.selected, stream=context.output_stream, overlay=overlay)
                    render_footer(context, stream=context.output_stream)
                    continue
                # If we hit the ValueError branch, skip the overlay refresh
                continue
            elif tokens[1].lower() == "orders":
                if len(tokens) < 3:
                    print("⚠️  Provide a subdirectory for 'sync orders' (for example emoji_runtime)", file=context.output_stream)
                    continue
                subpath = tokens[2]
                dry_run = any(token.lower() in {"preview", "dry", "dry-run"} for token in tokens[3:])
                safe_label = subpath.replace("/", "_")
                label_suffix = "preview" if dry_run else "run"
                run_targeted_sync(
                    context,
                    categories=["orders"],
                    orders_subpath=subpath,
                    quiet=True,
                    dry_run=dry_run,
                    label=f"targeted_sync_orders_{safe_label}_{label_suffix}",
                    event=f"targeted_sync_orders_{label_suffix}",
                    announce=(
                        f"🔄 Previewing orders/{subpath}…" if dry_run else f"🔄 Syncing orders/{subpath}…"
                    ),
                )
                overlay = compute_quilt_overlay(context.repo_root)
                render_grid(context.selected, stream=context.output_stream, overlay=overlay)
                render_footer(context, stream=context.output_stream)
                continue
            else:
                print("⚠️  Unknown sync option", file=context.output_stream)
                continue
            overlay = compute_quilt_overlay(context.repo_root)
            render_grid(context.selected, stream=context.output_stream, overlay=overlay)
            render_footer(context, stream=context.output_stream)
            continue
        if command in {"info"}:
            show_cell_info(context.selected, context.output_stream)
            continue
        if command in {"w", "up"}:
            move_selection(context, -1, 0)
            overlay = compute_quilt_overlay(context.repo_root)
            render_grid(context.selected, stream=context.output_stream, overlay=overlay)
            render_footer(context, stream=context.output_stream)
            continue
        if command in {"s", "down"}:
            move_selection(context, 1, 0)
            overlay = compute_quilt_overlay(context.repo_root)
            render_grid(context.selected, stream=context.output_stream, overlay=overlay)
            render_footer(context, stream=context.output_stream)
            continue
        if command in {"a", "left"}:
            move_selection(context, 0, -1)
            overlay = compute_quilt_overlay(context.repo_root)
            render_grid(context.selected, stream=context.output_stream, overlay=overlay)
            render_footer(context, stream=context.output_stream)
            continue
        if command in {"d", "right"}:
            move_selection(context, 0, 1)
            overlay = compute_quilt_overlay(context.repo_root)
            render_grid(context.selected, stream=context.output_stream, overlay=overlay)
            render_footer(context, stream=context.output_stream)
            continue
        if command in {"dispatch", "fire", "send"}:
            dispatch_selected(context)
            overlay = compute_quilt_overlay(context.repo_root)
            render_grid(context.selected, stream=context.output_stream, overlay=overlay)
            continue

        try:
            cell = parse_cell_token(raw)
        except ValueError as exc:
            print(f"⚠️  {exc}", file=context.output_stream)
            continue

        select_cell(context, cell)
        overlay = compute_quilt_overlay(context.repo_root)
        render_grid(context.selected, stream=context.output_stream, overlay=overlay)
        render_footer(context, stream=context.output_stream)


def run_single_dispatch(context: UIContext, cell: Cell) -> None:
    select_cell(context, cell)
    dispatch_selected(context)


def build_context(
    outbox_override: Optional[str],
    telemetry: Optional[str],
    *,
    emit_events: bool,
    event_stream: Optional[TextIO],
    auto_contracts: bool,
    lore_enabled: bool = False,
    music_enabled: bool = False,
) -> UIContext:
    bridge = build_bridge(outbox_override)
    telemetry_path = Path(telemetry).expanduser().resolve() if telemetry else None
    output_stream = sys.stderr if emit_events and event_stream is sys.stdout else sys.stdout
    # Session metrics path (fixed location under repo logs)
    metrics_dir = bridge.repo_root / "logs" / "alfa_zero"
    metrics_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = metrics_dir / "session_metrics.jsonl"
    action_log_path = metrics_dir / "play_session_actions.log"

    # Lightweight session identifier
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    session_id = f"alfa_zero_ui-{os.getpid()}-{ts}"

    return UIContext(
        bridge=bridge,
        telemetry_path=telemetry_path,
        emit_events=emit_events,
        event_stream=event_stream,
        output_stream=output_stream,
        metrics_path=metrics_path,
        action_log_path=action_log_path,
        session_id=session_id,
        session_start_ts=datetime.now(timezone.utc),
        auto_contracts=auto_contracts,
        lore_layer_enabled=lore_enabled,
        music_layer_enabled=music_enabled,
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
    parser.add_argument(
        "--auto-contracts",
        action="store_true",
        help="Automatically run the contract test suite after each dispatch.",
    )
    parser.add_argument(
        "--enable-lore",
        action="store_true",
        help="Start with the Lore overlay toggle enabled (still requires operator consent when using the interactive loop).",
    )
    parser.add_argument(
        "--enable-music",
        action="store_true",
        help="Start with the Music overlay toggle enabled (pairs with lore for dual Outlands dispatches).",
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
        auto_contracts=args.auto_contracts,
        lore_enabled=args.enable_lore,
        music_enabled=args.enable_music,
    )

    try:
        if args.cell:
            cell = parse_cell_token(args.cell)
            run_single_dispatch(context, cell)
            return

        interactive_loop(context)
    finally:
        # Record session end
        _log_session_event(context, event="session_end")
        if close_stream and event_stream is not None:
            event_stream.close()


def _log_session_event(context: UIContext, *, event: str, extra: Optional[Dict[str, object]] = None) -> None:
    """Append a simple JSONL record for session metrics.

    Events: session_start, dispatch, contract_tests, offline_sync, offline_sync_latest,
    offline_sync_orders, targeted_sync, storyboard_run, storyboard_guardrail, storyboard_error,
    session_end. Extend with caution to keep downstream parsing simple.
    We track elapsed overlay time and dispatch count to support 70/30 analysis
    downstream.
    """
    if context.metrics_path is None:
        return
    now = datetime.now(timezone.utc)
    if event == "dispatch":
        context.dispatch_count += 1
    elapsed_s = None
    if context.session_start_ts is not None:
        elapsed_s = (now - context.session_start_ts).total_seconds()
    record = {
        "session_id": context.session_id,
        "event": event,
        "timestamp": now.isoformat().replace("+00:00", "Z"),
        "selected_cell": cell_label(context.selected),
        "dispatch_count": context.dispatch_count,
        "elapsed_s": elapsed_s,
        "source": "alfa_zero_ui",
        "lore_overlay_enabled": context.lore_layer_enabled,
        "music_overlay_enabled": context.music_layer_enabled,
    }
    if extra:
        for key, value in extra.items():
            if value is None:
                continue
            record[key] = value
    try:
        with context.metrics_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False))
            handle.write("\n")
    except Exception:
        pass


def compute_quilt_overlay(repo_root: Path) -> Dict[Cell, str]:
    """Compute a minimal telemetry quilt overlay for rows C–F.

    Sources: logs/alfa_zero/phase_2_latencies.jsonl
    - Row C (index 12): 🔥 count for high latency (>5000 ms)
    - Row D (13): ⚠️ count for pending/warning states
    - Row E (14): 📉 count if recent latency trend is worsening
    - Row F (15): ❌ count for failures
    """
    overlay: Dict[Cell, str] = {}
    log_path = repo_root / "logs" / "alfa_zero" / "phase_2_latencies.jsonl"
    durations: List[int] = []
    status_counts = {"failure": 0, "warning": 0, "pending": 0}
    high_latency = 0

    try:
        if log_path.exists():
            with log_path.open("r", encoding="utf-8") as handle:
                # Process last ~512 lines defensively
                lines = handle.readlines()[-512:]
            import json as _json
            for line in lines:
                try:
                    rec = _json.loads(line)
                except Exception:
                    continue
                d = rec.get("telemetry_duration_ms")
                if isinstance(d, (int, float)):
                    durations.append(int(d))
                    if d > 5000:
                        high_latency += 1
                st = rec.get("telemetry_status")
                if isinstance(st, str):
                    s = st.lower()
                    if s in status_counts:
                        status_counts[s] += 1
                    elif s == "success":
                        pass
                    else:
                        status_counts["warning"] += 1
    except Exception:
        # On any error, return empty overlay
        return overlay

    # Trend calculation (very simple): compare last 8 vs previous 8
    downtrend = 0
    if len(durations) >= 16:
        prev = durations[-16:-8]
        last = durations[-8:]
        try:
            prev_avg = sum(prev) / max(1, len(prev))
            last_avg = sum(last) / max(1, len(last))
            if last_avg > prev_avg * 1.15:
                # Scale to grid width
                downtrend = min(16, int((last_avg - prev_avg) / 500) + 1)
        except Exception:
            downtrend = 0

    # Map counts to grid rows
    fire = min(16, int(high_latency))
    warn = min(16, status_counts["pending"] + status_counts["warning"]) 
    fail = min(16, status_counts["failure"]) 

    for i in range(fire):
        overlay[(12, i)] = "🔥"
    for i in range(warn):
        overlay[(13, i)] = "⚠️"
    for i in range(downtrend):
        overlay[(14, i)] = "📉"
    for i in range(fail):
        overlay[(15, i)] = "❌"

    return overlay


def render_footer(context: UIContext, *, stream: TextIO = sys.stdout) -> None:
    """Render a one-line footer with session stats and auto-promotion state."""
    now = datetime.now(timezone.utc)
    elapsed_s = 0
    if context.session_start_ts is not None:
        elapsed_s = int((now - context.session_start_ts).total_seconds())
    mm = elapsed_s // 60
    ss = elapsed_s % 60
    auto_env = os.getenv("OVERLAY_AUTO_PROMOTE_FACTORY_ORDERS", "1").lower()
    auto_on = auto_env not in {"0", "false", "no"}
    contracts_state = "ON" if context.auto_contracts else "OFF"
    lore_state = "ON" if context.lore_layer_enabled else "OFF"
    music_state = "ON" if context.music_layer_enabled else "OFF"
    print(
        f"— Elapsed {mm:02d}:{ss:02d} | Dispatches {context.dispatch_count} | Auto-promote {'ON' if auto_on else 'OFF'} | Auto-contracts {contracts_state} | Lore {lore_state} | Music {music_state} —",
        file=stream,
    )


if __name__ == "__main__":  # pragma: no cover - manual entry point
    main()
