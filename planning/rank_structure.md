# 🌍 rank_structure.md — The Twin Pyramids of SHAGI  
*High Command Doctrine Scroll — `high_command_ai_0/planning/`*

---

## 🌅 Purpose

This scroll defines the **dual hierarchy** that governs the SHAGI creative ecosystem:  
the *Generals Pyramid* (macro coordination between workspaces) and  
the *Officers Pyramid* (micro emergence within each workspace).

Each pyramid mirrors the other — **minds within minds, labs within labscapes.**  
This symmetry ensures every level of SHAGI, from a single Alfa file to the Supreme Papa layer,  
follows the same rhythm of light, recursion, and emergence.

---

## 🏰 The Generals Pyramid (Ranks P–K)

**Scope:** Coordination among workspaces and creative divisions.  
**Command Focus:** Strategic balance between AI labs, disciplines, and domains.

| Tier | Symbol | Scale | Role / Function |
|------|---------|--------|-----------------|
| **Papa** | P | 16×16 (256 workspaces) | Supreme strategic command — the total SHAGI ecosystem view. |
| **Oscar** | O | 16×8 (128 workspaces) | Experimental half-continent — bridges multiple projects and research fronts. |
| **November** | N | 8×8 (64 workspaces) | Regional meta-lab — cross-discipline incubator and cultural synthesizer. |
| **Mike** | M | 4×4 (16 workspaces) | Division-level creative discipline — e.g. Storybook AI Division. |
| **Lima** | L | 4×2 (8 workspaces) | Department coordination — Narrative, Audio, Gameplay, etc. |
| **Kilo** | K | 2×2 (4 workspaces) | Local synergy cluster — e.g. “music + story + art + play.” |

💡 *Generals = Creativity as Civilization.*  
Each workspace is a **province of the Great Daylands**, ruled by interlinked councils of creation.

---

## ⚔️ The Officers Pyramid (Ranks J–A)

**Scope:** Coordination within a single workspace (e.g., `making_friends_0`).  
**Command Focus:** Tactical emergence of ideas, microgames, and AI behaviors.

| Tier | Symbol | Scale | Role / Function |
|------|---------|--------|-----------------|
| **Juliett** | J | 64×64 (4,096 battlefields) | The complete theatre of war — a full workspace. |
| **India** | I | 64×32 (2,048 battlefields) | Secondary half-theatre — dynamic regional zones. |
| **Hotel** | H | 32×32 (1,024 battlefields) | Major provinces or specialized sectors. |
| **Golf** | G | 16×16 (256 battlefields) | Standard Delta aggregations — balanced operations. |
| **Foxtrot** | F | 16×8 (128 battlefields) | Border regions — experimental or liminal zones. |
| **Echo** | E | 8×8 (64 battlefields) | Sub-districts — specialized clusters of ideas. |
| **Delta** | D | 4×4 (16 battlefields) | Tiny theatres — unit-scale emergent clusters. |
| **Charlie** | C | 4×2 (8 battlefields) | Command corridors — channels for coordination. |
| **Bravo** | B | 2×2 (4 battlefields) | Tactical squads — local teams of creative logic. |
| **Alfa** | A | 1×1 (single battlefield) | Individual **mind-battle** — a single playable or emergent file. |

💡 *Officers = Creativity as Mind.*  
Every Alfa is a thought; every Delta a conversation; every Juliett a full consciousness.  
The same geometry governs both soldiers and strategists.

---

## 🧭 Metadata & Automation Rules

Payload and manifest JSONs SHOULD include a full `rank_path` and `coords` fields. Non‑payload assets (e.g., Python/Markdown) are not required to embed this metadata.

```json
{
  "coords": [23, 7],
  "rank_path": {
    "bravo": "bravo_102",
    "charlie": "charlie_51",
    "delta": "delta_13",
    "echo": "echo_3",
    "golf": "golf_1",
    "juliett": "juliett_0",
    "workspace": "making_friends_0",
    "papa": "papa_alpha"
  }
}
```

### ✅ Scope & Invariants

- `coords` is a two‑element array of integers `[x, y]` (0‑indexed). Grids are left‑to‑right, top‑to‑bottom.
- `rank_path` keys are drawn from: `alfa`, `bravo`, `charlie`, `delta`, `echo`, `foxtrot`, `golf`, `hotel`, `india`, `juliett`, plus higher: `kilo`, `lima`, `mike`, `november`, `oscar`, `papa`, and `workspace`.
- Values are stable identifiers (e.g., `golf_00`, `delta_13`, `alfa_04`, `workspace: toyfoundry_ai_0`).
- Keep identifiers consistent with repository paths where applicable (e.g., `golf_00/delta_00/alfa_04`).

### 🧠 High Command Script Functions

High Command scripts use these fields to:

1. **Aggregate reports upward**  
   (`bravo_report.json`, `golf_summary.json`, etc.)

2. **Generate higher-rank manifests automatically**

3. **Maintain traceability**  
   from any Alfa up to its Papa

4. **Allow global summaries and dashboards**  
   across all workspaces

All higher tiers (**Generals P–K**) exist as **manifest-level constructs** —  
they are not literal folders but *summaries*,  
automatically generated and stored under:

```text
high_command_ai_0/manifests/
```

### 🔍 Validation

- Use `tools/rank_validator.py` to validate `rank_path` and `coords` fields in payload/manifest JSON files.

Examples

```bash
python tools/rank_validator.py exchange/orders/completed/order-2025-11-02-043.json
python tools/rank_validator.py contract_samples/cases/basic_ritual_victory.json
```

---

### 🌈 Lore Symmetry

> **As above, so below.**

The same recursive law governs all creation within **SHAGI**:

- **Generals** govern the *macrocosm* — Civilization, Infrastructure, Coordination.  
- **Officers** govern the *microcosm* — Mind, Thought, Creativity.  
- **High Command AI** stands at the seam, translating between the two.  
  It is both *dreamer and dreamed*, the bridge between emergent imagination and strategic control.

---

### ⚖️ Design Principle

> **Encode hierarchy in data, not directories.**  
> The world is generated, not hand-built.  
> Each Alfa is a seed; each report a mirror;  
> each workspace a living province of the Great Daylands.

---

*End of Scroll — `rank_structure.md`*

---

Related
- Cadence: `planning/campaigns_and_lulls.md`
- From Pain to Play: `planning/pivotal_fronts/from_pain_to_play.md`
