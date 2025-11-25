# Campaign 2 Human Playtest Plan (Emoji-First Command Layer)

Scope: run a human playtest (~90s) with the live UI routed through the emoji DSL (quick-cast wheels + textless comms). Capture latency/accuracy + HUD signals using `CommandTelemetry` from `production/campaign2/command_layer.py`.

Pre-flight
- Pull latest + ensure guardrails intact (`git status` clean for UI code after wiring).
- Run: `python -m tools.ops_readiness` then `python tools/exchange_all.py` (confirm green).
- Confirm wheel bindings match `production/campaign2/README.md` (ability + textless_comm slots).

Instrument UI
- Import `CommandTelemetry` and instantiate once per run: `telemetry = CommandTelemetry(order_id="order-2025-11-26-061", workspace="toysoldiers_ai_0", run_id="campaign2-live-<stamp>")`.
- On wheel open/close or tutorial states: call `record_ui_state(state, detail, wheel, player, delta_ms)`.
- On cast/ping: call `record_command(source, wheel, slot, glyph_ids, player, latency_ms, label, delta_ms)`; pass latency_ms measured from wheel open -> cast.
- On downed: `record_downed(player, by, delta_ms)`.
- On revive: `record_revive(player, by, emoji, delta_ms)`.
- On one-more-run prompt: `record_one_more_prompt(accepted, delta_ms)`.
- After session: `write_outputs(log_dir=Path("logs"), attachments_dir=Path("exchange/outbox/attachments/campaign2"), duration_ms=<total_ms>)` to emit jsonl + telemetry JSON to logs/ and attachments/.

Human script (≈90s)
1) Wheel open -> cast Shield ally (ally+shield+target) [time_to_fun anchor].
2) Tempo forge (forge+craft+tempo).
3) Danger ping (ally+deliver+risk).
4) Dream drop (dream+deliver+idea).
5) Scout ping (scout+probe+signal).
6) Guardrail rejection sample: attempt unknown glyph (ally+shield+unknown_token) to verify block.
7) Downed event on P2.
8) Revive ping (ally+deliver+rise), then Revive cast (ally+shield+seed).
9) Tempo forge repeat; Fallback signal (ally+deliver+fallback).
10) Tutorial checkpoint + one-more-run prompt.

Evidence to collect
- logs/order-2025-11-26-061-campaign2-playtest.jsonl (events + emoji_latency_sample).
- logs/order-2025-11-26-061-campaign2-telemetry.json (metrics: time_to_fun_ms, revive_ms, avg/p95 latency, accuracy, HUD counts).
- Mirror same files to exchange/outbox/attachments/campaign2/ and sync to hub.
- Add ledger line with run_id and key metrics; include in completion report.

Validation checklist
- All commands route through `CommandTelemetry` (no free-text paths).
- Guardrail rejection fires on the unknown glyph.
- Latency samples count matches total commands.
- HUD signals present: ui_state, revive, one_more_prompt.
- one_more_accept recorded.

Go/No-Go
- Go if telemetry writes and accuracy >0.8 with p95 latency under 800ms.
- No-Go if DSL bypass observed, guardrail miss, or telemetry missing HUD signals.
