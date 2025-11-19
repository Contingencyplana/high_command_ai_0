"""Helpers for executing Alfa Zero storyboards with overlay guardrails."""

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple

from overlay_bridge import OverlayBridge, cell_label
from trace_utils import generate_trace_id

Cell = Tuple[int, int]
DEFAULT_OVERLAY = "overlay-alpha"


class StoryboardGuardrailError(RuntimeError):
    """Raised when storyboard execution would violate guardrails."""


@dataclass(frozen=True)
class StoryboardStep:
    label: str
    cell: Cell
    description: str
    overlay_stack: Sequence[Tuple[str, str]]
    requires_lore: bool = False
    requires_music: bool = False


@dataclass(frozen=True)
class Storyboard:
    storyboard_id: str
    title: str
    cooldown_seconds: int
    steps: Sequence[StoryboardStep]


@dataclass
class StoryboardStatus:
    storyboard_id: str
    last_run_at: datetime | None
    cooldown_seconds: int
    log_path: Path


@dataclass
class StoryboardRunResult:
    storyboard_id: str
    trace_id: str
    payload_paths: List[Path]
    log_path: Path
    recorded_at: datetime
    force: bool


def _storyboard_log_path(repo_root: Path, storyboard_id: str) -> Path:
    log_dir = repo_root / "logs" / "alfa_zero" / "storyboards"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir / f"{storyboard_id}_runs.jsonl"


def _read_last_run(log_path: Path) -> datetime | None:
    if not log_path.exists():
        return None
    try:
        with log_path.open("r", encoding="utf-8") as handle:
            lines = [line.strip() for line in handle if line.strip()]
    except OSError:
        return None
    if not lines:
        return None
    import json

    try:
        record = json.loads(lines[-1])
    except json.JSONDecodeError:
        return None
    stamp = record.get("timestamp")
    if not isinstance(stamp, str):
        return None
    try:
        return datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    except ValueError:
        return None


def load_storyboard_status(repo_root: Path, storyboard: Storyboard) -> StoryboardStatus:
    log_path = _storyboard_log_path(repo_root, storyboard.storyboard_id)
    last_run = _read_last_run(log_path)
    return StoryboardStatus(
        storyboard_id=storyboard.storyboard_id,
        last_run_at=last_run,
        cooldown_seconds=storyboard.cooldown_seconds,
        log_path=log_path,
    )


def format_storyboard_preview(storyboard: Storyboard) -> List[str]:
    lines: List[str] = [f"Storyboard: {storyboard.title} ({storyboard.storyboard_id})"]
    for index, step in enumerate(storyboard.steps, start=1):
        overlay_labels = ", ".join(f"{kind} ({oid})" for oid, kind in step.overlay_stack)
        lines.append(
            f"  {index}. {step.label} — cell {cell_label(step.cell)} | overlays: {overlay_labels}"
        )
        lines.append(f"     cue: {step.description}")
    lines.append(f"Cooldown: {storyboard.cooldown_seconds // 60} min between runs")
    return lines


def cooldown_remaining(status: StoryboardStatus, *, now: Optional[datetime] = None) -> Optional[int]:
    """Return remaining cooldown seconds for a storyboard, or 0/None when ready."""

    if status.last_run_at is None:
        return None
    current = now or datetime.now(timezone.utc)
    elapsed = current - status.last_run_at
    remaining = int(status.cooldown_seconds - elapsed.total_seconds())
    if remaining <= 0:
        return 0
    return remaining


def _enforce_cooldown(storyboard: Storyboard, *, status: StoryboardStatus, now: datetime, force: bool) -> None:
    if force or status.last_run_at is None:
        return
    remaining = cooldown_remaining(status, now=now)
    if remaining is None or remaining <= 0:
        return
    minutes, seconds = divmod(remaining, 60)
    raise StoryboardGuardrailError(
        f"Cooldown active for {storyboard.storyboard_id}. Try again in {minutes}m {seconds}s or pass force=True."
    )


def run_storyboard(
    bridge: OverlayBridge,
    storyboard: Storyboard,
    *,
    lore_enabled: bool,
    music_enabled: bool,
    force: bool = False,
    now: datetime | None = None,
) -> StoryboardRunResult:
    """Execute the storyboard steps sequentially and log the run."""

    moment = now or datetime.now(timezone.utc)
    status = load_storyboard_status(bridge.repo_root, storyboard)
    _enforce_cooldown(storyboard, status=status, now=moment, force=force)

    payload_paths: List[Path] = []
    trace_id = ""
    total_steps = len(storyboard.steps)

    for index, step in enumerate(storyboard.steps, start=1):
        if step.requires_lore and not lore_enabled:
            raise StoryboardGuardrailError("Lore overlay must be enabled before running this storyboard.")
        if step.requires_music and not music_enabled:
            raise StoryboardGuardrailError("Music overlay must be enabled before running this storyboard.")

        overlay_stack = list(step.overlay_stack)
        if trace_id:
            current_trace = trace_id
        else:
            current_trace = generate_trace_id(
                cell_label(step.cell),
                DEFAULT_OVERLAY,
                overlays=overlay_stack,
            )
            trace_id = current_trace

        primary_overlay_id = overlay_stack[0][0] if overlay_stack else None
        primary_layer = overlay_stack[0][1] if overlay_stack else None

        destination = bridge.dispatch_cell(
            step.cell,
            description=step.description,
            trace_id=current_trace,
            overlay_id=primary_overlay_id,
            layer_kind=primary_layer,
            overlays=overlay_stack,
            extra_payload={
                "storyboard_id": storyboard.storyboard_id,
                "storyboard_title": storyboard.title,
                "storyboard_step": step.label,
                "storyboard_sequence": index,
                "storyboard_total_steps": total_steps,
            },
        )
        payload_paths.append(destination)

    log_path = _storyboard_log_path(bridge.repo_root, storyboard.storyboard_id)
    _record_storyboard_run(
        log_path,
        storyboard=storyboard,
        trace_id=trace_id,
        payload_paths=payload_paths,
        recorded_at=moment,
        force=force,
    )

    return StoryboardRunResult(
        storyboard_id=storyboard.storyboard_id,
        trace_id=trace_id,
        payload_paths=payload_paths,
        log_path=log_path,
        recorded_at=moment,
        force=force,
    )


def _record_storyboard_run(
    log_path: Path,
    *,
    storyboard: Storyboard,
    trace_id: str,
    payload_paths: Iterable[Path],
    recorded_at: datetime,
    force: bool,
) -> None:
    import json

    entries = []
    for step in storyboard.steps:
        entries.append(
            {
                "label": step.label,
                "cell": cell_label(step.cell),
                "overlays": [
                    {"overlay_id": overlay_id, "layer_kind": layer_kind} for overlay_id, layer_kind in step.overlay_stack
                ],
            }
        )

    payload_strings: List[str] = []
    for path in payload_paths:
        try:
            payload_strings.append(str(path.relative_to(log_path.parent.parent.parent)))
        except ValueError:
            payload_strings.append(str(path))

    record = {
        "timestamp": recorded_at.isoformat().replace("+00:00", "Z"),
        "storyboard_id": storyboard.storyboard_id,
        "storyboard_title": storyboard.title,
        "trace_id": trace_id,
        "force": force,
        "cooldown_seconds": storyboard.cooldown_seconds,
        "steps": entries,
        "payloads": payload_strings,
    }
    try:
        with log_path.open("a", encoding="utf-8") as handle:
            json.dump(record, handle, ensure_ascii=False)
            handle.write("\n")
    except OSError:
        pass


NIGHTLANDS_DUET_STORYBOARD = Storyboard(
    storyboard_id="nightlands_duet_v1",
    title="Nightlands Duet - Lore + Music",
    cooldown_seconds=15 * 60,
    steps=(
        StoryboardStep(
            label="Lore Invocation",
            cell=(8, 10),
            description="Nightlands courier whispers through the dream relay; embers glow along the path.",
            overlay_stack=(("outland-lore-v1", "lore"),),
            requires_lore=True,
        ),
        StoryboardStep(
            label="Duet Crescendo",
            cell=(9, 11),
            description="Music swells beneath the lore chant as focus locks on the targeting relay.",
            overlay_stack=(
                ("outland-lore-v1", "lore"),
                ("outland-music-v1", "music"),
            ),
            requires_lore=True,
            requires_music=True,
        ),
        StoryboardStep(
            label="Twilight Strategy",
            cell=(8, 12),
            description="Project strategic directives through the targeting lattice as the second operator mirrors cadence.",
            overlay_stack=(
                ("outland-lore-v1", "lore"),
                ("outland-music-v1", "music"),
            ),
            requires_lore=True,
            requires_music=True,
        ),
        StoryboardStep(
            label="Counter Pulse",
            cell=(9, 12),
            description="Stabilize tempo along the targeting corridor and defend against Nightland counter-chants.",
            overlay_stack=(
                ("outland-lore-v1", "lore"),
                ("outland-music-v1", "music"),
            ),
            requires_lore=True,
            requires_music=True,
        ),
    ),
)
