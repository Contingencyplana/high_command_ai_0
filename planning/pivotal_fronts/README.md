# Pivotal Fronts (Canon)

See also: planning/civilians_and_troops.md — concise index of the civil layer, gates, and pivot criteria.

**Last Updated:** 2025-10-31  
**Authorizing Body:** War Office + High Command  

This index orients work across all pivotal fronts and links to canon documents. Keep this as the single source of truth in High Command.

---

## The Seven Pivotal Fronts

### Front 1: Tons of Fun (Game Design & Balance)
**File:** `planning/pivotal_fronts/tons_of_fun.md`  
**Purpose:** Ensure Nightlands is genuinely fun, sticky, and replayable  
**Focus:** Balance, economy, anti-exploit gates, player retention

### Front 2: Safety (AI Safety & Containment)
**File:** `planning/pivotal_fronts/safety.md`  
**Purpose:** Prevent catastrophic outcomes; contain unsafe trajectories  
**Focus:** Kill-switches, dual-key approvals, incident response

### Front 3: Documentation (Clarity & Standards)
**File:** `planning/pivotal_fronts/docs.md`  
**Purpose:** Make doctrine clear, parseable, actionable for humans and AI  
**Focus:** Templates, schemas, safety notes, stable headings

### Front 4: R&D (Research & Development)
**File:** `planning/pivotal_fronts/r_and_d.md`  
**Purpose:** Advance SHAGI capabilities while maintaining safety  
**Focus:** Experiments, proposals, innovation within safety gates

### Front 5: Manufacturing (Toyfoundry)
**File:** `planning/pivotal_fronts/manufacturing.md`  
**Purpose:** Build and validate toy units via Forge/Parade/Purge/Promote rituals  
**Focus:** Production pipelines, telemetry, quality gates

### Front 6: Field Ops (Toysoldiers)
**File:** `planning/pivotal_fronts/field_ops.md`  
**Purpose:** Deploy and operate units in field theaters  
**Focus:** Deployment, monitoring, battlefield intelligence

### Enabler: Operations (Exchange Integrity)
**File:** `planning/pivotal_fronts/ops.md`  
**Purpose:** Keep exchange, ledger, and sync reliable  
**Focus:** Config-driven publish/pull, validation, watcher scans

---

## Guiding Principles

1. **One canon, many implementers** — Satellites link back; no drift
2. **Changes travel via Exchange** — Orders/acknowledgements/reports for all changes
3. **Safety gates guard promotions** — Proposal → sandbox → canary → GA
4. **Fronts coordinate, don't compete** — Shared telemetry, unified doctrine

---

## Cross-Cutting Concerns

### Telemetry & Monitoring
- **Quilt Loom:** `tools/quilt_loom.py` — Aggregates factory-reports
- **Watcher:** `tools/ci/safety_watcher.ps1` — Scans for violations
- **Ledger:** `exchange/ledger/` — Order lifecycle tracking

### Playable Workflow Overlay (New)
- **Four Major Pivots:** `new_major_pivots/README.md`
- **Alfa Zero Spec:** `docs/alfa_zero_spec.md`
- **Fractal Structure:** `golf_00/` through `golf_15/` (4,096 Alfas)

### Core Infrastructure

### Offline Continuity Mode Guardrails


### Offline Continuity Mode (Active)
- **Shared bus:** `C:/Users/Admin/high_command_exchange/` (set via `SHAGI_EXCHANGE_PATH` in every workspace).
- **Heartbeat + sync:** `python tools/exchange_heartbeat.py` then `python tools/offline_sync_exchange.py` keeps orders/reports mirrored across fronts.
- **Ledger discipline:** Append actions immediately (`exchange/ledger/2025-10.md` → `2025-11.md` on rollover) before or right after syncing.
- **Guardrails:** No Git pushes until War Office lift; escalate heartbeat 🟠/🔴 events with a report drop in `exchange/reports/inbox/`.
- **Monitoring hook milestones:**
	- `M0 — same shift:` Document refresh logged in ledger and heartbeat + sync pair executed.
	- `M1 — within 12h:` Dispatch `tools/quilt_loom.py --snapshot` to confirm report ingestion across pivots.
	- `M2 — within 24h:` Run `tools/ci/safety_watcher.ps1` for drift scan and file findings under `exchange/reports/inbox/`.

---

## Related Documents

- **Daylands Charter:** `planning/daylands_and_nightlands.md`
- **Pipeline & Gates:** `planning/internal_alfa_architecture.md`
- **AI Agents & Safety:** `planning/ai_agents_and_safety.md`
- **Safety Gate Template:** `planning/templates/safety_gate_template.md`
- **Change Order Template:** `exchange/orders/templates/change-order.template.json`
- **War Office Charter:** `war_office.md`

---

## Front Health Dashboard

| Front | Status | Last Review | Priority |
|-------|--------|-------------|----------|
| **Tons of Fun** | 🟢 Active | 2025-10-18 | High (post-pivot focus) |
| **Safety** | 🟢 Active | 2025-10-18 | Critical |
| **Documentation** | 🟡 Needs Update | 2025-10-18 | Medium |
| **R&D** | 🟢 Active | 2025-10-17 | High |
| **Manufacturing** | 🟢 Active | 2025-10-17 | High |
| **Field Ops** | 🟢 Active | 2025-10-17 | High |
| **Operations** | 🟢 Active | 2025-10-18 | Critical |

**Legend:**

- 🟢 Active — Front operational with current doctrine
- 🟡 Needs Update — Requires revision to reflect pivots
- 🔴 Blocked — Waiting on dependencies

---

## Version History

**v2.0 (2025-10-18):**

- Renamed from "Four Pivotal Fronts" to "Pivotal Fronts"
- Acknowledged all 7 fronts (was 4)
- Added Front 1 (Tons of Fun), Front 3 (Documentation), Enabler (Operations)
- Merged duplicate `ai_apocalypse.md` into `safety.md`
- Added cross-cutting concerns section (telemetry, playable overlay)

**v1.0 (pre-2025-10-17):**

- Original four-front structure
- Safety, R&D, Manufacturing, Field Ops only

---

*"Every front is a nerve in High Command's thinking body. Together, they form the mind that builds SHAGI."*  
— High Command Strategic Doctrine
