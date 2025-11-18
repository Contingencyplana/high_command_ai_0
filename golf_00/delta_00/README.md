# Golf_00 / Delta_00 - Alfa Zero Staging Hub

Golf_00 is the first 16×16 battlegrid. Delta_00 is where we wire Alfa Zero’s playable overlay into Toyfoundry payloads before scaling across batches. This README keeps the component map and operational loop aligned with Pivot Two (playable workflow) and Pivot Five (emoji-first commands).

---

## Active Alfa Map

| Alfa | Focus | Key Files / Commands | Status |
|------|-------|----------------------|--------|
| `alfa_00` | Overlay harness + controller | `overlay_test_harness.py`, `alfa_zero_controller.py`, `alfa_zero_ui.py` | Prototype harness translating grid clicks into emoji chains and firing ledger + sync hooks automatically (toggle with `--no-auto-sync`). |
| `alfa_01` | Runtime bridge slot | *(Reserved)* | Reserved for the Toyfoundry runtime bridge once overlay dispatch promotion is stable. |
| `alfa_02` | Narrator shell | `python -m golf_00.delta_00.alfa_02.narrator_shell --say "..."` | Stub that prints narration lines; pending JSONL export wiring for guided co-play. |
| `alfa_03` | Telemetry shell | `python -m golf_00.delta_00.alfa_03.telemetry_shell --event forge.craft --status success` | Stub that prints/records telemetry events; ties into the overlay comfort loop during Order-044/045. |
| `alfa_04` | Emoji composer + translator | `emoji_translator.py`, `dispatch_sample_chains.py`, `factory_adapter.py` | Level-0 glyph translator plus factory adapter; `dispatch_sample_chains.py` drops payloads into `outbox/orders/emoji_runtime/` and optional `factory_orders/`. |
| `alfa_m05` | Batch 1 hydration witness | `production/mass_alfa_batch1/alfa_m05/…`, `logs/mass_alfa_batch1/Alfa-M05/…` | Mirrors Toyfoundry readiness evidence for Batch 1, ensuring doc refresh + ledger automation hooks land before Batch 2. |

The remaining slots (`alfa_05`–`alfa_15`) stay empty until the overlay stack demands additional helpers (audio packs, comfort scoring, automated QA, etc.).

---

## Payload Flow (Today)

1. **Overlay Click (Alfa_00)**  
   `alfa_zero_controller.py` or `overlay_test_harness.py` maps cells (e.g., `04`, `4C`, `8A`, `C0`) to glyph chains and writes emoji-runtime payloads into `outbox/orders/emoji_runtime/`.

2. **Translator (Alfa_04)**  
   `emoji_translator.py` processes the chain; `dispatch_sample_chains.py --emit-factory-orders` can promote each payload into `factory-order@1.0` using `factory_adapter.py`.

3. **Narration & Telemetry (Alfa_02 + Alfa_03)**  
   The narrator shell provides spoken/text feedback, while the telemetry shell records loop latency via `logs/alfa_zero/phase_2_latencies.jsonl` (helpers live beside the overlay bridge).

4. **Ledger & Sync**  
   After each sequence, log a DOC-REFRESH/PLAYTEST/etc. entry in `exchange/ledger/2025-11.md` (see `template.md` for the exact format) and run the heartbeat + sync pair so the exchange mirrors the payloads.

This pipeline keeps Pivot Two (playable overlay) and Pivot Five (emoji-first language) in lockstep: every click yields a glyph chain, translator evidence, narration stub, telemetry stub, and a ledger breadcrumb.

---

## Operator Checklist

1. Choose the mapped cell (or pass `--event-stream` data) through `alfa_zero_controller.py`.
2. Confirm payload emission in `outbox/orders/emoji_runtime/` (and optionally `factory_orders/` if using the adapter).
3. Capture narration/telemetry context via the Alfa_02/Alfa_03 shells when needed.
4. Log your work:
   - Append a ledger line following `template.md`.
   - Update `planning/doc_refresh_queue.md` if the session refreshed canon scrolls.
   - Run `python tools/exchange_heartbeat.py` then `python tools/offline_sync_exchange.py`.
5. If the session produced readiness evidence (Batch 1 hydration, toddler co-play trials, etc.), copy artifacts into the relevant `logs/` or `production/` folders and mention them in the ledger summary.

Following this loop ensures every Alfa Zero touchpoint is measurable before we enter the Batch 2 planning lull.
