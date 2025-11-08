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

```
Name: <Campaign Name>
Window: <YYYY-MM-DD → YYYY-MM-DD>
Type: Major|Minor
Objective: <1–2 lines>
Orders: <IDs>
Outcomes: <1–3 bullets>
Evidence: <key files/paths>
```

## Current State Snapshot
- Orders queue: clear (`exchange/orders/pending` only `.gitkeep`).
- Inbox: cleared 2025-11-08; backlog archived to `exchange/reports/archived/inbox_backlog/`; Order 035 monitor result published (promote recommendation).
- Recent completions: 040/041/043 closed; reports and acks archived (see `exchange/ledger/index.json`).

## Chronicle — Recent Campaigns

```
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

```
Name: Cross‑Workspace Telemetry & Narration
Window: 2025-11-01 → 2025-11-01
Type: Minor → alignment/stubs
Objective: Align narration/telemetry stubs and monitoring across workspaces.
Orders: order-2025-11-01-041
Outcomes:
- Narration + payload alignment briefs published under `quint_synced/`.
- Monitoring/ingestion guidance documented; runtime shells pending in alfa_02/alfa_03.
Evidence:
- exchange/reports/archived/order-2025-11-01-041-report.json
- quint_synced/payload_alignment.md
- quint_synced/narration_alignment.md
```

```
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

## Next

- Walk the lull checklist now: review Order 044 evidence, clear any straggling inbox artifacts, and log retrospective notes.
- Draft candidate scope for the UI overlay push (targeted as Order 045) with runtime shell enhancements, narration hooks, and comfort loop validation baked in.
- Confirm tooling readiness — contract suite, heartbeat scripts, and offline bridge — so the next campaign launches on a clean baseline.

Related

- Comfort path: `exchange/attachments/guides/comfort_happy_path.md`
- From Pain to Play: `planning/pivotal_fronts/from_pain_to_play.md`

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
- Reports: `exchange/reports/inbox/order-2025-11-07-044-report.json` (promote to archived on close)
- Tools: `tools/exchange_heartbeat.py`, `tools/offline_sync_exchange.py`, `tools/contract_test_runner.py`

### Risks & Mitigations

- Scope creep: keep “automation” to lightweight scripts and docs; avoid new infra.
- Schema drift: validate with `tools/schema_validator.py` + contract tests before closing.
- Partial runtime wiring: deliver minimal shells first, then iterate.

### Window

- 2025-11-08 → 2025-11-12 (day 1: inbox triage + runtime shell stubs; day 2+: automation coverage, comfort docs, validation).
