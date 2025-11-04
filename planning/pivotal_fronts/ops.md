# Enabler Front: Operations & Exchange Integrity

Purpose
- Keep the exchange, ledger, and sync reliable so the other fronts can move.

Practices
- Config-driven publish/pull; outbox stays empty post-publish.
- Pre-push hook runs validator + outbox scan (blocks malformed items).
- Daily watcher scans; log rotation under logs/safety_watcher.log.
- Keep safety_config YAML↔JSON mirrored (tools/ci/sync_safety_config.ps1).
- Offline Continuity cadence: `python tools/exchange_heartbeat.py` → `python tools/offline_sync_exchange.py` → `python tools/offline_bridge.py push|pull --move` logged in ledger.
- Contract suite guardrail: run `python -m tools.contract_test_runner` whenever emoji/factory schemas change and before publishing exchange artifacts.

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
- Offline Continuity trio recorded in ledger within 24h of any exchange change.
- Contract suite passes against curated fixtures before publishing promoted payloads.
