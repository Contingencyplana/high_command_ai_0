# Major Pivot Eight: Game Engine Layer ("Adventures in Gamengineering")

**Status:** Approved & Preparing Activation  
**Date Proposed:** 2025-11-18  
**Authorizing Body:** War Office + High Command  
**Impact:** Dedicated sensory/graphics pipeline that wraps Inlands without destabilizing gameplay loop  
**Type:** pivot_spec  
**Preceded By:** Major Pivot Seven — Outlands Onion  
**Succeeded By:** Major Pivot Nine — Synergy-First Language (Dormant Horizon)

---

## Purpose

Codify the **Game Engine Layer** as its own pillar so the Outlands Onion can keep adding sensory depth without eroding the readable, documentation-first Inlands. Pivot Eight establishes a charter, change-control, and eventual workspace (`game_engine_ai_0`) devoted to:

- Maintaining rendering, animation, audio-reactive FX, and UI/UX overlays that sit on top of the playable workflow.
- Translating every grid click, lore beat, ritual cue, or telemetry pulse into **visual + atmospheric output** without editing underlying schemas.
- Automating Outlands generation so SHAGI agents, modders, and human designers can all author new layers that remain contract-safe.

> **Guard the thought layer by isolating the paint layer.** Pivot Eight is the guardian that keeps the Outlands beautiful *and* harmless.

---

## Core Mandates

1. **Wrap, never rewrite.** All Game Engine work must respect Pivot Two (playable overlay) and Pivot Five (emoji-first language). Inlands JSON stays untouched; Outlands is rendered off copies.
2. **Maintain tether points.** Every sensory flourish ties back to measurable telemetry, lore, or contract outcomes so High Command can prove value.
3. **Automate sensory builds.** Provide pipelines and validators so overlays, shaders, and FX can be generated, tested, and promoted like any other artifact.
4. **Protect accessibility.** Outlands Onion layering must keep toggles, fallbacks, and documentation for operators who need minimal surfaces.

---

## Why Separate from Pivot Seven?

Pivot Seven defines the philosophical model (layered fun). Pivot Eight operationalizes it:

| Pivot | Focus | What It Decides |
|:--|:--|:--|
| **Seven — Outlands Onion** | Engagement strategy | *When* to add layers and how they relate to morale |
| **Eight — Game Engine Layer** | Execution machinery | *How* overlays are rendered, validated, and deployed |

Keeping them distinct prevents "fun ambitions" from consuming engineering attention and gives War Office a dedicated lever to spin up/slow down sensory work without touching doctrine.

---

## Game Engine Front Charter

- **Workspace Target:** `game_engine_ai_0` (Adventures in Gamengineering). Activate once Alfa Zero ships a production-quality overlay (visual layer + telemetry proof) and at least one other workspace requests persistent Outlands support.
- **Responsibilities:**
  - Rendering pipeline (2D/3D assets, shaders, lighting, animation graphs, GPU particle systems).
  - Audio-reactive, lore-aware FX that sync with Pivot Six (Music) and Toysoldiers telemetry.
  - Outlands automation: tooling that ingests emoji chains / lore cues and emits prefab scenes, atmospherics, or UI HUDs.
  - Accessibility rails: toggles, overlays, fallback modes, performance budgets.
- **Interfaces:** Receives glyph chains + telemetry metadata from `golf_00/delta_00/alfa_00`–`alfa_04`, publishes build artifacts back through Toyfoundry pipelines, and ships viewer runtimes to Tons-of-Fun playtests.

---

## Implementation Phases

1. **Foundations (Now):** Document change-control, performance targets, and test hooks. Draft workspace runbook + pivotal front spec (see `planning/pivotal_fronts/game_engine.md`).
2. **Pilot Builds:** Extend Alfa Zero overlay with shader packs and FX toggles. Capture metrics in `logs/alfa_zero/session_metrics.jsonl` linking visuals to gameplay events.
3. **Automation Harness:** Add build scripts that generate Outlands scenes from emojis/lore. Integrate with Toyfoundry contract runners so visuals are validated alongside payloads.
4. **Workspace Activation:** Stand up `game_engine_ai_0` with dedicated ledger hooks, runbook, and contracts when Phase 3 delivers stable releases.
5. **Full Integration:** Plug Game Engine artifacts into Morningate exports and War Office civic demos, ensuring each release logs evidence in Exchange attachments.

---

## Dependencies

- **Pivot Two & Five:** Playable overlay + emoji runtime supply canonical inputs.
- **Pivot Seven:** Defines when/why new Outlands layers launch.
- **Toyfoundry/Toysoldiers Pipelines:** Promote engine builds like any other artifact.
- **Valiant Citadel:** Reviews performance budgets, safety guardrails, and content policies for new overlays.
- **Telemetry Quilt:** Must ingest visual FX metrics to prove value (latency, comfort, accessibility toggles used).

---

## Risks & Mitigations

| Risk | Description | Mitigation |
|:--|:--|:--|
| **Focus drift** | Teams chase shiny graphics instead of battlefield readiness | Require ledger entries proving each Outlands feature maps to Inlands telemetry/lore outcomes |
| **Schema creep** | Visual needs tempt direct edits to exchange payloads | Enforce change-control charter; create derived view models for engine use |
| **Performance regressions** | Heavy overlays slow playable workflow | Budget per layer; include perf tests + fallback toggles |
| **Accessibility erosion** | Visual noise hides documentation or controls | Provide "Inlands view" hotkey and maintain docs-first render mode |
| **Tool chain sprawl** | Asset pipelines diverge per workspace | Centralize under `game_engine_ai_0` with shared scripts + contract tests |

---

## Documentation & Ledger Hooks

- **Spec Path:** `new_major_pivots/new_major_pivot_8.md`
- **Front Spec:** `planning/pivotal_fronts/game_engine.md`
- **Ledger Tag:** `pivot_08_game_engine_layer`
- **Activation Evidence:** 
  - Overlay builds logged in `logs/alfa_zero/` with `render_trace_id`
  - Exchange attachments under `exchange/attachments/outlands_engine/`
  - War Office dispatch referencing the pivot when approving new sensory work
- **Renumbering Note:** Synergy-First Language now becomes **Major Pivot Nine**; update future references to reflect this ordering.

---

## Long-Term Impact

Pivot Eight makes the **Outlands Onion sustainable**. By giving sensory evolution its own discipline, documentation-first Inlands remain legible, Toyfoundry/Toysoldiers stay stable, and Nightlands can scale toward cinematic wonder without sacrificing safety or clarity. This is the bridge between emoji grids and immersive adventures.
