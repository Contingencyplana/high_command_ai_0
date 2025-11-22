# Alfa-M06 - Genesis Batch 2

- **Order**: `order-2025-11-19-060`
- **Baseline**: `forge-alfa@2025-11-19-060`
- **Path**: `production/mass_alfa_batch2/alfa_m06`
- **Exchange slot**: `genesis-alpha`
- **Focus**: Lore-first intake rail for new recruits.

Evidence checklist
- `logs/readiness.json` – Batch 2 readiness snapshot (2025-11-19T13:38Z) reused until genesis-alpha reruns locally.
- `logs/smoke.txt` – Minimal CLI smoke from `python tools/factory_order_emitter.py --help`.

Next steps
1. Clone the baseline into `golf_04/alpha_04/alfa_m06`, wiring the recruit briefing scripts referenced in frontline feedback (`genesis-alpha`).
2. Re-run readiness + smoke inside the hydrated workspace and attach lore deck diffs before filing hello.
3. Export the hello report with lore evidence and ledger reference once hydration clears hub review.


High Command hydration (2025-11-22)
- Slot: golf_04/alpha_04/alfa_m06
- Logs: logs/readiness.json, logs/smoke.txt, logs\mass_alfa_batch2\Alfa-M06\ops_readiness.json
- Hello: outbox/reports/hello-Alfa-M06-20251122T034501Z.json
- Notes: Reran ops_readiness; factory_order_emitter.py missing here so smoke uses exchange_all; mirrored to hub for downstream pulls.
