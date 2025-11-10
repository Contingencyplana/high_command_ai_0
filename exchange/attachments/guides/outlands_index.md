# Outlands Index (Pivot Seven)

Purpose: provide a single jumping-off point for the layered playability work introduced with Major Pivot Seven (Outlands Onion).

## Core References

- **Outlands Framework** — structural attachment points for Lore, Music, Ritual, and emergent overlays; see `exchange/attachments/guides/outlands_framework.md`.
- **Fun Guardian Protocol** — engagement sensing and recommendation loop for activating/deactivating overlays; see `exchange/attachments/guides/fun_guardian_protocol.md`.
- **Pivot Seven Charter** — overarching vision and success metrics; see `new_major_pivots/new_major_pivot_7.md`.

## Usage Checklist

1. Identify the desired layer (`lore`, `music`, `ritual`, or `emergent`).
2. Consult the Outlands Framework for the attachment points and evidence sinks.
3. Run the Fun Guardian protocol to capture engagement signals and secure operator consent.
4. In `alfa_zero_ui`, opt into the layer via `lore enable` (status with `lore status`, exit with `lore disable`).
5. Tag resulting traces, ledger entries, and payload extensions with the chosen `overlay_id`.

## Evidence & Ledger Hooks

- Traces: `logs/alfa_02/narration_traces.jsonl`, `logs/alfa_03/telemetry.jsonl`, and overlay payload exports should include matching `trace_id` and `overlay_id` fields after activation. Lore activations use `overlay_id=outland-lore-v1` and `overlay_layer=lore`.
- Ledger: annotate entries with `Pivot Seven` or the specific overlay name to preserve campaign history.

## Lore Layer (Order 046 Activation)

- `overlay_id`: `outland-lore-v1`
- UI toggle: `lore enable` inside `python -m golf_00.delta_00.alfa_00.alfa_zero_ui`
- Single-dispatch shortcut: `python -m golf_00.delta_00.alfa_00.alfa_zero_ui --enable-lore --cell 04`
- Evidence bundle:
  - Payload export: see latest file under `outbox/orders/emoji_runtime/` with matching `overlay_id`
  - Narration trace: `logs/alfa_02/narration_traces.jsonl`
  - Telemetry trace: `logs/alfa_03/telemetry.jsonl`
  - Phase 2 log: `logs/alfa_zero/phase_2/*.json`
  - Ledger entry: `exchange/ledger/journal.md` (tagged `Pivot Seven / Lore overlay`)

Promote additional overlay layers (music, ritual, emergent) by replicating this pattern with new `overlay_id` values and documenting playbooks below.

Keep this index updated as new Outland layers come online or when additional guardian playbooks are authored.
