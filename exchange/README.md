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

Every workspace (`toyfoundry_ai_0`, `toysoldiers_ai_0`, `valiant_citadel_ai_0`, `r_and_d_ai_0`, `high_command_ai_0`) sets `SHAGI_EXCHANGE_PATH` to `C:/Users/Admin/high_command_exchange`. Symlinks are optional but not required so long as tools resolve the environment variable.

- Confirm the env var with `echo $env:SHAGI_EXCHANGE_PATH` (PowerShell) and fix any drift before running sync tools.
- Ensure `outbox/orders/` and `outbox/reports/` exist in each workspace; create empty folders if needed so sync logs stay clean.

## Sync Utility

Run offline propagation through the heartbeat + sync pair in each workspace:

```powershell
python tools/exchange_heartbeat.py
python tools/offline_sync_exchange.py
```

- `exchange_heartbeat.py` confirms reachability and write access (🟢 / 🟠 / 🔴).
- `offline_sync_exchange.py` copies `outbox/orders/` and `outbox/reports/` into the shared `orders/` and `reports/` folders and reports the result.
- Run both commands sequentially from each workspace after notable changes (orders issued, reports filed, documentation updates).

## Ledger Discipline

Record every significant action in `ledger/2025-10.md` using the format:

```text
YYYY-MM-DD HH:MM <Origin> <Order ID> <Summary>
```

Include the activation entry already logged on 2025-10-29 as the starting point for this mode. Roll over to `ledger/2025-11.md` on November 1, keeping the same format.

## Returning to Normal Operations

When GitHub service is restored:

1. Capture a snapshot of the entire exchange directory.
2. Re-enable Git tracking and push the snapshot as a single commit to the High Command repository.
3. Coordinate the transition back to the standard sync tooling (re-enable `tools/quint_sync.py --push` after snapshot commit is accepted).

## Guardrails

- Do **not** push to remote repositories until War Office issues the unlock directive.
- Escalate immediately if `exchange_heartbeat.py` reports 🟠/🔴 status; log incident details in `reports/inbox/` and notify High Command.
- Keep acknowledgements and completion reports flowing by copying them into `reports/` and logging the action in the ledger before syncing.
- Maintain parity across all workspaces—if one node updates documentation or orders, rerun the heartbeat + sync pair on the other four to pull the changes.

Until that directive arrives, keep this workspace in Offline Continuity Mode and avoid remote pushes.
