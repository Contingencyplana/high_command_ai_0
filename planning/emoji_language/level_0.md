# Emoji Language Level-0 Grammar (Draft)

**Status:** In Progress  
**Last Updated:** 2025-10-25  
**Owner:** High Command, War Office Liaison (Language)

---

## Purpose

Establish the initial 32-glyph lexicon and sentence patterns required to power Major Pivot Five (Emoji-First Computing Language). This draft acts as the workbench for designing toddler-friendly commands that compile into Toyfoundry/Toysoldiers rituals without textual input.

---

## Deliverables

- ✅ Vocabulary inventory aligned with nouns, verbs, qualifiers, and outcomes
- ✅ Sample Level-0 sentence templates (Noun → Verb → Target → Outcome)
- ✅ Audio narration guide for each glyph chain
- ✅ Compiler mapping strategy (emoji → JSON payloads)

---

## Level-0 Glyph Inventory (32 Glyphs)

| Emoji | Category | Lore Anchor | Spoken Prompt | JSON Token |
|:------|:---------|:------------|:--------------|:-----------|
| 🛠️ | Noun | Forge Hall | "forge" | `actor.forge` |
| 🌾 | Noun | Field Depot | "field" | `actor.field` |
| 🌌 | Noun | Dream Tower | "dream" | `actor.dream` |
| 🌊 | Noun | River Gate | "river" | `actor.river` |
| 🧱 | Noun | Wall Foundry | "wall" | `actor.wall` |
| 🔥 | Noun | Ember Vault | "ember" | `actor.ember` |
| 🌱 | Noun | Seed Nursery | "seed" | `actor.seed` |
| 🤖 | Noun | Ally Barracks | "ally" | `actor.ally` |
| ⚒️ | Verb | Artisan Crew | "craft" | `verb.craft` |
| 🚀 | Verb | Launch Pad | "launch" | `verb.launch` |
| 🌿 | Verb | Greenhouse | "grow" | `verb.grow` |
| 🛡️ | Verb | Shield Wall | "shield" | `verb.shield` |
| 🧶 | Verb | Loomworks | "weave" | `verb.weave` |
| 🔄 | Verb | Relay Ring | "loop" | `verb.loop` |
| 📦 | Verb | Courier Run | "deliver" | `verb.deliver` |
| 🪄 | Verb | Transmutation Lab | "transmute" | `verb.transmute` |
| ⏱️ | Qualifier | Timekeepers | "quick" | `qualifier.tempo` |
| 💡 | Qualifier | Idea Forge | "bright" | `qualifier.idea` |
| 🛰️ | Qualifier | Signal Mast | "signal" | `qualifier.signal` |
| 🧭 | Qualifier | North Gate | "north" | `qualifier.direction` |
| 🔍 | Qualifier | Inspectors | "scan" | `qualifier.inspect` |
| ☁️ | Qualifier | Cloud Ward | "cloud" | `qualifier.cloud` |
| 🔒 | Qualifier | Safehouse | "safe" | `qualifier.safe` |
| 🎯 | Qualifier | Target Range | "focus" | `qualifier.target` |
| ✅ | Outcome | Victory Banner | "victory" | `outcome.success` |
| ⚠️ | Outcome | Risk Beacon | "warning" | `outcome.risk` |
| 💤 | Outcome | Stasis Pod | "sleep" | `outcome.pause` |
| 📈 | Outcome | Rise Tower | "rise" | `outcome.gain` |
| 🌀 | Outcome | Storm Well | "storm" | `outcome.chaos` |
| 🌈 | Outcome | Blessing Arch | "blessing" | `outcome.bless` |
| 🧊 | Outcome | Ice Keep | "freeze" | `outcome.freeze` |
| 🔁 | Outcome | Encore Square | "again" | `outcome.repeat` |

> **Narration cues** are single-syllable or two-syllable words for toddler co-play; each glyph also maps to a lore location so the storybook voice can situate the action.

---

## Level-0 Sentence Templates

1. **Basic Ritual:** `Noun → Verb → Target → Outcome`  
	Example: `🛠️ ⚒️ 🤖 ✅` → "Forge craft ally victory" (compile to forge orders success)
2. **Guarded Delivery:** `Noun → Verb → Qualifier → Target → Outcome`  
	Example: `🤖 📦 🔒 🧱 ✅` → secure delivery to wall infrastructure
3. **Signal Loop:** `Noun → Qualifier → Verb → Outcome`  
	Example: `🌌 🛰️ 🔄 📈` → dream signal loops to raise telemetry confidence
4. **Conditional Repeat:** `Noun → Verb → Outcome → Outcome`  
	Example: `🌱 🌿 ✅ 🔁` → grow seed, repeat on success

Every chain is capped at **five glyphs** in Level-0. Longer rituals are constructed by stacking multiple chains on the grid composer.

---

## Audio Narration Guide

- Narration cadence: **beat-per-glyph**, with warm storyteller tone ("Forge... craft... ally... victory!").
- Outcomes trigger **call-and-response**: after `✅`, narrator prompts toddler to cheer; after `⚠️`, narrator asks adult to review.
- Qualifiers inject **adverbs** ("quick", "safe") while maintaining simple vocabulary.
- Provide downloadable audio pack: `audio/level_0/{emoji}.ogg` mirroring spoken prompts above.

---

## Compiler Mapping Strategy

1. **Tokenization:** Split glyph chain into slot-based structure using deterministic template detection (see `emoji_translator.py`).
2. **Validation:** Ensure glyphs exist in inventory and match template length; reject ambiguous chains with friendly narrated prompt.
3. **Translation:** Map tokens to JSON payload `{ "actor": ..., "verb": ..., "qualifiers": [...], "target": ..., "outcome": ... }`.
4. **Emission:** Write payload to `exchange/orders/outbox/emoji_runtime/` alongside narrated `.ogg` cue.
5. **Round-trip:** After Toyfoundry execution, translate telemetry back to glyph chain and push into composer log.

---

## Next Actions

1. Record and package narration clips using spoken prompts listed above
2. Prototype drag-and-drop composer inside `golf_00/delta_00/alfa_04/`
3. Expand `emoji_translator.py` with Toyfoundry payload contracts and validation suite
4. Draft toddler co-play test plan (audio narration + supervision prompts)

---

*This document evolves alongside `new_major_pivots/new_major_pivot_5.md` as the emoji spellbook matures.*
