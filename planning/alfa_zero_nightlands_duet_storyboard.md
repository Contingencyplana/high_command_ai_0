# Alfa Zero Storyboard — Nightlands Duet (Lore + Music)

**Storyboard ID:** `nightlands_duet_v1`

## Intent

Craft a contained Nightlands vignette that exercises the Lore and Music overlays in a single mission beat. The duet walks operators through a call-and-response exchange: Lore sets the narrative scene, then Music swells to reinforce the emotional cadence while both layers remain active.

## Scenario Overview

| Phase | Cell | Chain | Active Layers | Cue & Sensory Notes |
| --- | --- | --- | --- | --- |
| 1 — Lore Invocation | `8A` (signal_loop_dream) | "Signal the dream relay for telemetry" | Lore only (`outland-lore-v1`) | Whispered Nightlands courier recounts the path through the dream relay; describe moonlit embers & hushed footsteps. |
| 2 — Duet Crescendo | `9B` (signal_loop_focus) | "Tighten the targeting relay for precision guidance" | Lore + Music stack (`outland-lore-v1`, `outland-music-v1`) | Music layer swells with low strings while storytellers chant the rallying cry. Mix should favor Lore narration; Music underpins tempo shifts. |

## Trigger Flow

1. **Readiness** — Confirm `fun_flags.balance_toggles` is active and run `python -m tools.ops_readiness`.
2. **Consent** — Enable Lore and Music toggles inside Alfa Zero UI (`lore enable`, `music enable`).
3. **Storyboard Run** — From Alfa Zero UI, use `storyboard preview` to review steps, then `storyboard run` to execute both phases.
4. **Evidence Sweep** — Collect payloads under `outbox/orders/emoji_runtime/` and telemetry in `logs/alfa_zero/`. The run also logs to `logs/alfa_zero/storyboards/nightlands_duet_runs.jsonl`.

## Cooldown & Guardrails

- Minimum cooldown between duet runs: **15 minutes**. The runner enforces this against `logs/alfa_zero/storyboards/nightlands_duet_runs.jsonl` unless `--force` (or `storyboard run force`) is used.
- Maintain ledger notes when the duet is executed during an ops session.
- Respect existing Outlands guidance: limit dual-layer activations to **≤3 per 24h** per front unless cleared with Fun Guardians.

## Telemetry Expectations

- Shared `trace_id` for both phases, emitted as `nightlands_duet_v1-<timestamp>`.
- Payload fields: `storyboard_id`, `storyboard_title`, `storyboard_step`, `storyboard_sequence`, `storyboard_total_steps`.
- `overlays[]` array always lists Lore first, Music second when both are active.
- Phase 2 payload should include both overlays and retain Lore as the primary layer (`overlay_id`).
- `logs/alfa_zero/session_metrics.jsonl` now records per-step `dispatch` entries with storyboard metadata plus a `storyboard_run` summary (payload count, trace, force flag).
- Guardrail blocks are also logged to session metrics as `storyboard_guardrail` events for postmortem review.
- Targeted sync executions now append structured telemetry (trace IDs, operator IDs, counts, destinations, copied paths) alongside storyboard runs into `exchange/attachments/telemetry/nightlands_duet/nightlands_duet_storyboard_sync_feed.jsonl`.

## Scoreboard & Cadence Artifacts

- Placeholder scoreboard composites with annotation metadata now live under `exchange/attachments/media/nightlands_duet/` (`nightlands_duet_scoreboard_lore_invocation.png` / `.metadata.json` and `nightlands_duet_scoreboard_duet_crescendo.png` / `.metadata.json`). Use the manifest (`scoreboard_imagery_manifest.md`) to keep filenames and overlays aligned when swapping in higher-fidelity exports.
- `exchange/attachments/guides/nightlands_duet_playtest_packet.md` embeds both scoreboard frames plus sync evidence so cohorts can rehearse briefing points without re-running the storyboard.
- Cadence snapshots for storyboard runs + targeted sync executions live in `docs/nightlands_duet_telemetry_panel.md`; run the included script against `exchange/attachments/telemetry/nightlands_duet/nightlands_duet_storyboard_sync_feed.jsonl` during debriefs until the full dashboard returns.

## Telemetry Dashboard Hook

- `logs/alfa_zero/session_metrics.jsonl` remains the canonical local source for duet dispatch + targeted sync events; every storyboard run must ensure the append-only feed at `exchange/attachments/telemetry/nightlands_duet/nightlands_duet_storyboard_sync_feed.jsonl` is updated via the Alfa Zero UI instrumentation.
- The interim dashboard documented in `docs/nightlands_duet_telemetry_panel.md` reads directly from that feed. After each run, execute the snapshot helpers in that scroll and drop the rendered table into `exchange/attachments/guides/nightlands_duet_session_metrics_excerpt.jsonl` so the broader telemetry notebook can ingest it.
- `python tools/export_nightlands_duet_panel.py` now emits `exchange/attachments/telemetry/nightlands_duet/nightlands_duet_storyboard_sync_panel.json`, a lightweight JSON panel mirroring the latest storyboard and targeted sync telemetry (trace IDs, operator IDs, files copied). Regenerate it after every session so Tons-of-Fun and Morningate can consume a stable artifact while the full dashboard remains offline.
- When the shared telemetry dashboard tooling returns, publish the latest excerpt plus script output alongside the duet scoreboard imagery; this keeps the Operator Brief and Nightlands campaign summaries aligned without parsing raw logs.

## Operator Checklist

1. Run `storyboard status` to confirm cooldown, last run, and toggle requirements.
2. Use `storyboard preview` for cues before dispatching.
	- Status output now shows the remaining cooldown timer and the next eligible timestamp; only use `storyboard run force` if explicitly cleared.
3. Execute `storyboard run` and monitor output summary plus telemetry log. The action log (`logs/alfa_zero/play_session_actions.log`) captures trace, force flag, and payload references automatically.
   - Status output now shows the remaining cooldown timer and the next eligible timestamp; only use `storyboard run force` if explicitly cleared.
4. Review `logs/alfa_zero/session_metrics.jsonl` to verify both dispatch steps and the `storyboard_run` aggregate were recorded, then confirm the append-only feed at `exchange/attachments/telemetry/nightlands_duet/nightlands_duet_storyboard_sync_feed.jsonl` picked up the run and any follow-on targeted sync.
   - Capture updated scoreboard snapshots or reuse the staged composites from `exchange/attachments/media/nightlands_duet/` for briefings; keep `exchange/attachments/guides/nightlands_duet_playtest_packet.md` in sync.
5. Append ledger entry (`exchange/ledger/2025-11.md`) citing the duet run and evidence log path.
6. File telemetry snippets or screenshots into the applicable report when closing the work order.

## Follow-Up Hooks

- Add ritual overlay variant in future orders after validating telemetry parity.
- Feed extracted cues into Music Maker feedback loops via `tools/frontline_feedback` once duet sentiment is collected.
- Extend contract coverage with a multi-layer regression to catch metadata drift.
