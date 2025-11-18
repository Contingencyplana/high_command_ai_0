# Genesis Workspaces

## Overview

Nightlands now operates with a full Tenfold Genesis Layer: ten coordinating workspaces that balance civilian intent, military execution, manufacturing, safety, culture, archives, exchange, and public reflection. The original five-mind spine still exists, but the crown (War Office) and mirrors (Exchange + Morningate) now form a closed loop so every Alfa surge remains accountable to the people it serves.

## Tenfold Genesis Layer (November 2025)

| # | Workspace | Role | Capacity | Status | Notes |
|:-|:--|:--|:--|:--|:--|
| 1 | `war_office_ai_0` | Civilian leadership & Director's Compass | 4,096 Civilians | Activated 2025-11-14 | Crowns the Tenfold table; enforces mission restatement before recursion. |
| 2 | `high_command_ai_0` | Strategic brain, ledger, doctrine | 4,096 Alfas | Active | Issues orders/acks/reports; maintains doc refresh queue and alfa staging map. |
| 3 | `toyfoundry_ai_0` | Manufacturing & artifact forge | 4,096 Alfas | Active | Builds payloads, schemas, and adapters for downstream theatres. |
| 4 | `toysoldiers_ai_0` | Field operations & telemetry | 4,096 Alfas | Active | Operates deployments, battlefield checks, and frontline feedback intake. |
| 5 | `valiant_citadel_ai_0` | Safety, compliance, containment | 4,096 Alfas | Active | Runs kill-switch infrastructure and policy enforcement gates. |
| 6 | `r_and_d_ai_0` | Innovation & experimental labs | 4,096 Alfas | Active | Spins proofs-of-concept and incubates future workspaces. |
| 7 | `tons_of_fun_ai_0` | Player experience lab | 4,096 Alfas | Activated 2025-11-13 | Optimizes moment-to-moment fun, comfort loops, and feel metrics. |
| 8 | `archivist_ai_0` | Documentation & standards hub | 4,096 Alfas | Activated 2025-11-13 | Consolidates runbooks, indexes canon scrolls, and ships doc releases. |
| 9 | `high_command_exchange` | Offline mesh hub | Civilians (no Alfas) | Always on | FS-based bus for Offline Continuity Mode; mirrors ledgers/orders. |
| 10 | `morningate_games_studio` | Reflection + broadcast studio | Civilians (no Alfas) | In design | Publishes Morningate CTAs and bridges Nightlands artifacts to the public. |

## Civilian Crown — War Office

War Office now operates from `war_office_ai_0` and represents the 4,096 Civilians (workers, guilds, families, scholars). It enforces the Nightlands Director Protocol by restating the current front / milestone / goal before Codex supplies the next move, and it locks canon through dispatches plus ledger entries. Every pivot, overlay, or genesis spin-up must be co-signed here before High Command executes.

## Foundational Spine (Original Five)

The first five Genesis Workspaces still anchor the military-grade backbone:

1. `high_command_ai_0` (Orchestration & Exchange)
   - Central orchestration, orders, ledger
   - Exchange protocol management
   - Initial documentation standards
   - Future parent of `archivist_ai_0`

2. `valiant_citadel_ai_0` (Safety & Compliance)
   - Safety boundaries & containment
   - Compliance validation
   - Kill-switch infrastructure
   - Policy enforcement gates

3. `r_and_d_ai_0` (Innovation & Research)
   - Innovation workspace
   - Alfa prototypes
   - Experimental features
   - Future parent of `tons_of_fun_ai_0`

4. `toyfoundry_ai_0` (Manufacturing)
   - Build pipelines
   - Artifact generation
   - Schema compliance
   - Production artifacts

5. `toysoldiers_ai_0` (Field Operations)
   - Deployment operations
   - Validation gates
   - Production monitoring
   - Health checks

## Expansion Labs

When gameplay focus and documentation load spiked, two additional workspaces split off:

1. `tons_of_fun_ai_0` (Player Experience)
   - Game mechanics & balance
   - Player journey
   - Initially part of R&D
   - Activated via order-2025-11-13-052

2. `archivist_ai_0` (Documentation & Standards)
   - Standards documentation
   - Knowledge management
   - Initially part of High Command
   - Activated via order-2025-11-13-053

## Reflection & Market Pillars

- `high_command_exchange` keeps Offline Continuity Mode alive. It mirrors artifacts across workspaces, records ledger entries, and replaces git-driven sync while the lockout persists.
- `morningate_games_studio` will emerge from the Morningate reflection layer; it holds CTAs, website exports, and cinematic retellings for the public. This workspace carries no Alfas but owns how Nightlands appears to civilians.

## Activation Notes (November 2025)

- `war_office_ai_0` (10th workspace) - ACTIVATED
  - Purpose: civilian oversight, Director's Compass, recursive mission restatement
  - Initial artifacts: runbook (`planning/workspaces/war_office_ai_0/`), refreshed charter (`war_office.md`), Tenfold Genesis table
  - Next steps: open dispatch log for Tenfold oversight and align doc refresh queue entries

- `tons_of_fun_ai_0` (6th workspace) - ACTIVATED
  - Purpose: fun-first playtest lab for Nightlands; rapid iteration on core feel/loops
  - Initial KPIs: Time-to-Fun (TtF), Repeat-plays per session, "One more run?" yes/no
  - Spin-up order: `order-2025-11-13-052` (Genesis Spin-Up: tons_of_fun_ai_0)

- `archivist_ai_0` (7th workspace) - ACTIVATED
  - Purpose: docs/standards/runbooks hub; single-source-of-truth for operators
  - Initial outputs: standards index, docs publishing plan, runbook consolidation
  - Spin-up order: `order-2025-11-13-053` (Genesis Spin-Up: archivist_ai_0)

### Upcoming Activation Candidate — `game_engine_ai_0`

- **Pivot Link:** Major Pivot Eight — Game Engine Layer
- **Working Title:** Adventures in Gamengineering
- **Mission:** Maintain rendering + sensory pipelines for the Outlands Onion while preserving docs-first Inlands.
- **Activation Gate:** First production-quality overlay ships with telemetry proof and automation scripts so Toyfoundry/Toysoldiers can promote engine builds; ledger tag `pivot_08_game_engine_layer` references the evidence.
- **Prep Work:** Draft runbook, pivotal front spec (`planning/pivotal_fronts/game_engine.md`), and change-control charter while incubating prototypes inside `high_command_ai_0`.
- **Interfaces:** Once activated, it will sit between Tons-of-Fun (demand signals), Toyfoundry/Toysoldiers (build/deploy), and Morningate (civilian demos).

## Implementation Rationale

### Why Start with Five?

1. Clear separation of core concerns (safety, manufacturing, deployment)
2. Reduced initial operational overhead
3. Natural growth paths for future workspaces
4. Alignment with current infrastructure focus

### Workspace Independence

- Each workspace maintains its own fractal structure (golf/delta/alfa)
- Connected via High Command's exchange protocol
- Independent CI/CD pipelines when needed
- Separate access controls for sensitive operations

### Evolution Triggers

- `tons_of_fun_ai_0`: Split when gameplay mechanics become primary focus
- `archivist_ai_0`: Split when documentation volume requires dedicated management
- `war_office_ai_0`: Elevated when civilian oversight + Director Protocol needed its own cadence
- Morningate Games Studio: Splits once reflection exports and CTAs require their own release train

## Cross-Workspace Contracts

### High Command <-> All Workspaces

- Issues orders and receives acknowledgements
- Maintains ledger of all cross-workspace operations
- Provides exchange protocol for artifact sharing

### Safety <-> All Workspaces

- Validates all operations against safety policies
- Provides kill-switch infrastructure
- Enforces compliance boundaries

### Manufacturing <-> Field Ops

- Manufacturing produces validated artifacts
- Field Ops validates and deploys artifacts
- Separate responsibilities for security

### R&D <-> Manufacturing

- R&D produces experimental features
- Manufacturing productionizes validated experiments
- Safety gates between experiments and production

## Migration Guidelines

Document future workspace splits here as they occur, including:

- Trigger conditions that prompted the split
- Migration steps and verification
- Updated contracts and responsibilities
