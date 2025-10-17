# Alfa Zero: Game Overlay Prototype Specification

**Status:** Draft  
**Version:** 0.1.0  
**Date:** 2025-10-17  
**Authorizing Body:** War Office + High Command  

---

## Purpose

Transform the VSCode/PowerShell/GitHub workflow into a **playable 16×16 emoji battleground** where tactical decisions trigger automation, and telemetry feeds victory conditions. The user commands toy soldiers on a grid; the system translates moves into High Command orders, dispatches them to Toyfoundry/Toysoldiers, and reports outcomes as battlefield events.

**Design Ratio:** 70% play / 30% dev-ops visibility

---

## Alfa Zero Scope

**Alfa Zero** is the **first playable prototype**—a single 16×16 grid representing one manufacturing workflow task. This prototype validates:

1. **Grid-to-Order translation:** User clicks grid cells → system issues High Command factory-order
2. **Telemetry-to-Victory mapping:** Factory reports feed win/loss conditions
3. **Emoji battlefield UX:** All game state rendered as 16×16 emoji grid
4. **Fractal extensibility:** Alfa Zero sits in `golf_00/delta_00/alfa_00`; future Alfas (001-4095) follow same pattern

---

## Mission: "The First Forge"

### Battlefield Setup

**Grid:** 16×16 emoji matrix  
**Objective:** Build 10 toy units (swords) from raw materials (ore) before time/resources expire  
**Theme:** Manufacturing workflow = tactical supply chain game

#### Grid Zones (16×16 layout)

```
 0 1 2 3 4 5 6 7 8 9 A B C D E F
0 🏔️🏔️🏔️🏔️⛏️⛏️⛏️⛏️📦📦📦📦🏭🏭🏭🏭
1 🏔️🏔️🏔️🏔️⛏️⛏️⛏️⛏️📦📦📦📦🏭🏭🏭🏭
2 🏔️🏔️🏔️🏔️⛏️⛏️⛏️⛏️📦📦📦📦🏭🏭🏭🏭
3 🏔️🏔️🏔️🏔️⛏️⛏️⛏️⛏️📦📦📦📦🏭🏭🏭🏭
4 🌾🌾🌾🌾👷👷👷👷🔨🔨🔨🔨⚔️⚔️⚔️⚔️
5 🌾🌾🌾🌾👷👷👷👷🔨🔨🔨🔨⚔️⚔️⚔️⚔️
6 🌾🌾🌾🌾👷👷👷👷🔨🔨🔨🔨⚔️⚔️⚔️⚔️
7 🌾🌾🌾🌾👷👷👷👷🔨🔨🔨🔨⚔️⚔️⚔️⚔️
8 🚢🚢🚢🚢📊📊📊📊🎯🎯🎯🎯✅✅✅✅
9 🚢🚢🚢🚢📊📊📊📊🎯🎯🎯🎯✅✅✅✅
A 🚢🚢🚢🚢📊📊📊📊🎯🎯🎯🎯✅✅✅✅
B 🚢🚢🚢🚢📊📊📊📊🎯🎯🎯🎯✅✅✅✅
C 🔥🔥🔥🔥⚠️⚠️⚠️⚠️📉📉📉📉❌❌❌❌
D 🔥🔥🔥🔥⚠️⚠️⚠️⚠️📉📉📉📉❌❌❌❌
E 🔥🔥🔥🔥⚠️⚠️⚠️⚠️📉📉📉📉❌❌❌❌
F 🔥🔥🔥🔥⚠️⚠️⚠️⚠️📉📉📉📉❌❌❌❌
```

#### Zone Legend

| Zone (rows) | Emoji | Function | Automation Trigger |
|-------------|-------|----------|-------------------|
| **0-3** (top) | 🏔️⛏️📦🏭 | **Resource Extraction & Initial Processing** | Click → Order: "extract_ore" + "forge_batch" |
| **4-7** (mid) | 🌾👷🔨⚔️ | **Manufacturing & Assembly** | Click → Order: "assemble_units" + "quality_check" |
| **8-B** (lower-mid) | 🚢📊🎯✅ | **Logistics & Validation** | Click → Order: "ship_batch" + "validate_schema" |
| **C-F** (bottom) | 🔥⚠️📉❌ | **Risk & Failure States** | Display only: telemetry warnings, failed batches |

---

## Game Mechanics

### Turn Structure

1. **Player Turn:** Click any cell in zones 0-B to queue an action
2. **System Turn:** High Command translates clicked cells → factory-order → dispatch to Toyfoundry
3. **Resolution:** Toyfoundry executes → factory-report → battlefield updates with outcome emoji

### Actions (Grid Cell → High Command Order)

| Grid Cell | Player Action | High Command Order | Expected Outcome |
|-----------|---------------|-------------------|------------------|
| `[0-3][0-3]` 🏔️ | "Extract Ore" | `{"action": "extract_ore", "quantity": 5}` | +5 ore units → 📦 counter |
| `[0-3][4-7]` ⛏️ | "Mine Faster" | `{"action": "speed_extraction", "duration_s": 60}` | 2× ore/turn for 3 turns |
| `[0-3][8-B]` 📦 | "Stockpile Check" | `{"action": "query_inventory", "resource": "ore"}` | Display current ore count |
| `[0-3][C-F]` 🏭 | "Forge Batch" | `{"action": "forge_batch", "input_ore": 5, "output_ingots": 1}` | -5 ore, +1 ingot |
| `[4-7][4-7]` 🔨 | "Assemble Unit" | `{"action": "assemble_unit", "input_ingots": 1, "output_swords": 1}` | -1 ingot, +1 ⚔️ |
| `[4-7][C-F]` ⚔️ | "Quality Check" | `{"action": "validate_quality", "batch_id": "current"}` | Pass/fail → ✅ or ❌ |
| `[8-B][8-B]` 🎯 | "Ship Units" | `{"action": "ship_batch", "units": 10}` | -10 ⚔️ → **Victory** if ≥10 available |

### Victory Conditions

- **Primary:** Ship 10 ⚔️ units (grid shows **10/10** → triggers "Mission Complete" animation)
- **Bonus:** Complete with ≥50% resource efficiency (telemetry: `ore_used / swords_shipped ≤ 60`)
- **Time:** Achieve victory within 20 player turns

### Defeat Conditions

- **Timeout:** 20 turns elapse without shipping 10 units → bottom rows (C-F) fill with 🔥❌
- **Quality Failure:** 3 consecutive failed quality checks → automatic defeat (too many defects)
- **Resource Depletion:** Ore count = 0 and ingots < 10 (impossible to win)

---

## Telemetry Integration

### Real-time Battlefield Updates

**Factory Reports** feed grid state:

```json
{
  "ritual": "Forge",
  "outcome": "success",
  "metrics": {
    "ore_consumed": 5,
    "ingots_produced": 1,
    "duration_ms": 1200
  }
}
```

→ Grid updates:
- 📦 counter decreases by 5
- 🏭 cell animates (brief glow effect)
- Ingot counter increases by 1

### Telemetry Quilt Display

**Bottom rows (C-F)** show live telemetry warnings:

- 🔥 = high latency (duration_ms > 5000)
- ⚠️ = policy violations (dark_pattern detected)
- 📉 = declining throughput (units/turn dropping)
- ❌ = failed batch (outcome = "failure")

**Example:** If 3 consecutive Forge rituals take >5s, row C fills with 🔥 cells proportional to delay.

---

## Architecture: Game-to-Automation Translation Layer

### Component Stack

```
┌─────────────────────────────────┐
│  Alfa Zero UI (16×16 Grid)      │  ← Player sees/clicks emoji
├─────────────────────────────────┤
│  Grid Controller (Python/TS)    │  ← Translates clicks → orders
├─────────────────────────────────┤
│  High Command Exchange API       │  ← Issues factory-orders
├─────────────────────────────────┤
│  Toyfoundry (Manufacturing)      │  ← Executes rituals
├─────────────────────────────────┤
│  Telemetry Quilt Loom            │  ← Aggregates factory-reports
├─────────────────────────────────┤
│  Grid State Updater              │  ← Renders telemetry → emoji
└─────────────────────────────────┘
```

### Grid Controller Pseudocode

```python
class AlfaZeroController:
    def __init__(self):
        self.grid = Grid16x16(initial_state="first_forge.json")
        self.resources = {"ore": 0, "ingots": 0, "swords": 0}
        self.turn_count = 0
        
    def on_cell_click(self, row, col):
        action = self.map_cell_to_action(row, col)
        order = self.create_factory_order(action)
        self.high_command.issue(order)  # → exchange/orders/pending/
        self.turn_count += 1
        
    def on_factory_report(self, report):
        self.update_resources(report.metrics)
        self.update_grid(report.outcome)
        self.check_victory_defeat()
        
    def update_grid(self, outcome):
        if outcome == "success":
            self.grid.animate_cell(emoji="✅")
        else:
            self.grid.fill_zone("C-F", emoji="❌", count=1)
```

### High Command Order Format

**Player clicks [0][0] (🏔️ Extract Ore):**

```json
{
  "order_id": "alfa-zero-turn-001",
  "target": "toyfoundry_ai_0",
  "schema": "factory-order@1.0",
  "summary": "AlfaZero Turn 1: Extract Ore",
  "directives": [
    {
      "step": 1,
      "action": "extract_ore",
      "details": "quantity=5, source=mountain_zone"
    }
  ],
  "priority": "realtime",
  "requires_ack": false,
  "game_context": {
    "alfa_id": "alfa_000",
    "grid_cell": [0, 0],
    "turn": 1
  }
}
```

---

## File Structure

```
high_command_ai_0/
├── golf_00/
│   └── delta_00/
│       └── alfa_00/
│           ├── grid_state.json          # Current 16×16 emoji state
│           ├── resources.json           # {ore, ingots, swords, turn_count}
│           ├── controller.py            # Grid click → order translation
│           ├── renderer.py              # Telemetry → emoji updates
│           └── victory_check.py         # Win/loss evaluation
├── exchange/
│   └── orders/
│       └── alfa_zero/               # Alfa Zero-specific orders
│           ├── pending/
│           ├── dispatched/
│           └── logged/
└── docs/
    └── alfa_zero_spec.md            # This document
```

---

## Development Roadmap

### Phase 1: Static Grid Prototype (1-2 days)
- [ ] Render 16×16 emoji grid in terminal (Python rich library)
- [ ] Hardcode cell click → print order JSON
- [ ] Manually trigger one Toyfoundry order, display fake factory-report

### Phase 2: Exchange Integration (2-3 days)
- [ ] Connect Grid Controller to `exchange/orders/pending/`
- [ ] Implement `on_factory_report()` listener
- [ ] Update grid state from real factory-reports

### Phase 3: Telemetry + Victory (1-2 days)
- [ ] Wire telemetry quilt → bottom rows (C-F) warning display
- [ ] Implement victory/defeat detection
- [ ] Add turn counter + resource tracker

### Phase 4: Polish + Fractal Prep (1 day)
- [ ] Add cell animations (emoji glow/pulse)
- [ ] Save/load game state (pause/resume)
- [ ] Document fractal replication pattern for Alfas 001-4095

---

## Success Metrics

**Prototype validates when:**

1. ✅ User clicks grid → High Command order auto-generated
2. ✅ Toyfoundry executes order → grid updates with outcome emoji
3. ✅ Telemetry warnings appear in bottom rows without user intervention
4. ✅ Victory condition triggers (10 swords shipped) → game declares win
5. ✅ All interaction happens via grid clicks—zero VSCode/PowerShell commands needed

**Fractal extensibility validates when:**

6. ✅ Alfa_00 code can be cloned → Delta_01/Alfa_00 with different mission parameters
7. ✅ 16 Alfas (00-15) fit cleanly in `golf_00/delta_00/` folder structure
8. ✅ Pattern scales to 16 deltas × 16 alfas = 256 missions per golf theater

---

## Open Questions

1. **UI Platform:** Terminal (Python rich) vs. VSCode Webview vs. Electron window?
2. **Realtime Updates:** Poll factory-reports every 1s, or use file watcher?
3. **Multiplayer:** Do multiple Alfas share telemetry quilt, or isolated per grid?
4. **Save States:** JSON snapshots or SQLite for game history?

---

## Appendix: Emoji Battlefield Vocabulary

| Emoji | Meaning | Usage |
|-------|---------|-------|
| 🏔️ | Raw materials (ore source) | Resource zones |
| ⛏️ | Extraction tool | Mining actions |
| 📦 | Stockpile/inventory | Resource counters |
| 🏭 | Factory/forge | Manufacturing zones |
| 👷 | Worker/assembler | Labor allocation |
| 🔨 | Crafting tool | Assembly actions |
| ⚔️ | Finished unit (sword) | Victory resource |
| 🚢 | Logistics/shipping | Transport zones |
| 📊 | Telemetry dashboard | Data display |
| 🎯 | Mission objective | Goal zones |
| ✅ | Success/validation | Positive outcomes |
| 🔥 | Critical error | Failure states |
| ⚠️ | Warning | Degraded performance |
| 📉 | Declining metric | Negative trends |
| ❌ | Failure/rejected | Defeat conditions |

---

**End of Alfa Zero Specification v0.1.0**

*"Where every click commands armies, and telemetry writes the battlefield."*  
— War Office Strategic Planning Division
