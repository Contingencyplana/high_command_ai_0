# Field Ops Front (Toysoldiers)

Mission
- Ingest and validate producer exports; enforce schema + DQ; set consumer acceptance.

Core Docs
- Field workspaces: `planning/field_workspaces.md:1`
- Command Exchange Protocol: `planning/command_exchange_protocol.md:1`
- Safety Gate Template: `planning/templates/safety_gate_template.md:1`

Checks
- non_empty, allowed_enums, positive/valid ranges, schema version
- Required metadata (Order 025): owner, timestamp, approvers (protected)

Interfaces
- Reports (consumer acceptance), monitoring notes, alerting
