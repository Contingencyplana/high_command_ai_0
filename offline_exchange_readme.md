# Offline Exchange Protocol (Genesis Mesh)

This workspace is linked to the shared high_command_exchange bus.

Run from workspace root:
    python tools/offline_sync_exchange.py

The shared hub is defined by SHAGI_EXCHANGE_PATH or tools/offline_exchange_config.json.

Folders synced:
- outbox/orders → high_command_exchange/orders
- outbox/reports → high_command_exchange/reports

Ledger of all events:
C:/Users/Admin/high_command_exchange/ledger/2025-10.md
