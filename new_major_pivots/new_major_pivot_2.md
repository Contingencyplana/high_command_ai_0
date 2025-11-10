# Major Pivot Two: Playable Workflow Overlay (16×16 Emoji Battlegrids)

**Status:** Approved  
**Date Proposed:** 2025-10-17  
**Authorizing Body:** War Office + High Command  
**Impact:** Transformational — replaces dev-ops interfaces with game layer

---

## Problem Statement

Current workflow requires direct interaction with:
- **VSCode** — text editor, file management, git operations
- **PowerShell** — terminal commands, script execution
- **GitHub** — version control, pull requests, issues
- **Azure Cloud** — infrastructure deployment, monitoring

**Operator experience:** These tools are necessary but soul-destroyingly boring for human operator.

---

## Pivot Description

**Build a playable workflow overlay** that shields human operator from VSCode/PowerShell/GitHub/Azure:

### Core Concept: Alfas (Workflow Nodes as Battlegrids)

Each **Alfa** is:
- A **16×16 emoji grid** representing one workflow task (e.g., "run Forge ritual," "deploy to Azure," "validate telemetry")
- A **playable battlefield** with tactical zones, resources, objectives
- A **workflow node** that translates player actions into automation (git commits, deployments, tests)

### Game Loop

1. **Spawn:** Operator enters Alfa battleground (grid displays current state via emoji)
2. **Play:** Operator clicks grid cells to issue tactical commands
3. **Execute:** High Command translates clicks → factory-orders → Toyfoundry/Toysoldiers execute
4. **Resolve:** Telemetry feeds back as grid updates (success = ✅, failure = ❌)
5. **Victory:** Task completes (tests pass, deployment succeeds) → route to next critical Alfa
6. **Defeat:** Task fails → respawn with adjusted strategy (debug mode, retry with different parameters)

### Routing & Progression

- **After victory:** Game routes operator to next high-priority Alfa based on telemetry (e.g., "Forge backlog," "failing CI/CD pipeline," "untriaged issues")
- **After defeat:** Operator respawns in same Alfa or escalates to "War Room" for strategic planning
- **Idle state:** Game suggests next Alfa or enters "patrol mode" (low-priority maintenance tasks as mini-games)

---

## Architecture

### Abstraction Layers

```
┌──────────────────────────────────────┐
│  Game Client (16×16 Emoji Grids)    │  ← Human operator plays here
├──────────────────────────────────────┤
│  Grid Controller (Python/TypeScript)│  ← Translates clicks → orders
├──────────────────────────────────────┤
│  High Command Exchange Protocol      │  ← Issues factory-orders
├──────────────────────────────────────┤
│  AI Agents (Toyfoundry, Toysoldiers)│  ← Execute VSCode/PowerShell/git/Azure ops
├──────────────────────────────────────┤
│  Telemetry Quilt Loom                │  ← Aggregates outcomes → grid state
└──────────────────────────────────────┘
```

**Analogy:**
- VSCode/PowerShell/GitHub/Azure = **assembly code & machine language**
- High Command/Toyfoundry/Toysoldiers = **LLVM & compilers**
- Game Overlay = **high-level programming language** (accessible, intuitive)

---

## Example Alfa: "The First Forge"

**Workflow Task:** Execute Forge ritual (mint 10 toy units)

**16×16 Grid Zones:**
- **Rows 0-3:** Resource extraction (🏔️ ore, ⛏️ mining tools)
- **Rows 4-7:** Manufacturing (👷 workers, 🔨 crafting, ⚔️ swords)
- **Rows 8-B:** Logistics (🚢 shipping, 📊 telemetry, ✅ validation)
- **Rows C-F:** Danger zones (🔥 errors, ⚠️ warnings, ❌ failures)

**Player Actions:**
- Click `[0][0]` (🏔️) → "Extract ore" → High Command issues `extract_ore` order
- Click `[4][4]` (🔨) → "Forge batch" → Toyfoundry executes Forge ritual
- Click `[8][8]` (🚢) → "Ship units" → If 10 units ready, **victory**

**Victory Condition:** Ship 10 ⚔️ swords within 20 turns  
**Defeat Condition:** Timeout, 3 failed quality checks, or resource depletion

---

## Success Criteria

1. ✅ **Human operator never opens VSCode/PowerShell/GitHub UI** during normal gameplay
2. ✅ **All workflow tasks executable via grid clicks** (100% coverage for routine ops)
3. ✅ **Telemetry surfaced as game state** (warnings = danger zone emoji, success = positive animations)
4. ✅ **Victory/defeat conditions tied to real automation outcomes** (not fake game state)
5. ✅ **Routing algorithm sends operator to highest-priority Alfas** (based on telemetry quilt)

---

## Dependencies

- **Major Pivot One** — requires 70/30 ratio to justify game layer investment
- **Major Pivot Four** — requires fractal folder structure (golf_00–15) for 4,096 Alfas
- **Exchange Protocol** — must support real-time order issuance from game client
- **Telemetry Quilt** — must feed grid state updates at <1s latency

---

## Progress Log — 2025-11-09

- **2025-11-08 — Order 044:** Seeded narrator and telemetry shells in `golf_00/delta_00/alfa_02` and `alfa_03`, refreshed comfort-loop guidance, and validated automation-path contracts to back overlay traces.
- **2025-11-09 — Order 045 Kickoff:** Issued the UI overlay integration slice with baseline readiness sweep (heartbeat, offline sync, contract suite) confirmed green; stretch backlog tracked separately to protect the core slice.
- **2025-11-09 - Order 045 Day 0:** Upgraded narrator/telemetry shells with overlay context, comfort toggles, and JSONL trace capture sowing logs under `logs/alfa_02/narration_traces.jsonl` and `logs/alfa_03/telemetry.jsonl`.
- **Telemetry Hooks:** Runtime shells now expose overlay hook points with trace capture earmarked as Order 045 milestone evidence.
- **2025-11-09 - Order 045 Day 1:** Wired the first overlay interaction end-to-end via `overlay_flow` (correlated narrator + telemetry with comfort and overlay context). Captured traces and added `overlay_first_click` to the contract suite; all contracts passing.
- **2025-11-10 - Order 045 Day 2:** Expanded overlay regression coverage with `overlay_guarded_wall` and `overlay_guarded_warning`; threaded `trace_id` correlation into overlay dispatch payloads and refreshed rollout notes/ledger entries to lock both success and risk paths.
- **2025-11-10 - Order 045 Day 3:** Verified trace parity across direct Alfa Zero UI and event-stream paths so telemetry, payloads, and factory orders carry matching `trace_id` values.

---

## Risks

| Risk | Mitigation |
|------|------------|
| Game UI too simplistic for complex tasks | Retain VSCode access for 30% edge cases; expand grid vocabulary iteratively |
| Latency between click and outcome breaks immersion | Optimize telemetry pipeline; add "executing" animations |
| Operator gets stuck in losing Alfa | Implement "call for reinforcements" (escalate to AI agent or War Room) |
| 4,096 Alfas = too much content to manage | Procedural generation + telemetry-driven prioritization (only surface critical Alfas) |

---

## Development Roadmap

### Phase 1: Alfa Zero Prototype (1 week)

- Build one playable 16×16 grid (static first, then live) in `golf_00/delta_00/alfa_00/`
- Wire to exchange protocol (clicks → orders → reports → grid updates)
- Validate victory/defeat conditions

### Phase 2: Fractal Expansion (2-4 weeks)

- Clone Alfa Zero → 16 variants (populate full `golf_00/delta_00/` sector)
- Implement routing algorithm (victory → next priority Alfa)
- Add save/load game state

### Phase 3: Full Deployment (2-3 months)

- Scale to 4,096 Alfas (golf_00 through golf_15, all delta sectors populated)
- Procedural generation of Alfas from workflow templates
- Multiplayer support (multiple human operators + AI agents)

---

## Long-Term Vision

**This overlay becomes the foundation for:**

- **Nightlands Multiplayer Game** — workflow Alfas are tactical missions in larger campaign
- **SHAGI Multiverse** — each Big Ideas Family has its own game overlay
- **Human-AI collaboration at scale** — thousands of operators playing workflows across thousands of games

---

## Approval Status

**Approved by:** War Office (civilian oversight) + High Command (military execution)  
**Effective Date:** 2025-10-17  
**Review Cycle:** After each fractal expansion phase (16, 256, 4,096 Alfas)

---

*"The best interface is the one you never have to think about—unless it's fun."*  
— High Command Strategic Doctrine, Volume III
