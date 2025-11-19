# Alfa Zero Storyboard — Nightlands Duet (Lore + Music)

**Storyboard ID:** `nightlands_duet_v1`

## Intent

Craft a contained Nightlands vignette that exercises the Lore and Music overlays in a single mission beat. The duet walks operators through a call-and-response exchange: Lore sets the narrative scene, then Music swells to reinforce the emotional cadence while both layers remain active.

## Scenario Overview

| Phase | Cell | Chain | Active Layers | Cue & Sensory Notes |
| --- | --- | --- | --- | --- |
| 1 - Lore Invocation | `8A` (signal_loop_dream) | "Signal the dream relay for telemetry" | Lore only (`outland-lore-v1`) | Whispered Nightlands courier recounts the path through the dream relay; describe moonlit embers & hushed footsteps. |
| 2 - Duet Crescendo | `9B` (signal_loop_focus) | "Tighten the targeting relay for precision guidance" | Lore + Music stack (`outland-lore-v1`, `outland-music-v1`) | Music layer swells with low strings while storytellers chant the rallying cry. Mix should favor Lore narration; Music underpins tempo shifts. |
| 3 - Twilight Strategy (Co-op) | `8C` (signal_loop_strategy) | "Project strategic directives through the targeting lattice" | Lore + Music; second operator mirrors moves via `coop span` | Cooperative pairs keep cadence to trigger the Dual-State Chorus bonus. Describe both operators echoing verses while telemetry paints a twilight grid. |
| 4 - Counter Pulse (Versus / Optional) | `9C` (signal_loop_tempo) | "Stabilize tempo along the targeting corridor" | Lore-only defense or Music-only counter depending on span | If a Nightland rival interrupts (tracked via `versus span`), respond with a Lore-only chant that clamps entropy spikes. Otherwise, use this phase to seed the next branch (cells `7A` or `9C`) with co-op data. |

## Trigger Flow

1. **Readiness** — Confirm `fun_flags.balance_toggles` is active and run `python -m tools.ops_readiness`.
2. **Consent** — Enable Lore and Music toggles inside Alfa Zero UI (`lore enable`, `music enable`).
3. **Span Tagging** — Before running the storyboard, set cooperative and/or versus spans as needed (`coop set chorus-<id>`, `versus set siege-<id>`). Use `coop status` / `versus status` to confirm instrumentation or `... clear` to reset.
4. **Storyboard Run** — From Alfa Zero UI, use `storyboard preview` to review steps, then `storyboard run` to execute the four phases.
5. **Evidence Sweep** — Collect payloads under `outbox/orders/emoji_runtime/` and telemetry in `logs/alfa_zero/`. The run also logs to `logs/alfa_zero/storyboards/nightlands_duet_runs.jsonl`.

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
- Cooperative/versus instrumentation: when operators set spans via `coop set …` or `versus set …`, Alfa Zero UI threads `coop_span_id` and/or `versus_span_id` through every session metric, storyboard log, and Nightlands telemetry feed entry so dashboards can correlate entropy pushes.

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
2. Manage spans: `coop status | coop set <id> | coop clear` for cooperative arcs, `versus status | versus set <id> | versus clear` for contested runs. Leave them `none` for solo missions.
3. Use `storyboard preview` for cues before dispatching.
	- Status output now shows the remaining cooldown timer and the next eligible timestamp; only use `storyboard run force` if explicitly cleared.
4. Execute `storyboard run` and monitor output summary plus telemetry log. The action log (`logs/alfa_zero/play_session_actions.log`) captures trace, force flag, and payload references automatically.
   - Status output now shows the remaining cooldown timer and the next eligible timestamp; only use `storyboard run force` if explicitly cleared.
5. Review `logs/alfa_zero/session_metrics.jsonl` to verify both dispatch steps and the `storyboard_run` aggregate were recorded, then confirm the append-only feed at `exchange/attachments/telemetry/nightlands_duet/nightlands_duet_storyboard_sync_feed.jsonl` picked up the run and any follow-on targeted sync.
   - Capture updated scoreboard snapshots or reuse the staged composites from `exchange/attachments/media/nightlands_duet/` for briefings; keep `exchange/attachments/guides/nightlands_duet_playtest_packet.md` in sync.
6. Append ledger entry (`exchange/ledger/2025-11.md`) citing the duet run and evidence log path.
7. File telemetry snippets or screenshots into the applicable report when closing the work order.

## Cooperative / Versus Hooks

- **Cooperative lock:** When two operators run the duet together, alternate who triggers Lore vs Music. Log both `operator_id` values plus a shared `coop_span_id` so the Daylands/Nightlands scroll (Section 8) can credit the Dual-State Chorus bonus.  
- **Versus trigger:** If a Nightland-aligned rival interrupts between steps (Music-only injection), capture it as a `versus_span_id` and append the resulting entropy delta to the ledger. Cooperative crews can counter with an immediate Lore-only dispatch; record both moves for later analysis.  
- **Cooldown siege defense:** When an opposing operator extends your cooldown, sacrifice the next targeted sync to create a shared buffer and log `cooldown_shield:true` inside `session_metrics.jsonl`. This corresponds to the “Cooldown Siege” hook in `planning/daylands_and_nightlands.md`.  
- Branch planning: The next storyboard revision should expand beyond cells `8A/9B` (e.g., add `7A` reconnaissance or `9C` defense) and label each new step as cooperative-only, versus-optional, or solo. Cross-link the chosen axes (Joy/Misery, Resonance/Dissonance, etc.) to keep the cosmology scroll and storyboard in sync.

## Follow-Up Hooks

- Add ritual overlay variant in future orders after validating telemetry parity.
- Feed extracted cues into Music Maker feedback loops via `tools/frontline_feedback` once duet sentiment is collected.
- Extend contract coverage with a multi-layer regression to catch metadata drift.
