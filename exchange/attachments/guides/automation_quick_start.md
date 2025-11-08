# Automation Quick-Start — Order 044 Comfort Loop

Use this checklist when spinning up the automation + comfort tooling introduced with Order 044.

## 1. Prep & Environment

- Ensure `SHAGI_EXCHANGE_PATH` points at the shared exchange hub.
- Activate the repo virtual environment: `.\\.venv\\Scripts\\activate` (or preferred shell equivalent).

## 2. Contract Coverage

- Focus run: `python -m tools.contract_test_runner --case automation_path_happy_flow`
- Full sweep (optional): `python -m tools.contract_test_runner`
- If a case fails, inspect `contract_samples/cases/<name>.json`, adjust expectations, and rerun until green.

## 3. Narration + Telemetry Pulses

- Narration stub: `python -m golf_00.delta_00.alfa_02.narrator_shell --say "Forge delivers the Ally → Victory" --out logs/alfa_02/narration.jsonl`
- Telemetry stub: `python -m golf_00.delta_00.alfa_03.telemetry_shell --event forge.deliver --status success --details "automation quick-start" --out logs/alfa_03/telemetry.jsonl`
- These stubs prove the runtime hook points without requiring the full overlay.

## 4. Heartbeat & Sync

- `python tools/exchange_heartbeat.py`
- `python tools/offline_sync_exchange.py --latest 5 --quiet`
- Resolve any warnings before filing reports; heartbeat + sync evidence is expected in the Order 044 completion package.

## 5. Journal & Reports

- Log completion notes in `exchange/ledger/journal.md` (reference Order 044 progress).
- Promote updated field reports from `outbox/reports/` → `exchange/reports/inbox/`, tagging artifacts such as `comfort_happy_path.md` or contract runner output.

## 6. Continue the Loop

- Re-run Steps 2–5 whenever comfort tooling changes.
- Share highlights in the next lull recap so the 70/30 cadence stays healthy.
