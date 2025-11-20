# Alfa Batch 2 Hydration Checklist (Draft)

Purpose: capture the prerequisites High Command must clear before hydrating Alfa Batch 2. Treat this as the gate document for War Office sign-off.

## 1. Ops & Overlay Readiness

- [x] **Nightlands storyboard** - Run the four-phase duet path (8A → 9B → 8C → 9C) using `logs/alfa_zero/nightlands_cohort_commands_20251119T1351.txt` so the latest trace and spans are fresh.
- [x] **Span instrumentation** - Confirm `coop set …` / `versus set …` are being used and the UI banner / telemetry feed reflect the same IDs across storyboard + targeted sync entries.
- [x] **Log rotation guard** - After the cohort, verify `play_session_actions.log` rotated (or remained <250 KB) and archive artefacts exist in `logs/alfa_zero/archive/`.
- [x] **Telemetry panel** - Rerun `python tools/export_nightlands_duet_panel.py` and stash the JSON alongside the run evidence.

## 2. Ledger & Reporting

- [x] **Ledger entries** - Append the run + span IDs in `exchange/ledger/2025-11.md`, referencing the storyboard log, action log, and panel artefact.
- [x] **Playtest packet** - Ensure `exchange/attachments/guides/nightlands_duet_playtest_packet.md` reflects the latest trace, payload list, and cooperative procedures.
- [x] **RUNBOOK references** - Keep `RUNBOOK.md` updated with the log-rotation and telemetry guardian steps (see “Nightlands Log & Telemetry Guards” section).

## 3. Imagery & Attachments

- [x] **Scoreboard captures** - Confirm `exchange/attachments/media/nightlands_duet/scoreboard_imagery_manifest.md` describes the current Lore Invocation / Duet Crescendo captures and that the raw PNGs match the latest trace.
- [x] **Telemetry manifest** - Verify `exchange/attachments/telemetry/nightlands_duet/nightlands_duet_telemetry_manifest.md` lists all required fields (including `coop_span_id` / `versus_span_id`) and is in sync with the feed/panel.
- [x] **Session metrics excerpt** - Refresh `exchange/attachments/guides/nightlands_duet_session_metrics_excerpt.jsonl` whenever the trace or spans change.

## 4. Sign-Off

- [x] Ops Lead reviewed the checklist, confirmed every box above and attached evidence bundle (panel JSON, feed tail, ledger diff).
- [x] War Office briefed on the readiness state and granted hydration approval for Batch 2.

*Update this checklist whenever new prerequisites emerge. Once every box is checked with evidence, Batch 2 hydration can begin.*

## 5. High Command Intake (2025-11-20)

- [x] Pulled Toyfoundry Batch 2 bundle via `python tools/offline_bridge.py pull --move`; hello packets now live in `exchange/reports/inbox/hello-Alfa-M06-20251120T005726Z.json` through `hello-Alfa-M11-20251120T010909Z.json`.
- [x] Ran `python tools/ledger_update.py` and logged the ORDER-060 import in `exchange/ledger/2025-11.md` so downstream fronts can trace the evidence path.
- [ ] Coordinate trooptrain pulls across Gamma/Delta/Theta/Zeta (and others) plus archive the hello packets once acknowledgements land.
