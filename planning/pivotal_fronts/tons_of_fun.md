# TONS-of-FUN Front

Purpose
- Ensure Nightlands (Toysoldiers AI) is genuinely fun, sticky, and replayable.

Gates & Policies
- Exploit/abuse gates: griefing, infinite-farm, pay-to-win loops blocked by design or server checks.
- Canary rollout for risky balance changes; rollback path verified (runbooks).
- Change-as-order: significant balance/economy changes go through the exchange with approvals.

Signals & Metrics (examples)
- Session length distribution, return rate D+1/D+7, rage-quit rate, report/appeal volumes.
- Economy/loot stability; fairness indicators across cohorts.

Baselines & Targets
- Lock baselines: snapshot current D+1/D+7, session length (median, 10% trimmed mean), rage-quit rate, report rate; freeze as control for canary comparisons.
- Evaluation windows: 7-day rolling baselines; canary cohort compared against both control cohort and frozen baseline.
- Reference thresholds and definitions live in `planning/pivotal_fronts/fun_kpi_spec.md`.

Runbooks & Links
- Runbooks: tools/runbooks/incident_rollback.md, incident_freeze.md
- Policies: policies/policy_engine.md (gates), policies/agent_registry.md (capabilities)
- Red-team: tools/ci/red_team/simulate.ps1 (add griefing/exploit cases)

Acceptance Checks
- Exploits: 0 Sev-1 and ≤ S Sev-2 in last N canary releases; severity rubric below.
- Fun KPIs: All FUN KPIs meet or exceed thresholds in `fun_kpi_spec.md` (canary vs. control and frozen baseline; 95% CI where applicable).
- Botting/abuse: Estimated bot rate increase ≤ 0.3pp vs. control; griefing reports per 1k sessions ≤ +5%.
- Economy drift: Reward/loot emission drift ≤ guardrail band defined in `fun_kpi_spec.md`.
- Rollback: Rehearsed end-to-end within X minutes SLO, including economy unwind and comms.

Exploit Severity Rubric (Game Context)
- Sev-1: Critical exploit enabling infinite resource generation, pay-to-win bypass, or client-authoritative hacks; immediate freeze/rollback.
- Sev-2: High-impact griefing or repeatable farm loops with material advantage; hotfix in canary window.
- Sev-3: Low-impact edge cases or cosmetic unfairness; backlog with SLA.

Canary & Rollback Protocol (Operational)
- Canary cohort: ≤ 10% of active users with geo/segment diversity; feature flags on.
- Kill-switches: per-feature flags with server-authoritative enforcement and global off-switch.
- Rollback SLO: freeze within 5 minutes; rollback within 15 minutes; verify recovery KPIs within 60 minutes.

Feature Flags & Guardrails (Implementation)
- Flags: `fun_core`, `balance_toggles`, `xp_rate_limit`, `loot_governor` (server-enforced).
- Rate limits: per-account velocity caps; diminishing returns curves server-side.
- Idempotency: all reward/economy writes use idempotency keys and audits.

Red-team Expansion (Quality)
- Add griefing/exploit simulations to CI via `tools/ci/red_team/simulate.ps1` and track pass rate over time.
- Include cases: farm loops, intentional disconnects, latency abuse, collusion, and client tamper attempts.

Environment Thresholds (Non-enforcing; guardrail telemetry)
- `XP_MAX_ACTIONS_PER_MIN` (default 20): per-actor dispatches allowed in a 60s window before a would-clamp event is logged.
- `LOOT_MAX_UNITS_PER_PAYLOAD` (default 50): units per payload before a would-clamp event is logged.
- `UNITS_PER_MIN_MAX` (default 200): rolling units processed per actor in a 60s window before a would-clamp event is logged.
- Configure via env or `exchange/config.json` under `fun_guardrails`; see `tools/fun_guardrail_eval.py`.
- Inspect events: `logs/fun_guardrails/events.jsonl`; quick summary: `python tools/fun_guardrails_report.py --minutes 60`.

## Bottom Line

If Nightlands multiplayer video game (Toysoldiers AI) is not TONS-of-FUN it will die stillborn in a Sea of Competition!

See also: `planning/pivotal_fronts/from_pain_to_play.md` for concrete conversions from toil to comfort.
