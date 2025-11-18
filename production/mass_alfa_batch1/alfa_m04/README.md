# Alfa-M04 — Genesis Batch 1

- **Order**: `order-2025-11-13-054`
- **Baseline**: `forge-alfa@2025-11-13-054`
- **Path**: `production/mass_alfa_batch1/alfa_m04`
- **Exchange slot**: `genesis-kappa`
- **Focus**: Comfort + UI overlay instrumentation (post Order‑045 learnings).

Evidence checklist
- `logs/readiness.json` → copy of the shared readiness pass establishing green status pre-seeding.
- `logs/smoke.txt` → CLI smoke output confirming schema + tooling availability.

Next steps
1. Clone baseline into `golf_03/kappa_04/alfa_m04` with overlay instrumentation toggled on.
2. Layer telemetry hooks for comfort metrics (TtF, repeat-play) before playtesters touch it.
3. After smoke + readiness reruns, escalate to Toysoldiers for joint exercises.
