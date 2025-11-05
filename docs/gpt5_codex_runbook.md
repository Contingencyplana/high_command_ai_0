# GPT‑5‑Codex Operator Runbook — High Command AI

Purpose: delegate routine play sessions and health checks to GPT‑5‑Codex while preserving safety and measurability. Keep creative/structural changes gated for review.

## Preconditions

- Python available on PATH.
- `SHAGI_EXCHANGE_PATH` set if using a shared exchange hub (optional; defaults documented in tools).
- Auto‑promotion ON by default (`OVERLAY_AUTO_PROMOTE_FACTORY_ORDERS=1`).

## Core Commands

- Play session (interactive overlay + background sync)
  - `python scripts/play_session.py`
  - Outputs: emoji payloads → `outbox/orders/emoji_runtime/`, factory orders → `outbox/orders/factory_orders/`
  - Logs: `logs/alfa_zero/overlay_events.jsonl`, `logs/alfa_zero/session_metrics.jsonl`, `logs/alfa_zero/phase_2_latencies.jsonl`

- Canary (Level‑0 emoji translator) — nightly
  - `python tools/run_emoji_canary.py --promote`
  - Logs: `logs/canary/emoji_translator/results.jsonl`
  - Fails non‑zero on translation/validation errors.

- Smoke test (mapped cell dispatch)
  - `pytest -q tests/test_overlay_smoke.py`

## Success Criteria (green state)

- Canary returns exit code 0; results show only `success`/`factory_status: ok` entries.
- Smoke test passes; at least one emoji payload written per mapped cell.
- Play session produces new payloads and updates quilt rows C–F based on `phase_2_latencies.jsonl`.

## Failure Actions

- Canary failure: stop automation, capture failing chain name and exception from results JSONL, file an issue. Do not modify `emoji_translator.py` or grammar without review.
- Smoke failure: stop automation, attach error and temp outbox listing, file an issue.
- Play loop anomalies (no quilt updates or empty outbox): verify `OVERLAY_AUTO_PROMOTE_FACTORY_ORDERS` and exchange heartbeat; file an issue if unresolved.

## Guardrails

- Do not edit code. Allowed actions: run tasks/commands, read logs, open issues.
- Do not change grammar, cell mappings, or translator logic.
- Toggling auto‑promotion only for debugging: `OVERLAY_AUTO_PROMOTE_FACTORY_ORDERS=0`.

## VSCode Tasks

- Open Command Palette → “Run Task…”
  - Play: “Play: Alfa Zero Session”
  - Canary: “Canary: Emoji Translator (promote)”

## File Map

- Overlay UI: `golf_00/delta_00/alfa_00/alfa_zero_ui.py`
- Overlay bridge (auto‑promotion): `golf_00/delta_00/alfa_00/overlay_bridge.py`
- Translator + samples: `golf_00/delta_00/alfa_04/emoji_translator.py`, `sample_chains.json`
- Factory adapter: `golf_00/delta_00/alfa_04/factory_adapter.py`
- Canary runner: `tools/run_emoji_canary.py`
- Play session: `scripts/play_session.py`
- Schema validator: `tools/schema_validator.py`

