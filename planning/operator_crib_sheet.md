# Operator Crib Sheet — Hybrid Comms (Local/Staged)

Purpose: run the loop safely with Hybrid Communications. No network; staged “online” writes mirror to a local folder for inspection.

## Preflight
- Ops readiness: `python -m tools.ops_readiness`
  - Expect all sections [OK]. If heartbeat fails, set `SHAGI_EXCHANGE_PATH` and re-run.
- Exchange validator: `python -m tools.exchange_validator`
  - Expect: `Exchange looks consistent.`

## Send (Shadow and Stage)
- Shadow report (no writes):
  - `python -m tools.comm_send --kind report --payload-file <path.json> --validate`
- Stage report (local mirror to stage_dir):
  - `python -m tools.comm_send --kind report --payload-file <path.json> --write`
- Stage ack (local mirror to stage_dir):
  - `python -m tools.comm_send --kind ack --payload-file <ack.json> --write`

Notes
- Staged files appear under: `exchange/outbox/online_stage/`
- Orders remain plan-only (never write via adapter).

## Flags (exchange/config.json)
- `mode`: "hybrid"
- `online.enabled`: true (staging enabled)
- `online.offline_write_kinds`: ["report", "ack"]
- `online.online_write_kinds`: ["report", "ack"]
- `online.stage_dir`: "exchange/outbox/online_stage"

## Hygiene
- Prune staged files (dry-run): `python -m tools.stage_retention`
- Apply deletion: `python -m tools.stage_retention --keep 200 --write`
- Generate reflection: `python -m tools.morningate_reflection` (writes under `logs/reflection/`)

## Rollback
- Disable staging: set `online.enabled` to false and re-run readiness
- Remove kinds from `online.online_write_kinds` to restrict staging
- Record changes in ledger if part of an Order

## Troubleshooting
- Schema errors: run `python -m tools.schema_validator <files>` and share the first error line
- Validator errors: `python -m tools.exchange_validator` to list missing paths; fix `exchange/ledger/index.json` or file locations accordingly
- Heartbeat errors: verify `SHAGI_EXCHANGE_PATH` points to the hub (e.g., `C:/Users/Admin/high_command_exchange`)

---
Hand-off: This sheet is sufficient for GPT-5-Codex to operate the loop with Hybrid staging safely.
