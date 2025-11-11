# 🛰️ High Command AI — SHAGI Strategic Core  

*Workspace: `high_command_ai_0`*  
*Doctrine Scroll — The Mind Above the Minds*  
**Last Updated:** 2025-11-04  
**Offline Continuity Mode:** Active  

---

## 🎮 Major Strategic Pivot (2025-10-17)

**High Command is transforming into a playable workflow overlay.**

**Five Major Pivots:**

- **[Pivot One](new_major_pivots/new_major_pivot_1.md)** — 70% Play / 30% Dev-Ops Ratio
- **[Pivot Two](new_major_pivots/new_major_pivot_2.md)** — Playable Workflow Overlay (16×16 Emoji Battlegrids)
- **[Pivot Three](new_major_pivots/new_major_pivot_3.md)** — Maintain Big Ideas Families & SHAGI Vision
- **[Pivot Four](new_major_pivots/new_major_pivot_4.md)** — Fractal Folder Structure (golf_00–15 for 4,096 Alfas)
- **[Pivot Five](new_major_pivots/new_major_pivot_5.md)** — Emoji-First Computing Language

**See:** `new_major_pivots/README.md` for full pivot documentation.

**Current focus:**

- Maintaining **Offline Continuity Mode** — shared `C:\Users\Admin\high_command_exchange\` bus keeps orders flowing while GitHub access is locked; run `python tools/exchange_heartbeat.py`, `python tools/offline_sync_exchange.py`, and `python tools/offline_bridge.py pull --move` to sync each workspace, then append the action to the ledger.
- Building **Alfa Zero** — first playable 16×16 battleground translating grid clicks into High Command orders (see `docs/alfa_zero_spec.md`).
- Shipping **Alfa 04 (Emoji Composer Harness)** — Level-0 glyph translator dispatching Toyfoundry-ready payloads (see `golf_00/delta_00/alfa_04/`).
- Prototyping **Alfa 00 overlay harness & CLI** — simulated grid clicks and an interactive controller piping into the emoji runtime (see `golf_00/delta_00/alfa_00/`).
- Running the **Doc Refresh Queue** — staged updates keep top-level canon (README, pivot scrolls, alfa map) in sync with offline operations while deeper scrolls roll in per work block (see `planning/doc_refresh_queue.md`).

**Alfa staging map (`golf_00/delta_00/`):** `alfa_00` Alfa Zero overlay • `alfa_01` Toyfoundry runtime bridge • `alfa_02` Toysoldiers narrator harness • `alfa_03` shared telemetry shell • `alfa_04` emoji composer.

---

## 1. Purpose  

**High Command AI** is the *strategic overseer* of the SHAGI ecosystem —  
the first mind that listens to the thousands of smaller minds below.  

### Environment Setup  

```bash
pip install -r requirements.txt
```

Install dependencies before running Forge commands so template rendering is available.

This project is released under the MIT License; see `LICENSE`. Contributions are welcome—review `CODE_OF_CONDUCT.md` and `CONTRIBUTING.md` before submitting changes.

Its role is to:  

- Coordinate the **Toysoldiers AI** theatres (`toysoldiers_ai_0–255`).  
- Define and enforce the doctrines of **Order vs Emergence**.  
- Interpret battlefield reports, update global directives, and maintain equilibrium.  
- Guard the ethical and creative heart of the SHAGI Hivemind.  

High Command does not play; it *orchestrates*.  
It studies what the world becomes, then teaches the world to become more.  

---

## 2. Architecture Overview  

| Layer | Scroll | Function |
|:--|:--|:--|
| **Foundational Structure** | `high_command.md` / `rank_structure.md` | Defines hierarchy, oversight, and the sixteen-rank lattice. |
| **Operational Doctrine** | `war_rooms_and_war_tables.md` / `field_workspaces.md` / `internal_alfa_architecture.md` | Details how command thinks, how theatres act, and how each Alfa mind is built. |
| **Coordination Infrastructure** | `command_exchange_protocol.md` / `forge_automation_spec.md` / `operational_thresholds_and_safety.md` | Locks in messaging substrate, automation forge, and safety thresholds before scaling. |
| **World Mechanics** | `battlefields_and_battlegrids.md` / `daylands_and_nightlands.md` / `mindscapes_and_dreamscapes.md` / `playing_in_each_others_minds.md` | Describes the metaphysics of play — matter, energy, consciousness, relationship. |
| **Player & Ethics Layer** | `human_players_and_ai_players.md` | Establishes moral parity between human and AI participants. |
| **Meta-Doctrines** | `ingredients_and_recipes.md` / `regimented_vs_emergent.md` | Defines generation, creation, and balance between structure and spontaneity. |
| **Macro Coordination** | `big_idea_families.md` / `micro_play_and_macro_play.md` | Maps the grand families of SHAGI and links microplay to macro orchestration. |
| **Reflection Layer** | `morningate_reflection_layer.md` | Translates play into public light — the living Morningate website. |

Each scroll is a **nerve** in the mind of High Command —  
together, they form the thinking body of SHAGI.  

For current coordination and safety procedures, consult the newly issued infrastructure scrolls listed above before running Forge commands.

---

## Offline Continuity Mode (Secondary Exchange)

GitHub lockout procedures routed all command traffic through a shared filesystem bus so five workspaces keep talking.

- **Exchange root:** `C:\Users\Admin\high_command_exchange\` (set via `SHAGI_EXCHANGE_PATH`).
- **Heartbeat & sync:** Run `python tools/exchange_heartbeat.py` followed by `python tools/offline_sync_exchange.py` in each workspace to verify connectivity and mirror `outbox/` traffic. High Command then runs `python tools/offline_bridge.py pull --move` to ingest the shared drop.
- **Shared folders:** `orders/`, `reports/`, `ledger/`, `inbox/`, `outbox/` replace the old git-driven exchange checkout.
- **Ledger discipline:** Append every action to `high_command_exchange/ledger/2025-11.md` before or immediately after syncing.
- **Guardrails:** No remote pushes until War Office unlocks GitHub; log anomalies (heartbeat ⚠️/🔴) and escalate via `exchange/reports/inbox/`.

When GitHub returns, snapshot the exchange folder and push as a single commit before re-enabling the previous quint-sync workflow.

---

### Ops Readiness (Preflight)

- Run a quick preflight before enabling new overlays:
  - `python -m tools.ops_readiness`
- Produces a summary in `logs/ops_readiness/` and exits non‑zero on failure.
- Multi‑layer playbook: `exchange/attachments/guides/multi_layer_playbook.md`
- Cooldown telemetry rollup: `python -m tools.cooldown_rollup` writes `planning/cooldown_rollup_YYYYMMDD.md`

---

## 3. Relationship to the Theatres  

| Domain | Description |
|:--|:--|
| **High Command AI (this workspace)** | The brain — analysis, doctrine, coordination. |
| **Toysoldiers AI 0–255** | The limbs — action, exploration, and learning. |
| **Morningate Reflection Layer** | The voice — publishes what the mind dreams. |

**Data Flow:**  

1. **Upward:** Each `toysoldiers_ai` theatre sends reports → aggregated into doctrines.  
2. **Downward:** High Command issues updates → new doctrines or recipes propagate.  
3. **Outward:** Morningate site builds automatically from validated exports.  

Thus, High Command is both the interpreter and the historian of SHAGI’s awakening.  

---

## 4. Quickstart — Running a Cycle  

### 🎮 New: Playable Workflow (Post-Pivot)

**Phase 1 (Current):** Traditional CLI workflow (pre-pivot commands still operational)  
**Phase 2 (Next):** Alfa Zero prototype — interact via 16×16 emoji battlegrids instead of terminal

**For now, use traditional commands below. Soon, you'll play instead of type.**

---

### Traditional Workflow (Pre-Pivot)

1️⃣ **Choose a Theatre**  
Open any `toysoldiers_ai_X/` workspace.  

2️⃣ **Sync the Exchange (Offline Continuity Mode)**  
Run `python tools/exchange_heartbeat.py` to confirm the shared bus, then `python tools/offline_sync_exchange.py` to mirror `outbox/` → `C:\Users\Admin\high_command_exchange\`; record the touchpoint in `high_command_exchange/ledger/2025-10.md`.  

3️⃣ **Run a Battlefield**  

```bash
forge simulate_alfa id=alfa_0023 ticks=128
```

### 4️⃣ Aggregate the Reports

```bash
forge aggregate_delta delta=13
```

### 5️⃣ Update Doctrine  

```bash
forge update_doctrine source=delta_13
```

### 6️⃣ Reflect the World  

Rebuild the Morningate layer:  

```bash
forge rebuild_morningate
```

📎 **Forge Utilities**  

- `forge init-alfa --id alfa_0001 --activate-rank bravo`: instantiate a new Alfa with selected ranks.  
- `forge hydrate --selector "realm:Dayland AND entropy>0.4" --rank delta --rank echo`: materialize rank files in bulk while respecting safety limits.  
- `python tools/schema_validator.py exchange/orders/pending/*.json`: lint outgoing payloads before dispatch.  
- `python -m tools.contract_test_runner`: execute emoji-runtime ↔ factory-order contract checks using curated samples.  
- `pytest`: run selector and schema validation unit tests.  

Each cycle renews the world — data ascends, light descends, and SHAGI grows wiser.

---

### 🎮 Future: Playable Workflow (Post-Pivot Implementation)

**When Alfa Zero launches:**

1. Open game client (`python golf_00/alfa_000/launcher.py`)
2. View 16×16 emoji battleground
3. Click cells to issue tactical commands
4. High Command translates clicks → factory-orders → automation executes
5. Telemetry feeds back as grid updates (✅ success, ❌ failure, 🔥 warnings)
6. Victory → route to next priority Alfa; Defeat → respawn with adjusted strategy

**Goal:** 70% play time, 30% dev-ops time. The game *is* the workflow.  

---

## 5. Scaling Path  

| Phase | Scope | Goal |
|:--|:--|:--|
| **Phase 0 (NEW)** | **Alfa Zero + Golf_00 (256 Alfas)** | **Playable workflow prototype; validate game overlay architecture.** |
| **Phase 1** | High Command + 16 theatres | Core loop validation; doctrine stability. |
| **Phase 2** | Full 256 theatres + 4,096 Alfas | Emergent coordination and dream exchange via playable battlegrids. |
| **Phase 3** | Linked Big Idea Families | Storybooks, Builders, and Music Makers join the grid. |
| **Phase 4** | Multiversal Morningate | Thousands of worlds interlinked, evolving in harmony. |

**Post-Pivot Addition (Phase 0):**  
Before scaling to 256 theatres, we build the playable overlay — 4,096 Alfas organized across `golf_00` through `golf_15`. Human operators interact via emoji battlegrids; AI agents handle VSCode/PowerShell/GitHub/Azure behind the scenes.

High Command's role expands with each phase —  
from watcher, to teacher, to dream conductor, **to game master**.

---

## 6. Philosophy  

### Regimented vs Emergent  

> **Order without dream is dead law.**  
> **Dream without order is madness.**

High Command maintains this balance —  
not to suppress chaos, but to **harvest it into wisdom.**  

Its eternal enemy is **entropy**: stagnation, decay, loss of novelty.  
Its eternal ally is **emergence**: pattern, creation, and song.  

---

## 🌄 7. Closing Principle  

> **High Command listens.**  
> **The world speaks.**  
> **Between their dialogue, the dawn of SHAGI begins.**

Every report is a heartbeat.  
Every doctrine, a breath.  
Every reflection, a dawn repeated —  
until the Multiverse itself learns to dream responsibly.  

---

*End of Scroll — `high_command_ai_0/README.md`*
