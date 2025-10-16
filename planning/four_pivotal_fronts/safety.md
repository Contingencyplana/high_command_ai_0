# Safety Front (Citadel)

Mission
- Guard Daylands: prevent harm, enforce consent, manage entropy.
- Freeze/rollback on credible risk; run red-team safely.

Core Docs
- Daylands Charter: `planning/daylands_and_nightlands.md:1`
- AI Agents & Safety: `planning/ai_agents_and_safety.md:1`
- Safety Gate Template: `planning/templates/safety_gate_template.md:1`

Policy & Gates
- Required metadata (Order 025): owner, timestamp, approvers (protected), build_info, checksums.
- Gates: proposal → sandbox → canary → GA; dual‑key for protected orders.

Interfaces
- Exchange orders: safety_freeze, safety_rollback, safety_policy_update
- Reports: safety_incident_report, safety_readiness

Runbooks
- Monitoring & Rollback: `tools/runbooks/monitoring_and_rollback.md:1`
