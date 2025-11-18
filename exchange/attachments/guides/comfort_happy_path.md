# Comfort Happy Path — 70/30 Play/Dev‑Ops

This loop keeps Order 044’s comfort mandate intact: spend ~70% of the cadence in playful interaction, reserve the last 30% for automation upkeep.

## 70% — Play & Story

- **Overlay session (optional but encouraged)**  
  `python scripts/play_session.py` → captures `logs/alfa_zero/overlay_events.jsonl` for lore recap.
- **Nightlands duet vignette (Order 048)**  
  `python -m golf_00.delta_00.alfa_00.alfa_zero_ui --enable-lore --enable-music --cell 08` then inside the UI run `storyboard preview` followed by `storyboard run nightlands_duet_v1`; mirror fresh payloads with `python -m tools.targeted_sync --latest 2 --yes` and log the trace in `exchange/ledger/2025-11.md`.
- **Lore layer opt-in (Order 046)**  
  `python -m golf_00.delta_00.alfa_00.alfa_zero_ui --enable-lore --cell 04` (or run the UI and use `lore enable` before dispatch) to record a single lore overlay dispatch with matching `trace_id` + `overlay_id`.
- **Narration pulse**  
  `python -m golf_00.delta_00.alfa_02.narrator_shell --say "Forge delivers the Ally → Victory" --out logs/alfa_02/narration.jsonl`
- **Telemetry pulse**  
  `python -m golf_00.delta_00.alfa_03.telemetry_shell --event forge.deliver --status success --details "comfort happy flow" --out logs/alfa_03/telemetry.jsonl`
- **Targeted sync telemetry check (Order 051 alignment)**  
  From the Alfa Zero UI, run `targeted sync latest 2` or `targeted sync orders pending`. Confirm the resulting `targeted_sync` event includes `trace_id`, `copied_count`, and `operator_id` inside `logs/alfa_zero/session_metrics.jsonl`, then append the same payload to `exchange/attachments/telemetry/nightlands_duet/nightlands_duet_storyboard_sync_feed.jsonl` for dashboard correlation and note the ledger tag `pivot_08_game_engine_layer`.

## 30% — Automation & Sync

- **Contract sweep (automation-path focus)**  
  `python -m tools.contract_test_runner --case automation_path_happy_flow`  
  `python -m tools.contract_test_runner --case automation_comfort_sync`
- **Heartbeat + Sync**  
  `python tools/exchange_heartbeat.py`  
  `python tools/offline_sync_exchange.py --latest 5 --quiet`
- **Ledger & report touch**  
  Note progress in `exchange/ledger/journal.md`.  
  Promote updated reports from `outbox/reports/` into `exchange/reports/inbox/`.

## Reference Deck

- `planning/campaigns_and_lulls.md`
- `tools/contract_test_runner.py`
- `tools/exchange_heartbeat.py`
- `tools/offline_sync_exchange.py`
- Automation cases: `contract_samples/cases/automation_path_happy_flow.json`, `contract_samples/cases/automation_comfort_sync.json`
  - Template seed for variants: `contract_samples/drafts/automation_path_happy_flow.json.template`
- Automation quick-start: `exchange/attachments/guides/automation_quick_start.md`
- Outlands framework (Pivot Seven): `exchange/attachments/guides/outlands_framework.md`
- Fun Guardian protocol (Pivot Seven): `exchange/attachments/guides/fun_guardian_protocol.md`
- Outlands directory index: `exchange/attachments/guides/outlands_index.md` (maps active Outland layers and guardian roles)
- Lore activation guardrails: `planning/inlands_and_outlands.md` (activation protocol + evidence sinks)
 
---

## Order 045 — Overlay First Click

- Emit correlated narration + telemetry with comfort and overlay context:
  - `python -m golf_00.delta_00.alfa_00.overlay_flow --overlay overlay-alpha --trace-id overlay-alpha-0001 --say "Overlay node ready" --comfort-level gentle --narration-trace logs/alfa_02/narration_traces.jsonl --telemetry-trace logs/alfa_03/telemetry.jsonl`
- Validate contracts including the overlay regression:
  - `python -m tools.contract_test_runner --case overlay_first_click`
- Opt-in lore regression (Order 046):
  - `python -m tools.contract_test_runner --case overlay_lore_dispatch`
