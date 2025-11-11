# Multi-Layer Overlay Playbook (Pilot)

## Scope

- Covers Lore + Music pilots on Alfa Zero.
- Applies to stacked metadata where multiple layers are active.

## Precedence & Merging

- Primary layer: lore (overlay_id=outland-lore-v1).
- Secondary layer: music (overlay_id=outland-music-v1).
- Single-layer compatibility fields reflect primary only: overlay_id, overlay_layer.
- Full ordered stack emitted in overlays[]. Order must be deterministic.

## Consent Flow

- Default off. Operator explicitly enables each layer in the UI:
  - lore enable
  - music enable
- Dual-layer dispatch OK; UI shows ordered list and combined trace_id.

## Preflight Checklist

- Run readiness pack before enabling new layers:
  - python -m tools.ops_readiness
  - Expect: all sections [OK], summary artifact in logs/ops_readiness/.

## Guardrails & Cooldown (Pilot)

- Generate weekly metrics with `python -m tools.cooldown_rollup` (report lands in `planning/`).
- Track activation cadence in telemetry; avoid flapping.
- Suggested guideline: no more than 3 dual-layer activations per 24h per front without approval.

## Rollback

- Disable layer toggles in UI (lore disable, music disable).
- If issues persist, revert to single layer (lore only) to preserve compatibility fields.
- File a note in exchange/ledger/journal.md with trace_id and symptoms.

## Troubleshooting

- Missing overlay fields: verify UI toggles and check payload overlays[] ordering.
- Readiness failures: open latest logs/ops_readiness/summary-*.txt and fix the first failing step.
- Trace mismatch: confirm trace_utils.generate_trace_id inputs (cell label + overlays).

## References

- UI: golf_00/delta_00/alfa_00/alfa_zero_ui.py
- Bridge: golf_00/delta_00/alfa_00/overlay_bridge.py
- Readiness: tools/ops_readiness.py
- Samples: contract_samples/cases/overlay_lore_music_stack.json

