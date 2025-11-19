# Nightlands Duet Scoreboard Imagery Manifest

This manifest tracks the storyboard scoreboard frames captured for Order 2025-11-13-050.

| Image | State | Description | Annotation Highlights | Capture Notes |
|:--|:--|:--|:--|:--|
| `nightlands_duet_scoreboard_lore_invocation.png` | Lore Invocation | Full scoreboard capture from the 2025-11-19 trace (`outland-lore-v1-8A-20251119035924`) immediately after Step 1. Shows 15:00 cooldown, Lore-only overlay state, and prior targeted sync summary. | Cooldown timer, Lore overlay toggle, trace badge + sync chip. | Rendered from CLI output + telemetry feed; references real cadence data stored in `nightlands_duet_storyboard_sync_feed.jsonl`. |
| `nightlands_duet_scoreboard_duet_crescendo.png` | Duet Crescendo | Full scoreboard capture from the same trace immediately after Step 2. Displays 14:58 cooldown reset, Lore+Music overlays engaged, and the `[OK] Synced 2 orders → high_command_exchange/orders` indicator. | Cooldown pill, dual overlay toggles, targeted sync chip with operator ID. | Rendered from CLI output + telemetry feed to reflect the post-sync state preceding `sync latest 2`. |

## Annotation Guidance

- Use the annotation layer to highlight UI affordances the cohort asked about (cooldown countdown, overlay toggles, targeted sync summary chip).
- Store annotated exports in this directory with the filenames listed above and ensure metadata is mirrored alongside the imagery.
- When re-exporting, keep the original resolution and include a short alt-text block in the metadata file so the playtest packet stays accessible.

## Metadata Files

Each image has a companion metadata file describing annotations and trace alignment:

- `nightlands_duet_scoreboard_lore_invocation.metadata.json`
- `nightlands_duet_scoreboard_duet_crescendo.metadata.json`

These records capture trace IDs, operator, and cooldown measurements for ledger provenance.
