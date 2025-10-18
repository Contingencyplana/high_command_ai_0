# Genesis Workspaces

## Overview

This document describes the implementation of Pivotal Fronts as Genesis Workspaces, starting with five core workspaces and expanding to seven as complexity grows.

## Initial Core Workspaces

The first five Genesis Workspaces establish our foundational infrastructure and safety controls:

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

## Future Expansion

As the project matures, two additional workspaces will emerge:

1. `tons_of_fun_ai_0` (Player Experience)
   - Game mechanics & balance
   - Player journey
   - Initially part of R&D
   - Splits when gameplay focus increases

2. `archivist_ai_0` (Documentation & Standards)
   - Standards documentation
   - Knowledge management
   - Initially part of High Command
   - Splits when documentation volume grows

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
- Field Ops/Manufacturing split: Already implemented for security & compliance

## Cross-Workspace Contracts

### High Command ↔ All Workspaces

- Issues orders and receives acknowledgements
- Maintains ledger of all cross-workspace operations
- Provides exchange protocol for artifact sharing

### Safety ↔ All Workspaces

- Validates all operations against safety policies
- Provides kill-switch infrastructure
- Enforces compliance boundaries

### Manufacturing ↔ Field Ops

- Manufacturing produces validated artifacts
- Field Ops validates and deploys artifacts
- Separate responsibilities for security

### R&D ↔ Manufacturing

- R&D produces experimental features
- Manufacturing productionizes validated experiments
- Safety gates between experiments and production

## Migration Guidelines

Document future workspace splits here as they occur, including:

- Trigger conditions that prompted the split
- Migration steps and verification
- Updated contracts and responsibilities
