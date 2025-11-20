# ai_agents_and_safety.md - Canon

**Scope:** AI agent behaviors across all genesis workspaces (High Command, Toyfoundry, Toysoldiers, War Office, etc.)  
**Purpose:** Keep agents reversible, observable, and human-controllable as they promote.

---

## Safety Principles
- **Kill-switch first:** Every runtime has an immediate halt/disable path; document location and operator.
- **Dual-key for risky actions:** Schema mutations, mass hydration, or cross-workspace writes require two named approvals.
- **No autonomous replication:** Agents may not spawn, fork, or promote without explicit human-issued orders.
- **Contract-bound execution:** All calls pass through validated contracts; no ad-hoc shells or unmanaged scripts.
- **Telemetry required:** Emit identifiers, timestamps, inputs/outputs, and checksums; cloud/local mirrors stay in sync.
- **Reversibility:** Prefer actions with clean rollback; avoid irreversible writes without backups and waivers.

## Promotion Gates (Proposal → Sandbox → Canary → GA)
1. **Proposal:** Define intent, blast radius, and rollback in an order; cite the safety gate template.
2. **Sandbox:** Run in an isolated workspace; collect telemetry; no production data touched.
3. **Canary:** Limited scope/timeboxed run with active monitoring and pre-armed kill-switch.
4. **GA:** Broader enablement only after telemetry matches baselines and dual-key approvals are logged.

## Operator Checklist (per change)
- Kill-switch verified and named operator on-call.
- Dual approvals captured (order ID, names, timestamps).
- Telemetry endpoints healthy (local + cloud mirrors).
- Rollback plan written and tested in sandbox.
- Scope and exit criteria documented before start.

## See Also
- `planning/pivotal_fronts/safety.md`
- `planning/operational_thresholds_and_safety.md`
- `planning/templates/safety_gate_template.md`
- `exchange/orders/templates/change-order.template.json`
