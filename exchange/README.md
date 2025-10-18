# Field Operations Exchange Repository

This directory manages the exchange of field operations data, tactical intelligence, and command protocols between High Command and the Field Operations Front. All field operations are coordinated through this exchange structure, powered by AI Labscapes integration.

## Field Operations Directory Structure

- `orders/pending/` — Incoming tactical directives for field execution
- `orders/dispatched/` — Completed field operation orders with results
- `reports/inbox/` — Field intelligence and operational reports
- `reports/archived/` — Historical field operation records
- `acknowledgements/pending/` — Field operation signals pending processing
- `acknowledgements/logged/` — Processed field operation signals
- `ledger/` — Complete field operations journal and index

Each directory integrates with the AI Labscapes (ai_labscapes_0 through ai_labscapes_255) to ensure intelligent processing and tactical optimization of field operations.

Populate this structure via Forge tooling or manual commits until the standalone exchange repository is provisioned.

## Governance

- License: MIT (`LICENSE`)
- Contribution guidelines: see `CONTRIBUTING.md`
- Audit trail: update `ledger/journal.md` and `ledger/index.json` whenever orders close

---

## Local Sync (Config-Driven)

This workspace can sync with an upstream Exchange checkout using a simple config file.

1) Copy `exchange/config.example.json` to `exchange/config.json` and edit:

```
{
  "mode": "local",
  "upstream_root": "C:/path/to/high_command_exchange",
  "mapping": {
    "local": {
      "orders_pending": "exchange/orders/pending",
      "reports_inbox": "exchange/reports/inbox",
      "acks_pending": "exchange/acknowledgements/pending",
      "acks_logged": "exchange/acknowledgements/logged"
    },
    "upstream": {
      "orders_pending": "orders/pending",
      "orders_dispatched": "orders/dispatched",
      "reports_inbox": "reports/inbox",
      "reports_archived": "reports/archived",
      "acks_pending": "acknowledgements/pending",
      "acks_logged": "acknowledgements/logged"
    }
  }
}
```

2) Publish outbox (push local pending orders and inbox reports up to upstream):
- `pwsh -NoProfile -File tools/ci/publish_outbox.ps1 -ConfigPath exchange/config.json`

3) Pull inbox (refresh local from upstream pending/dispatched orders, inbox reports, and acks):
- `pwsh -NoProfile -File tools/ci/pull_inbox.ps1 -ConfigPath exchange/config.json`

Notes
- Scripts are copy-only (no deletions). They overwrite by filename.
- For dry-run, add `-WhatIf`.
