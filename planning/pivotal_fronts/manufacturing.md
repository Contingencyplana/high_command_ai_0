# Manufacturing Front (Toyfoundry)

Mission
- Mint and upgrade builds safely; emit telemetry; ship artifacts with checksums and build info.

Core Docs
- Toyfoundry overview: `planning/toyfoundry/toyfoundry.md:1`
- Forge automation spec: `planning/forge_automation_spec.md:1`
- Telemetry export schema: `planning/toyfoundry/telemetry/export_schema.md:1`

Artifacts
- composite_export.csv/json, build_info.json, .sha256 files
- Required metadata (Order 025): owner, timestamp, approvers (protected), build_info, checksums

Interfaces
- Exchange reports (factory-report@1.0)
- Orders (manufacturing runs, canary/standard)
