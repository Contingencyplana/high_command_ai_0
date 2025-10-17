# 🚨 SCHEMA DRIFT SITUATION REPORT
**Classification:** CRITICAL  
**Date:** 2025-10-18  
**Reported By:** Toysoldiers Field Ops (via Orders 021/029/031)  
**Reviewed By:** High Command

---

## Executive Summary

**Consumer acceptance gates have BLOCKED all Toyfoundry export validation** due to critical schema drift between Order 021 specification and actual Toyfoundry export implementation.

**Status:** ⛔ **BLOCKING** — All downstream consumers (Toysoldiers, analytics, monitoring) cannot accept Toyfoundry data until schema alignment resolved.

**Good News:** 🛡️ Validation gates worked perfectly — they detected and prevented corrupted data from entering production systems.

---

## The Problem

### Order 021 Expected Schema (v1.0)
```json
{
  "batch_id": "string",
  "ritual": "forge|parade|purge|promote",
  "units_processed": "integer",
  "status": "success|failure|partial",
  "duration_ms": "integer"
}
```

### Toyfoundry Actual Export Schema
```json
{
  "operation_id": "string",
  "mint_name": "string",
  "ritual": "string",
  "event_status": "string",
  "event_metadata": {
    "batch_id": "string",
    // nested structure
  },
  "mint_runs": "integer",
  "ritual_completed": "boolean"
  // ... additional fields
}
```

### Impact
- ❌ **Order 021** (standard run validation): BLOCKED
- ❌ **Order 029** (canary C1 validation): BLOCKED  
- ❌ **Order 031** (canary B1/B2 validation): BLOCKED
- ❌ **All 3 validation orders** cannot proceed until schema aligned

### Additional Issues
- **SHA256 checksums stale** — Exports regenerated after manifest creation
- **No schema version field** — Cannot auto-detect version for backward compatibility
- **DQ thresholds incompatible** — Validation logic designed for expected schema structure

---

## Root Cause Analysis

**Hypothesis:** Toyfoundry and High Command evolved export schemas independently without coordination.

**Evidence:**
1. Order 021 issued 2025-10-15 with schema v1.0 specification
2. Toyfoundry exports use different schema (likely evolved from earlier version)
3. No schema versioning mechanism to detect/handle multiple versions
4. No integration tests between Toyfoundry (producer) and Toysoldiers (consumer)

**Contributing Factors:**
- Lack of canonical schema registry
- No contract testing between workspaces
- Schema changes not communicated via exchange protocol

---

## Remediation Options

### Option 1: Update Toyfoundry Exports (Recommended)
**Change Toyfoundry to emit Order 021-compliant schema**

**Pros:**
- ✅ Order 021 spec is well-documented and explicit
- ✅ Consumer expectations already built (validation logic exists)
- ✅ Aligns producer with consumer contract
- ✅ Future consumers can rely on stable schema

**Cons:**
- ❌ Requires Toyfoundry code changes
- ❌ May break other consumers if they exist
- ❌ Need to validate no upstream dependencies on current schema

**Implementation:**
1. High Command issues corrective order to Toyfoundry
2. Toyfoundry updates export generation logic to match v1.0 spec
3. Toyfoundry adds `schema_version: "1.0"` field to all exports
4. Toyfoundry regenerates SHA256 checksums after schema fix
5. Toysoldiers re-runs validation orders
6. Estimated timeline: 2-3 days

---

### Option 2: Update Toysoldiers Validation
**Change validation logic to accept Toyfoundry's actual schema**

**Pros:**
- ✅ Faster implementation (Toysoldiers local change)
- ✅ No coordination with Toyfoundry required
- ✅ Accepts "truth on the ground" implementation

**Cons:**
- ❌ Order 021 spec becomes incorrect/misleading
- ❌ Future consumers may build against wrong spec
- ❌ Perpetuates undocumented schema drift
- ❌ Validation logic becomes more complex (field mapping)

**Implementation:**
1. Update `tools/validate_order_021.py` to accept actual schema
2. Add field mapping layer (operation_id → batch_id, etc.)
3. Update Order 021 spec documentation to match reality
4. Re-run validation orders
5. Estimated timeline: 1 day

---

### Option 3: Schema Versioning Framework (Long-term)
**Implement proper schema versioning and contract testing**

**Pros:**
- ✅ Future-proof: handles schema evolution gracefully
- ✅ Multiple schema versions can coexist
- ✅ Consumers auto-detect and adapt
- ✅ Producer/consumer contract testing prevents future drift

**Cons:**
- ❌ Significant engineering investment
- ❌ Requires changes across all workspaces
- ❌ Doesn't solve immediate blocking issue

**Implementation:**
1. Create canonical schema registry in exchange/schemas/
2. Add schema_version field to all exports
3. Build validation library that supports multiple versions
4. Implement contract tests (producer → consumer)
5. Establish schema change governance process
6. Estimated timeline: 1-2 weeks (doesn't unblock current crisis)

---

## High Command Decision Required

**Recommended Immediate Action:** **Option 1** (Update Toyfoundry)

**Rationale:**
- Order 021 spec is explicit and well-documented
- Producer should honor consumer contract
- Sets precedent for schema governance
- Cleanest long-term solution

**Recommended Follow-up:** **Option 3** (Schema Versioning Framework)

**Rationale:**
- Prevents recurrence of this issue
- Essential for scaling to multiple consumers
- Aligns with SHAGI safety/quality gates philosophy

---

## Proposed Corrective Order

**High Command should issue:**

**Order-2025-10-18-036: Align Toyfoundry Export Schema**

**Target:** `toyfoundry_ai_0`  
**Priority:** `critical`  
**Expires:** 2025-10-25

**Directives:**
1. Update export generation to match Order 021 schema v1.0 specification
2. Add `schema_version: "1.0"` field to all export JSONs
3. Regenerate SHA256 checksums in export_manifest.json
4. Validate schema compliance using provided schema validator
5. Re-export all batches (standard + canary C1/B1/B2)
6. Submit completion report with sample exports for verification

**Success Criteria:**
- All exports contain Order 021-specified fields
- SHA256 checksums validate correctly
- Toysoldiers validation orders can be re-run successfully

---

## Lessons Learned

1. **Schema changes require coordination** — Producer/consumer must align via exchange protocol
2. **Integration tests needed** — Catch schema drift before production
3. **Version all schemas** — Enable graceful evolution and backward compatibility
4. **Contract testing essential** — Automated validation of producer/consumer contracts
5. **Validation gates work!** — Toysoldiers consumer gates successfully prevented bad data propagation 🛡️

---

## Supporting Documents

- **Blocked Orders:** 021, 029, 031
- **Field Reports:** `exchange/reports/archived/order-2025-10-15-021-report.json` (detailed schema diff)
- **Validation Tool:** `toysoldiers_ai_0/tools/validate_order_021.py`
- **Export Samples:** `toysoldiers_ai_0/.imports/toyfoundry/telemetry/quilt/exports/`

---

## Status

**Current State:** ⛔ BLOCKED — Awaiting High Command decision  
**Next Action:** Issue corrective order to Toyfoundry (Option 1)  
**Watchlist:** Monitor for similar schema drift in other workspace integrations

---

*End of Situation Report*  
*Classification: CRITICAL | Distribution: War Office, All Fronts*
