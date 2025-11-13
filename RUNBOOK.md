# high_command_ai_0 – Runbook (v1)

Purpose: serve as High Command’s genesis workspace, authoring and clearing orders/acks/reports so Toyfoundry and sibling fronts always have fresh, validated directives.

Core Objectives
- Keep `tools.ops_readiness` green (docs + staging hygiene) before every exchange sweep.
- Ensure exchange ledger mirrors reality: every outbound order has an ack/report plan and landing slot.
- Guard hybrid-shadow posture: confirm gateway workspaces stay synced via `tools/exchange_all.py` heartbeat.

Operator Loop (per session)
1. Intake: run `python -m tools.ops_readiness`; remediate missing docs/artifacts immediately.
2. Author: draft new orders in `outbox/orders/`, pair acknowledgements/reports under `outbox/acks|reports/`.
3. Validate + sync: execute `python tools/exchange_all.py` to push staged payloads into the hub exchange; inspect `logs/exchange_all.json`.
4. Ledger: update `exchange/ledger/index.json` with new order IDs, targets, and linkage to evidence.
5. Signal Toyfoundry: once orders land, notify Toyfoundry to pull via `tools/offline_bridge.py pull --move`.

Evidence & Logging
- Ops checks: `logs/ops_readiness.json`
- Exchange pushes: `logs/exchange_all.json`
- Ledger diffs: `exchange/ledger/index.json`
- Attachments: `exchange/attachments/` (reference docs, playbooks)

Escalation
- Gatekeeper (Ops): halt outbound traffic if readiness fails twice in a row.
- Gatekeeper (Ledger): no Alfa production directives unless ledger references prior ack/report trails.

References
- `README.md`
- `planning/workspaces/*/RUNBOOK.md` (peer patterns)
- `exchange/ledger/index.json`

## Active Mitigation Playbooks

### Dual-Layer Cooldown Blitz (genesis-delta + genesis-theta)
Inputs:
- `exchange/reports/inbox/frontline_feedback_20251111T065332Z_genesis-delta.json`
- `exchange/reports/inbox/frontline_feedback_20251111T072050Z_genesis-theta.json`

Checklist:
1. Convene ops leads from `genesis-delta`, `genesis-theta`, and the Ritual queue owners; anchor the agenda on the reports above (lines 8-11 in each file).
2. Pull cooldown telemetry by 15-minute blocks for the last 24h; annotate where dual-layer spikes overlap with night operations.
3. Choose mitigation:
   - **Queue parallelization**: double-buffer ritual slots so lore/music requests never share the same worker.
   - **Staggered rituals**: offset lore/music dispatch by >= 90 seconds to let cooldown timers settle.
4. Document the chosen mitigation in this Runbook and log the action item owner in `exchange/ledger/2025-11.md`.
5. Verification gate: rerun `python -m tools.frontline_feedback_summary` once the fix ships; expect delta/theta notes to drop the cooldown complaint.

Cooldown Mitigation Actions (complete all that apply):
- [ ] Parallel queue deploy staged and dry-run traced.
- [ ] Staggered schedule published to Ritual ops channel.
- [ ] Night-ops cooldown chart attached to `exchange/attachments/guides/multi_layer_playbook.md`.
- [ ] Follow-up frontline sessions booked (delta + theta) to confirm the fix held for 3 consecutive drills.

### Night-Drill Music Patch (genesis-zeta)
Trigger: `exchange/reports/inbox/frontline_feedback_20251111T072102Z_genesis-zeta.json` flagged music/ritual clashes during night drills (lines 8-11).

Workflow:
1. Pair the Music lead with operator `op-music-09`; catalogue every clash case with timestamp + ritual ID.
2. Capture stems/presets that were active during each failure; drop them into `audio/motifs/` for reference.
3. Apply one of the following:
   - **Retune** the existing preset to respect ritual cue envelopes (tighten attack, reduce sustain overlap).
   - **Fallback** to a dedicated “ritual-safe” mix where the percussion layer is side-chained to ritual calls.
4. Smoke-test against a mocked ritual queue (use the stagger profiles from the cooldown blitz if already in place).
5. Log the outcome:
   - `python -m tools.frontline_feedback --workspace genesis-zeta --operator op-music-09 --layer-focus music --experience-rating <score> --music-support boosts --ritual-dependency supportive --note "<post-patch summary>"`
   - `python -m tools.frontline_feedback_summary`
6. If the summary still shows conflicts, re-open the preset tuning loop and keep publishing notes until conflicts drop to zero for three consecutive night drills.

Zeta Patch Checklist:
- [ ] Clash catalogue filed in `exchange/attachments/guides/multi_layer_playbook.md`.
- [ ] Retuned preset committed under `audio/motifs/` (or fallback mix documented).
- [ ] Post-patch frontline entry written and synced.
- [ ] Summary artifact reviewed; results relayed to High Command + Ritual ops.
