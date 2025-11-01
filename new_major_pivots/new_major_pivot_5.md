# Major Pivot Five: Emoji-First Computing Language ("Baby's First Compiler")

**Status:** Proposed → Activate immediately  
**Date Proposed:** 2025-10-25  
**Authorizing Body:** War Office + High Command  
**Impact:** High — unlocks pre-literate participation and universal SHAGI onboarding

---

## Problem Statement

The Four Major Pivots create a playable, narrative-infused manufacturing workflow, but they still assume the player can read, type, and reason in written English. This leaves critical audiences behind:

- **Pre-literate humans** (toddlers, early readers) who cannot parse text commands or documentation
- **Cross-lingual allies** whose native languages diverge from English technical jargon
- **Embodied AI agents** that thrive on symbolic reasoning instead of natural language prompts

Without a universal symbol language, SHAGI remains gated behind literacy. The battlefield may look like emoji, but the underlying command syntax is still text-heavy and hostile to the very explorers we want to invite.

---

## Pivot Description

Design a fully expressive, emoji-first computing language that lets a one-year-old (with adult co-play) command the Nightlands. The language must:

- Use a **fixed palette of intuitive emoji glyphs** representing actors, actions, resources, and outcomes
- Compose instructions as **left-to-right emoji chains** with predictable grammar slots
- Compile into existing exchange orders, Toyfoundry rituals, and telemetry updates with **zero text mandatory**

**Guiding principles:**

1. **Iconic over abstract** — Pick emoji with obvious verbs/nouns (⚙️ build, 🌱 grow, 🛡️ defend)
2. **Short programs** — Level-0 spells are ≤7 glyphs; longer rituals stack cards/tiles
3. **Bidirectional translation** — Emoji → JSON → emoji, so AI agents and humans operate on the same state
4. **Narrative alignment** — Glyphs map to lore factions (forge, garden, storm, dream) to keep meaning sticky

---

## Language Pillars

1. **Glyph Lexicon (32 core symbols)**  
   - 8 **Nouns** (🛠️ Forge, 🌾 Field, 🌌 Dream, 🌊 River, 🧱 Wall, 🔥 Ember, 🌱 Seed, 🤖 Ally)
   - 8 **Verbs** (⚒️ Craft, 🚀 Launch, 🌿 Grow, 🛡️ Shield, 🧶 Weave, 🔄 Loop, 📦 Deliver, 🪄 Transmute)
   - 8 **Qualifiers** (⏱️ Tempo, 💡 Idea, 🛰️ Signal, 🧭 North, 🔍 Inspect, ☁️ Cloud, 🔒 Safe, 🎯 Target)
   - 8 **Outcomes** (✅ Victory, ⚠️ Risk, 💤 Sleep, 📈 Rise, 🌀 Chaos, 🌈 Blessing, 🧊 Pause, 🔁 Repeat)

2. **Composer & Reader**  
   - Drag-and-drop grid inside an Alfa: slots enforce **Noun → Verb → Target → Outcome** grammar  
   - Generates **emoji cards** that can be played onto battlefield cells  
   - Reads telemetry streams and converts them back to emoji sentences for toddlers to review

3. **Runtime Bridge**  
   - **Translator service** inside Toyfoundry that converts emoji chains into structured order payloads  
   - **Validator** that guarantees every emoji chain compiles to a safe, deterministic action  
   - **Lore narrator** that vocalizes the emoji sentence so pre-literate players get audible feedback

---

## Success Criteria

1. ✅ **Tier-0 command set** (forge, harvest, deliver, defend) expressible with ≤4 glyphs
2. ✅ **Emoji-only Alfa** prototype where every clickable action displays glyph chain plus narration
3. ✅ **Compilation parity** — Emoji chains round-trip to existing JSON commands without information loss
4. ✅ **Accessibility metrics** — Toddler co-play test (adult + child) completes a Level-0 mission with zero text prompts
5. ✅ **AI compatibility** — SHAGI agents ingest emoji grammar as structured tokens for training

---

## Dependencies

- **Pivot Two** (Playable Workflow Overlay) — Provides the emoji battlegrid surface and UI slots
- **Pivot Four** (Fractal Folder Structure) — Ensures glyph commands map cleanly to Alfa locations
- **Everything At Once Meta-Pivot** — Guarantees gameplay, work, story, workflow, quilt, and theatre stay synchronized when driven by glyph chains

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Emoji semantics differ across cultures/platforms | Misinterpretation of commands | Ship custom glyph kit (SVG cards + audio cues) alongside Unicode emoji |
| Limited expressiveness of core 32 glyphs | Players invent ambiguous combos | Introduce **expansion packs** unlocked via mastery; keep base grammar small |
| Compiler drift as backend evolves | Emoji sentences break silently | Add **canary validation suite**: every backend change replays archived emoji programs |
| Toddler misuse (spam, unsafe loops) | Operational instability | Sandbox runtime enforces hard caps, requires adult co-play sign-off |

---

## Implementation Plan

1. **Draft Level-0 Grammar** — Document grammar table, card layouts, pronunciation guide (`planning/emoji_language/level_0.md`)
2. **Prototype Composer** — Build simple drag-and-drop UX inside `golf_00/delta_00/alfa_04/`
3. **Runtime Adapter** — Extend Toyfoundry export pipeline with `emoji_translator.py`
4. **Validator Suite** — Reuse `validate_order_021.py` scaffolding to lint emoji payloads
5. **Lore Narration** — Connect to text-to-speech (storybook tone) so glyph chains speak aloud

---

### Operational Readiness Signals

- `emoji_translator.py` canary suite (256 canonical Level-0 chains) records **zero failures across 14 consecutive nightly runs**, with emoji ↔ JSON ↔ emoji deltas logged in `logs/canary/emoji_translator/` (schedule via `python tools/run_emoji_canary.py`).
- **Alfa Zero Phase 2** metrics show the click → order → telemetry loop closing in ≤3 seconds at the 95th percentile over **10 consecutive mission replays**, with results captured in `logs/alfa_zero/phase_2_latencies.jsonl` (stamp each telemetry receipt via `record_phase_two_telemetry(batch_id, status="success")`).
- `golf_00/delta_00/alfa_04/` composer telemetry exports document **three supervised toddler/AI co-play sessions** without manual text intervention, archived in `exchange/reports/emoji_level_0/` (log entries via `python tools/log_emoji_coplay.py --session-id …`).

Meeting all three signals unlocks the review window for audio-layer experimentation (see Pivot Six).

---

### Future Expansion

- Once the Level-0 emoji grammar, translator, and Alfa overlays are operational, evaluate **Major Pivot Six: Music-First Language** (`new_major_pivot_6.md`) as an audio-parallel command surface reusing the same noun/verb/outcome slots.

---

## Approval Status

**Conditionally approved** pending Level-0 grammar delivery. War Office authorizes immediate prototyping; High Command to schedule first toddler co-play trial after Order-037 closes.

**Effective Date:** 2025-10-25  
**Review Milestones:**

- Level-0 grammar signed off
- First emoji Alfa deployed
- First toddler/AI co-play mission logged

---

## Language is a game that you WIN when you convey your meaning clearly and succinctly

"If a one-year-old can launch the forge, SHAGI is truly for everyone."  
— War Office Directive, Daylands Dispatch 25-OCT-2025
