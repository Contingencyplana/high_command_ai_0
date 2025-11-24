# Offline Continuity Mode — Active

Use this folder as the staging area for artifacts that need to be published to the shared exchange.

Expected subfolders:

- `orders/`
- `reports/`

Populate those folders inside each workspace, then run `python tools/quint_sync.py --offline` from the workspace root to propagate the files into the central exchange.
