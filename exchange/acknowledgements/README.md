# Acknowledgements (ACKs)

Purpose
- Standardize how field workspaces acknowledge and accept orders.
- Provide a lightweight record of ownership, intent, and initial plan.

When to ACK
- ACK is required when an order has `requires_ack: true`.
- Create the ACK promptly after pickup and before starting work.

Where files live
- Templates: `exchange/acknowledgements/templates/`
- Logged ACKs: `exchange/acknowledgements/logged/`
- Naming: `order-<ORDER_ID>-ack.json` (e.g., `order-2025-10-14-010-ack.json`)

How to use a template
1) Copy the relevant template from `exchange/acknowledgements/templates/`.
2) Replace placeholders (`<...>`) with real values.
3) Set `timestamp_ack` to UTC ISO‑8601 (e.g., `2025-10-14T10:32:00Z`).
4) Fill `initial_approach` with concrete paths and plan.
5) Add any known risks and the next events you will take.
6) Save to `exchange/acknowledgements/logged/order-<ORDER_ID>-ack.json`.

Required fields
- `schema`: must be `factory-ack@1.0`
- `order_id`: exactly matches the order JSON
- `workspace`, `acknowledged_by`, `owner`: your workspace name
- `timestamp_ack`: ISO‑8601 UTC
- `status`: `accepted` (or `declined` with reason)
- `initial_approach`: include key paths (schemas, exports, provenance)
- `risks`: known risks
- `next_events`: your immediate follow‑ups

Checksums (SHA256)
- Compute a SHA256 per artifact and include in the ACK under `initial_approach.checksums`.
- PowerShell example:
  - `Get-FileHash -Algorithm SHA256 ".toyfoundry/telemetry/quilt/exports/composite_export.json" | Select-Object Hash`

Quick example (trimmed)
```
{
  "schema": "factory-ack@1.0",
  "order_id": "order-2025-10-14-010",
  "workspace": "toyfoundry_ai_0",
  "acknowledged_by": "toyfoundry_ai_0",
  "owner": "toyfoundry_ai_0",
  "timestamp_ack": "2025-10-14T10:35:00Z",
  "status": "accepted",
  "initial_approach": {
    "export_schema_path": "planning/toyfoundry/telemetry/export_schema.md",
    "exports": {
      "json": ".toyfoundry/telemetry/quilt/exports/composite_export.json",
      "csv": ".toyfoundry/telemetry/quilt/exports/composite_export.csv"
    },
    "build_info_path": ".toyfoundry/telemetry/quilt/exports/build_info.json",
    "checksums": [
      { "path": ".toyfoundry/telemetry/quilt/exports/composite_export.json", "sha256": "<HASH>" }
    ],
    "sample_excerpt_path": ".toyfoundry/telemetry/quilt/exports/sample_10_rows.csv"
  },
  "risks": ["Schema drift"],
  "next_events": ["Share paths with High Command"]
}
```

Lifecycle tie‑in
- Typical flow: pending → dispatched → in_progress → completed.
- Posting an ACK signals start of work and ownership; High Command may then move the order to `in_progress`.

Validation tips
- JSON validity (PowerShell): `Get-Content -Raw <ack.json> | ConvertFrom-Json | Out-Null`
- Ensure paths resolve in your repository before submitting.

Contact
- Questions or improvements: coordinate with High Command / War Office.
