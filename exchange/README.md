# High Command Exchange Repository

This directory mirrors the structure of the forthcoming `high_command_exchange` git repository. All workspaces mount this layout at `exchange/`.

## Directory Map

- `orders/pending/` — Fresh directives awaiting acknowledgement.
- `orders/dispatched/` — Orders with acknowledgements on record.
- `reports/inbox/` — Field submissions awaiting review.
- `reports/archived/` — Closed reports retained for history.
- `acknowledgements/pending/` — Signals not yet reconciled.
- `acknowledgements/logged/` — Signals tied to ledger entries.
- `ledger/` — Journal and machine index linking every payload.

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
