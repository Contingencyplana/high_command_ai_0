# Nightlands Duet Telemetry Feed

This directory collects the aggregated telemetry promised in Order 051. It combines nightly storyboard executions and the Alfa Zero targeted sync helper into a single JSONL feed so operators can refresh dashboards and reports without scraping raw session logs.

## Files

- `nightlands_duet_storyboard_sync_feed.jsonl` — Append-only timeline containing `storyboard_run` and `targeted_sync` events relevant to the duet. Existing entries were backfilled from `logs/alfa_zero/session_metrics.jsonl`.

## Event Fields

All records emit the following shared fields:

- `timestamp` — UTC timestamp recorded by the Alfa Zero UI session metrics pipeline.
- `event` — Either `storyboard_run` or `targeted_sync`.
- `session_id` — Session identifier emitted by Alfa Zero UI.
- `source` — Always `alfa_zero_ui` for the current instrumentation pass.

`storyboard_run` records add:

- `storyboard_id`, `trace_id`, `payload_count`, `cooldown_seconds`, `force` flag.
- `storyboard_log` — Relative path to the storyboard run log file.
- `payloads` — Relative paths to payloads emitted during the run.

`targeted_sync` records add:

- `categories`, `orders_subpath`, `latest`, `dry_run`, `quiet` — Parameters used for the helper invocation.
- `returncode` — Process exit status.
- `summary_line` — Final status line from the helper (`[OK]` or `[INFO]` declarations).
- `destination` — Reported sync destination when available.
- `copied_count`, `copied_paths` — Parsed counts and relative output paths.
- `no_changes` — Boolean indicating whether the helper reported that no files were copied.
- `action_log` — Relative path to the appended action log entry.

## Update Notes

- Alfa Zero now emits enriched targeted sync telemetry and automatically appends new records to this feed via `alfa_zero_ui._maybe_record_nightlands_feed`.
- The feed is designed for downstream dashboards in `docs/` and upcoming telemetry notebooks.
- Interim cadence script documented at `docs/nightlands_duet_telemetry_panel.md` converts the feed into an hourly storyboard/sync summary while offline tooling persists.
