"""Shared overlay bridge for Alfa Zero battlegrid interactions."""

from __future__ import annotations

import importlib.util
import json
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Tuple

Cell = Tuple[int, int]

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

    def dispatch_cell(self, cell: Cell, *, description: str | None = None) -> Path:
        if cell not in CELL_MAPPINGS:
            raise KeyError(f"Cell {cell_label(cell)} is not mapped to a chain yet")
        chain_name, default_description = CELL_MAPPINGS[cell]
        description = description or default_description
        return self.dispatch_chain_name(chain_name, cell=cell, description=description)

    def dispatch_cells(self, cells: Iterable[Cell]) -> Dict[str, Path]:
        results: Dict[str, Path] = {}
        for cell in cells:
            path = self.dispatch_cell(cell)
            results[cell_label(cell)] = path
        return results

    def dispatch_chain_name(
        self,
        chain_name: str,
        *,
        cell: Cell | None = None,
        description: str | None = None,
    ) -> Path:
        if chain_name not in self.sample_chains:
            raise KeyError(f"Chain {chain_name} missing from sample_chains.json")
        chain = self.sample_chains[chain_name]
        return self.dispatch_raw_chain(chain, chain_name=chain_name, cell=cell, description=description)

    def dispatch_raw_chain(
        self,
        chain,
        *,
        chain_name: str | None = None,
        cell: Cell | None = None,
        description: str | None = None,
    ) -> Path:
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
        hint = chain_name or "custom_chain"
        return _write_payload(self.outbox, f"alfa_zero_{hint}", payload)


def build_bridge(outbox_override: str | None = None) -> OverlayBridge:
    script_dir = Path(__file__).resolve().parent
    repo_root = find_repo_root(script_dir)
    translator = load_translator(repo_root)
    sample_chains = load_sample_chains(repo_root)
    outbox = resolve_outbox(repo_root, outbox_override)
    return OverlayBridge(repo_root, translator, sample_chains, outbox)


__all__ = [
    "CELL_MAPPINGS",
    "OverlayBridge",
    "build_bridge",
    "cell_label",
]
