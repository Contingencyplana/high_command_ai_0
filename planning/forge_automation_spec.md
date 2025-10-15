# ⚒️ forge_automation_spec.md — The Forge Design Doctrine

*Division: High Command AI — Forge Automation Doctrine*

---

## 🌍 Purpose

Defines the automation toolkit ("The Forge") that constructs, hydrates, archives, and audits Alfa minds across High Command, Toyfoundry, and field workspaces. Establishes interface contracts, template strategy, and safety instrumentation before large-scale Alfa generation begins.

### Non-Goals

- Selecting model architectures or runtime orchestration.
- Acting as a deployment runner; integrates with existing CI/CD.
- Providing data labeling or evaluation frameworks.
- Replacing human review; instead, it enforces review gates.

### Success Criteria

- Reproducible outputs from versioned templates with checksums recorded.
- Complete audit trail per run (JSONL logs + human journal entries).
- Safety gates enforced (diff-plan, lockfile, batch limits) by default.
- Cross-repo parity: same commands/flags behave identically.
- CI hook verifies templates/config on PRs that touch Forge areas.
- New Alfa bootstrap + validate completes in ≤ 5 minutes locally.

---

## 🧭 1. Guiding Principles

- **Deterministic Templates:** Every generated file derives from versioned blueprints to guarantee reproducibility.
- **Lazy Materialization:** Only create rank files when required for a mission; keep dormant structure compressed.
- **Symmetric Operations:** Forge commands behave identically in High Command and field workspaces.
- **Auditability:** Every Forge action writes to a log with inputs, outputs, and Git diffs.
- **Human Override:** High Command can pause or roll back automated actions via a fail-safe lock file.

---

## 🔧 2. CLI Surface

`forge <command> [options]`

| Command | Description | Key Options |
|---------|-------------|-------------|
| `init-alfa` | Create new Alfa folder from templates. | `--id`, `--workspace`, `--activate-ranks`, `--template-version` |
| `hydrate` | Populate missing rank files for existing Alfa. | `--id`, `--ranks`, `--force` |
| `archive` | Compress inactive Alfa into archive bundle. | `--id`, `--reason`, `--retain-manifest` |
| `batch-run` | Execute simulation run across selection. | `--selector`, `--ticks`, `--report` |
| `sync-ledger` | Regenerate manifests and checksum tables. | `--scope`, `--output` |
| `validate` | Lint manifests, schemas, and templates. | `--id`, `--schema`, `--fix` |
| `diff-plan` | Preview changes without applying them. | Inherits options from target command |

`diff-plan` acts as a dry-run wrapper around any command, outputting patch previews and log entries without touching the workspace.

---

## 🧱 3. Template Architecture

Templates live in `template/forge/` inside each workspace (tracked by git). Versioning uses semantic tags (e.g., `forge-template@1.2.0`).

```plaintext
template/
 └─ forge/
     ├─ alfa/
     │   ├─ alfa.py.j2
     │   ├─ manifest.json.j2
     │   └─ metadata.yaml
     ├─ ranks/
     │   ├─ bravo.json.j2
     │   ├─ charlie.json.j2
     │   └─ ...
     └─ macros/
         └─ filters.py
```

- `metadata.yaml` declares required variables, default values, and validation rules.
- Jinja2 (or equivalent) renders templated files; macros provide reusable filters (e.g., checksum seeds).
- Templates include placeholder comments describing their purpose; Forge strips scaffolding comments unless `--keep-notes` is passed.

---

## 📦 4. Configuration

Forge looks for `forge.config.json` at workspace root:

```json
{
  "version": "1.0.0",
  "default_template_version": "forge-template@1.0.0",
  "alfa_root": "alfas/",
  "archive_root": "archives/",
  "log_path": "logs/forge.log",
  "safety": {
    "max_alfa_per_batch": 64,
    "require_diff_plan": true,
    "lockfile": "forge.lock"
  }
}
```

- `max_alfa_per_batch` prevents runaway operations.
- `require_diff_plan` forces operators to review dry-run output for destructive actions.
- Presence of `forge.lock` freezes all commands except `status` and `unlock`.

---

## 🧮 5. Selector Syntax

`--selector` accepts expressions for batch operations:

```text
# Examples
id:alfa_0001
rank:golf
entropy>=0.5
workspace:toysoldiers_ai_0 AND realm:nightland
```

Selectors run against `ledger/index.json` to build target lists. Forge refuses commands that match more than `max_alfa_per_batch` entries unless `--override` is approved by High Command (flag recorded in logs).

---

## 🗂️ 6. Logging & Telemetry

- Primary log: `logs/forge.log` (rotating 5 MB files).
- Each command run emits a JSON line entry containing timestamp, operator, parameters, target IDs, and git diff summaries.
- Forge also appends a human-readable entry to `logs/forge_journal.md` for quick audits.
- Failed commands emit diagnostic bundles under `logs/failures/<timestamp>/` including stack traces and partial outputs.

---

## 🛡️ 7. Safety Instrumentation

1. **Pre-flight Checks:** Validate workspace cleanliness (no uncommitted changes) unless `--allow-dirty` is set.
2. **Checksum Guard:** After file generation, compute SHA256 checksums and update `manifest.json` accordingly.
3. **Rollback Pack:** If a command modifies more than 10 files, Forge snapshots originals to `logs/rollback/<command-id>/`.
4. **Human Approval Gate:** Commands that mutate Nightlands -> Daylands transitions require `--approved-by` metadata stored in log entry.
5. **Rate Limiter:** Enforce minimum 5-second interval between batch operations to avoid resource thrash.

---

## 🔄 8. Integration Points

- **Command Exchange:** `batch-run` can emit `field-report@1.0` payloads automatically into the exchange repo.
- **CI Hooks:** Optional GitHub Actions workflow can run `forge validate` on pull requests touching template or config files.
- **Schema Validator:** Shared library used by both Forge and manual scripts to ensure `manifest.json` and message payloads stay in sync.
- **Ops Playbook:** See "10. Verification Playbook" for quick validation commands (dry-run renders, safety gates, logs, CI checks).

---

## 🚀 9. Immediate Implementation Tasks

1. **Bootstrap template library** inside `template/forge/` with minimal Alfa pair (`alfa.py`, `manifest.json`).
   - Acceptance: Rendering from versioned templates produces identical outputs across machines; `manifest.json` includes SHA256 checksums recorded.
2. **Author Forge CLI skeleton** (Python `typer` or Node `oclif` suggested) with commands `init-alfa`, `diff-plan`, and `validate` stubbed.
   - Acceptance: `diff-plan` runs without mutation and is required for destructive ops; command/flag surface is identical in High Command, Toyfoundry, and field repos.
3. **Implement logging subsystem** writing JSON lines + journal entries.
   - Acceptance: Each run emits JSONL entries with {timestamp, operator, params, targets, git-diff}; `logs/forge_journal.md` updated; failures create bundles under `logs/failures/<ts>/`.
4. **Draft selector interpreter** operating on `ledger/index.json`.
   - Acceptance: Safety gates enforced — batch limit respected, lockfile halts mutations, and `--approved-by` required for sensitive transitions.
5. **Write integration tests** that spin up a synthetic workspace, run `init-alfa`, and assert manifest correctness.
   - Acceptance: Test suite (including template/config validation) completes locally in ≤ 5 minutes; CI hook verifies Forge areas on PRs.

Completing these tasks will arm High Command with a disciplined automation forge ready for large-scale Alfa deployment.

---

## 🧪 10. Verification Playbook {#verification-playbook}

_Provenance: Synchronized with High Command on 2025-10-15._

Use these quick checks to validate the Success Criteria and Acceptance bullets manually.

- Templates
  - Render (dry-run): `forge init-alfa --id alfa_test --template-version forge-template@1.0.0 --diff-plan`
  - Repro check: run render on two machines; compare checksums in `alfas/alfa_test/manifest.json`.

- CLI Safety
  - Destructive guard: `forge hydrate --id alfa_test --force` → must require `--diff-plan` first.
  - Lockfile: `New-Item forge.lock`; rerun a mutating command → must refuse; then `Remove-Item forge.lock`.

- Logging
  - JSONL present: search `logs/forge.log` for the command, e.g., `init-alfa`.
  - Journal present: `tail -n 20 logs/forge_journal.md` (or platform equivalent).
  - Failure bundle: intentionally fail `forge validate`; confirm `logs/failures/<timestamp>/` created.

- Selector & Batch Limits
  - Batch limit enforced: `forge batch-run --selector 'entropy>=0.5'` → capped unless `--override` used.
  - Sensitive transition gate: `forge batch-run --selector 'realm:nightland' --approved-by "Ops Lead"` required.

- CI Hook
  - Open a PR that changes `template/forge/**`; ensure CI runs `forge validate` and reports status.

- Time Budget
  - Measure: run `forge init-alfa ...` then `forge validate ...` locally; total ≤ 5 minutes.
