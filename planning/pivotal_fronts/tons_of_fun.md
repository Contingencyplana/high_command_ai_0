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

Runbooks & Links
- Runbooks: tools/runbooks/incident_rollback.md, incident_freeze.md
- Policies: policies/policy_engine.md (gates), policies/agent_registry.md (capabilities)
- Red-team: tools/ci/red_team/simulate.ps1 (add griefing/exploit cases)

Acceptance Checks
- No new critical exploits in last N canary releases.
- Fun KPIs stable or improving in canary vs. control.
- Rollback rehearsed within X minutes SLO.

## Bottom Line

If Nightlands multiplayer video game (Toysoldiers AI) is not TONS-of-FUN it will die stillborn in a Sea of Competition!
