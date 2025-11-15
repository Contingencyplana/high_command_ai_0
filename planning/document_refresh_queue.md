# Documentation Refresh Queue — Offline Continuity Mode

**Purpose:** Track staged updates while major pivots settle and the GitHub outage keeps us on the local exchange.

## Priority Bands

| Priority | Scroll / Path | Focus | Status | Owner | Next Action |
|:--|:--|:--|:--|:--|:--|
| P0 | `README.md` | Advertise offline mesh, Alfa staging map, pivot status | Done | High Command | ✅ Added metadata + ledger reminders; revisit Quickstart links once Alfa Zero prototype lands. |
| P0 | `exchange/README.md` | Describe Offline Continuity Mode bus (`high_command_exchange/`) + heartbeat/sync flow | Done | High Command | ✅ Added heartbeat/sync guidance, env var instructions, guardrails. |
| P1 | `planning/pivotal_fronts/README.md` | Confirm seven-front canon, add offline supervision guardrails | Done | High Command | ✅ Added offline guardrails + monitoring hook milestones; queue follow-up drift check after M2 reports. |
| P1 | `planning/morningate_reflection_layer.md` | Capture CTA updates + offline publication path | Done | War Office Liaison | ✅ Added offline publishing guardrails, metadata, CTA notes. |
| P2 | `planning/player_routing_brief.md` | Align with understaffed-front response + offline comms | Done | Toysoldiers Liaison | ✅ Added offline continuity cadence + metadata. |
| P2 | `new_major_pivots/README.md` | Summarise post-pivot state incl. emoji language progress | Done | High Command | ✅ Added metadata, Level-0 baseline, and Alfa staging checklist. |
| P2 | `new_major_pivots/new_major_pivot_2.md` | Capture overlay progress, telemetry hooks, and Order 045 plan | Done 2025-11-09 | High Command | ✅ Progress log aligned with Orders 044/045; revisit after overlay slice evidence lands. |
| P2 | `planning/pivotal_fronts/ops.md` | Fold in Order 045 trace parity guardrails + offline cadence reminders | Done 2025-11-10 | High Command | ✅ Added trace parity guardrail, refreshed heartbeat/sync checklist, logged in ledger. |
| P2 | `exchange/attachments/guides/comfort_happy_path.md` | Weave Pivot Seven Outlands links into comfort loop references | Done 2025-11-10 | High Command | ✅ Added Outlands index reference, linked framework + guardian protocol, created shared index stub. |

## Working Norms

1. Update scroll → log entry in `high_command_exchange/ledger/2025-10.md` (or `2025-11.md` after rollover).
2. Run `python tools/exchange_heartbeat.py` + `python tools/offline_sync_exchange.py` after each batch so satellites see the new canon.
3. Keep filesize diffs tight; we are deferring deep lore rewrites until Toyfoundry/Toysoldiers confirm live telemetry.

## UX Notes

- 2025-11-08 — Alfa Zero overlay now fires contract tests automatically post-dispatch (see `logs/alfa_zero/play_session_actions.log`); next slice is adding an inline targeted sync trigger.
- 2025-11-07 — Scripted play session flow captured in `logs/alfa_zero/play_session_commands.txt` to keep dispatch/contract/sync loop inside High Command.
- 2025-11-08 — Targeted `sync latest` / `sync orders` commands live with quiet-mode logging (see `planning/alfa_zero_targeted_sync_scope.md` for log rotation follow-up).

## Next Target Candidate

- 2025-11-12 - ✅ Staged Nightlands duet scoreboard placeholder composites and wired into `exchange/attachments/guides/nightlands_duet_playtest_packet.md`; metadata lives in `exchange/attachments/media/nightlands_duet/` (Order 050).
- 2025-11-13 - ✅ Promoted Nightlands duet telemetry into `exchange/attachments/telemetry/nightlands_duet/nightlands_duet_storyboard_sync_feed.jsonl`, published `docs/nightlands_duet_telemetry_panel.md`, and updated manifests + scope docs (Order 051).
- 2025-11-12 - Promote duet session metrics into the shared telemetry dashboard and document the dashboard hook in `planning/alfa_zero_nightlands_duet_storyboard.md`.
- 2025-11-13 - In progress: monitoring targeted sync quiet output via telemetry feed; revisit `planning/alfa_zero_targeted_sync_scope.md` after next cohort to decide on log rotation.
- 2025-11-10 - Evaluate propagating `trace_id` through `golf_00/delta_00/alfa_00/overlay_bridge.py` into payload extensions for cross-pipeline correlation; document toggle and evidence sinks. *(Completed 2025-11-10 via Order 045 trace parity refresh; future tweaks will spin as new entries as needed.)*

## Recently Completed

- 2025-10-31 — README current focus + Quickstart sync instructions (High Command).
- 2025-10-31 — exchange/README offline continuity guidance + guardrails (High Command).
- 2025-10-31 — Pivotal fronts canon updated with offline guardrails (High Command).
- 2025-10-31 — Morningate reflection layer aligned with offline publishing flow (War Office Liaison).
- 2025-10-31 — Player routing brief updated with offline mesh cadence (Toysoldiers Liaison).
- 2025-10-31 — README metadata + ledger reminders for offline ops (High Command).
- 2025-10-31 — Major pivots overview refreshed with Level-0 baseline + staging checklist (High Command).
- 2025-11-05 — Pivotal fronts ops scroll updated with Offline Continuity cadence and contract suite guardrails (High Command).
- 2025-11-07 — Ops scroll acceptance evidence updated with Toysoldiers ORDER-043 adoption log review (High Command).
- 2025-11-09 — new_major_pivot_2.md progress log aligned with Orders 044/045 overlay plan (High Command).
- 2025-11-10 — Comfort Happy Path guide now links Outlands framework, Fun Guardian protocol, and Outlands index (High Command).
- 2025-11-12 — Contract samples README updated with Music Pilot overlay cases (High Command).
- 2025-11-14 — War Office Tenfold genesis bundle (war_office_ai_0 runbook + genesis table refresh).
