# From Pain to Play — Flipping The Defaults

Purpose: replace orthodox “Bring the Pain” software habits with a joyful, reliable cadence that prefers comfort, clarity, and play — without sacrificing rigor.

## Common Pain Anti‑Patterns
- Toil gates: progress requires manual, error‑prone steps and approvals.
- Opaque CI: failures without fast local reproduction or clear artifacts.
- Log churn: generated logs pollute source control and mental bandwidth.
- Schema drift: payloads evolve without shared fixtures or validators.
- Surprise work: dynamic imports and hidden dependencies break unexpectedly.

## Play Conversions (What We Do Instead)
- Comfort happy path: follow a single 70/30 flow (play → tests → stubs → heartbeat → sync) — see `exchange/attachments/guides/comfort_happy_path.md`.
- Contracts as fun gates: green contract suite is your “level clear” — run `python -m tools.contract_test_runner`.
- Drafts → Cases: stage new contract ideas under `contract_samples/drafts/` and promote to `cases/` only when ready.
- Lull discipline: during lulls, triage inbox, refresh docs, verify heartbeat/sync, and plan the next campaign — see `planning/campaigns_and_lulls.md`.
- Logs untracked: generated telemetry stays out of VCS by default; track only curated evidence.

## Guardrails
- Do not close a campaign unless:
  - Contract suite is green for all cases.
  - Narration/payload alignment reviewed (see `quint_synced/payload_alignment.md` and `quint_synced/narration_alignment.md`).
  - Heartbeat + offline sync pass across workspaces.
  - Inbox triaged and ledger entries added.

## Metrics That Matter
- Time‑to‑fun: time from intent to a passing contract case.
- Red→Green ratio: failing vs. passing contract runs during a campaign.
- Lull exit readiness: checklist complete without human heroics.

## Pointers
- Cadence: `planning/campaigns_and_lulls.md`
- Comfort path: `exchange/attachments/guides/comfort_happy_path.md`
- Contracts: `tools/contract_test_runner.py`, `contract_samples/README.md`
- Emoji compiler surface: `golf_00/delta_00/alfa_04/emoji_translator.py`, `golf_00/delta_00/alfa_04/factory_adapter.py`
