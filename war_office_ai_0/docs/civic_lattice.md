# Civic Lattice — 4,096 Civilians

War Office mirrors the Officers Pyramid but uses civilian nomenclature so the 4,096 Civilians remain distinct from the military metaphor. Each level divides into sixteen sublevels, forming the same 16×16×16 geometry that drives Alfa deployments.

| Civic Tier | Symbol | Scale | Military Analog | Purpose |
|:--|:--|:--|:--|:--|
| **Commonwealth** | CW | 64×64 (4,096 slots) | Juliett | Entire civilian consciousness; crowns the Tenfold layer. |
| **Prefecture** | PF | 64×32 (2,048 slots) | India | Half-theatres that watch specific halves of the lattice. |
| **Province** | PR | 32×32 (1,024 slots) | Hotel | Major civic provinces or specialist bureaus. |
| **Guild** | GD | 16×16 (256 slots) | Golf | Paired with individual workspaces (High Command, Toyfoundry, etc.). |
| **Quarter** | QT | 16×8 (128 slots) | Foxtrot | Border guilds managing liminal contexts (Outlands, rituals). |
| **District** | DT | 8×8 (64 slots) | Echo | Deep-focus civilian cohorts (telemetry, lore, comfort). |
| **House** | HS | 4×4 (16 slots) | Delta | Families/crews that maintain rituals and dispatch cadence. |
| **Chorus** | CH | 4×2 (8 slots) | Charlie | Voice clusters for simultaneous narrations. |
| **Cell** | CL | 2×2 (4 slots) | Bravo | Micro-teams for experiments or rapid decisions. |
| **Citizen** | CZ | 1×1 (1 slot) | Alfa | Individual civilian mind-battle slot (one playable idea or guardian).

## Folder Scheme
```
war_office_ai_0/civic_lattice/commonwealth/
  guild_00/
    house_00/
      citizen_000000.md
      ... citizen_00000f.md
    ...
  ... guild_0f/
```

- Guild index (`00`-`0f`) maps to paired workspaces (see `docs/tenfold_mapping.md`).
- House index (`00`-`0f`) captures district/household responsibilities.
- Citizen index (`000000`-`0f0f0f`) encodes guild + house + cell for ledger tracking.

## Slot Ledger Fields
Each citizen file contains:
- `civ_id` — hex-coded slot (e.g., `civ-0a0d03`).
- `guild`, `house`, `cell` references.
- `aspect` (love/light/safety/sanity/play).
- `paired_workspace` or focus area.
- `status` (active/resting/honored).
- `missions` log (front, milestone, goal, ledger trace).

Use `python tools/civic_slot_report.py` to aggregate fill-state and export ledger snapshots.
