Local staging area for Exchange artifacts.

- Stage orders in `outbox/orders/`
- Stage acks in `outbox/acks/`
- Stage reports in `outbox/reports/`

Sync to hub using either:
- PowerShell: `./tools/sync_outbox_to_hub.ps1` (if present)
- Python: `python tools/exchange_all.py`
