# Nightlands Duet Telemetry Feed

This directory collects the aggregated telemetry promised in Order 051. It combines nightly storyboard executions and the Alfa Zero targeted sync helper into a single JSONL feed so operators can refresh dashboards and reports without scraping raw session logs.

## Files

- `nightlands_duet_storyboard_sync_feed.jsonl` — Append-only timeline containing `storyboard_run` and `targeted_sync*` events relevant to the duet. Existing entries were backfilled from `logs/alfa_zero/session_metrics.jsonl`.
- `nightlands_duet_storyboard_sync_panel.json` — Lightweight panel generated via `python tools/export_nightlands_duet_panel.py`; mirrors the latest feed entries so dashboards can load a compact JSON blob while offline tooling persists.

## Event Fields

All records emit the following shared fields:

- `timestamp` — UTC timestamp recorded by the Alfa Zero UI session metrics pipeline.
- `event` — Either `storyboard_run` or a `targeted_sync*` variant (custom suffixes allowed).
- `session_id` - Session identifier emitted by Alfa Zero UI.
- `source` - Always `alfa_zero_ui` for the current instrumentation pass.
- `operator_id` - Operator identifier captured via `--operator` or `SHAGI_OPERATOR`.
- `trace_id` - Correlation identifier for the storyboard or targeted sync run.
- `coop_span_id` - Optional cooperative span identifier set via `coop set <id>` inside Alfa Zero UI. Present whenever operators tag a Dual-State Chorus run.
- `versus_span_id` - Optional versus span identifier set via `versus set <id>` for contested runs or cooldown sieges.

`storyboard_run` records add:

- `storyboard_id`, `trace_id`, `payload_count`, `cooldown_seconds`, `force` flag.
- `storyboard_log` — Relative path to the storyboard run log file.
- `payloads` - Relative paths to payloads emitted during the run.
- `coop_span_id` / `versus_span_id` are repeated here for emphasis; dashboards correlate them with targeted sync events to show multi-operator pushes.

`targeted_sync*` records add:

- `categories`, `orders_subpath`, `latest`, `dry_run`, `quiet` — Parameters used for the helper invocation.
- `returncode` - Process exit status.
- `summary_line` - Final status line from the helper (`[OK]` or `[INFO]` declarations).
- `destination` - Reported sync destination when available.
- `copied_count`, `copied_paths` - Parsed counts and relative output paths.
- `files_copied` - Convenience field mirroring `copied_count` (defaults to `0` when quiet runs report no changes).
- `no_changes` - Boolean indicating whether the helper reported that no files were copied.
- `action_log` - Relative path to the appended action log entry.
- `coop_span_id`, `versus_span_id` - When spans are active, these mirror the values attached to the corresponding storyboard run so dashboards can trace sync evidence to the same cooperative or contested arc.

## Update Notes

- Alfa Zero now emits enriched targeted sync telemetry (trace IDs, operator IDs, files copied) and automatically appends new records to this feed via `alfa_zero_ui._maybe_record_nightlands_feed`. Event names prefixed with `targeted_sync` are ingested alongside plain `targeted_sync` records.
- The feed is designed for downstream dashboards in `docs/` and upcoming telemetry notebooks.
- Interim cadence script documented at `docs/nightlands_duet_telemetry_panel.md` converts the feed into an hourly storyboard/sync summary while offline tooling persists; `tools/export_nightlands_duet_panel.py` now automates the JSON export into `nightlands_duet_storyboard_sync_panel.json` for Tons-of-Fun and Morningate.
- Any schema change must update this manifest first, then refresh `docs/nightlands_duet_telemetry_panel.md` so snapshot helpers parse the new fields correctly.
- `planning/alfa_zero_nightlands_duet_storyboard.md` references this feed for operator guardrails; keep that scroll aligned whenever event fields or destinations change.
