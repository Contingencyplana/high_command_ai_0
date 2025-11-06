# FUN Feature Flags – Plumbing Map

Purpose
- Identify where to wire and enforce FUN front feature flags with minimal, server-authoritative changes.

Flags (server-enforced)
- `fun_core`: Enables FUN cohort code paths and telemetry.
- `balance_toggles`: Allows live tuning of balance parameters under flag.
- `xp_rate_limit`: Applies diminishing returns/velocity caps for XP.
- `loot_governor`: Caps loot emission and clamps outliers.

Configuration
- Source of truth: `exchange/config.json` (defaults) with per-env overrides.
- Access pattern: inject into runtime via config loader; expose read-only getters.

Plumbing Points
- `golf_00/delta_00/alfa_00/alfa_zero_controller.py`
  - Apply `xp_rate_limit` and `loot_governor` checks before reward writes.
  - Use idempotency keys on economy writes; emit audit events.

- `golf_00/delta_00/alfa_00/overlay_bridge.py`
  - Gate UI/overlay actions by `fun_core` and `balance_toggles` to prevent client-side exposure when disabled.

- `golf_00/delta_00/alfa_00/overlay_test_harness.py`
  - Add paramization to run with flags on/off and validate behavior parity.

- `tools/exchange_heartbeat.py`
  - Monitor flag states; provide global kill-switch handler to disable `fun_core`/`loot_governor` at runtime.

- `tools/contract_test_runner.py`
  - Add fixtures for flag-on/flag-off runs; assert idempotency and rate-limit behavior under `xp_rate_limit`/`loot_governor`.

Test Strategy
- Unit: enforce guards on reward paths; table-driven tests for edge cases.
- Contract: simulate farm loops and verify clamps; confirm idempotent writes.
- CI Red-team: integrate `tools/ci/red_team/simulate.ps1` and track pass/fail.

Operational Notes
- All client-visible flags must still be enforced server-side.
- Default to safest posture (flags off) in production; canary enables per cohort.
- Ensure flags are queryable for telemetry segments (tag sessions with active flags).
