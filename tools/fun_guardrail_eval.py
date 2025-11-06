from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Tuple


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _append_jsonl(path: Path, record: Dict[str, object]) -> None:
    try:
        with path.open("a", encoding="utf-8") as handle:
            json.dump(record, handle, ensure_ascii=False)
            handle.write("\n")
    except OSError:
        pass


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return int(str(raw).strip())
    except Exception:
        return default


def _parse_actor_action(batch_id: str) -> Tuple[str, str]:
    # Expected format: "{actor}-{action}-{stamp}"
    if not batch_id:
        return ("unbound", "command")
    parts = str(batch_id).split("-")
    if len(parts) < 3:
        return (parts[0] or "unbound", parts[1] if len(parts) > 1 else "command")
    return (parts[0] or "unbound", parts[1] or "command")


def _recent_dispatch_count(repo_root: Path, actor: str, window_seconds: int) -> int:
    log_path = repo_root / "logs" / "alfa_zero" / "phase_2_latencies.jsonl"
    if not log_path.exists():
        return 0
    now = datetime.now(timezone.utc)
    since = now - timedelta(seconds=window_seconds)
    count = 0
    try:
        with log_path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except Exception:
                    continue
                if not isinstance(entry, dict):
                    continue
                ts_raw = entry.get("dispatched_at")
                batch = entry.get("batch_id")
                if not isinstance(ts_raw, str) or not isinstance(batch, str):
                    continue
                try:
                    ts = datetime.fromisoformat(ts_raw.replace("Z", "+00:00"))
                except Exception:
                    continue
                a, _ = _parse_actor_action(batch)
                if a == actor and ts >= since:
                    count += 1
    except OSError:
        return 0
    return count


def _load_thresholds(repo_root: Path) -> Dict[str, int]:
    cfg_path = repo_root / "exchange" / "config.json"
    base = {
        "LOOT_MAX_UNITS_PER_PAYLOAD": 50,
        "XP_MAX_ACTIONS_PER_MIN": 20,
        "UNITS_PER_MIN_MAX": 200,
    }
    try:
        data = json.loads(cfg_path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            guard = data.get("fun_guardrails")
            if isinstance(guard, dict):
                for k in list(base.keys()):
                    v = guard.get(k)
                    if isinstance(v, int):
                        base[k] = v
    except Exception:
        pass
    # env overrides
    for k in list(base.keys()):
        base[k] = _env_int(k, base[k])
    return base


def _append_observation(repo_root: Path, actor: str, units: int, ts: datetime) -> None:
    log_dir = repo_root / "logs" / "fun_guardrails"
    _ensure_dir(log_dir)
    rec = {
        "ts": ts.isoformat().replace("+00:00", "Z"),
        "actor": actor,
        "units": units,
    }
    _append_jsonl(log_dir / "observations.jsonl", rec)


def _units_last_minute(repo_root: Path, actor: str, window_seconds: int = 60) -> int:
    log_path = repo_root / "logs" / "fun_guardrails" / "observations.jsonl"
    if not log_path.exists():
        return 0
    now = datetime.now(timezone.utc)
    since = now - timedelta(seconds=window_seconds)
    total = 0
    try:
        with log_path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except Exception:
                    continue
                if not isinstance(entry, dict):
                    continue
                if entry.get("actor") != actor:
                    continue
                ts_raw = entry.get("ts")
                if not isinstance(ts_raw, str):
                    continue
                try:
                    ts = datetime.fromisoformat(ts_raw.replace("Z", "+00:00"))
                except Exception:
                    continue
                if ts >= since:
                    try:
                        total += int(entry.get("units", 0))
                    except Exception:
                        continue
    except OSError:
        return 0
    return total


def evaluate_payload(repo_root: Path, payload: Dict[str, object], flags: Dict[str, bool]) -> List[Dict[str, object]]:
    """Return a list of would-clamp triggers and emit log events (no enforcement).

    Checks:
    - loot_units_per_payload: units_processed > LOOT_MAX_UNITS_PER_PAYLOAD
    - xp_velocity: recent dispatch count per actor in last 60s > XP_MAX_ACTIONS_PER_MIN
    Thresholds via env:
      LOOT_MAX_UNITS_PER_PAYLOAD (default 50)
      XP_MAX_ACTIONS_PER_MIN (default 20)
    """

    if not flags:
        flags = {}
    now = datetime.now(timezone.utc)

    thresholds = _load_thresholds(repo_root)
    loot_cap = thresholds["LOOT_MAX_UNITS_PER_PAYLOAD"]
    xp_cap = thresholds["XP_MAX_ACTIONS_PER_MIN"]
    upm_cap = thresholds["UNITS_PER_MIN_MAX"]

    telemetry = payload.get("telemetry_stub") if isinstance(payload.get("telemetry_stub"), dict) else {}
    batch_id = str(getattr(telemetry, "get", lambda k, d=None: None)("batch_id") or payload.get("batch_id") or "")
    actor, action = _parse_actor_action(batch_id)
    units = 0
    if isinstance(telemetry, dict):
        try:
            units = int(telemetry.get("units_processed", 0))
        except Exception:
            units = 0

    triggers: List[Dict[str, object]] = []

    # Check per-payload loot unit cap
    if flags.get("loot_governor", False) and units > loot_cap:
        triggers.append({
            "type": "loot_units_per_payload",
            "observed": units,
            "threshold": loot_cap,
        })

    # Check per-actor velocity in last 60 seconds
    if flags.get("xp_rate_limit", False):
        recent = _recent_dispatch_count(repo_root, actor, window_seconds=60)
        if recent > xp_cap:
            triggers.append({
                "type": "xp_velocity",
                "observed": recent,
                "threshold": xp_cap,
            })

    # Record observation and check units per minute
    _append_observation(repo_root, actor, units, now)
    if flags.get("loot_governor", False):
        upm = _units_last_minute(repo_root, actor, window_seconds=60)
        if upm > upm_cap:
            triggers.append({
                "type": "units_per_minute",
                "observed": upm,
                "threshold": upm_cap,
            })

    if triggers:
        log_dir = repo_root / "logs" / "fun_guardrails"
        _ensure_dir(log_dir)
        event = {
            "ts": now.isoformat().replace("+00:00", "Z"),
            "batch_id": batch_id,
            "actor": actor,
            "action": action,
            "triggers": triggers,
            "fun_flags": dict(flags),
            "source": "tools/fun_guardrail_eval.py",
        }
        events_path = log_dir / "events.jsonl"
        _append_jsonl(events_path, event)
        # per-batch index for consumers (e.g., controller warnings)
        by_batch = log_dir / "by_batch"
        _ensure_dir(by_batch)
        try:
            with (by_batch / f"{batch_id}.json").open("w", encoding="utf-8") as handle:
                json.dump(event, handle, ensure_ascii=False, indent=2)
                handle.write("\n")
        except OSError:
            pass

    return triggers
