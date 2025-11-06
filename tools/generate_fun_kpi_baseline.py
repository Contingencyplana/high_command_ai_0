from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


def load_guardrail_summary(repo: Path, minutes: int) -> dict:
    events_path = repo / "logs" / "fun_guardrails" / "events.jsonl"
    if not events_path.exists():
        return {"note": "no guardrail events in window"}
    since = datetime.now(timezone.utc) - timedelta(minutes=minutes)
    counts = {}
    total = 0
    with events_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            try:
                ts = datetime.fromisoformat(str(obj.get("ts", "")).replace("Z", "+00:00"))
            except Exception:
                continue
            if ts < since:
                continue
            total += 1
            for t in obj.get("triggers", []) or []:
                ttype = str(t.get("type"))
                counts[ttype] = counts.get(ttype, 0) + 1
    return {"window_minutes": minutes, "total_events": total, "by_trigger": counts}


def main():
    ap = argparse.ArgumentParser(description="Generate FUN KPI baseline snapshot")
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--minutes", type=int, default=10080, help="window for guardrail summary (default 7 days)")
    args = ap.parse_args()

    repo = Path(args.repo_root).resolve()
    today = datetime.now(timezone.utc).date().isoformat()
    out = repo / "planning" / "pivotal_fronts" / f"fun_kpi_baseline_{today}.md"

    guardrails = load_guardrail_summary(repo, args.minutes)

    lines = []
    lines.append(f"# FUN KPI Baseline — {today}")
    lines.append("")
    lines.append("Scope")
    lines.append("- Snapshot of current FUN KPIs as baseline for canary comparisons.")
    lines.append("")
    lines.append("Cohort & Window")
    lines.append("- Cohort: all players (exclude test/dev accounts)")
    lines.append("- Window: last 7 full days")
    lines.append("")
    lines.append("KPIs")
    lines.append("- D+1 Retention: <fill>%")
    lines.append("- D+7 Retention: <fill>%")
    lines.append("- Session Length (median): <fill> min")
    lines.append("- Session Length (10% trimmed mean): <fill> min")
    lines.append("- Rage-Quit Rate: <fill>% of sessions")
    lines.append("- Report Rate: <fill> per 1,000 sessions")
    lines.append("- Appeals Uphold Rate: <fill>%")
    lines.append("- Fairness Gap (top vs bottom quintile win rate): <fill> pp")
    lines.append("- Economy Drift (rewards/min vs target): <fill>%")
    lines.append("- Bot Rate (estimated): <fill>%")
    lines.append("")
    lines.append("Guardrail Snapshot (last 7 days)")
    lines.append(f"- Total guardrail events: {guardrails.get('total_events', 0)}")
    by_tr = guardrails.get("by_trigger", {}) or {}
    if by_tr:
        for k, v in sorted(by_tr.items(), key=lambda kv: kv[0]):
            lines.append(f"  - {k}: {v}")
    else:
        lines.append("  - none observed")
    lines.append("")
    lines.append("Notes")
    lines.append("- Data sources: telemetry pipeline, reports, appeals logs.")
    lines.append("- Exclusions/filters: <fill>")
    lines.append("- Anomalies: <fill>")
    lines.append("")
    lines.append("DRI & Sign-off")
    lines.append("- DRI: <name>")
    lines.append("- Reviewed by: PM (FUN), Ops, Data")
    lines.append("")
    lines.append("References")
    lines.append("- Spec: `planning/pivotal_fronts/fun_kpi_spec.md`")
    lines.append("- FUN Front: `planning/pivotal_fronts/tons_of_fun.md`")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()

