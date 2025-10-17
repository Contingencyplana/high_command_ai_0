# Enabler Front: Operations & Exchange Integrity

Purpose
- Keep the exchange, ledger, and sync reliable so the other fronts can move.

Practices
- Config-driven publish/pull; outbox stays empty post-publish.
- Pre-push hook runs validator + outbox scan (blocks malformed items).
- Daily watcher scans; log rotation under logs/safety_watcher.log.
- Keep safety_config YAML↔JSON mirrored (tools/ci/sync_safety_config.ps1).

Runbooks & Links
- Exchange: exchange/README.md; Config: exchange/config.json
- Scripts: tools/ci/publish_outbox.ps1, tools/ci/pull_inbox.ps1
- Watcher: tools/ci/safety_watcher.ps1; Validator: tools/ci/validate_safety_repo.ps1

Acceptance Checks
- Watcher runs clean (no unexpected BLOCKED) on inbox/outbox.
- No drift between YAML and JSON config; pre-push passes.
- Ledger ACK/close-out is timely for active orders.
