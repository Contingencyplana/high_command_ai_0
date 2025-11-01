# Alfa 00 — Overlay Harness Staging

**Status:** Prototype harness
**Purpose:** Exercise the Alfa Zero battlegrid translation path before the real UI lands.

---

## What Lives Here

| File | Role |
|------|------|
| `overlay_test_harness.py` | Simulates grid clicks and drops translator payloads into the exchange |
| `alfa_zero_controller.py` | Interactive CLI that renders the 16×16 grid and dispatches mapped cells |
| `README.md` | This brief |

---

## Usage

- Dispatch a single mapped cell: `python overlay_test_harness.py --cell 0,4`
- Smoke test every mapped cell: `python overlay_test_harness.py --all-cells`
- Launch the interactive controller: `python alfa_zero_controller.py`
- Stream overlay events from the UI: `python alfa_zero_ui.py --emit-events | python alfa_zero_controller.py --event-stream -`

Each run imports the Level-0 translator from `alfa_04`, resolves the same emoji runtime outbox as the emoji composer, and writes timestamped JSON payloads annotated with the triggering grid cell. The controller automatically logs ledger entries and fires the heartbeat → sync loop unless you pass `--no-auto-sync` (useful for dry runs).

### Event Streaming

- `alfa_zero_ui.py --emit-events` emits JSON lines such as `{"cell":"4C","source":"alfa_zero_ui"}` to stdout (or a file via `--event-file`).
- While emitting events, the UI mirrors its grid output to stderr so streaming pipelines keep stdout clean.
- Pipe those events into `alfa_zero_controller.py --event-stream -` to reuse the ledger + sync discipline for real overlay clicks.
- Passing `--no-auto-sync` to the controller or `{"auto_sync": false}` in an event allows dry runs without touching the ledger.

### Phase 2 Telemetry Logging

- Every dispatch appends a stub entry to `logs/alfa_zero/phase_2_latencies.jsonl` and writes a per-batch JSON file under `logs/alfa_zero/phase_2/{batch_id}.json`.
- When Toyfoundry telemetry lands, call `record_phase_two_telemetry(batch_id, status="success")` to stamp the receipt time and duration automatically.
- The helper lives in `overlay_bridge.py` so UI or backend bridges can import it without reimplementing the logging semantics.
- For manual updates or cron workflows, run `python tools/record_phase_two_telemetry.py --batch-id …`.

---

## Mapping Snapshot

The harness currently binds four representative cells to the sample glyph chains:

| Cell (hex) | Chain | Description |
|------------|-------|-------------|
| `04` | `basic_ritual_forge` | Forge ritual from mountain supply line |
| `4C` | `guarded_delivery_wall` | Secure delivery to fortress wall |
| `8A` | `signal_loop_dream` | Signal the dream relay for telemetry |
| `C0` | `conditional_repeat_seed` | Seed repeatable growth cadence |

Extend `CELL_MAPPINGS` in the script as more grid interactions come online.
