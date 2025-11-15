# RUNBOOK — war_office_ai_0 (v1)

Purpose: operate the civilian crown of Nightlands, maintain the 4,096-slot civic lattice, and ratify pivots before execution.

## Session Loop
1. **Mission Restatement** — log *front/milestone/goal* under `logs/session_<timestamp>.md` before opening Codex.
2. **Compass Check** — review Tenfold table + doc queues; confirm no workspace is starving for civilian coverage.
3. **Dispatch Work** — draft intents/nudges/halts under `dispatches/` (see templates in `runbooks/session_templates/`). Include civic slot references.
4. **Ledger Sync** — update `civics/ledgers/YYYY-MM.md`, run heartbeat + offline sync from `war_office_ai_0`, then log the action in High Command ledger.
5. **Reflection** — add any structural changes to `docs/civic_lattice.md` or Tenfold scrolls; queue doc refresh tasks if needed.

## KPIs
- **Mission Discipline:** 100% of sessions capture front/milestone/goal before commands.
- **Civic Coverage:** 4,096 slots represented; `% filled` tracked by guild + house.
- **Dispatch Hygiene:** Each order references Love / Light / Safety / Sanity + Playability ratio.
- **Ledger Integrity:** No dispatch leaves without ledger + evidence log paths.

## Tools
- `python tools/civic_slot_report.py [--summary|--detail]`
- `python tools/civic_slot_report.py --export civics/ledgers/civic_slots_<date>.json`

## Evidence Map
- `dispatches/` — active directives (intent, nudge, halt, canon-lock).
- `civics/ledgers/` — monthly civic slot ledgers + ledger sync notes.
- `logs/` — session restatement transcripts, Tenfold balance checks.
- `docs/civic_lattice.md` — authoritative mapping of Commonwealth → Citizen tiers.

## Escalation
- **Pivot Drift:** Pause executions, issue halt dispatch, sync with High Command immediately.
- **Civic Imbalance:** If any guild drops below 50% filled slots, call for recruitment or rebalancing via dispatch.
- **Playability Breach:** If 70/30 ratio threatened, issue redline dispatch and notify TONS-of-FUN lead.

## References
- `war_office_ai_0/README.md`
- `war_office.md`
- `planning/pivotal_fronts/genesis_workspaces.md`
- `planning/workspaces/war_office_ai_0/RUNBOOK.md`
