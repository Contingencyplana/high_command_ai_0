# war_office_ai_0 — Civilian Crown Workspace

War Office (workspace 10 of the Tenfold Genesis layer) speaks for the 4,096 Civilians, carries the Director's Compass, and crowns every recursive loop. This workspace is where pivots are ratified, canon is locked, and the mission is restated before High Command or Codex advances.

## Purpose
- Restate *front / milestone / goal* before issuing any directive (Nightlands Director Protocol step zero).
- Maintain the civic lattice (Commonwealth → Citizen) so every Alfa surge references its civilian counterpart.
- Publish War Office dispatches, nudges, and halts with linked evidence.
- Keep the Tenfold Genesis table synchronized with ledger entries and doc refresh queues.

## Layout
```
war_office_ai_0/
  README.md
  RUNBOOK.md
  docs/
    civic_lattice.md
    directors_compass.md
  runbooks/
    session_templates/
  dispatches/
  civics/
    ledgers/
    schemas/
  civic_lattice/
    commonwealth/
      guild_00/ ... /guild_0f/
        house_00/ ... /house_0f/
          citizen_xxxxxx.md
  tools/
    civic_slot_report.py
```

## Quickstart
1. Open `RUNBOOK.md` for the session cadence.
2. Run `python tools/civic_slot_report.py --summary` to view guild/house fill levels.
3. Draft directives under `dispatches/` (use templates in `runbooks/session_templates/`).
4. Append ledger entries in `civics/ledgers/` and sync to `high_command_exchange` via standard heartbeat/sync loop.
5. Mirror any structural change back into `high_command_ai_0` and Tenfold docs.

## References
- `war_office.md` (shared charter)
- `planning/pivotal_fronts/genesis_workspaces.md`
- `planning/workspaces/war_office_ai_0/RUNBOOK.md`
- `planning/doc_refresh_queue.md`
