# Alfa 04 — Emoji Composer Prototype

**Status:** Prototype scaffolding  
**Purpose:** Host the Level-0 emoji composer, narration pack, and runtime adapter tests for Major Pivot Five.

---

## Layout

| File | Role |
|------|------|
| `emoji_translator.py` | Converts glyph chains into Toyfoundry-ready JSON payloads (schema `emoji-runtime@1.0`) |
| `sample_chains.json` | Playground chains used by the dispatch harness |
| `dispatch_sample_chains.py` | Lightweight harness that writes translator output to the exchange outbox |
| `README.md` | This brief |

## Usage Expectations

1. Accept emoji chains from the grid overlay (`Noun → Verb → Target → Outcome` and variants).
2. Translate chains via `emoji_translator.py` and save payloads to the exchange outbox.
3. Use `dispatch_sample_chains.py` to validate round-trips before the overlay is connected.
4. Round-trip telemetry back into glyph narration for toddlers and AI co-players.

### Quick Harness Check

- Run `python dispatch_sample_chains.py` to drop translator payloads into `outbox/orders/emoji_runtime` (the folder synced by Offline Continuity Mode).
- Inspect the emitted timestamped JSON files to confirm the glyph IDs, summary line, intent block, and telemetry stub look correct before integrating a live caller.
- After dispatching, follow the heartbeat → ledger → `python tools/offline_sync_exchange.py` loop so satellites receive the orders.

### Overlay Bridge

- `golf_00/delta_00/alfa_00/overlay_test_harness.py` simulates grid clicks and funnels the mapped cells into the same translator path.
- `golf_00/delta_00/alfa_00/alfa_zero_controller.py` offers an interactive CLI so operators can drive the translator with live grid selections.
- Keep `sample_chains.json` in sync so both harnesses emit the canonical Level-0 payloads.

Future milestones will wire this Alfa to the playable overlay so each click enqueues a glyph chain for translation.
