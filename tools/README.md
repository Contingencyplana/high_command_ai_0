# Tools Overview

- Contract tests: `python -m tools.contract_test_runner`
- Exchange heartbeat: `python -m tools.exchange_heartbeat`
- Offline sync: `python -m tools.offline_sync_exchange`
- Cooldown rollup: `python -m tools.cooldown_rollup`

## Ops Readiness

- Preflight before enabling overlays: `python -m tools.ops_readiness`
- Summary written to `logs/ops_readiness/`; exits non‑zero on failure.
- See playbook: `exchange/attachments/guides/multi_layer_playbook.md`

