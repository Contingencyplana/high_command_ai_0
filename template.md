# Ledger Logging Template - Offline Continuity Mode

Purpose: keep every work block measurable while Offline Continuity Mode routes traffic through `exchange/`. Treat this as the checklist before moving on from any Alfa/scroll update.

---

## 1. Prep the Session

1. Restate the front / milestone / goal (War Office Director Protocol) so the ledger summary has context.
2. Run `python tools/exchange_heartbeat.py` and confirm green/green/green.
3. If heartbeat is green, run `python tools/offline_sync_exchange.py` but **only after** you have staged new orders, reports, or docs.

---

## 2. Append the Ledger Entry

- File: `exchange/ledger/2025-11.md` (roll over to the next month on the 1st).
- Format (one line per action):

```text
YYYY-MM-DD HH:MM <Origin> <Channel> <Summary>
```

| Field | Example | Notes |
|-------|---------|-------|
| `YYYY-MM-DD HH:MM` | `2025-11-18 14:05` | Use 24-hour local time. |
| `<Origin>` | `HighCommand`, `Toyfoundry`, `WarOffice` | Match the workspace or team acting. |
| `<Channel>` | `DOC-REFRESH`, `OFFLINE-SYNC`, `ORDER-045`, `PLAYTEST` | Pick the closest tag. Orders keep their ID, utility work uses the function tags already present in the ledger. |
| `<Summary>` | `Refreshed war_office.md doc queue + pivot crosslinks` | 8-12 words describing what changed. Mention files or order IDs when possible. |

**Tip:** When logging multiple actions from the same session, keep the timestamp increasing and split the summaries across individual lines instead of stacking bullet points inside one entry.

---

## 3. Suggested Snippet (PowerShell)

```powershell
$entry = '2025-11-18 14:05 HighCommand DOC-REFRESH Updated template.md ledger checklist'
Add-Content -Path exchange/ledger/2025-11.md -Value $entry
```

Repeat with new timestamps for subsequent actions in the same block.

---

## 4. Close the Loop

1. Rerun `python tools/exchange_heartbeat.py` (post-change).
2. Run `python tools/offline_sync_exchange.py` to mirror the new ledger line + artifacts into the shared bus.
3. If you touched documentation, echo the refresh in `planning/doc_refresh_queue.md` (scope + date + actor).
4. Only then proceed to the next Alfa or enter the planning lull.

This sequence guarantees every doc refresh, playtest, or factory order has a timestamped breadcrumb plus a synced heartbeat before the next maneuver.
