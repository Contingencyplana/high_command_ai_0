# Alfa-M11 - Genesis Batch 2

- **Order**: `order-2025-11-19-060`
- **Baseline**: `forge-alfa@2025-11-19-060`
- **Path**: `production/mass_alfa_batch2/alfa_m11`
- **Exchange slot**: `genesis-iota`
- **Focus**: Layer-stacked cadence once cooldown stays under control.

Evidence checklist
- `logs/readiness.json` – Batch 2 readiness run (re-run after iota hydration to capture cooldown metrics).
- `logs/smoke.txt` – CLI smoke transcript stored for schema parity.

Next steps
1. Hydrate `golf_07/iota_05/alfa_m11` and wire cooldown telemetry hooks.
2. Re-run readiness + smoke with layered spans noted so Toyfoundry can trace cooldown performance.
3. File hello + telemetry delta referencing the layered cadence once the target workspace signs off.


High Command hydration (2025-11-22)
- Slot: golf_07/iota_05/alfa_m11
- Logs: logs/readiness.json, logs/smoke.txt, logs\mass_alfa_batch2\Alfa-M11\ops_readiness.json
- Hello: outbox/reports/hello-Alfa-M11-20251122T034506Z.json
- Notes: Reran ops_readiness; factory_order_emitter.py missing here so smoke uses exchange_all; mirrored to hub for downstream pulls.

- Smoke restored: using `python tools/factory_order_emitter.py --help` as of 2025-11-22; prior `exchange_all` smoke deprecated.

