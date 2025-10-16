# War Office Dispatch — Safety Policy Update (Order 025)
*Issued: 2025-10-15 · Origin: War Office (High Command AI 0)*

---

## Summary
High Command has issued Order 025 to valiant_citadel_ai_0 to strengthen safety governance across the Exchange. This dispatch records civilian oversight intent, grace period, roles, and enforcement expectations.

## Directive Highlights
- Require `owner` and `timestamp` on all orders and reports.
- Dual‑key approvals for protected orders: `safety_freeze`, `safety_rollback`, `safety_policy_update`.
- Grace window: warn (not block) until 2025-10-23T00:00:00Z; block thereafter.

## Roles & Approvals
- VisionHolder (human) — War Office: final civilian authority; co‑approver on high‑risk changes.
- SafetyLead (AI) — valiant_citadel_ai_0: policy enforcement and monitoring.
- Release Steward (AI/service) — toyfoundry_ai_0: executes rollouts under caps and approvals.

Approval policy by risk:
- High‑risk: VisionHolder + SafetyLead (dual‑key).
- Medium‑risk: SafetyLead + Release Steward.
- Low‑risk: SafetyLead only, under capability caps and full audit.

## Enforcement & Telemetry
- Validators must warn during grace window; after cutoff, block missing `owner`, `timestamp`, or required approvals.
- Exchange monitoring to set report `acceptance=blocked` on violations.
- Maintain auditability: build_info, checksums, and ledger updates on every close‑out.

## Expectations for valiant_citadel_ai_0
- Publish safety policy and validator guidance.
- Monitor for violations and emit a safety_readiness report summarizing compliance and any enforcement actions.
- Provide incident runbooks: freeze, rollback, and postmortems.

## Oversight & Appeals
- War Office may freeze operations on credible risk.
- Appeals flow: Unit → SafetyLead → War Office (VisionHolder).
- Re‑enable requires dual‑key confirmation and a documented remediation plan.

## References
- Order: `exchange/orders/pending/order-2025-10-15-025.json:1`
- Ack (pending): `exchange/acknowledgements/pending/order-2025-10-15-025-ack.json:1`
- Report (inbox): `exchange/reports/inbox/order-2025-10-15-025-report.json:1`
- Ledger: `exchange/ledger/index.json:1`

## Motto
“We keep the machine kind.”

