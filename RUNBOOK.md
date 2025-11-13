# high_command_ai_0 – Runbook (v1)

Purpose: serve as High Command’s genesis workspace, authoring and clearing orders/acks/reports so Toyfoundry and sibling fronts always have fresh, validated directives.

Core Objectives
- Keep `tools.ops_readiness` green (docs + staging hygiene) before every exchange sweep.
- Ensure exchange ledger mirrors reality: every outbound order has an ack/report plan and landing slot.
- Guard hybrid-shadow posture: confirm gateway workspaces stay synced via `tools/exchange_all.py` heartbeat.

Operator Loop (per session)
1. Intake: run `python -m tools.ops_readiness`; remediate missing docs/artifacts immediately.
2. Author: draft new orders in `outbox/orders/`, pair acknowledgements/reports under `outbox/acks|reports/`.
3. Validate + sync: execute `python tools/exchange_all.py` to push staged payloads into the hub exchange; inspect `logs/exchange_all.json`.
4. Ledger: update `exchange/ledger/index.json` with new order IDs, targets, and linkage to evidence.
5. Signal Toyfoundry: once orders land, notify Toyfoundry to pull via `tools/offline_bridge.py pull --move`.

Evidence & Logging
- Ops checks: `logs/ops_readiness.json`
- Exchange pushes: `logs/exchange_all.json`
- Ledger diffs: `exchange/ledger/index.json`
- Attachments: `exchange/attachments/` (reference docs, playbooks)

Escalation
- Gatekeeper (Ops): halt outbound traffic if readiness fails twice in a row.
- Gatekeeper (Ledger): no Alfa production directives unless ledger references prior ack/report trails.

References
- `README.md`
- `planning/workspaces/*/RUNBOOK.md` (peer patterns)
- `exchange/ledger/index.json`
