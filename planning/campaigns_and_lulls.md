# Campaigns and Lulls

Purpose: name the operating rhythm — Campaign → Lull → Next Campaign — so teams share vocabulary, cadence, and a compact chronicle of major/minor pushes.

## Lexicon
- Era/Phase: long arc crossing many campaigns (e.g., Foundation → Post‑Foundation/Refinement).
- Campaign (Major/Minor): multi‑order push to close dependencies. Major spans multiple fronts; Minor is narrower.
- Operation/Sprint: time‑boxed execution unit inside a campaign.
- Order: atomic directive with ack/report/ledger artifacts (exchange/orders, exchange/reports, exchange/ledger).
- Lull (Stabilization): active window to triage inbox, refresh docs, validate tooling, and plan the next campaign.

## Cadence
- Lull checklist: clear `exchange/reports/inbox`, run `tools/exchange_heartbeat.py`, sync via `tools/offline_sync_exchange.py`, refresh docs/roadmaps, and capture readiness.
- Plan: define objectives, success criteria, dependencies, and provisional order IDs.
- Execute: issue orders, close dependencies, validate (schema + contract tests), and keep the ledger current.
- Debrief: archive reports/acks, update ledger, note lessons; return to lull.

## Chronicle Template
Use this block per campaign:

```text
Name: <Campaign Name>
Window: <YYYY-MM-DD → YYYY-MM-DD>
Type: Major|Minor
Objective: <1–2 lines>
Orders: <IDs>
Outcomes: <1–3 bullets>
Evidence: <key files/paths>
```

## Current State Snapshot

- Orders queue: recent slice closed (045/047/048/049/050/051); queue clear for planning lull.
- Inbox: cleared 2025-11-09; backlog archived to `exchange/reports/archived/inbox_backlog/`; Order 035 monitor result published (promote recommendation); Order 2025-10-20-001 report promoted to `exchange/reports/archived/`.
- Recent completions: 040/041/043/045/047/048/049/050/051 closed; reports and acks archived (see `exchange/ledger/index.json`).
- Document refresh cadence: second-pass daily slices running from `planning/document_refresh_queue.md`; log updates to `exchange/ledger/2025-11.md` each block.
- Nightlands playtest: 2025-11-12 cohort (Vega, Lumen, Rook) ran the duet comfort loop; feedback archived in `logs/alfa_zero/play_session_feedback/` with follow-up work queued.

### Lull — UI Overlay Slice

- Status: Entered stabilization lull following Order 045 closure.
- Closed anchors: 045 (UI overlay integration), 047 (targeted sync CLI), 048 (storyboard run), 049 (playtest), 050 (scoreboard imagery), 051 (telemetry feed panel).
- Tracked follow-ups (not blocking lull):
  - Integrate Nightlands feed into the primary dashboard once tooling returns.
  - Decide targeted-sync log rotation after a few additional playtests.
  - Continue appending storyboard/targeted-sync runs to the feed during future sessions.

## Foundation Campaign (Orders 001–039)

```text
Name: Foundation Campaign (Orders 001–039)
Window: 2025-10-12 → 2025-10-26
Type: Major → infrastructure bring-up
Objective: Stand up exchange hub, heartbeat/sync loop, ledger discipline, and telemetry quilt; enact safety policy and stabilize governance.
Outcomes:
- Offline continuity mode active; exchange/README + heartbeat/sync tools shipped.
- Telemetry quilt loom stood up; composite exports aligned and versioned.
- Safety Policy 025 enacted; fronts closed and audit logged (Oct 16).
- Schema drift surfaced → corrective Order 036 scoped and tracked.
Evidence:
- exchange/ledger/2025-10.md, exchange/ledger/journal.md
- exchange/README.md, tools/exchange_heartbeat.py, tools/offline_sync_exchange.py
- exchange/reports/archived/all-fronts-closed-2025-10-16-report.json
- planning/SCHEMA_DRIFT_SITREP_2025-10-18.md
```

## Chronicle — Recent Campaigns

```text
Name: Emoji → Factory Bridge
Window: 2025-11-01 → 2025-11-01
Type: Minor → enabling bridge
Objective: Implement emoji_runtime → factory_order adapter with validator coverage.
Orders: order-2025-11-01-040
Outcomes:
- Adapter and translator wired in `golf_00/delta_00/alfa_04/`.
- Validator and samples established.
Evidence:
- golf_00/delta_00/alfa_04/emoji_translator.py
- golf_00/delta_00/alfa_04/factory_adapter.py
- exchange/reports/archived/order-2025-11-01-040-report.json
```

```text
Name: Cross‑Workspace Telemetry & Narration
Window: 2025-11-01 → 2025-11-01
Type: Minor → alignment/stubs
Objective: Align narration/telemetry stubs and monitoring across workspaces.
Orders: order-2025-11-01-041
Outcomes:
- Narration + payload alignment briefs published under `quint_synced/`.
- Monitoring/ingestion guidance documented; runtime shells available in alfa_02/alfa_03.
Evidence:
- exchange/reports/archived/order-2025-11-01-041-report.json
- quint_synced/payload_alignment.md
- quint_synced/narration_alignment.md
```

```text
Name: Contract Suite Rollout
Window: 2025-11-02 → 2025-11-02
Type: Minor → verification
Objective: Ship contract test runner + curated fixtures; document rollout.
Orders: order-2025-11-02-043
Outcomes:
- End‑to‑end runner verifying translator/adapter against samples.
- Rollout notes for Toyfoundry/Toysoldiers integration.
Evidence:
- tools/contract_test_runner.py
- contract_samples/cases/basic_ritual_victory.json
- exchange/attachments/guides/contract_suite_rollout_notes.md
- exchange/reports/archived/order-2025-11-02-043-report.json
```

```text
Name: Nightlands Comfort Loop Validation
Window: 2025-11-12 → 2025-11-12
Type: Minor → playtest validation
Objective: Brief a three-operator cohort, run the Nightlands duet comfort loop with targeted sync, and harvest qualitative signal before broader rollout.
Orders: order-2025-11-12-047, order-2025-11-12-048, order-2025-11-12-049
Outcomes:
- Cohort (Vega, Lumen, Rook) executed the duet storyboard; targeted sync quiet output confirmed.
- Feedback/metrics archived; scoreboard + telemetry follow-ups queued in the refresh backlog.
- Campaign docs updated with readiness signals and UI tweak recommendations (cooldown banner, dashboard panel).
Evidence:
- logs/alfa_zero/play_session_feedback/order-2025-11-12-049_session_20251112T143000Z.jsonl
- exchange/ledger/2025-11.md (14:20 / 14:44 / 14:55 entries)
- planning/document_refresh_queue.md (2025-11-12 additions)
- exchange/reports/archived/order-2025-11-12-047-report.json, order-2025-11-12-048-report.json
```

## Next

- Daily Doc Refresh: ✅ 2025-11-12 slice updated `docs/nightlands_duet_telemetry_panel.md` and linked artifacts across the Nightlands docs; queue rolled forward in `planning/document_refresh_queue.md` with ledger log.
- Nightlands scoreboard placeholder imagery embedded in `exchange/attachments/guides/nightlands_duet_playtest_packet.md`; future cohorts can reference metadata under `exchange/attachments/media/nightlands_duet/` while awaiting high-fidelity captures (Order 050 closed).
- Nightlands duet telemetry feed published under `exchange/attachments/telemetry/nightlands_duet/`; integrate the feed into the shared dashboard next and keep `planning/alfa_zero_nightlands_duet_storyboard.md` aligned.
- Evaluate targeted sync log rotation once additional playtests accumulate; record outcomes in `planning/alfa_zero_targeted_sync_scope.md`.

Related

- Comfort path: `exchange/attachments/guides/comfort_happy_path.md`
- From Pain to Play: `planning/pivotal_fronts/from_pain_to_play.md`

---

## Campaign Brief - Order 045: UI Overlay Integration Slice

- Status: **Completed 2025-11-12 (order-2025-11-09-045 closed)**
- Type: Minor (runtime shells and overlay integration)
- Objective: Deliver a demonstrable UI overlay slice that exercises narration and telemetry pipelines while locking validation coverage before broader rollout.

### Pillars

- Runtime shells upgraded with overlay hooks, logging hygiene, and comfort toggles across `golf_00/delta_00/alfa_02` and `golf_00/delta_00/alfa_03` (Order 045 Day 0 instrumentation).
- UI overlay proof path capturing one end-to-end interaction through the comfort loop with retained trace artifacts.
- Validation runway extending the contract suite plus baseline heartbeat and offline sync sweep.

### Milestones

- Baseline readiness sweep captured and filed with evidence links.
- Overlay instrumentation merged into runtime shells with documented entry points and toggles.
- Contract suite passes with the new overlay regression case.
- Comfort and planning docs updated with operator runbook and stretch backlog.

### Evidence Hooks (045)

- Order: `exchange/orders/completed/order-2025-11-09-045.json`
- Ledger: `exchange/ledger/index.json`
- Runtime shells: `golf_00/delta_00/alfa_02/`, `golf_00/delta_00/alfa_03/`
- Contract suite: `tools/contract_test_runner.py`
- Comfort guide: `exchange/attachments/guides/comfort_happy_path.md`
- Overlay traces: `logs/alfa_02/narration.jsonl`, `logs/alfa_03/telemetry.jsonl`

### Stretch Considerations (045)

- Cross-workspace overlay rollout once the slice stabilizes.
- Expanded manifest automation for narrator and telemetry assets.

### Window (045)

- 2025-11-09 → 2025-11-16 (target seven-day minor campaign cadence).

---

## Campaign Brief — Order 044: Relieve the President’s Burden

- Status: **Completed 2025-11-08 (order-2025-11-07-044 closed)**
- Type: Major (cross-workspace automation + comfort improvements)
- Objective: Reduce routine operational load on High Command while increasing playability and narrative coherence during everyday work.

### Success Criteria

- Inbox triage flow: repeatable checklist; target “inbox zero” after campaign close (all reports archived/linked in ledger).
- Automation: reduce manual ack/report handling by a measurable percentage using existing exchange tools (no new infra if avoidable).
- Runtime readiness: minimal narrator/telemetry shells available for `alfa_02`/`alfa_03` to support monitoring and VO alignment.
- Contract coverage: extend contract tests to include at least one “automation path” case; all cases pass locally.
- Comfort: document a 70/30 play/dev‑ops path (single “happy path” from overlay → logs → exchange sync).

### Progress Log

- Step 1 (2025-11-08T11:40Z) — Exchange inbox verified clear; ledger primed for Order 044 evidence.
- Step 2 (2025-11-08T11:45Z) — Exchange heartbeat [OK], acknowledgement logged, and offline sync mirrored latest orders/reports ahead of runtime shell work.
- Step 3 (2025-11-08T11:46Z) — Narrator/telemetry shells exercised; comfort guide updated with commands.
- Step 4 (2025-11-08T11:47Z) — Added `automation_path_happy_flow` contract case; contract runner passes focused sweep.
- Step 5 (2025-11-08T11:50Z) — Published comfort happy path refresh and automation quick-start guide to anchor the 70/30 loop.
- Step 6 (2025-11-08T11:55Z) — Completion report archived and ledger closed for Order 044.

### Retrospective (2025-11-08)

- **Wins** heartbeat discipline, refreshed guides, and the automation contract case kept comfort and tooling evidence aligned within a single campaign arc.
- **Friction** acknowledgement timing drifted before we realigned it with the ledger, and runtime shells stayed minimal stubs that still need explicit follow-up.
- **Action Items** capture lull lessons in planning docs, schedule shell enhancements for the UI order, and keep the comfort loop verified during every lull exit.

### Dependencies

- `quint_synced/` alignment docs adopted across fronts (payload + narration).
- `golf_00/delta_00/alfa_02` and `alfa_03` scaffolds activated (even minimally) to host narrator/telemetry shells.
- Exchange heartbeat reachable with correct `SHAGI_EXCHANGE_PATH` on all workspaces.
- Inbox triage for outstanding safety/analytics reports.

### Deliverables

- Updated guides: lull checklist and automation quick-start in `exchange/attachments/guides/`.
- Minimal narrator/telemetry shell entry points under `golf_00/delta_00/alfa_02` / `alfa_03` (even stubs with TODOs).
- Extended contract samples exercising an automation path.
- Final report and ACK for Order 044 archived in exchange.

### Evidence Hooks

- Ledger: `exchange/ledger/journal.md`
- Reports: `exchange/reports/archived/order-2025-11-07-044-report.json`
- Tools: `tools/exchange_heartbeat.py`, `tools/offline_sync_exchange.py`, `tools/contract_test_runner.py`

### Risks & Mitigations

- Scope creep: keep “automation” to lightweight scripts and docs; avoid new infra.
- Schema drift: validate with `tools/schema_validator.py` + contract tests before closing.
- Partial runtime wiring: deliver minimal shells first, then iterate.

### Window

- 2025-11-08 → 2025-11-12 (day 1: inbox triage + runtime shell stubs; day 2+: automation coverage, comfort docs, validation).
