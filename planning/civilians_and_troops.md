# Civilians and Troops — Pivot Readiness Index

Purpose: align the metaphor to concrete artifacts, gates, and links so we can pivot from civil infrastructure to mass Alfa manufacturing without drift.

## Definitions
- Troops: the 4,096 Alfas per workspace — playable workflow missions and overlays.
- Civilians: support layer that keeps runs safe and recoverable — schemas, validator, contracts, overlays, telemetry, ledger, and operator runbooks.

## Minimum Civilian Layer (links-first)
- Multi-layer playbook: exchange/attachments/guides/multi_layer_playbook.md
- Ack/report runbook: exchange/attachments/guides/ack_and_report_guidance.md
- Outlands overlays index: exchange/attachments/guides/outlands_index.md
- Contract runner: tools/contract_test_runner.py
- Schema validator: tools/schema_validator.py
- Ops readiness preflight: tools/ops_readiness.py
- Exchange heartbeat: tools/exchange_heartbeat.py

## Hybrid Comms Readiness
- Config and modes: exchange/config.json
- Offline sync bridge: tools/offline_sync_exchange.py and exchange/attachments/tools/sync_exchange.py
- Readiness gate: ops preflight must pass in hybrid shadow/dark modes (see tools/ops_readiness.py)
- Adapter note: the thin comm adapter will route to offline hub and gated online channel; feature flags remain off-by-default until gates are green.

## Troops Readiness Gates (Go/No‑Go)
- Contracts green: python -m tools.contract_test_runner
- Overlays safe: tests/test_overlay_smoke.py and golf_00/delta_00/alfa_00/overlay_flow.py
- End‑to‑end loop: ack → execute → report → archive visible in exchange/ and indexed in exchange/ledger/index.json
- Schema sweep OK: part of tools/ops_readiness.py

## Operator Runbooks and Feedback
- Comfort path: exchange/attachments/guides/comfort_happy_path.md
- Automation quick start: exchange/attachments/guides/automation_quick_start.md
- Frontline intake: tools/frontline_feedback.py (writes to exchange/reports/inbox)
- Frontline summary: tools/frontline_feedback_summary.py (writes to exchange/reports/outbox)

## Metrics and Ledger
- Trace helpers: golf_00/delta_00/alfa_00/trace_utils.py
- Ledger index: exchange/ledger/index.json (orders/acks/reports paths)
- Ops readiness logs: logs/ops_readiness/

## Change Control and Drift
- Contract suite rollout notes: exchange/attachments/guides/contract_suite_rollout_notes.md
- Schema drift sitrep: planning/SCHEMA_DRIFT_SITREP_2025-10-18.md
- Changelog: planning/change_log.md
- Validator coverage: tools/schema_validator.py (add schemas here as new payloads appear)

---
Decision rule: when all gates above are green in hybrid shadow mode and runbooks are current, pivot focus to mass Alfa production and spin up the remaining genesis workspaces.

## Comm Adapter (Hybrid Shadow)
- CLI: `python -m tools.comm_send --kind report --payload-file <path.json> [--validate] [--write]`
- Defaults to shadow: `--dry-run` is default; prints planned offline/online actions without writing.
- Safety guards:
  - Orders are plan-only (never write).
  - Offline writes allowed only when kind is listed in `exchange/config.json` → `online.offline_write_kinds` (default `["report"]`; add `"ack"` to enable acks).
  - `online.enabled` remains `false`; online sink is a noop until dark‑launch.
- Visibility: `python -m tools.ops_readiness` prints `mode`, `online.enabled`, `offline_write_kinds`, and runs the “Hybrid Shadow Check”.
- Examples:
  - `python -m tools.comm_send --kind report --payload-file exchange/reports/outbox/frontline_feedback_summary_20251111T072152Z.json --validate`
  - `python -m tools.comm_send --kind ack --payload-inline '{"schema":"signal-ack@1.0","ack_id":"x","referenced_id":"y","sender":"z","receiver":"hc","timestamp_sent":"2025-11-11T00:00:00Z","status":"acknowledged"}' --dry-run`

## Hybrid Rollout Checklist
- Shadow on: `mode=hybrid`, `online.enabled=false` (default), verify ops_readiness is green.
- Dark‑launch acks (optional): keep `online.enabled=false`, set `offline_write_kinds` to include `"ack"`; use comm_send `--write` for offline writes only.
- Stage reports “online”: set `online.enabled=true`, `online_write_kinds=["report"]`; verify staged files appear under `exchange/outbox/online_stage/`.
- Do not add `"order"` to write lists; orders remain plan‑only.
- Rollback: set `online.enabled=false` and remove staged kinds from `online_write_kinds`.
