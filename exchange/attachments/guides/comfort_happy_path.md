# Comfort Happy Path — 70/30 Play/Dev‑Ops

This loop keeps Order 044’s comfort mandate intact: spend ~70% of the cadence in playful interaction, reserve the last 30% for automation upkeep.

## 70% — Play & Story

- **Overlay session (optional but encouraged)**  
  `python scripts/play_session.py` → captures `logs/alfa_zero/overlay_events.jsonl` for lore recap.
- **Narration pulse**  
  `python -m golf_00.delta_00.alfa_02.narrator_shell --say "Forge delivers the Ally → Victory" --out logs/alfa_02/narration.jsonl`
- **Telemetry pulse**  
  `python -m golf_00.delta_00.alfa_03.telemetry_shell --event forge.deliver --status success --details "comfort happy flow" --out logs/alfa_03/telemetry.jsonl`

## 30% — Automation & Sync

- **Contract sweep (automation-path focus)**  
  `python -m tools.contract_test_runner --case automation_path_happy_flow`
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
- Automation case: `contract_samples/cases/automation_path_happy_flow.json`
  - Template seed for variants: `contract_samples/drafts/automation_path_happy_flow.json.template`
- Automation quick-start: `exchange/attachments/guides/automation_quick_start.md`
