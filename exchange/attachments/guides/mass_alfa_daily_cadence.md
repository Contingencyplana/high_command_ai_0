# Mass Alfa Daily Cadence (Operator Guide)

Use these steps to sustain predictable throughput during mass Alfa production. Run per workspace or centrally from Toyfoundry as applicable.

1) Readiness
- Command: `python -m tools.ops_readiness`
- Outcome: writes `logs/ops_readiness.json`; proceed if OK.

2) Seed/Update Batch
- Create or pull the day’s target instances (per order). Record IDs → paths.
- Freeze baseline template/version used (note in report).

3) Minimal Smoke
- Run the minimal smoke set for each instance; archive outputs under each instance `logs/`.

4) Stage Reports
- For each instance, stage a short “hello” completion report to `outbox/reports/` with: instance ID, baseline, readiness result, smoke summary, and paths.

5) Sync
- Command: `python tools/exchange_all.py`
- Outcome: pushes staged artifacts to hub; logs skips (if any) to `logs/exchange_all.json`.

6) Ledger Note
- Append a single ledger line summarizing the batch (IDs, count, exceptions).

7) Debrief Pulse (5–10 min)
- Review throughput, blockers, and next batch size.

References
- Readiness: `tools/ops_readiness.py`
- Sync: `tools/exchange_all.py`
- Alfa baseline: `template/forge/alfa/alfa.py.j2`

