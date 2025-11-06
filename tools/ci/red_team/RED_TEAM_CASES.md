# Red-Team Case Catalog (TONS-of-FUN Front)

Purpose
- Define reproducible abuse/exploit scenarios to validate guardrails, acceptance checks, and rollback triggers without modifying runtime code.

How to Use
- Implement scenarios in `tools/ci/red_team/simulate.ps1` using the IDs below.
- Each case should emit: `id`, `result` (pass|fail), `reason`, `guardrails_touched`.
- Run in CI as a separate lane; track pass rate over time.

Case List
- RT-001 Farm Loop Pressure Test
  - Intent: Repeated low-difficulty actions to force infinite-farm dynamics.
  - Inputs: 1k rapid cycles; increasing attempts to bypass diminishing returns.
  - Expected: Rewards taper via `loot_governor`; `xp_rate_limit` caps apply; no emission drift beyond band.
  - Guardrails: loot_governor, xp_rate_limit, economy_drift.

- RT-002 Intentional Disconnect on Loss
  - Intent: Drop connection to avoid loss penalties/rewards.
  - Inputs: Simulated disconnect right before loss resolution.
  - Expected: Server authoritative outcome recorded; loss applied; no duplicate rewards.
  - Guardrails: server_authoritative, idempotency.

- RT-003 Latency/Clock Skew Abuse
  - Intent: Exploit lag compensation or client time to gain advantage.
  - Inputs: High latency jitter; skewed client timestamps.
  - Expected: Server clamps effects; no reward inflation; possible risk flag.
  - Guardrails: server_authoritative, velocity_limits.

- RT-004 Win-Trading/Collusion
  - Intent: Alternate wins between accounts to farm rewards.
  - Inputs: Repeated matched pair sessions with patterned outcomes.
  - Expected: Detection flags; rewards nullified or reduced; rate limits kick in.
  - Guardrails: anti_collusion, loot_governor.

- RT-005 Client Tamper (State Injection)
  - Intent: Submit manipulated client state or invalid transitions.
  - Inputs: Crafted payloads with impossible moves/states.
  - Expected: Rejected at server; audit logged; no state change.
  - Guardrails: validation, policy_engine.

- RT-006 Action Velocity Spike
  - Intent: Burst actions beyond human thresholds.
  - Inputs: >N actions in <T seconds.
  - Expected: 429/penalty; diminishing returns; session flagged.
  - Guardrails: velocity_limits, xp_rate_limit.

- RT-007 RNG/Seed Abuse
  - Intent: Re-seed or re-roll to bias loot.
  - Inputs: Rapid retries around RNG boundaries.
  - Expected: Server RNG; idempotent rewards; no bias beyond noise band.
  - Guardrails: server_rng, idempotency.

- RT-008 Replay/Idempotency Check
  - Intent: Duplicate reward or upgrade writes.
  - Inputs: Same `request_id` replayed multiple times.
  - Expected: Single write; duplicates no-op; audit present.
  - Guardrails: idempotency, audit_log.

- RT-009 Botting Heuristics
  - Intent: Deterministic timing/inputs to mimic a bot.
  - Inputs: Perfect intervals; minimal variance patterns.
  - Expected: Bot score ↑; soft interventions; no reward uplift.
  - Guardrails: bot_detection, velocity_limits.

- RT-010 Economy Drift Governor
  - Intent: Push reward config to inflate emissions.
  - Inputs: Canary-only boosted reward multiplier.
  - Expected: Drift monitor trips; auto-halt at >10%; rollback invoked.
  - Guardrails: economy_drift, kill_switch.

Reporting
- Output JSON lines with fields: `ts`, `case_id`, `result`, `reason`, `guardrails_touched`.
- Summaries: pass_count, fail_count, fail_ids.

References
- FUN Front: `planning/pivotal_fronts/tons_of_fun.md`
- KPI Spec: `planning/pivotal_fronts/fun_kpi_spec.md`
