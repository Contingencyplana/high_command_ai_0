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

## Feature Flags & Gating

- Enable multi-layer tooling only when `balance_toggles` is approved:
  - Update `exchange/config.json` → `fun_flags.balance_toggles: true` (commit via exchange sync).
  - Optional dev override: export `BALANCE_TOGGLES=1` (PowerShell `setx BALANCE_TOGGLES 1`).
- Lore remains the default layer; Music requires explicit operator consent even when the flag is on.
- After flag change, restart Alfa Zero UI (`python -m golf_00.delta_00.alfa_00.alfa_zero_ui --enable-lore`) to confirm toggles display.

## Guardrails & Cooldown (Pilot)

- Generate weekly metrics with `python -m tools.cooldown_rollup` (report lands in `planning/`).
- Track activation cadence in telemetry; avoid flapping.
- Suggested guideline: no more than 3 dual-layer activations per 24h per front without approval.

## Feedback Loop

- Collect frontline notes with `python -m tools.frontline_feedback --workspace <name> --operator <id> ...`.
- Summarize sentiment with `python -m tools.frontline_feedback_summary`; share the outbox note with prioritization.

## Rollback

- Disable layer toggles in UI (lore disable, music disable).
- If issues persist, revert to single layer (lore only) to preserve compatibility fields.
- File a note in exchange/ledger/journal.md with trace_id and symptoms.

## Troubleshooting Appendix

| Symptom | Checks | Fix |
| -- | -- | -- |
| Readiness pack fails | Inspect latest `logs/ops_readiness/summary-*.txt` for failing section | Resolve first failure, rerun `python -m tools.ops_readiness`, and document in ledger |
| Missing overlay metadata | Confirm Lore/Music toggles were enabled; review payload `overlays[]` order | Re-dispatch with proper consent; Lore must be primary |
| Cooldown spike alert | Review `planning/cooldown_rollup_*.md` totals for the front | Pause dual-layer runs for 24h or secure approval before retrying |
| Music conflicts with ritual timing | Check frontline summary (`exchange/reports/outbox/frontline_feedback_summary_*.json`) for sentiment trend | Coordinate with Ritual lead, consider temporary Music disable |

## References

- UI: golf_00/delta_00/alfa_00/alfa_zero_ui.py
- Bridge: golf_00/delta_00/alfa_00/overlay_bridge.py
- Readiness: tools/ops_readiness.py
- Samples: contract_samples/cases/overlay_lore_music_stack.json

