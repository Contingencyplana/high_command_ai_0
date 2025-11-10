# Enabler Front: Operations & Exchange Integrity

Purpose
- Keep the exchange, ledger, and sync reliable so the other fronts can move.

Practices
- Config-driven publish/pull; outbox stays empty post-publish.
- Pre-push hook runs validator + outbox scan (blocks malformed items).
- Daily watcher scans; log rotation under logs/safety_watcher.log.
- Keep safety_config YAML↔JSON mirrored (tools/ci/sync_safety_config.ps1).
- Offline Continuity cadence: run `python tools/exchange_heartbeat.py` → `python tools/offline_sync_exchange.py` → `python tools/offline_bridge.py push|pull --move` every time the exchange changes, and log the trio in the ledger within 24 hours.
- Contract suite guardrail: run `python -m tools.contract_test_runner` whenever emoji/factory schemas change and before publishing exchange artifacts.
- Trace parity guardrail: overlay dispatches (UI and event stream) must emit matching `trace_id` values through payloads, factory orders, and telemetry logs; confirm whenever overlay slices ship.

Runbooks & Links

- Exchange: exchange/README.md; Config: exchange/config.json
- Scripts: tools/ci/publish_outbox.ps1, tools/ci/pull_inbox.ps1
- Watcher: tools/ci/safety_watcher.ps1; Validator: tools/ci/validate_safety_repo.ps1
- Offline Continuity: tools/exchange_heartbeat.py, tools/offline_sync_exchange.py, tools/offline_bridge.py
- Contract tests: tools/contract_test_runner.py, contract_samples/README.md

Acceptance Checks

- Watcher runs clean (no unexpected BLOCKED) on inbox/outbox.
- No drift between YAML and JSON config; pre-push passes.
- Ledger ACK/close-out is timely for active orders.
- Toysoldiers adoption of ORDER-043 contract suite recorded in ledger (2025-11-06) and reviewed within 24h of dispatch.
- Offline Continuity trio recorded in ledger within 24h of any exchange change, including daily doc refresh pushes.
- Contract suite passes against curated fixtures before publishing promoted payloads.
- Overlay Order 045 trace evidence captured: `logs/alfa_02/narration_traces.jsonl`, `logs/alfa_03/telemetry.jsonl`, and payload exports all share the same `trace_id` when parity is verified.
