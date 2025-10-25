# Payload Alignment: `factory-order@1.0`

## Action Required — 2025-10-26

- Review this payload brief together with `quint_synced/narration_alignment.md` in your workspace.
- Confirm the `factory-order@1.0` schema behaves in your local runtime; note any integration gaps immediately.
- Keep `quint_synced/` copies identical across all five workspaces—propagate any edits back to High Command and the remaining fronts as soon as they land.
- Reply with a quick ACK (or an annotated TODO) so the sync log can capture your status.
- Maintain lore alignment: the payload `summary` line must stay in lockstep with the narration guidance; flag War Office if you need extra VO, localization, or schema support.
- Treat this brief as the canonical **Pivot Five** integration checklist—emoji-first command chains must serialize exactly into this schema with no inferred tokens.

## Pivot Five Alignment Notes

- Verify local translators are using the 32 glyph Level‑0 lexicon; report any glyph ID drift to War Office immediately.
- Keep Level‑0 rituals at ≤7 glyphs until schema change control approves longer programs.
- Confirm `glyph_chain` ordering matches the original emoji input and that no fallback text strings are substituted.

## Reference Artifacts

- `C:\Users\Admin\toysoldiers_ai_0\samples\emoji_commands\level0_sample.json`
- `C:\Users\Admin\toysoldiers_ai_0\planning\emoji_language\spike_logs\translator_round_trips.jsonl`
- Narration stub: `"Forge crafts the Ally → Victory"`
- Level‑0 grammar draft: `C:\Users\Admin\toysoldiers_ai_0\planning\emoji_language\level_0.md`
- R&D staging scratchpad: `C:\Users\Admin\r_and_d_ai_0\planning\emoji_language\pivot_five_rollout.md` (create/update as work proceeds)

## Schema Overview

The translator currently emits payloads under the `factory-order@1.0` schema. Formalizing this contract allows the War Office to validate downstream integrations and approve telemetry capture.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `schema` | string | yes | Literal identifier; locked to `factory-order@1.0`. |
| `summary` | string | yes | Lore-facing sentence (see narration brief). Should remain <120 chars. |
| `glyph_chain` | array[string] | yes | Ordered glyph sequence representing the command path. Must mirror input emoji chain. |
| `intent` | object | yes | Canonical intent extraction (see breakdown below). |
| `telemetry_stub` | object | yes | Minimal operations telemetry for validator and dashboards. |

### `intent` object

- `actor` (string, required): Entity initiating the action. Enumerated during spike: `forge`, `barracks`, `arsenal`, `relay` (extendable with War Office approval).
- `action` (string, required): Verb in snake-case; examples: `craft`, `deploy`, `reinforce`.
- `target` (string, required): Primary object of the action (`ally`, `garrison`, etc.).
- `qualifiers` (array[string], optional): Ordered modifiers; default empty.
- `outcome` (string, required): Outcome taxonomy drawn from `victory`, `stalemate`, `retreat`, `catastrophic`, pending War Office confirmation.

### `telemetry_stub` object

- `batch_id` (string, required): Unique identifier `{actor}-{action}-{timestamp}`.
- `ritual` (string, required): Mirrors `actor`; used by validator routing.
- `units_processed` (integer, required): Count of glyph steps processed.
- `status` (string, required): One of `success`, `warning`, `error`.
- `duration_ms` (integer, required): Processing time; integer >=0.

## Validation & Workflow Expectations

- Translator emits payload; validator confirms schema shape + outcome taxonomy.
- Any deviation triggers `accepted: false` with populated `schema_errors` or `dq_errors` in round-trip logs.
- Toysoldiers must version-lock against this schema until War Office signs off on upgrades (capture change log in `payload_alignment.md`).

## Open Items for War Office Session

- Confirm final list + definitions for `outcome` taxonomy.
- Approve maximum glyph chain length and permitted emoji sets per ritual.
- Decide whether `summary` must always align with narration copy or can diverge for analytics.
- Determine retention window for `telemetry_stub` fields and whether additional telemetry is required.
- Identify reviewer to own schema change control going forward.

## Workspace Status — r_and_d_ai_0

- **2025-10-26:** Alignment packet reviewed; awaiting translator prototype implementation. ACK logged in local README sync table (v1.3).
