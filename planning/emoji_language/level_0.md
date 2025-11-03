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

## Audio Motif Experiment (Draft)

**Purpose:** Prototype a music-first parallel to the emoji grammar by assigning each Level-0 noun a canonical tone. Successful round-trips here become the seed for Major Pivot Six.

### Canonical Tone Map (Nouns)

| Emoji | Note | Frequency (Hz) | Instrument Patch | Duration |
|:------|:-----|:---------------|:-----------------|:---------|
| 🛠️ Forge | C4 | 261.63 | Warm marimba | 1 beat @ 120 BPM |
| 🌾 Field | D4 | 293.66 | Warm marimba | 1 beat @ 120 BPM |
| 🌌 Dream | E4 | 329.63 | Celesta pad | 1 beat @ 120 BPM |
| 🌊 River | F4 | 349.23 | Glass harmonics | 1 beat @ 120 BPM |
| 🧱 Wall | G4 | 392.00 | Low brass mute | 1 beat @ 120 BPM |
| 🔥 Ember | A4 | 440.00 | Choir ahh | 1 beat @ 120 BPM |
| 🌱 Seed | B4 | 493.88 | Plucked harp | 1 beat @ 120 BPM |
| 🤖 Ally | C5 | 523.25 | Synth bell | 1 beat @ 120 BPM |

> Keep timbres gentle so toddlers can replicate with humming or toy instruments. Record reference clips in `audio/motifs/nouns/`.

### Experiment Steps

1. **Palette Pack:** Generate `.wav` stems for each noun tone using 120 BPM quarter-note strikes; save metadata in `audio/motifs/nouns/index.json`.
2. **Composer Patch:** Add a "Tone Pad" layer to `golf_00/delta_00/alfa_04/` where the noun slot can trigger audio playback while logging the corresponding emoji token.
3. **Capture Loop:** Record three sample chains (e.g., `🛠️ ⚒️ 🤖 ✅`) by sequencing tones for noun slots and default narrator stings for non-noun glyphs; export MIDI + JSON in `experiments/motif_roundtrip/`.
4. **Translation Check:** Extend `emoji_translator.py` canary tests to accept paired `tone_id` metadata and ensure audio-tagged payloads still pass validation.
5. **Telemetry Replay:** Push motif-tagged orders through Toyfoundry sandbox and verify telemetry returns the same tone IDs; archive results in `logs/experiments/motif_roundtrip.jsonl`.

Document outcomes and deltas so High Command can evaluate the lift required for a full music-first grammar.

---

## Next Actions

1. Record and package narration clips using spoken prompts listed above
2. Prototype drag-and-drop composer inside `golf_00/delta_00/alfa_04/`
3. Expand `emoji_translator.py` with Toyfoundry payload contracts and validation suite
4. Draft toddler co-play test plan (audio narration + supervision prompts)
5. Build noun tone palette per the **Audio Motif Experiment** (run `python tools/generate_tone_palette.py`) and log first round-trip attempt
6. Schedule the nightly translator canary (`python golf_00/delta_00/alfa_04/dispatch_sample_chains.py`) so `logs/canary/emoji_translator/translation_events.jsonl` accrues the required 14 consecutive passes
   - Suggested cron entry (UTC): `0 3 * * * /usr/bin/env python3 /path/to/repo/tools/run_emoji_canary.py >> /path/to/repo/logs/canary/nightly.log 2>&1`
7. Pipe Toyfoundry telemetry acknowledgements into `python tools/process_phase_two_telemetry.py` (or call `tools/record_phase_two_telemetry.py`) so Phase 2 latency metrics stay current

---

*This document evolves alongside `new_major_pivots/new_major_pivot_5.md` as the emoji spellbook matures.*
