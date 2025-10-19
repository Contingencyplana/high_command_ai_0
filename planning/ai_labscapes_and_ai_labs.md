# 🧪 ai_labscapes_and_ai_labs.md — AI Labscapes & Labs Guide  
*Frontline Handbook — `high_command_ai_0/planning/`*
---
## 🌍 Purpose
Defines the AI Labscape and its Labs so squads share a clear model of how hypotheses, prototypes, and field drills interlock across the lattice (Alfa → Juliett). Complements battlefield and war‑room guides without duplicating them.
---
## 📚 Core Definitions
- AI Lab (Alfa): A 1×1 cell running a concrete hypothesis as a playable micro‑experiment (code + config + telemetry).
- AI Labscape: A themed collection of Labs arranged on the lattice (e.g., Golf 16×16 = 256; Juliett 64×64 = 4,096).
- Battlefield (Field Alfa): A Lab oriented to action/emergence under live drills (see `planning/field_workspaces.md`).
- War‑Room (HQ Alfa): A Lab oriented to deliberation/doctrine drafting (see `planning/high_command.md`).
- Mind/Dreamscapes: Concept terrains that inspire Lab design (see `planning/mindscapes_and_dreamscapes.md`).
---
## 🧭 Labscape Geometry
- Alfa: 1×1 — single Lab.
- Golf: 16×16 = 256 Labs — pilot scale for stable loops.
- Four Golfs: ~1,000 Labs — diversified pilots and comparative trials.
- Juliett: 64×64 = 4,096 Labs — full lattice for emergent behaviors.
- Mirrors doctrine: “Alfa 1×1 up to Juliett 64×64” and Phase 3 targets (4,096).
---
## 🔄 Lab Lifecycle (Hypothesis → Archive)
1. Hypothesis: Question, risks, expected signals, exit criteria.
2. Prototype: Mint via Toyfoundry Forge rituals; record build info and manifests.
3. Drill/Trial: Run in field cadence; emit structured telemetry.
4. Roll‑Up: Quilt telemetry into composite exports for review.
5. Deliberation: R&D war‑tables evaluate efficacy, tone, and safety.
6. Decision: Promote, iterate, quarantine (Nightland), or archive with provenance.

Required Metadata (Order 025)\n- owner (id, type=human|ai|service, workspace)\n- timestamp (ISO 8601 UTC)\n- approvers for protected actions (dual‑key: VisionHolder + SafetyLead)\n- uild_info.json (commit, generated_at, params)\n- Checksums (SHA256) for published artifacts\n\n---
## 🧵 Interfaces & Telemetry
- Manufacturing: Use Toyfoundry Forge to mint/upgrade Labs (see `planning/toyfoundry/` scrolls).
- Telemetry: Emit Alfa reports and composite quilt exports (e.g., `.imports/toyfoundry/telemetry/quilt/exports/samples/composite_export.sample.csv`).
- Governance: Route decisions through R&D War‑Tables and the rank structure.
---
## 👥 Roles
- Scientist: Frames hypotheses and evaluation criteria.
- Engineer: Implements prototypes and automation hooks.
- Safety Officer: Rates risk, watches tone/entropy; guards Nightland edges.
- Archivist: Maintains provenance, schemas, reproducibility.
- Squad (Toysoldiers): Exercises the experiment under live cadence.
---
## 🚀 Phased Growth Path
- Phase 1 — 256 Labs: Establish safe loops and reporting.
- Phase 2 — ~1,000 Labs: Diversify trials; compare families and doctrines.
- Phase 3 — 4,096 Labs: Full lattice; enable networked emergence with safeguards.
---
## 🌄 Field Maxim
> Keep the Labscape reproducible and the Labs speaking; emergence stays safe and legible across the lattice.
See Also\n- Safety Gate Template: planning/templates/safety_gate_template.md:1\n- AI Agents and Safety: planning/ai_agents_and_safety.md:1\n- Change-as-Order template (for promotions): exchange/orders/templates/change-order.template.json:1\n\n*End of Scroll - ai_labscapes_and_ai_labs.md*\n
