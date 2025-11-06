# Fun KPI Spec (TONS-of-FUN Front)

Purpose
- Define clear, measurable FUN KPIs, guardrails, and decision rules for canary evaluation and rollback.

Scope
- Applies to multiplayer gameplay changes affecting balance, rewards, difficulty, UX friction, or economy pacing.

KPI Definitions
- D+1 Retention: % of new users (day 0) returning on day 1.
- D+7 Retention: % of new users returning on day 7.
- Session Length: median session minutes and 10% trimmed mean.
- Rage-Quit Rate: % sessions ending within 60s of a loss/negative event.
- Report Rate: player reports per 1,000 sessions; Appeal Uphold Rate: % of appeals upheld.
- Fairness Gap: absolute difference in win rate between top and bottom skill quintiles.
- Economy Drift: % change vs. control in rewards/min, loot/session, and time-to-upgrade.
- Bot Rate: estimated % of sessions flagged as automated by heuristics/classifier.

Measurement Details
- Baselines: 7-day rolling baselines; freeze snapshot before canary start.
- Cohorts: canary ≤ 10% of active users; control = remaining similar segments.
- Confidence: non-inferiority where applicable at ~95% CI; guardrails use point estimates with safety margins.
- Sample sizes: minimum 5k users or 50k sessions in canary before decision unless Sev-1 exploit triggers earlier action.

Guardrails & Thresholds (Canary must satisfy all)
- D+1 Retention: canary ≥ control − 2pp (non-inferiority).
- D+7 Retention: canary ≥ control − 3pp.
- Session Length: median delta ≥ 0; trimmed mean ≥ −2% vs. control.
- Rage-Quit Rate: canary ≤ control × 1.05 (≤ +5% relative).
- Fairness Gap: increase ≤ +2pp vs. control.
- Economy Drift: |RPM|, loot/session drift ≤ 7%; automatic halt at > 10%.
- Report Rate: reports/1k sessions ≤ control × 1.10; appeals uphold rate not worse by > 5pp.
- Bot Rate: increase ≤ +0.3pp vs. control; classifier threshold unchanged during canary.
- Exploits: 0 Sev-1; ≤ S Sev-2 (S set by release manager; default S=0).

Decision Rules
- Ship: all guardrails met and no Sev-1; Sev-2 count ≤ S.
- Pause: any guardrail violated without Sev-1; investigate/hotfix before resuming canary.
- Rollback: any Sev-1, economy drift > 10%, or rage-quit > +10%.

Operational SLOs
- Freeze: ≤ 5 minutes from decision to flag disable.
- Rollback: ≤ 15 minutes to prior stable config and assets.
- Verification: ≤ 60 minutes to confirm KPI reversion within baseline bands.

Ownership
- DRI: Game PM (FUN front) with support from Data, Ops, and Live Service.
- Approvals: change-as-order through `exchange/` with PM + Ops sign-off.

References
- FUN Front: `planning/pivotal_fronts/tons_of_fun.md`
- Red-team: `tools/ci/red_team/simulate.ps1`
- Runbooks: `tools/runbooks/incident_freeze.md`, `tools/runbooks/incident_rollback.md`
