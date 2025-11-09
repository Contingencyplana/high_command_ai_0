# Outlands Framework (Pivot Seven)

Purpose: Define how outer overlays (Lore, Music, Ritual, emergent Outlands) attach to the emoji grid and exchange bus without changing core schemas.

- Attachment points
  - Grid: cell selection, zone hooks, battle-state adapters
  - Exchange: factory-order extensions, evidence tagging, comfort metadata
- Non-destructive principle: overlays wrap; core emoji-runtime/factory-order remain unchanged
- Minimal API surface
  - overlay_id, layer_kind (lore|music|ritual|emergent), enable/disable, evidence sinks
- Evidence
  - Trace JSONL locations, ledger tags, contract cases (when applicable)

Next steps
- Draft overlay_id conventions and evidence schema
- Provide sample Lore + Music layer adapters
