# Comfort Happy Path — 70/30 Play/Dev‑Ops

A quick, repeatable flow to keep things comfortable during daily work.

1) Play the overlay (optional)
- `python scripts/play_session.py` (records `logs/alfa_zero/overlay_events.jsonl`)

2) Run contract checks
- `python -m tools.contract_test_runner` (or `--case <name>`)

3) Narration + Telemetry stubs (044)
- Narration: `python -m golf_00.delta_00.alfa_02.narrator_shell --say "Forge crafts the Ally → Victory" --out logs/alfa_02/narration.jsonl`
- Telemetry: `python -m golf_00.delta_00.alfa_03.telemetry_shell --event forge.craft --status success --details "happy path" --out logs/alfa_03/telemetry.jsonl`

4) Heartbeat + Sync
- `python tools/exchange_heartbeat.py`
- `python tools/offline_sync_exchange.py`

5) Ledger + Reports
- Add concise ledger note in `exchange/ledger/journal.md` when closing an order.
- Use report skeletons in `outbox/reports/` and promote to `exchange/reports/inbox/`.

Links
- `planning/campaigns_and_lulls.md`
- `tools/contract_test_runner.py`
- `tools/exchange_heartbeat.py`
- `tools/offline_sync_exchange.py`
 - Template (automation case): `contract_samples/drafts/automation_path_happy_flow.json.template`
   - When filled, move to `contract_samples/cases/automation_path_happy_flow.json`
   - Run: `python -m tools.contract_test_runner --case automation_path_happy_flow`
