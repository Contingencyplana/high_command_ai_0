# 🛡️ operational_thresholds_and_safety.md — Doctrine of Restraint

*Planning Scroll — `high_command_ai_0/planning/`*

---

## 🌍 Purpose

Establishes quantitative guardrails, safety procedures, and tooling considerations that keep SHAGI’s growth disciplined. These thresholds apply to both High Command and field workspaces and must be revisited each phase before expansion.

---

## 📊 1. Phase Thresholds

| Phase | Scope | Max Active Alfas | Entropy Ceiling | Rotation Cadence | Action Trigger |
|-------|-------|------------------|-----------------|------------------|----------------|
| Phase 1 | 1 Golf (256 Alfas) | 128 active at once | 0.50 | Weekly | Any cell > 0.60 entropy enters quarantine |
| Phase 2 | 4 Golfs (~1,000 Alfas) | 512 active | 0.55 | Twice weekly | Division average > 0.52 entropy pauses scaling |
| Phase 3 | Full Juliett (4,096 Alfas) | 2,048 active | 0.58 | Daily rolling | Province > 0.60 requires human review |
| Phase 4 | Networked Alfas | Config-driven | Config-driven | Continuous | Automated alerts feed to Intermesh |

- “Active” means currently hydrated with more than the base two rank files.
- Quarantine moves Alfas to `archives/` via `forge archive` until a remediation plan exists.

---

## 🔄 2. Operational Rhythm

- **Morning Sweep:** High Command reviews previous day’s `field-report@1.0` summaries and updates `ledger/index.json` statuses.
- **Midday Sync:** Field workspaces pull `exchange/` repo, acknowledge new orders, and push progress logs.
- **Evening Reflection:** Intermesh Command consolidates insights, comparing entropy trends against table above.
- **Weekly Audit:** Human overseer samples 5% of orders/reports to verify adherence to schema and safety rails.

---

## 🧯 3. Safety Rails

1. **Rate Limits:** No workspace may process more than 20 High Command orders per UTC hour. Forge enforces this by tracking timestamps in `logs/forge.log`.
2. **Human Approvals:** Any directive that alters core templates, modifies Forge safety config, or touches Nightland quarantine requires a named human sign-off recorded in `ledger/journal.md`.
3. **Audit Trail:** All automated scripts append git tags of form `audit-YYYYMMDD-NN` before performing destructive changes.
4. **Lock Files:** Presence of `safety.lock` at workspace root halts Forge commands and exchange syncs except for `status`/`unlock`.
5. **Schema Guard:** CI or pre-commit hooks run schema validation on orders, reports, manifests, and Forge configs; failures block commit.
6. **Alerting:** Threshold breaches emit a new `alert@1.0` payload under `exchange/acknowledgements/pending/` to ensure acknowledgement loop captures anomalies.

---

## 🖥️ 4. IDE & Version Control Considerations

- **Lazy Provisioning:** Forge defaults to generating only active ranks; additional ranks materialize on demand to keep file counts manageable for VS Code.
- **Archive Bundles:** Dormant Alfa folders compress into `.zip` packages under `archives/` with manifest pointers, reducing git churn.
- **Batch Commits:** Scripts group changes by division (Golf/Hotel) to avoid massive single commits that hinder review.
- **Git LFS Avoidance:** Keep artifacts text-based or small; large binaries should reside outside repo, referenced by checksum.
- **Index Refresh:** Regenerate `ledger/index.json` after bulk operations rather than constantly watching files, reducing extension load.
- **Workspace Filters:** Provide recommended VS Code settings (`files.watcherExclude`, `search.exclude`) tailored for 4,096 Alfa structures.

---

## 🗂️ 5. Documentation Duties

- Update `README.md` with links to this doctrine and the command exchange spec.
- Maintain change log (`planning/change_log.md`) summarizing threshold adjustments and safety incidents.
- Record deviations and waivers in `ledger/journal.md` with unique waiver IDs (`waiver-YYYYMMDD-###`).

---

## 🚀 6. Immediate To-Do List

1. Add `safety.lock` handling to Forge CLI skeleton.
2. Draft VS Code settings snippet illustrating watcher exclusions for large Alfa counts.
3. Implement `alert@1.0` schema alongside existing message definitions.
4. Set up weekly audit checklist template under `planning/audit_templates/` (to be created).
5. Schedule first threshold review after Phase 1 pilot concludes.

Adhering to this doctrine keeps SHAGI’s growth deliberate, reversible, and accountable.
