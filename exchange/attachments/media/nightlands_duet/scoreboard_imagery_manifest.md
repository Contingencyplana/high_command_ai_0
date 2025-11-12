# Nightlands Duet Scoreboard Imagery Manifest

This manifest tracks the storyboard scoreboard frames captured for Order 2025-11-13-050.

| Image | State | Description | Annotation Highlights | Capture Notes |
|:--|:--|:--|:--|:--|
| `nightlands_duet_scoreboard_lore_invocation.png` | Lore Invocation | Placeholder composite approximating scoreboard immediately after Lore Invocation trigger. | Cooldown timer, Lore overlay toggle state, trace identifier badge. | Based on Alfa Zero UI layout references; swap in high-fidelity capture once art export pipeline resumes. |
| `nightlands_duet_scoreboard_duet_crescendo.png` | Duet Crescendo | Placeholder composite representing scoreboard after Duet Crescendo dispatch completes. | Cooldown recovery bar, Music overlay toggle, targeted sync indicator. | Derived from live run notes; replace with production capture when feasible in offline mode. |

## Annotation Guidance

- Use the annotation layer to highlight UI affordances the cohort asked about (cooldown countdown, overlay toggles, targeted sync summary chip).
- Store annotated exports in this directory with the filenames listed above and ensure metadata is mirrored alongside the imagery.
- When re-exporting, keep the original resolution and include a short alt-text block in the metadata file so the playtest packet stays accessible.

## Metadata Files

Each image has a companion metadata file describing annotations and trace alignment:

- `nightlands_duet_scoreboard_lore_invocation.metadata.json`
- `nightlands_duet_scoreboard_duet_crescendo.metadata.json`

These records capture trace IDs, operator, and cooldown measurements for ledger provenance.
