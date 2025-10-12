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
