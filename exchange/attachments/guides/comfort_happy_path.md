# Comfort Happy Path — 70/30 Play/Dev‑Ops

A quick, repeatable flow to keep things comfortable during daily work.

- **Step 1: Play the overlay (optional)**  
  Run `python scripts/play_session.py` (records `logs/alfa_zero/overlay_events.jsonl`).

- **Step 2: Run contract checks**  
  Run `python -m tools.contract_test_runner` (or `--case <name>`).

- **Step 3: Narration + Telemetry stubs (Order 044)**  
  Narration: `python -m golf_00.delta_00.alfa_02.narrator_shell --say "Forge crafts the Ally → Victory" --out logs/alfa_02/narration.jsonl`  
  Telemetry: `python -m golf_00.delta_00.alfa_03.telemetry_shell --event forge.craft --status success --details "happy path" --out logs/alfa_03/telemetry.jsonl`

- **Step 4: Heartbeat + Sync**  
  Run `python tools/exchange_heartbeat.py` and `python tools/offline_sync_exchange.py`.

- **Step 5: Ledger + Reports**  
  Add a concise ledger note in `exchange/ledger/journal.md` when closing an order, then promote report skeletons from `outbox/reports/` to `exchange/reports/inbox/`.

## Links

- `planning/campaigns_and_lulls.md`
- `tools/contract_test_runner.py`
- `tools/exchange_heartbeat.py`
- `tools/offline_sync_exchange.py`
- Automation case: `contract_samples/cases/automation_path_happy_flow.json`
  - Adjust expectations as needed, then run `python -m tools.contract_test_runner --case automation_path_happy_flow`
  - Template for future variants: `contract_samples/drafts/automation_path_happy_flow.json.template`
