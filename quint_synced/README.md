# Quint-Synced Guidance

This folder contains alignment documents that **must remain identical** across all five strategic workspaces:

- `high_command_ai_0`
- `toyfoundry_ai_0`
- `toysoldiers_ai_0`
- `valiant_citadel_ai_0`
- `r_and_d_ai_0`

Update the files here first, then immediately propagate the exact same change to the corresponding `quint_synced/` directory in each workspace. Add a brief entry to the version table below whenever you sync, so it is easy to confirm consistency.

## Sync Log

| Version | Date | Notes | Workspaces Updated |
| --- | --- | --- | --- |
| v1.0 | 2025-10-26 | Initial payload & narration alignment drop | HC · TF · TS · VC · RD |
| v1.1 | 2025-10-26 | Added action orders requesting ACK/TODO from each workspace | Pending front acknowledgements |
| v1.2 | 2025-10-26 | Toysoldiers production translator go-live; schema ACK recorded | TS (pending mirror to peers) |
| v1.3 | 2025-10-26 | Pivot Five emoji-first alignment updates staged here | VC (source) · Pending HC · TF · TS · RD |
| v1.4 | 2025-10-26 | RD review + adoption of Pivot Five alignment set; ready to propagate outward | RD · Pending HC · TF · TS |
| v1.5 | 2025-10-26 | Toyfoundry ACK: emitter bridge online + War Office handoff checklist drafted | TF · Pending HC · TS · VC · RD |

**Process reminder:**

1. Modify the alignment doc in `high_command_ai_0`.
1. Run `python tools/quint_sync.py` from any workspace root to mirror `quint_synced/` and capture ACK/TODO notes.
1. Commit the change in each repo.
1. Record the sync in the table (or review the generated entry in `quint_synced/sync_log.md`).

If a workspace cannot be updated immediately, annotate the table (e.g., "Pending TF") and resolve the gap as soon as possible.

 
