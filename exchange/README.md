# Offline Continuity Mode — Active

High Command Exchange now operates as a local-only message bus to keep SHAGI coordination flowing while GitHub access is restricted. Treat this directory as the shared drop-zone that every frontline workspace reads from and writes to.

## Directory Layout

- `orders/` — Authoritative catalog of issued orders (subfolders as needed).
- `reports/` — Intelligence drops and after-action reports.
- `ledger/` — Canonical operational log (see `ledger/2025-10.md`).
- `inbox/` — Items awaiting High Command review.
- `outbox/` — Staging area for assets moving into the exchange.

All folders must remain available on the local filesystem. Optional cloud mirroring is allowed for redundancy, but no remote execution or Git commits are permitted during this mode.

## Workspace Integration

Every workspace (`toyfoundry_ai_0`, `toysoldiers_ai_0`, `valiant_citadel_ai_0`, `r_and_d_ai_0`) should expose this path via either:

1. A filesystem symlink that maps its local `exchange/` directory to `C:/Users/Admin/high_command_exchange`, or
2. The `SHAGI_EXCHANGE_PATH` environment variable pointing to the same location.

Coordinate with each team to implement the approach that best fits their tooling.

## Sync Utility

Run offline propagation through `tools/quint_sync.py`.

```powershell
python tools/quint_sync.py --offline [--source C:/path/to/workspace]
```

- `--source` defaults to the current working directory and should contain an `outbox/orders/` and `outbox/reports/` structure.
- The script copies those payloads into the shared `orders/` and `reports/` folders and confirms completion.

## Ledger Discipline

Record every significant action in `ledger/2025-10.md` using the format:

```text
YYYY-MM-DD HH:MM <Origin> <Order ID> <Summary>
```

Include the activation entry already logged on 2025-10-29 as the starting point for this mode.

## Returning to Normal Operations

When GitHub service is restored:

1. Capture a snapshot of the entire exchange directory.
2. Re-enable Git tracking and push the snapshot as a single commit to the High Command repository.
3. Coordinate the transition back to the standard sync tooling.

Until that directive arrives, keep this workspace in Offline Continuity Mode and avoid remote pushes.
