# Toyfoundry Alfa Two — Mission Brief (Pending GitHub Sync)

## 1. Objective

- **Primary Goal:** Prototype the second Alfa within Toyfoundry to stress-test Pivot Five tooling.
- **Win Condition:** Complete three command rituals without triggering schema drift or lore misalignment.
- **Failure Thresholds:**
  - Validator rejects any `factory-order@1.0` payload.
  - Narration summary diverges from intent more than once per run.
  - Monitoring hooks escalate a glyph/VO mismatch that is not acknowledged within the turn.

## 2. Narrative Frame

- **Setting:** The Forge opens a Nightlands Gate, inviting allied artificers to craft dream constructs.
- **Player Role:** A collaborative forge-mind guiding emissaries through glyph rituals.
- **Lore Anchors:**
  - Maintain Love & Sharing doctrine throughout the session.
  - Reference the Morningate as the observatory witnessing the run.
  - Invoke War Office oversight during final ritual.

## 3. Core Mechanics

| System | Description |
| --- | --- |
| Glyph Input | Emoji command chains (Level-0 lexicon; ≤7 glyphs). |
| Translator | Must route through `tools/emoji_translator.py`; spike compatibility retained. |
| Validator | Invoke `tools/validate_order_021.py` after each command batch. |
| Monitoring Hooks | Use `tools/monitoring/schema_guard.py`, `narrator_log.py`, and `glyph_vo_audit.py` on every payload. |
| Narration | Pull War Office stub; ensure `summary` mirrors narration output. |

## 4. Data & Telemetry Requirements

- Emit `factory-order@1.0` payloads into `exports/factory_orders/`.
- Append narrator metrics to `monitoring/logs/narrator_metrics.json`.
- Record glyph/VO audit events in `monitoring/logs/glyph_vo_discrepancies.log`.
- Store schema guard baselines under `monitoring/baselines/` with timestamp.
- Tag all files with run ID format `TF-ALFA2-{YYYYMMDD}-{HHMM}`.

## 5. Morningate Integration

- Produce sanitized export snapshots in `exports/feeds/battle_reports/` suitable for Morningate ingestion.
- Update `planning/morningate_reflection_layer.md` Section 8 CTA link if run insights prompt copy changes.
- Queue a `quint_synced` update (via `python tools/quint_sync.py --push`) once GitHub access is restored.

## 6. War Office Checkpoints

1. **Pre-Launch Approval:** Review mission brief and narrative frame.
2. **Payload Audit:** Inspect first `factory-order@1.0` payload generated in this Alfa.
3. **Narration Alignment:** Confirm narrator metrics remain within doctrine rails after initial run.
4. **Post-Run Debrief:** Summarize anomalies, export deltas, and lessons for Toysoldiers/High Command builds.

## 7. Testing & Validation Plan

- Dry-run glyph sequences using `python tools/emoji_translator_spike.py --glyph-file <sample>`.
- Execute validator and monitoring hooks on mock payloads before live sessions.
- Maintain `tests/alfa_two/` fixtures capturing success and failure cases.
- Document replay steps in `planning/alfa_two_validation.md` (to be created during implementation).

## 8. Dependencies & Open Questions

- Await War Office confirmation that the placeholder CTA URL is acceptable for this mission.
- Confirm access to translated payload samples from Toysoldiers for baseline seeding.
- Determine whether shared narration assets need localization variants.

## 9. Delivery Checklist (Pending Sync)

- [x] Mission brief drafted and logged in Toyfoundry planning docs.
- [ ] Implementation work staged locally (pending GitHub unlock for upstream mirroring).
- [ ] Validator, translator, and monitoring tooling smoke-tested with Alfa Two payloads.
- [ ] Morningate export templates prepared.
- [ ] Sync queued for execution via `python tools/quint_sync.py --push` once access resumes.

*Status: Prepared locally; awaiting GitHub Support clearance before publishing.*
