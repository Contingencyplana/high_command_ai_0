# Hybrid Communications Restore (Mini-Campaign)

**Objective:** Restore hybrid/online channel parity, re-establish canonical smoke (factory_order_emitter), and ensure docs/ledger reflect the lifted block.

## Plan
- Confirm War Office scope: what online operations are permitted (push/pull), any rate limits, schema changes, or attachment constraints.
- Run hybrid smoke (once allowed):
  - `python tools/exchange_heartbeat.py` (online path)
  - `python tools/offline_sync_exchange.py`
  - `python -m tools.ops_readiness`
  - `python tools/exchange_all.py`
- Verify emitter-based smoke everywhere:
  - `python tools/factory_order_emitter.py --help` (installed 2025-11-22 from War Office)
  - Swap any remaining readiness stubs off `exchange_all` back to emitter.
- Update docs/ledger:
  - Add hybrid-restore note to `exchange/ledger/2025-11.md` once smoke passes.
  - Refresh `planning/document_refresh_queue.md` with the completed hybrid restore slice.
  - Confirm `planning/batch2_closeout.md` remains accurate (emitter restored).

## Exit Criteria
- Hybrid channel confirmed available (heartbeat/validator clean after online-allowed run).
- Emitter is the canonical smoke across workspaces; no “exchange_all smoke” caveats left.
- Ledger/doc updates captured; validator clean.
