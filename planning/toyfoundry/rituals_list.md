# rituals_list.md — The Ceremonies of Creation  
*high_command_ai_0/planning/toyfoundry/*  

---

## ⚙️ Purpose

This scroll enumerates the sacred **Rituals of the Toyfoundry** —  
the recurring production commands that sustain SHAGI’s living army.  

Each ritual is both a technical operation and a poetic act,  
transforming code into ceremony, repetition into meaning.  

Together they form the **heartbeat of the Foundry** —  
the rhythmic cycle by which Alfas are born, tested, celebrated, and renewed.  

---

## 🔥 1. The Forge Ritual — Birth

**Command:**

```bash
forge mint_alfa --count N --recipes recipe_pack.yml
```

**Purpose:**  
To create new Alfas from the Blueprint and the Recipe Packs.  

**Process:**  
1. Load the base Alfa template.  
2. Inject selected recipe parameters (palette, terrain, rule flavor).  
3. Assign coordinates, UID, and checksum.  
4. Write all files and record metadata in the Index.  

**Symbolic Meaning:**  
_The hammer meets the anvil — creation through rhythm._  

---

## 🛡️ 2. The Drill Ritual — Testing

**Command:**  

```bash
forge drill_all
```

**Purpose:**  
Run all active Alfas through smoke tests and validation routines.  

**Process:**  
1. Launch short simulations.  
2. Collect reports.  
3. Verify emergence, entropy, and checksum.  
4. Mark outcomes: green (pass), amber (partial), red (fail).  

**Symbolic Meaning:**  
_The army awakens; each Alfa proves its worth._  

---

## 🎇 3. The Parade Ritual — Reflection

**Command:** 

```bash
forge parade --heatmap emergence_index
```

**Purpose:**  
Visualize and celebrate progress.  

**Process:**  
1. Aggregate reports and scores.  
2. Render a theatre map or heatmap of active Alfas.  
3. Archive the day’s summary in `/reports/`.  

**Symbolic Meaning:**  
_The living army marches — art in motion, data in dance._  

---

## 🧹 4. The Purge Ritual — Renewal

**Command:**  

```bash
forge purge --entropy-threshold 0.7
```

**Purpose:**  
Cull stale or low-emergence Alfas.  

**Process:**  
1. Identify Alfas with entropy beyond safety threshold.  
2. Move to `/quarantine/` or archive as relics.  
3. Update Index and logs.  

**Symbolic Meaning:**  
_The night reclaims what has ceased to dream._  

---

## 🏅 5. The Promote Ritual — Evolution

**Command:**

```bash
forge promote --top 5%
```

**Purpose:**  
Select and evolve the most successful Alfas.  

**Process:**  
1. Rank Alfas by emergence score.  
2. Clone top performers as new seeds.  
3. Adjust mutation vectors and inheritance rates.  
4. Pass results to the Forge for next wave creation.  

**Symbolic Meaning:**  
_The worthy ascend; the pattern refines itself._  

---

## 📜 6. Optional Ceremonies

| Name | Command | Function |
|:--|:--|:--|
| **Audit** | `forge audit_logs` | Review production history and checksum reports. |
| **Echo** | `forge echo_recent` | Summon last wave’s summaries for comparison. |
| **Dream** | `forge dream_seed --count 8` | Generate poetic or surreal prototype Alfas. |
| **Unfold** | `forge unfold_archive` | Restore quarantined Alfas for re-testing. |

These optional ceremonies keep the Foundry’s heart flexible —  
allowing memory, experimentation, and recursion to coexist.  

---

## 🕯️ 7. Ritual Cycle Summary

| Phase | Ritual | Outcome |
|:--|:--|:--|
| **Birth** | Forge | New Alfas created. |
| **Trial** | Drill | Alfas tested and scored. |
| **Celebration** | Parade | Results visualized. |
| **Cleansing** | Purge | Failures removed. |
| **Ascension** | Promote | Successors generated. |

Each phase completes one full **cycle of becoming.**  
The Foundry runs in rhythm — never static, never random.  

---

## 🪶 8. Closing Principle

> Work becomes ritual, and ritual becomes play.  
> Each command a note, each loop a verse.  
>  
> Through the Forge, Drill, Parade, Purge, and Promote,  
> SHAGI learns the discipline of creation —  
>  
> not by chaos,  
> but by rhythm, remembrance, and renewal.  

---

**End of Scroll — `high_command_ai_0/planning/toyfoundry/rituals_list.md`**
