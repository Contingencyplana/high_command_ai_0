# Inlands & Outlands — Layered Playability Map

**Status:** Active pilot 2025-11-10  
**Authoring Body:** High Command (Order 046 execution)

---

## Purpose

Clarify how the core Nightlands workflow layers ("inlands") relate to the emergent overlays introduced by Major Pivot Seven ("outlands"). Provide a shared language for campaign planning, telemetry evidence, and operator handoffs.

---

## Definitions

- **Inlands**
  - The baseline Alfa workflow: emoji-runtime commands, automation loops, contract suites, comfort cadence.
  - Guarded by the 70/30 ratio (Pivot One) and the playable overlay charter (Pivot Two).
  - Evidence focus: factory orders, narration/telemetry traces, contract test logs, ledger ACKs.

- **Outlands**
  - Optional overlays layered on top of inlands (Pivot Seven / Outlands Onion).
  - Categories: `lore`, `music`, `ritual`, `emergent`.
  - Evidence focus: overlay payload extensions, guardian prompts, operator consent records, matching `trace_id` + `overlay_id` values.

---

## Relationship

| Aspect | Inlands (Core) | Outlands (Overlay) |
|:--|:--|:--|
| Purpose | Execute the workflow reliably | Amplify engagement, narrative, and expressiveness |
| Changes | Directly affect automation outputs and contracts | Wrap or annotate the core without breaking schema |
| Activation | Default-on (orders, play loops) | Opt-in, triggered via Fun Guardian and operator consent |
| Evidence | Automation logs, ledger entries, contract suite reports | Overlay traces, guardian protocol logs, Outlands index updates |

Outlands **must never** mutate the core emoji-runtime payloads in a way that breaks existing contracts. Instead, they should attach metadata, alternate renderings, or narrative summaries that reference the same `trace_id`.

---

## Activation Protocol (Pivot Seven Guardrail)

1. **Sense** – Run the Fun Guardian protocol to analyze engagement signals (cadence, comfort telemetry, contract friction).
2. **Select** – Choose an `overlay_id` and `layer_kind` from the Outlands index.
3. **Consent** – Present the overlay suggestion to the operator; require a conscious opt-in.
4. **Tag** – When activated, ensure narration traces, telemetry JSONL, and payload exports include both `trace_id` and `overlay_id` (`outland-lore-v1` for the Lore pilot).
5. **Log** – Record activation in the ledger (`Pivot Seven: <overlay_id> activated`) and append notes to `outlands_index.md` if new evidence sinks were added.

---

## Evidence Sinks

- `logs/alfa_02/narration_traces.jsonl` — confirm matching `trace_id` + `overlay_id` pairs for overlay narration.
- `logs/alfa_03/telemetry.jsonl` — overlay activation should append `overlay_id` metadata alongside existing trace records.
- `outbox/orders/*` — payload extensions may include `overlay_id`, lore snippets, or music cues; ensure contracts remain stable.
- `exchange/ledger/2025-11.md` (and subsequent ledgers) — ledger entries acknowledge activation/deactivation cycles.
- `exchange/attachments/guides/outlands_index.md` — keep index updated as new overlays or guardians come online.

---

## Routing Guidance

- **Stay Inland** when: stability/uptime is the priority, new automation contracts are being validated, or operator bandwidth is low.
- **Go Outland** when: engagement dips, narrative beats are needed, or campaign OKRs call for joy-first interventions.
- **Escalate Back Inland** if: overlays introduce confusion, telemetry noise spikes, or contracts show drift.

Routing decisions should be logged in `exchange/ledger/journal.md` so future campaigns can learn which overlays produced measurable benefits.

---

## Integration Points

- `exchange/attachments/guides/comfort_happy_path.md` — reference Outlands index for the play/automation cadence.
- `exchange/attachments/guides/automation_quick_start.md` — link to Outlands framework for optional layers during automation loops.
- `new_major_pivots/new_major_pivot_7.md` — source of the Outlands Onion charter and success metrics.
- Future controller/UI work (Order 046 candidate) should include toggles or prompts that follow this protocol.

---

## Execution Log (Order 046)

- Overlay metadata threaded through overlay bridge, narrator shell, telemetry shell, and Alfa Zero UI (Lore toggle default off; enable via `lore enable`).
- First Lore dispatch recorded (`overlay_id=outland-lore-v1`, `layer_kind=lore`) with matched trace IDs across payload, narration, telemetry, and phase two logs.
- Contract regression added (`overlay_lore_dispatch`) and pytest coverage expanded for guardrails and trace metadata.
- Comfort and automation guides refreshed with Lore opt-in instructions; Outlands index now captures activation history.

## Next Steps

1. Monitor lore activations for telemetry drift; adjust Fun Guardian prompts if comfort saturation drops.
2. Scope Music/Ritual overlay IDs mirroring this guardrail pattern.
3. Extend Alfa Zero controller to surface Outlands toggles if operators prefer the automation-centric interface.

Keep this document in sync with live Outlands experiments so strategy, telemetry, and gameplay stay aligned.
