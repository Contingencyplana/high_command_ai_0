# Alfa Slot Map — Golf_00 / Delta_00 (November 2025)

> Track who owns each Alfa within the first 16×16 grid so operational handoffs stay synchronized while Offline Continuity Mode runs the show.

## Purpose

- Provide a single reference for golf/delta/alfa responsibilities during the pivot rollout.
- Link each slot to its coordinating workspace and exchange touchpoints.
- Surface readiness and next actions so the doc refresh queue can assign follow-up work quickly.

## Slot Ownership Table

| Slot | Focus | Primary Workspace | Status | Offline Hooks |
|:-----|:------|:------------------|:-------|:---------------|
| `golf_00/delta_00/alfa_00` | Alfa Zero overlay harness & CLI | `high_command_ai_0` | In progress — static grid renderer queued | Log heartbeat → sync → bridge after each harness iteration |
| `golf_00/delta_00/alfa_01` | Toyfoundry runtime bridge adapter | `toyfoundry_ai_0` | Active — awaiting Alfa 00 handshake spec | Push TF payload updates via `exchange/orders/` + `telemetry/emoji_runtime/` |
| `golf_00/delta_00/alfa_02` | Toysoldiers narrator harness | `toysoldiers_ai_0` | Active — monitoring loop validated by ORDER-041 | File after-action reports through `exchange/reports/` |
| `golf_00/delta_00/alfa_03` | Shared telemetry shell | `high_command_ai_0` + `toyfoundry_ai_0` | Planned — wiring quilt feeds next | Stage schema drafts in `exchange/inbox/` for review |
| `golf_00/delta_00/alfa_04` | Emoji composer harness (Level-0 glyph runtime) | `high_command_ai_0` | Active — Toyfoundry payloads validating cleanly | Record glyph/routing changes in ledger before sync |
| `golf_00/delta_00/alfa_05` | Reserved — Alfa Zero HUD theme pack | TBD | Planned | Queue design brief in doc refresh backlog |
| `golf_00/delta_00/alfa_06` | Reserved — Safety telemetry sentinel | TBD | Planned | Define escalation path in War Office scroll |
| `golf_00/delta_00/alfa_07` | Reserved — Morningate uplink | TBD | Planned | Map export cadence to reflection layer refresh |
| `golf_00/delta_00/alfa_08` | Reserved — Forge automation smoke tests | TBD | Planned | Route results into `exchange/reports/` |
| `golf_00/delta_00/alfa_09` | Reserved — Battlegrid tutorial deck | TBD | Planned | Draft scripts in `docs/player_routing_brief.md` |
| `golf_00/delta_00/alfa_10` | Reserved — Multiplayer session broker | TBD | Exploratory | Hold until Alfa Zero Phase 2 complete |
| `golf_00/delta_00/alfa_11` | Reserved — Lore canonicalizer | TBD | Exploratory | Coordinate with War Office lore custodians |
| `golf_00/delta_00/alfa_12` | Reserved — Dreamseed editor | TBD | Exploratory | Mirror edits through offline bridge once defined |
| `golf_00/delta_00/alfa_13` | Reserved — Voice pack synthesizer | TBD | Exploratory | Capture output in `telemetry/audio_samples/` |
| `golf_00/delta_00/alfa_14` | Reserved — Analytics dashboard | TBD | Exploratory | Publish snapshots to Morningate once pipeline ready |
| `golf_00/delta_00/alfa_15` | Reserved — Disaster recovery drill | TBD | Exploratory | Script exercises alongside offline bridge resets |

## Coordination Notes

- **Offline cadence:** Every workspace continues the `exchange_heartbeat.py` → `offline_sync_exchange.py` → `offline_bridge.py pull --move` loop; log each touchpoint in `exchange/ledger/2025-11.md`.
- **Doc refresh queue:** Use `planning/doc_refresh_queue.md` to record ownership changes or new slot assignments.
- **Escalation:** When a reserved slot activates, append a line to the November ledger and push an acknowledgement through `exchange/acknowledgements/outbox/` so satellites learn the new alignment.

## Next Updates

1. Land the Alfa Zero static grid renderer (`alfa_00`) and document run instructions here.
2. Capture Toyfoundry ↔ Toysoldiers interface contracts once Alfa 01 integrates the bridge.
3. Backfill reserved slots with mission briefs as pivots unlock new workstreams.
