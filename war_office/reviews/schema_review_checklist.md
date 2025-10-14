# Schema Review Checklist — Composite Telemetry Quilt

Purpose: Ensure downstream consumers can reliably ingest telemetry exports without privacy or compatibility issues.

Reviewer roles: toyfoundry_ai_0 (producer), toysoldiers_ai_0 (consumer), High Command (sign-off).

- Contract basics
  - [ ] File formats provided (JSON, CSV) and sample rows/objects included
  - [ ] JSON Schema or equivalent specification available and versioned
  - [ ] Schema version noted in artifacts and docs

- Fields and semantics
  - [ ] Each field documented: name, type, units, allowed values, nullability
  - [ ] Timestamps include timezone/offset and format documented (ISO-8601 preferred)
  - [ ] IDs have defined uniqueness and scope; join keys documented
  - [ ] Derived fields include lineage and formulas

- Privacy and safety
  - [ ] No PII or sensitive data present; redaction/aggregation applied where needed
  - [ ] Minimum-necessary data principle observed
  - [ ] Sensitivity label and retention policy documented

- Quality and stability
  - [ ] Deterministic generation; stable field ordering and naming
  - [ ] Backward compatibility plan; deprecation policy for breaking changes
  - [ ] Null/default handling documented for missing/unknown values

- Provenance and freshness
  - [ ] build_info present (commit, generation time, parameters)
  - [ ] Checksums provided for artifacts
  - [ ] Cadence/SLA documented; timestamps per record or batch

- Validation
  - [ ] Sample export validates against JSON Schema
  - [ ] Consumer ingestion test passes end-to-end
  - [ ] README includes CLI usage and expected workflow

