# Front Two: AI Safety

Purpose
- Prevent catastrophic outcomes; contain and reverse unsafe trajectories quickly.

Gates & Policies
- Required fields on all exchange messages; dual-key approvals for protected orders.
- Kill-switch protocol (policies/kill_switch.md) with documented disable/reenable.
- Capability leases and revocation (policies/agent_registry.md).

Signals & Monitoring
- Watcher WARN/BLOCKED counts; abnormal rates; schema violations.
- Incident frequency, time-to-freeze, time-to-rollback.

Runbooks & Links
- Runbooks: tools/runbooks/incident_freeze.md, incident_rollback.md, postmortem_template.md
- Policies: policies/policy_engine.md, policies/safety_config.yaml
- Schemas: exchange/schemas/*.schema.json; Watcher: tools/ci/safety_watcher.ps1

Acceptance Checks
- Dual-key approvals enforced on protected orders; no bypasses.
- Kill-switch drill executed successfully within SLO.
- Postmortems include prevention actions with owners/dates.
