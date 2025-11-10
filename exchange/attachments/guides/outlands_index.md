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
4. Tag resulting traces, ledger entries, and payload extensions with the chosen `overlay_id`.

## Evidence & Ledger Hooks

- Traces: `logs/alfa_02/narration_traces.jsonl`, `logs/alfa_03/telemetry.jsonl`, and overlay payload exports should include matching `trace_id` and `overlay_id` fields after activation.
- Ledger: annotate entries with `Pivot Seven` or the specific overlay name to preserve campaign history.

Keep this index updated as new Outland layers come online or when additional guardian playbooks are authored.
