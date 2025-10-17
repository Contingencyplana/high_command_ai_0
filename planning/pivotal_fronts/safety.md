# Safety Front (Citadel)

**Front Number:** 2  
**Category:** Core Front  

---

## Mission

- Guard Daylands: prevent harm, enforce consent, manage entropy
- Prevent catastrophic outcomes; contain and reverse unsafe trajectories quickly
- Freeze/rollback on credible risk; run red-team safely

---

## Core Docs

- Daylands Charter: `planning/daylands_and_nightlands.md:1`
- AI Agents & Safety: `planning/ai_agents_and_safety.md:1`
- Safety Gate Template: `planning/templates/safety_gate_template.md:1`

---

## Policy & Gates

- **Required metadata** (Order 025): owner, timestamp, approvers (protected), build_info, checksums
- **Required fields** on all exchange messages; dual-key approvals for protected orders
- **Gates:** proposal → sandbox → canary → GA; dual‑key for protected orders
- **Kill-switch protocol:** (policies/kill_switch.md) with documented disable/reenable
- **Capability leases and revocation:** (policies/agent_registry.md)

---

## Signals & Monitoring

- Watcher WARN/BLOCKED counts; abnormal rates; schema violations
- Incident frequency, time-to-freeze, time-to-rollback

---

## Interfaces

- **Exchange orders:** safety_freeze, safety_rollback, safety_policy_update
- **Reports:** safety_incident_report, safety_readiness

---

## Runbooks & Links

- **Runbooks:** 
  - `tools/runbooks/monitoring_and_rollback.md:1`
  - `tools/runbooks/incident_freeze.md`
  - `tools/runbooks/incident_rollback.md`
  - `tools/runbooks/postmortem_template.md`
- **Policies:** 
  - `policies/policy_engine.md`
  - `policies/safety_config.yaml`
- **Schemas:** `exchange/schemas/*.schema.json`
- **Watcher:** `tools/ci/safety_watcher.ps1`

---

## Acceptance Checks

- ✅ Dual-key approvals enforced on protected orders; no bypasses
- ✅ Kill-switch drill executed successfully within SLO
- ✅ Postmortems include prevention actions with owners/dates
