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
- Inbox: cleared 2025-11-08; backlog archived to `exchange/reports/archived/inbox_backlog/`; follow-up needed for Order 035 monitoring result.
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

- During the current lull: confirm heartbeat/sync across workspaces, follow up on Order 035 monitoring result, and scope Order 044 (automation/comfort focus) with success criteria and dependencies.

---

## Planning Stub — Order 044: Relieve the President’s Burden

- Type: Major (cross‑workspace automation + comfort improvements)
- Objective: Reduce routine operational load on High Command while increasing playability and narrative coherence during everyday work.

### Success Criteria

- Inbox triage flow: repeatable checklist; target “inbox zero” after campaign close (all reports archived/linked in ledger).
- Automation: reduce manual ack/report handling by a measurable percentage using existing exchange tools (no new infra if avoidable).
- Runtime readiness: minimal narrator/telemetry shells available for `alfa_02`/`alfa_03` to support monitoring and VO alignment.
- Contract coverage: extend contract tests to include at least one “automation path” case; all cases pass locally.
- Comfort: document a 70/30 play/dev‑ops path (single “happy path” from overlay → logs → exchange sync).

### Dependencies

- `quint_synced/` alignment docs adopted across fronts (payload + narration).
- `golf_00/delta_00/alfa_02` and `alfa_03` scaffolds activated (even minimally) to host narrator/telemetry shells.
- Exchange heartbeat reachable with correct `SHAGI_EXCHANGE_PATH` on all workspaces.
- Inbox triage for outstanding safety/analytics reports.

### Deliverables

- Updated guides: lull checklist and automation quick‑start in `exchange/attachments/guides/`.
- Minimal narrator/telemetry shell entry points under `golf_00/delta_00/alfa_02` / `alfa_03` (even stubs with TODOs).
- Extended contract samples exercising an automation path.
- Final report and ACK for Order 044 archived in exchange.

### Evidence Hooks

- Ledger: `exchange/ledger/journal.md`
- Reports: `exchange/reports/archived/order-2025-11-xx-044-report.json` (to be created)
- Tools: `tools/exchange_heartbeat.py`, `tools/offline_sync_exchange.py`, `tools/contract_test_runner.py`

### Risks & Mitigations

- Scope creep: keep “automation” to lightweight scripts and docs; avoid new infra.
- Schema drift: validate with `tools/schema_validator.py` + contract tests before closing.
- Partial runtime wiring: deliver minimal shells first, then iterate.

### Window

- Proposed: 3–5 days, with day 1 focused on inbox triage and runtime shell stubs.
