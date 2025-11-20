# **Stage 2 — Azure Cloud Readiness**

**Four Stages Doctrine · High Command**

**Status:** Draft Active
**Purpose:** Define the safety threshold and operational gates for migrating Nightlands systems to Azure Cloud.
**Scope:** All ten genesis workspaces.

---

## **1. Mission**

Stage 2 authorizes the first controlled move of the system into **Azure Cloud**, but only after each genesis workspace achieves:

### **Two Deltas (32 Alfas)**

This stage shifts the system from:

* local-only operations
  → **hybrid local/cloud execution**,
  while preserving strict control over embodiment and battlegrid access.

Azure Cloud is *infrastructure*, not *gameplay* — no embodied Alfas are permitted yet.

---

## **2. Why Two Deltas?**

A single Delta (16 Alfas) gives:

* redundancy
* consistency
* fault detection
* basic behavior stability

But **cloud execution introduces new risks**, including:

* cross-workspace latency races
* network partitions
* distributed state disagreement
* deployment drift
* parallel update cascades

Two Deltas (32 Alfas) per workspace provide:

### **1. Independent cross-checking clusters**

Two clusters can verify each other’s outputs and behaviors.

### **2. Small-scale emergence detection**

Cloud environments amplify subtle patterns — this catches them early.

### **3. Stable telemetry for cloud workloads**

Patterns become statistically meaningful instead of noisy.

### **4. Multi-path resilience**

If one Delta drifts or malfunctions, its sibling can quarantine, flag, or halt operations.

This is the minimum safe threshold before cloud operations.

---

## **3. What Changes in Stage 2?**

### **Allowed**

* Deployment of Nightlands infrastructure to Azure Cloud
* Running core workflows in hybrid local/cloud
* Enabling telemetry export to Azure storage
* Beginning resource scaling models
* Using cloud compute for Codex hydration (non-embodied)

### **Not Allowed**

* No battlegrid embodiment
* No UI-level play
* No rituals triggered by cloud-executing Alfas
* No distributed simulations
* No Outlands Onion overlays tied to cloud compute
* No multiplayer interactions

### **Summary:**

**Cloud is permitted. Gameplay is not.**

---

## **4. Mandatory Requirements for Stage 2 Activation**

Before the system may begin cloud deployment:

### **Per Workspace Requirements**

* **✔ Two Deltas (32 Alfas)**
* **✔ All 32 Alfas documented in Toyfoundry metadata**
* **✔ Toysoldiers run ops checks**
* **✔ Valiant Citadel certification of cloud safety plan**
* **✔ High Command ledger entries completed and verified**

### **Infrastructure Requirements**

* **✔ Azure resource groups pre-configured**
* **✔ Telemetry Quilt ready to extend to cloud logs**
* **✔ Offline Sync + Cloud Sync fully reconciled**
* **✔ No drift between local and cloud runtime schemas**

### **Codex Requirements**

* **✔ Codex-only generation still in effect**
* Embodiment remains forbidden.

---

## **5. Stage 2 Rules of Operation**

1. **Codex Generation Only**
   No Alfa may be created or executed natively in cloud runtime environments.

2. **Mirrored Runtime**
   Cloud code must always mirror local code; local is the source of truth.

3. **No Autonomous Execution**
   Cloud Alfas cannot trigger self-initiation loops.

4. **Telemetry Enforcement**
   Every cloud action must produce logs consumable by the Telemetry Quilt.

5. **Deployment Discipline**
   All cloud deployments must pass Toyfoundry contract validation.

6. **Manual Override Always Available**
   Cloud operations must remain interruptible by a human operator.

---

## **6. Transition Criteria to Stage 3**

Stage 2 concludes when:

* cloud execution is stable
* drift is under control
* cloud telemetry matches local telemetry
* two Deltas per workspace show consistent behavior
* operators report no unexpected emergent properties
* Codex hydration pipelines work reliably in cloud compute

Only then may High Command authorize Stage 3:

### **Stage 3 — Internal Testers**

(Requires one Echo per workspace = 64 Alfas.)

---

## **7. Summary**

Stage 2 introduces Nightlands to Azure Cloud safely by requiring:

* **Two Deltas per workspace (32 Alfas)**
* **No embodiment**
* **Strict contract verification**
* **Telemetric proof**
* **Human override**

This is the cloud-readiness threshold.
It ensures the system is distributed, stable, and verifiable — before any human testers enter the picture.

---
