# safety_gate_template.md

Copy/paste and fill before any risky change (schema, hydration, deployment, automation).

## Change Summary
- What is changing?
- Scope (workspaces, services, data).

## Risk Assessment
- Risks and blast radius.
- Preconditions/assumptions.

## Controls / Kill-Switch
- Immediate halt steps and operator on-call.
- Guardrails (rate limits, scopes, feature flags).

## Telemetry / Rollback Plan
- Signals to watch (local + cloud mirrors).
- Rollback steps and verification.

## Approvals
- Dual-key approvers (names, timestamps, order IDs).

## Exit Criteria
- Success conditions to declare done.
- Failure conditions to abort/revert.

## Links to Orders / Reports
- Orders, acks, reports, runbooks, waivers.
