# Tools Overview

- Contract tests: `python -m tools.contract_test_runner`
- Exchange heartbeat: `python -m tools.exchange_heartbeat`
- Offline sync: `python -m tools.offline_sync_exchange`
- Schema validator: `python -m tools.schema_validator <files>`
- Cooldown rollup: `python -m tools.cooldown_rollup`
- Frontline feedback intake: `python -m tools.frontline_feedback`
- Frontline feedback summary: `python -m tools.frontline_feedback_summary`
- Hybrid send (shadow): `python -m tools.comm_send --kind report --payload-file <path.json> [--validate] [--write]`
  - With staging enabled (config `online.enabled=true`, `online_write_kinds` includes kind), `--write` mirrors to `exchange/outbox/online_stage/`.
  - Defaults: reports and acks can write offline; reports and acks can stage online when enabled.

## Ops Readiness

- Preflight before enabling overlays: `python -m tools.ops_readiness`
- Includes heartbeat, contract tests, offline sync, and a schema sweep across exchange payloads (orders/reports/acks).
- Summary written to `logs/ops_readiness/`; exits non‑zero on failure.
- See playbook: `exchange/attachments/guides/multi_layer_playbook.md`
