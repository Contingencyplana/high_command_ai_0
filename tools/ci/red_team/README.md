# Red-Team CI Lane

Quick start
- List cases: `pwsh tools/ci/red_team/simulate.ps1 -List`
- Dry run: `pwsh tools/ci/red_team/simulate.ps1 -DryRun`
- Execute with cases: `pwsh tools/ci/red_team/simulate.ps1 -CasesPath tools/ci/red_team/cases.json -OutputPath logs/red_team/results.jsonl`

Outputs
- Per-case JSONL at `logs/red_team/results.jsonl` with fields: `ts`, `case_id`, `result`, `reason`, `guardrails_touched`.
- Summary printed to stdout: `{ "pass": n, "fail": m }`.
- Non-zero exit code if any case fails.

Implementing cases
- Define scenario list in `tools/ci/red_team/cases.json`.
- Implement logic in `tools/ci/red_team/simulate.ps1` inside `Invoke-RedTeamCase`.
- Align expectations with `tools/ci/red_team/RED_TEAM_CASES.md` and FUN acceptance checks.

References
- FUN Front: `planning/pivotal_fronts/tons_of_fun.md`
- KPI Spec: `planning/pivotal_fronts/fun_kpi_spec.md`
