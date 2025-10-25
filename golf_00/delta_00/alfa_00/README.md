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

Each run imports the Level-0 translator from `alfa_04`, resolves the same emoji runtime outbox as the emoji composer, and writes timestamped JSON payloads annotated with the triggering grid cell.

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
