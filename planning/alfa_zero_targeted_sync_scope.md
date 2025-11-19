# Alfa Zero Inline Sync Trigger Scope

## Context

The scripted `python scripts/play_session.py` loop now drives dispatch, contract tests, and the full offline sync without leaving High Command. The next refinement is to add a targeted sync trigger directly inside the Alfa Zero overlay so operators can mirror only the assets they just produced instead of re-copying the entire outbox tree.

## Status

- [x] Added filtered sync arguments and quiet mode to `tools/offline_sync_exchange.py`.
- [x] Wired new `sync latest` / `sync orders` commands into `alfa_zero_ui.py` and updated the play session script.
- [ ] Evaluate long-term log rotation needs after observing quiet-mode output. Latest Nightlands cohort (2025-11-19T03:59Z) still copied only two files in quiet mode and kept `logs/alfa_zero/play_session_actions.log` at 33 KB, so rotation stays deferred while monitoring continues.

## Targeted Sync Trigger

### Primary Objectives

- Offer an in-grid command that limits sync to the most recent payloads or a single category (for example `orders/emoji_runtime`).
- Preserve the existing full sync path for fallback and parity with notebooks and scripted runs.
- Keep execution entirely within the overlay UI so High Command does not need to swap shells mid-play.

### Current Signals

- `OverlayBridge.run_offline_sync` currently shells `tools/offline_sync_exchange.py`, which mirrors the whole `outbox/orders` and `outbox/reports` trees and emits one log entry per file.
- `alfa_zero_ui.py` exposes the `sync` command that calls the bridge helper and appends logs to `logs/alfa_zero/play_session_actions.log`.
- UX notes flagged the overlay as still lacking a targeted sync trigger after dispatch.

### Scope Notes

1. **Surface area**: extend `overlay_bridge.py` with a helper capable of calling a filtered sync routine (likely by passing flags to the sync script or importing it in-process). ✅ `OverlayBridge.run_targeted_sync` shells the new CLI (2025-11-12).
2. **Sync script changes**: teach `tools/offline_sync_exchange.py` to accept optional arguments such as `--category orders` or `--only-latest 1` while keeping the default behaviour unchanged. ✅ Implemented via new `--dry-run` and targeting options (2025-11-12).
3. **UI wiring**: introduce a new command (draft name `sync latest` or `sync orders`) that calls the targeted helper and reports a concise summary back to the operator. ✅ Integrated into `alfa_zero_ui` with preview support (2025-11-12).
4. **Play session script**: once the command exists, update `logs/alfa_zero/play_session_commands.txt` so automated runs exercise the new path.
5. **Telemetry**: log targeted sync executions in both `logs/alfa_zero/session_metrics.jsonl` and `play_session_actions.log` with a distinctive label to keep metrics comparable. ✅ Order 051 instrumentation appends structured JSONL records and mirrors them into `exchange/attachments/telemetry/nightlands_duet/nightlands_duet_storyboard_sync_feed.jsonl` (2025-11-13).

### Open Questions

- Should we infer the latest files by timestamp or track dispatch destinations during the session to sync only those paths?
- Do we need a quiet mode for the sync script to avoid large per-file output once the target set is small? ✅ Quiet mode now defaults on for the targeted CLI and sync helper (2025-11-12).
- How should the command behave if no new files are detected (silence vs explicit confirmation)? ✅ emits `[INFO] No new … files` messages to keep operators informed (2025-11-12).

## Exchange Log Trimming

### Observations

- Full sync runs copy up to ~120 files and write a line per file into `play_session_actions.log`, causing the action log to balloon during repeated automated loops.
- The command-loop output already compresses console display to the head and tail of the sync script logs, but the persisted file remains verbose.
- Quiet-mode targeted sync runs now emit compact output; the new telemetry feed captures copy counts and destinations for post-run review without reading raw logs.

### Options

1. Add a summary-only mode to `offline_sync_exchange.py` that prints the first few copy operations and then aggregates totals unless `--verbose` is specified.
2. Post-process the sync output inside `alfa_zero_ui.py` before writing it to the action log, keeping the full raw output in a rotated file under `logs/alfa_zero/sync/`.
3. Rotate or truncate `play_session_actions.log` once it crosses a size threshold, archiving historical runs in `logs/alfa_zero/archive/`.

### Proposed Direction

- Implement option (1) alongside the targeted sync helper, giving both the overlay UI and the scripted play session a quiet flag for routine runs. ✅ Landed in `tools/offline_sync_exchange.py --quiet` and `tools.targeted_sync` default behaviour.
- Preserve the ability to request full verbosity for debugging by exposing a `--verbose-sync` flag in the UI. → CLI exposes `--no-quiet`; UI toggle still pending.
- Review rotation once the reduced-output path lands; postpone automated truncation until we observe long-term log growth.

## 2025-11-12 Update

- Introduced `python -m tools.targeted_sync` to wrap the offline sync helper with confirmation prompts, quiet mode, and optional dry-run previews.
- `tools/offline_sync_exchange.py` now accepts `--dry-run`, `--latest`, and `--orders-subpath` for filtered runs. The helper preserves full sync defaults for existing automation.
- Targeted CLI defaults to syncing orders only, latest files unlimited, and quiet mode on. Operators can pass `--yes` to skip prompts when running inside scripted flows. UI commands (`sync latest`, `sync orders`) now invoke the helper with auto-confirm and optional `preview` dry-run.
- Targeted sync telemetry now lands in session metrics and powers the `nightlands_duet_storyboard_sync_feed.jsonl` attachment.

## 2025-11-13 Update

- `alfa_zero_ui` parses targeted sync output to capture counts, destinations, and relative paths for telemetry.
- Session metrics append to `exchange/attachments/telemetry/nightlands_duet/nightlands_duet_storyboard_sync_feed.jsonl`, creating the combined storyboard + targeted sync feed requested in Order 051.
- Feed manifest documents the schema for downstream dashboards and reporting.
- Interim cadence panel captured in `docs/nightlands_duet_telemetry_panel.md` while the main dashboard tooling remains offline.
- Quiet-mode log rotation decision deferred until the next cohort run; use telemetry feed totals plus `play_session_actions.log` size to judge whether archival is required.

## 2025-11-16 Update

- Nightlands duet follow-up cohort confirmed the quiet-mode targeted sync output stays compact: the latest telemetry feed entry (`2025-11-12T10:50:26Z` in `nightlands_duet_storyboard_sync_feed.jsonl`) shows a single `[OK] Synced 2 orders file(s)` summary with just two `copied_paths`, and `logs/alfa_zero/targeted_sync_20251112T105026Z.log` mirrors the same short transcript.
- `logs/alfa_zero/play_session_actions.log` now captures only the condensed summary lines plus command metadata; file size remains stable under 50 KB after multiple loops, so we can defer rotation and rely on the telemetry feed for historical counts.
- Action: continue to spot-check the telemetry feed after each cohort; if the feed reports more than 20 copied files or if `play_session_actions.log` exceeds 250 KB, trigger the rotation plan from "Exchange Log Trimming" and archive the previous log under `logs/alfa_zero/archive/`.

## 2025-11-18 Update

- Alfa Zero UI now captures `operator_id` (CLI flag `--operator` or env `SHAGI_OPERATOR`) and threads it through every session metric, providing per-run attribution for storyboard and targeted sync telemetry.
- Targeted sync commands emit deterministic `trace_id` values plus `files_copied` counts inside `logs/alfa_zero/session_metrics.jsonl`; feed entries inherit the same fields so downstream dashboards can correlate sync bursts to storyboard traces.
- Added `tools/export_nightlands_duet_panel.py`, which compiles the append-only feed into `exchange/attachments/telemetry/nightlands_duet/nightlands_duet_storyboard_sync_panel.json`. Run it after each lull block to publish a lightweight panel for Tons-of-Fun/Morningate until the shared dashboard returns.
- `exchange/attachments/guides/comfort_happy_path.md` now instructs operators to verify the targeted sync telemetry hook (and contract case `automation_comfort_sync.json`) during every 70/30 loop.

## 2025-11-19 Update

- Ran another Nightlands duet cohort at `2025-11-19T03:59:24Z` (trace `outland-lore-v1-8A-20251119035924`) using the recorded command script `logs/alfa_zero/nightlands_cohort_commands_20251119T1351.txt`; the paired targeted sync (`sync latest 2`) copied two payloads into `high_command_exchange/orders` and emitted the usual `[OK] Synced 2 orders file(s)` summary.
- Feed `nightlands_duet_storyboard_sync_feed.jsonl` now holds eight records covering two storyboard + targeted-sync pairs on 2025-11-19; `tools/export_nightlands_duet_panel.py` was rerun so downstream dashboards inherit the refreshed cadence.
- Quiet-mode output remains compact: `logs/alfa_zero/play_session_actions.log` grew to just 33 KB and shows a four-line targeted-sync transcript, so the log-rotation trigger (`>250 KB` or `>20` copies) remains unmet.
- Quiet-mode observation for this cohort satisfies the "observe quiet-mode sync output" action; keep the guard in place for upcoming cohorts but no archival work is required yet.

## 2025-11-12 Playtest Feedback

- Nightlands cohort (Vega, Lumen, Rook) executed the duet storyboard and confirmed the targeted sync helper’s quiet output during a live comfort-loop session.
- Operators appreciated the dry-run preview but requested a UI banner surfacing remaining cooldown time after each run.
- Metrics excerpt was easy to retrieve; cohort asked for a dashboard panel that graphs targeted sync cadence alongside storyboard runs.
- Follow-up actions are logged in `planning/document_refresh_queue.md` and the November ledger for tracking.

## Next Actions

1. Continue observing quiet-mode sync output after each Nightlands cohort (2025-11-19 remained at two copied files and 33 KB action log) to decide whether log rotation or archival is still required.
2. Promote the interim telemetry panel (`docs/nightlands_duet_telemetry_panel.md`) into the primary dashboard once the offline tooling is back.
3. Coordinate with UI workstream on the cooldown banner request and link the outcome back to this scope.
