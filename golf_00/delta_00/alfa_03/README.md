# Alfa_03 — Telemetry Shell (Stub)

Purpose: minimal entry point to exercise basic telemetry event logging during Order 044.

- Module: `golf_00.delta_00.alfa_03.telemetry_shell`
- CLI: `python -m golf_00.delta_00.alfa_03.telemetry_shell --event forge.craft --status success`
- Status: stub (prints JSON and can append JSONL with --out)

Next steps (044):
- Align fields with `quint_synced/payload_alignment.md` `telemetry_stub`.
- Add integration points once downstream consumers are ready.
