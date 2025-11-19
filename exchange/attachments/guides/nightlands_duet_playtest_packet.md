# Nightlands Duet Playtest Packet

## Objective

Provide operators with everything needed to replay and validate the Nightlands duet storyboard run executed at 2025-11-19T08:33:58Z as part of the Nov 19 cohort refresh.

## Storyboard Run Summary

- Storyboard ID: `nightlands_duet_v1`
- Run timestamp: `2025-11-19T08:33:58.495875Z`
- Trace ID: `outland-lore-v1-8A-20251119083358`
- Steps:
  1. Lore Invocation → Cell `8A` → Overlay `outland-lore-v1`
  2. Duet Crescendo → Cell `9B` → Overlays `outland-lore-v1`, `outland-music-v1`
  3. Twilight Strategy → Cell `8C` → Overlays `outland-lore-v1`, `outland-music-v1`
  4. Counter Pulse → Cell `9C` → Overlays `outland-lore-v1`, `outland-music-v1`
- Force override: `true` (explicitly logged; requires ledger approval)
- Cooldown at dispatch: ~15 minutes remaining

Source log: `logs/alfa_zero/storyboards/nightlands_duet_v1_runs.jsonl`

### Quick verification

```pwsh
Get-Content logs/alfa_zero/storyboards/nightlands_duet_v1_runs.jsonl | Select-String "outland-lore-v1-8A-20251112004957"
```

## Payload Artifacts

The refreshed four-step run emitted four payloads; all were synced to the exchange hub.

| Kind | Local path |
| ---- | ---------- |
| Signal Loop (dream) | `outbox/orders/emoji_runtime/20251119T083358Z_alfa_zero_signal_loop_dream.json` |
| Signal Loop (focus) | `outbox/orders/emoji_runtime/20251119T083358Z_alfa_zero_signal_loop_focus.json` |
| Signal Loop (strategy) | `outbox/orders/emoji_runtime/20251119T083358Z_alfa_zero_signal_loop_strategy.json` |
| Signal Loop (tempo) | `outbox/orders/emoji_runtime/20251119T083358Z_alfa_zero_signal_loop_tempo.json` |

### Suggested spot-checks

1. Confirm payload trace alignment:

   ```pwsh
   Get-Content outbox/orders/emoji_runtime/20251112T004957Z_alfa_zero_signal_loop_focus.json | Select-String "outland-lore-v1-8A-20251112004957"
   ```


2. Validate duet overlays were requested (music + lore) inside all four payloads.

## Scoreboard Imagery

Annotated scoreboard frames now live under `exchange/attachments/media/nightlands_duet/` for both key storyboard states:

- Lore Invocation → `nightlands_duet_scoreboard_lore_invocation.png`
- Duet Crescendo → `nightlands_duet_scoreboard_duet_crescendo.png`

Each export has a companion metadata file describing annotations, cooldown timers, and targeted sync signals:

- `nightlands_duet_scoreboard_lore_invocation.metadata.json`
- `nightlands_duet_scoreboard_duet_crescendo.metadata.json`

Current exports are production captures from the Nov 19 cohort (`outland-lore-v1-8A-20251119035924`). Replace only when newer captures supersede this run.

Embed previews when presenting to cohorts:

![Nightlands Lore Invocation scoreboard](../media/nightlands_duet/nightlands_duet_scoreboard_lore_invocation.png)

![Nightlands Duet Crescendo scoreboard](../media/nightlands_duet/nightlands_duet_scoreboard_duet_crescendo.png)

Field Usage:

- Reference cooldown deltas during operator briefings so the cohort expects the 15-minute guardrail between duet runs.
- Use the targeted sync summary chip callout to remind operators when the helper last mirrored payloads.
- When updating the packet, review `scoreboard_imagery_manifest.md` to keep filenames and annotations aligned.

## Cooperative / Versus Procedure

- The Alfa Zero UI exposes `coop` and `versus` commands to tag the current mission arc:
  - `coop status` → show current cooperative span (defaults to `none`).
  - `coop set <id>` → e.g. `coop set chorus-automation` before a Dual-State Chorus run.
  - `coop clear` → reset after the arc ends.
  - `versus set <id>` / `versus clear` mirror the above for Nightland sieges or contested runs.
- Once set, the UI banner displays the spans, and every telemetry artifact (`logs/alfa_zero/session_metrics.jsonl`, `nightlands_duet_storyboard_sync_feed.jsonl`, `nightlands_duet_storyboard_sync_panel.json`) records `coop_span_id` / `versus_span_id`.
- Always tag spans before running the storyboard so dashboards can correlate cooperative pushes with targeted sync proof.
## Targeted Sync Evidence

A post-run targeted sync mirrored the latest duet payloads to the exchange hub, carrying the same cooperative/versus span identifiers as the storyboard run.

- Latest log entries: see `logs/alfa_zero/play_session_actions.log` (search for `targeted_sync_latest_run` and the `[OK] Synced 2 orders` summary).
- Key lines:
  - `Latest: 2`
  - `Copied ... emoji_runtime/20251119T083358Z_alfa_zero_signal_loop_tempo.json`
  - `Copied ... factory_orders/20251119T083358Z_emoji-signal-loop-tempo-20251119083358_465801.json`
- Combined telemetry feed: `exchange/attachments/telemetry/nightlands_duet/nightlands_duet_storyboard_sync_feed.jsonl` (append-only JSONL for duet storyboard runs and targeted syncs).

Re-run helper (optional):

```pwsh
python -m tools.targeted_sync --latest 2 --yes
```

## Operator Brief Excerpt

- Readiness: Verify `fun_flags.balance_toggles` and run `python -m tools.ops_readiness`.
- Consent: Enable Lore and Music overlays inside Alfa Zero UI before dispatching.
- Span tagging: Set cooperative and/or versus spans (`coop set …`, `versus set …`) so telemetry reflects the mission context.
- Preview: Use `storyboard preview` to review all four phases and confirm cooldown timers.
- Dispatch: Trigger `storyboard run` (reserve `storyboard run force` for cleared overrides only). The UI will warn if spans are unset.
- Evidence: Collect payloads under `outbox/orders/emoji_runtime/`, run `sync latest 2`, and ensure span IDs propagate through the feed/panel.
- Post-run: Check `logs/alfa_zero/session_metrics.jsonl` for dispatch entries covering all four steps and confirm the telemetry feed at `exchange/attachments/telemetry/nightlands_duet/nightlands_duet_storyboard_sync_feed.jsonl` captured the storyboard + targeted sync pairing with the same spans.

## Operator Playtest Checklist

1. Review `storyboard status` in the Alfa Zero UI to confirm cooldown expiry before rerunning.
2. Set cooperative/versus spans (`coop set <id>`, `versus set <id>`) or confirm they remain `none` for solo runs.
3. Execute the `nightlands_duet_v1` storyboard via `alfa_zero_ui.py` (`nightlands duet` command) and verify all four payload summaries.
4. Capture the resulting trace ID and span IDs; compare with the baseline listed above.
5. Sync the newly generated payloads using the targeted sync helper (`--latest 2`) so sync telemetry inherits the same spans.
6. Record results in `exchange/ledger/2025-11.md` and attach supporting logs.

## Session Metrics Snapshot

- Excerpt file: `exchange/attachments/guides/nightlands_duet_session_metrics_excerpt.jsonl`
- Trace recorded: `outland-lore-v1-8A-20251119083358`
- Source log: `logs/alfa_zero/session_metrics.jsonl`
- For future runs, capture the relevant lines with:

  ```pwsh
  Select-String -Path logs/alfa_zero/session_metrics.jsonl -Pattern "nightlands_duet_v1" -Context 0,2
  ```

- File new excerpts alongside this packet whenever the duet trace changes.

## Follow-up Notes

- Session metrics excerpt captured; update when new traces or spans are introduced.
- Scoreboard imagery now reflects the Nov 19 cohort captures; refresh the manifest + packet when newer art ships.
- Telemetry feed schema documented in `exchange/attachments/telemetry/nightlands_duet/nightlands_duet_telemetry_manifest.md`; cooperative/versus spans are now first-class fields.
- Interim cadence panel lives in `docs/nightlands_duet_telemetry_panel.md` with a quick script that summarises storyboard and targeted sync activity (including span IDs); include its output in debriefs until the full dashboard tooling returns.
