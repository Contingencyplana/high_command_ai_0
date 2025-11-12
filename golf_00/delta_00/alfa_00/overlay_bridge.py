# pyright: reportMissingImports=false
"""Shared overlay bridge for Alfa Zero battlegrid interactions.

Adds optional (default-on) promotion of emoji-runtime payloads to
factory-order envelopes to reduce manual dev-ops steps during play.
Disable with env `OVERLAY_AUTO_PROMOTE_FACTORY_ORDERS=0`.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import os
import subprocess
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Tuple
import re

try:
    from fun_flags import load_fun_flags, FunFlags
except ModuleNotFoundError:  # pragma: no cover - fallback for CLI runners
    from golf_00.delta_00.alfa_00.fun_flags import load_fun_flags, FunFlags

Cell = Tuple[int, int]

_OVERLAY_ID_PATTERN = re.compile(r"^[a-z0-9._-]{1,64}$")
VALID_LAYER_KINDS = {"lore", "music", "ritual", "emergent"}


@dataclass(frozen=True)
class OverlayMetadata:
    overlay_id: str | None
    layer_kind: str | None


@dataclass(frozen=True)
class OverlaySpec:
    overlay_id: str
    layer_kind: str


OverlayInput = OverlayMetadata | OverlaySpec | dict[str, str] | tuple[str, str]


def _prepare_overlay_metadata(overlay_id: str | None, layer_kind: str | None) -> OverlayMetadata:
    if overlay_id is None and layer_kind is None:
        return OverlayMetadata(None, None)
    if not overlay_id:
        raise ValueError("overlay_id must be provided when layer_kind is set")
    if layer_kind is None:
        raise ValueError("layer_kind must accompany overlay_id")
    normalized = overlay_id.strip().lower()
    if not _OVERLAY_ID_PATTERN.match(normalized):
        raise ValueError(
            "overlay_id must be 1-64 chars using lowercase letters, digits, '.', '-', or '_'"
        )
    if layer_kind not in VALID_LAYER_KINDS:
        raise ValueError(f"layer_kind must be one of {sorted(VALID_LAYER_KINDS)}")
    return OverlayMetadata(normalized, layer_kind)


def _coerce_overlay_spec(overlay_id: str | None, layer_kind: str | None) -> OverlaySpec:
    meta = _prepare_overlay_metadata(overlay_id, layer_kind)
    if meta.overlay_id is None or meta.layer_kind is None:
        raise ValueError("overlay specification requires both overlay_id and layer_kind")
    return OverlaySpec(meta.overlay_id, meta.layer_kind)


def _normalize_overlay_inputs(
    overlay_id: str | None,
    layer_kind: str | None,
    overlays: Sequence[OverlayInput] | None,
) -> tuple[OverlaySpec | None, list[OverlaySpec]]:
    overlay_list: list[OverlaySpec] = []
    if overlays:
        for item in overlays:
            if isinstance(item, OverlaySpec):
                overlay_list.append(item)
            elif isinstance(item, OverlayMetadata):
                if item.overlay_id and item.layer_kind:
                    overlay_list.append(OverlaySpec(item.overlay_id, item.layer_kind))
                else:
                    raise ValueError("overlay metadata entries must include overlay_id and layer_kind")
            elif isinstance(item, dict):
                overlay_list.append(_coerce_overlay_spec(item.get("overlay_id"), item.get("layer_kind")))
            elif isinstance(item, tuple) and len(item) == 2:
                overlay_list.append(_coerce_overlay_spec(item[0], item[1]))
            else:
                raise TypeError("overlay entries must be OverlaySpec, OverlayMetadata, dict, or (id, kind) tuple")

    primary: OverlaySpec | None = None
    if overlay_id is not None or layer_kind is not None:
        primary = _coerce_overlay_spec(overlay_id, layer_kind)
    elif overlay_list:
        primary = overlay_list[0]

    if primary:
        combined: list[OverlaySpec] = [primary]
        for spec in overlay_list:
            if spec.overlay_id == primary.overlay_id and spec.layer_kind == primary.layer_kind:
                continue
            combined.append(spec)
        overlay_list = combined
    return primary, overlay_list

# Centralized mapping between grid cells and Level-0 emoji chains.
CELL_MAPPINGS: Dict[Cell, Tuple[str, str]] = {
    (0, 4): ("basic_ritual_forge", "Forge ritual from mountain supply line"),
    (1, 6): ("rapid_ore_pulse", "Accelerate ore extraction cadence"),
    (4, 12): ("guarded_delivery_wall", "Secure delivery to fortress wall"),
    (5, 8): ("harvest_guarded_wall", "Harvest and reinforce the garden wall"),
    (8, 10): ("signal_loop_dream", "Signal the dream relay for telemetry"),
    (8, 11): ("signal_loop_coordination", "Align targeting array for allied volleys"),
    (8, 12): ("signal_loop_strategy", "Project strategic directives through the targeting lattice"),
    (8, 8): ("dream_transmute_bless", "Transmute dream residue into a blessing"),
    (9, 11): ("signal_loop_focus", "Tighten the targeting relay for precision guidance"),
    (9, 10): ("signal_loop_command", "Channel command signals across the targeting relay"),
    (9, 12): ("signal_loop_tempo", "Stabilize tempo along the targeting corridor"),
    (10, 10): ("signal_loop_analysis", "Analyze targeting data for actionable patterns"),
    (10, 11): ("signal_loop_cover", "Maintain targeting cover for the logistics wing"),
    (10, 12): ("signal_loop_shield", "Reinforce targeting shield for the logistics advance"),
    (10, 1): ("river_signal_loop", "Loop river telemetry and flag risks"),
    (12, 0): ("conditional_repeat_seed", "Seed repeatable growth cadence"),
}

HEX_DIGITS = "0123456789ABCDEF"


def cell_label(cell: Cell) -> str:
    """Convert a (row, col) tuple into Alfa Zero's hex grid notation."""

    row, col = cell
    return f"{HEX_DIGITS[row]}{HEX_DIGITS[col]}"


def find_repo_root(start: Path) -> Path:
    """Locate the repository root by walking upward until .git exists."""

    for parent in [start] + list(start.parents):
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Could not locate repository root (missing .git directory)")


def load_module_from_path(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot import {name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module


def load_translator(repo_root: Path):
    translator_path = repo_root / "golf_00" / "delta_00" / "alfa_04" / "emoji_translator.py"
    return load_module_from_path("emoji_translator", translator_path)


def load_factory_adapter(repo_root: Path):
    adapter_path = repo_root / "golf_00" / "delta_00" / "alfa_04" / "factory_adapter.py"
    return load_module_from_path("factory_adapter", adapter_path)


def load_sample_chains(repo_root: Path) -> Dict[str, str]:
    sample_path = repo_root / "golf_00" / "delta_00" / "alfa_04" / "sample_chains.json"
    with sample_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("sample_chains.json must contain a JSON object of name → chain")
    return {str(name): str(chain) for name, chain in data.items()}


def resolve_outbox(repo_root: Path, override: str | None) -> Path:
    if override:
        outbox = Path(override)
        if not outbox.is_absolute():
            outbox = repo_root / outbox
    else:
        outbox = repo_root / "outbox" / "orders" / "emoji_runtime"
    return outbox


def resolve_factory_outbox(repo_root: Path) -> Path:
    """Return path where factory-order envelopes should be written."""
    return repo_root / "outbox" / "orders" / "factory_orders"


def _sanitize_hint(hint: str) -> str:
    return "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in hint)


def _write_payload(outbox: Path, filename_hint: str, payload: Dict[str, object]) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    filename = f"{timestamp}_{_sanitize_hint(filename_hint)}.json"
    destination = outbox / filename
    outbox.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return destination


@dataclass
class OverlayBridge:
    repo_root: Path
    translator: object
    sample_chains: Dict[str, str]
    outbox: Path
    _factory_adapter: object | None = None
    fun_flags: FunFlags | None = None

    def dispatch_cell(
        self,
        cell: Cell,
        *,
        description: str | None = None,
        trace_id: str | None = None,
        overlay_id: str | None = None,
        layer_kind: str | None = None,
        overlays: Sequence[OverlayInput] | None = None,
        extra_payload: dict[str, object] | None = None,
    ) -> Path:
        if cell not in CELL_MAPPINGS:
            raise KeyError(f"Cell {cell_label(cell)} is not mapped to a chain yet")
        chain_name, default_description = CELL_MAPPINGS[cell]
        description = description or default_description
        return self.dispatch_chain_name(
            chain_name,
            cell=cell,
            description=description,
            trace_id=trace_id,
            overlay_id=overlay_id,
            layer_kind=layer_kind,
            overlays=overlays,
            extra_payload=extra_payload,
        )

    def dispatch_cells(self, cells: Iterable[Cell]) -> Dict[str, Path]:
        results: Dict[str, Path] = {}
        for cell in cells:
            path = self.dispatch_cell(cell)
            results[cell_label(cell)] = path
        return results

    def run_contract_tests(self, *, cases: Sequence[str] | None = None) -> subprocess.CompletedProcess[str]:
        """Execute the contract test suite and return the completed process."""

        cmd = [sys.executable, "-m", "tools.contract_test_runner"]
        if cases:
            for case in cases:
                cmd.extend(["--case", case])
        return subprocess.run(cmd, cwd=self.repo_root, capture_output=True, text=True)

    def run_offline_sync(
        self,
        *,
        categories: Sequence[str] | None = None,
        orders_subpath: str | None = None,
        latest: int | None = None,
        quiet: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        """Run the offline exchange sync with optional filters."""

        script = self.repo_root / "tools" / "offline_sync_exchange.py"
        if not script.exists():
            raise FileNotFoundError(f"Offline sync script missing at {script}")

        cmd = [sys.executable, str(script)]
        if categories:
            for category in categories:
                cmd.extend(["--category", category])
        if orders_subpath:
            cmd.extend(["--orders-subpath", orders_subpath])
        if latest is not None:
            cmd.extend(["--latest", str(latest)])
        if quiet:
            cmd.append("--quiet")

        return subprocess.run(cmd, cwd=self.repo_root, capture_output=True, text=True)

    def run_targeted_sync(
        self,
        *,
        categories: Sequence[str] | None = None,
        orders_subpath: str | None = None,
        latest: int | None = None,
        quiet: bool = True,
        dry_run: bool = False,
        auto_confirm: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        """Invoke the targeted sync helper with optional filtering."""

        cmd = [sys.executable, "-m", "tools.targeted_sync"]
        if categories:
            for category in categories:
                cmd.extend(["--category", category])
        if orders_subpath:
            cmd.extend(["--orders-subpath", orders_subpath])
        if latest is not None:
            cmd.extend(["--latest", str(latest)])
        if not quiet:
            cmd.append("--no-quiet")
        if dry_run:
            cmd.append("--dry-run")
        if auto_confirm:
            cmd.append("--yes")

        return subprocess.run(cmd, cwd=self.repo_root, capture_output=True, text=True)

    def dispatch_chain_name(
        self,
        chain_name: str,
        *,
        cell: Cell | None = None,
        description: str | None = None,
        trace_id: str | None = None,
        overlay_id: str | None = None,
        layer_kind: str | None = None,
        overlays: Sequence[OverlayInput] | None = None,
        extra_payload: dict[str, object] | None = None,
    ) -> Path:
        if chain_name not in self.sample_chains:
            raise KeyError(f"Chain {chain_name} missing from sample_chains.json")
        chain = self.sample_chains[chain_name]
        return self.dispatch_raw_chain(
            chain,
            chain_name=chain_name,
            cell=cell,
            description=description,
            trace_id=trace_id,
            overlay_id=overlay_id,
            layer_kind=layer_kind,
            overlays=overlays,
            extra_payload=extra_payload,
        )

    def dispatch_raw_chain(
        self,
        chain,
        *,
        chain_name: str | None = None,
        cell: Cell | None = None,
        description: str | None = None,
        trace_id: str | None = None,
        overlay_id: str | None = None,
        layer_kind: str | None = None,
        overlays: Sequence[OverlayInput] | None = None,
        extra_payload: dict[str, object] | None = None,
    ) -> Path:
        primary_overlay, overlay_stack = _normalize_overlay_inputs(overlay_id, layer_kind, overlays)
        overlay_id = primary_overlay.overlay_id if primary_overlay else None
        layer_kind = primary_overlay.layer_kind if primary_overlay else None
        payload = dict(self.translator.translate_chain(chain))
        if "created_at" not in payload:
            created_at = datetime.now(timezone.utc)
            payload["created_at"] = created_at.isoformat().replace("+00:00", "Z")
            stub = payload.get("telemetry_stub")
            if isinstance(stub, dict):
                intent = payload.get("intent") if isinstance(payload.get("intent"), dict) else {}
                actor = str(intent.get("actor", "unbound"))
                action = str(intent.get("action", "command"))
                stamp = created_at.strftime("%Y%m%dT%H%M%S%f")[:-3] + "Z"
                stub.setdefault("batch_id", f"{actor}-{action}-{stamp}")
                stub.setdefault("ritual", actor)
                glyph_chain = payload.get("glyph_chain")
                if isinstance(glyph_chain, Sequence):
                    stub.setdefault("units_processed", len(glyph_chain))
                else:
                    stub.setdefault("units_processed", len(payload.get("raw", [])))
                stub.setdefault("status", "success")
                stub.setdefault("duration_ms", 0)
        payload["source"] = "golf_00/delta_00/alfa_00/overlay_bridge.py"
        if chain_name:
            payload["chain_name"] = chain_name
        if description:
            payload["overlay_description"] = description
        if cell:
            payload["overlay_cell"] = {"row": cell[0], "col": cell[1], "label": cell_label(cell)}
        # tag active FUN flags for telemetry segmentation
        try:
            flags = self.fun_flags.as_dict() if self.fun_flags else load_fun_flags(self.repo_root).as_dict()
            payload["fun_flags"] = flags
        except Exception:
            payload.setdefault("fun_flags", {})

        if trace_id:
            payload["trace_id"] = trace_id
            stub = payload.get("telemetry_stub")
            if isinstance(stub, dict):
                stub["trace_id"] = trace_id

        if overlay_stack:
            payload["overlays"] = [
                {"overlay_id": spec.overlay_id, "layer_kind": spec.layer_kind} for spec in overlay_stack
            ]
            stub = payload.get("telemetry_stub")
            if isinstance(stub, dict):
                stub["overlays"] = [
                    {"overlay_id": spec.overlay_id, "layer_kind": spec.layer_kind} for spec in overlay_stack
                ]

        if overlay_id:
            payload["overlay_id"] = overlay_id
            payload["overlay_layer"] = layer_kind
            stub = payload.get("telemetry_stub")
            if isinstance(stub, dict):
                stub["overlay_id"] = overlay_id
                stub["overlay_layer"] = layer_kind

        if extra_payload:
            for key, value in extra_payload.items():
                if value is None:
                    continue
                payload[key] = value

        # Evaluate guardrails in log-only mode (no enforcement)
        try:
            # Dynamically load evaluator to avoid hard import-time path dependence
            eval_module = load_module_from_path(
                "fun_guardrail_eval_module", self.repo_root / "tools" / "fun_guardrail_eval.py"
            )
            if hasattr(eval_module, "evaluate_payload"):
                eval_module.evaluate_payload(self.repo_root, payload, payload.get("fun_flags", {}))  # type: ignore[attr-defined]
        except Exception:
            # Non-fatal: guardrail evaluation should never block dispatch
            pass

        hint = chain_name or "custom_chain"
        destination = _write_payload(self.outbox, f"alfa_zero_{hint}", payload)
        self._log_phase_two_dispatch(
            payload,
            destination,
            trace_id=trace_id,
            overlay_id=overlay_id,
            layer_kind=layer_kind,
            overlays=overlay_stack,
        )
        # Auto-promote to factory-order unless disabled via env
        auto = os.getenv("OVERLAY_AUTO_PROMOTE_FACTORY_ORDERS", "1").lower() not in {"0", "false", "no"}
        if auto:
            try:
                self._maybe_promote_factory_order(payload, chain_name)
            except Exception:
                # Non-fatal; operator can inspect emoji payload even if promotion fails
                pass
        return destination

    def _maybe_promote_factory_order(self, emoji_payload: Dict[str, object], chain_name: str | None) -> None:
        """Promote an emoji-runtime payload to a factory-order envelope and save it.

        Uses default metadata suitable for Alfa Zero. Safe to call multiple times.
        """

        # Lazy-load to avoid hard dependency at import time
        if self._factory_adapter is None:
            self._factory_adapter = load_factory_adapter(self.repo_root)

        adapter = self._factory_adapter
        if not adapter:
            return

        created_at = None
        try:
            created_at = str(emoji_payload.get("created_at"))  # type: ignore[arg-type]
        except Exception:
            created_at = None

        safe_chain = chain_name or str(emoji_payload.get("chain_name") or "command")
        order_id = adapter.derive_order_id(safe_chain, created_at)

        # Defaults can be tuned later or read from config; keep deterministic now
        issued_by = "high_command_alfa_zero"
        target = "toyfoundry_ai_0"
        priority = "realtime"
        requires_ack = False

        order = adapter.emoji_runtime_to_factory_order(
            emoji_payload,
            order_id=order_id,
            issued_by=issued_by,
            target=target,
            priority=priority,
            requires_ack=requires_ack,
        )

        dst_dir = resolve_factory_outbox(self.repo_root)
        _ = _write_payload(dst_dir, order_id, order)

    def _log_phase_two_dispatch(
        self,
        payload: Dict[str, object],
        destination: Path,
        *,
        trace_id: str | None = None,
        overlay_id: str | None = None,
        layer_kind: str | None = None,
        overlays: Sequence[OverlaySpec] | None = None,
    ) -> None:
        """Append a Phase 2 latency stub entry for later reconciliation."""

        log_dir = self.repo_root / "logs" / "alfa_zero"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / "phase_2_latencies.jsonl"

        dispatched_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

        try:
            relative_outbox = destination.relative_to(self.repo_root)
        except ValueError:
            relative_outbox = destination

        telemetry_stub = payload.get("telemetry_stub") if isinstance(payload.get("telemetry_stub"), dict) else {}
        batch_id = str(telemetry_stub.get("batch_id") or dispatched_at)
        entry = {
            "dispatched_at": dispatched_at,
            "chain_name": payload.get("chain_name"),
            "template": payload.get("template"),
            "overlay_cell": payload.get("overlay_cell"),
            "outbox_path": str(relative_outbox),
            "batch_id": batch_id,
            "trace_id": trace_id,
            "overlay_id": overlay_id,
            "overlay_layer": layer_kind,
            "overlays": [
                {"overlay_id": spec.overlay_id, "layer_kind": spec.layer_kind} for spec in overlays or []
            ]
            if overlays
            else None,
            "storyboard_id": payload.get("storyboard_id"),
            "storyboard_step": payload.get("storyboard_step"),
            "storyboard_sequence": payload.get("storyboard_sequence"),
            "storyboard_total_steps": payload.get("storyboard_total_steps"),
            "telemetry_received_at": None,
            "telemetry_duration_ms": None,
            "telemetry_status": "pending",
        }

        try:
            with log_path.open("a", encoding="utf-8") as handle:
                json.dump(entry, handle, ensure_ascii=False)
                handle.write("\n")
        except OSError:
            pass

        phase_dir = log_dir / "phase_2"
        phase_dir.mkdir(parents=True, exist_ok=True)
        entry_path = phase_dir / f"{batch_id}.json"
        try:
            with entry_path.open("w", encoding="utf-8") as handle:
                json.dump(entry, handle, ensure_ascii=False, indent=2)
                handle.write("\n")
        except OSError:
            pass


def record_phase_two_telemetry(
    batch_id: str,
    *,
    received_at: datetime | None = None,
    duration_ms: int | None = None,
    status: str = "success",
) -> None:
    """Update a Phase 2 latency entry when telemetry arrives."""

    script_dir = Path(__file__).resolve().parent
    repo_root = find_repo_root(script_dir)
    entry_path = repo_root / "logs" / "alfa_zero" / "phase_2" / f"{batch_id}.json"
    if not entry_path.exists():
        raise FileNotFoundError(f"Phase 2 entry for batch {batch_id!r} not found at {entry_path}")

    with entry_path.open("r", encoding="utf-8") as handle:
        entry = json.load(handle)
    if not isinstance(entry, dict):
        entry = {}

    timestamp = received_at or datetime.now(timezone.utc)
    entry["telemetry_received_at"] = timestamp.isoformat().replace("+00:00", "Z")
    if duration_ms is not None:
        entry["telemetry_duration_ms"] = duration_ms
    elif isinstance(entry.get("dispatched_at"), str):
        try:
            dispatched_at = datetime.fromisoformat(entry["dispatched_at"].replace("Z", "+00:00"))
            entry["telemetry_duration_ms"] = int(
                (timestamp - dispatched_at).total_seconds() * 1000
            )
        except Exception:  # pragma: no cover - defensive parsing
            entry.setdefault("telemetry_duration_ms", None)
    entry["telemetry_status"] = status

    with entry_path.open("w", encoding="utf-8") as handle:
        json.dump(entry, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    log_path = repo_root / "logs" / "alfa_zero" / "phase_2_latencies.jsonl"
    update_record = {
        "batch_id": batch_id,
        "trace_id": entry.get("trace_id"),
        "telemetry_received_at": entry["telemetry_received_at"],
        "telemetry_duration_ms": entry.get("telemetry_duration_ms"),
        "telemetry_status": status,
        "event": "telemetry_update",
    }
    try:
        with log_path.open("a", encoding="utf-8") as handle:
            json.dump(update_record, handle, ensure_ascii=False)
            handle.write("\n")
    except OSError:
        pass


def build_bridge(outbox_override: str | None = None) -> OverlayBridge:
    script_dir = Path(__file__).resolve().parent
    repo_root = find_repo_root(script_dir)
    translator = load_translator(repo_root)
    sample_chains = load_sample_chains(repo_root)
    outbox = resolve_outbox(repo_root, outbox_override)
    flags = load_fun_flags(repo_root)
    return OverlayBridge(repo_root, translator, sample_chains, outbox, _factory_adapter=None, fun_flags=flags)


__all__ = [
    "CELL_MAPPINGS",
    "OverlayBridge",
    "build_bridge",
    "record_phase_two_telemetry",
    "cell_label",
]
