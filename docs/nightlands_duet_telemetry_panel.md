# Nightlands Duet Telemetry Panel (Order 051)

## Goal

Provide a lightweight offline panel that correlates Nightlands duet storyboard runs with Alfa Zero targeted sync executions while the full dashboard tooling remains offline.

## Data Source

- Feed: `exchange/attachments/telemetry/nightlands_duet/nightlands_duet_storyboard_sync_feed.jsonl`
- Each record is appended by `alfa_zero_ui` when a duet storyboard completes or the targeted sync helper runs.

## Schema & Companion Artefacts

- Schema and field notes live in `exchange/attachments/telemetry/nightlands_duet/nightlands_duet_telemetry_manifest.md`; consult it before extending the feed or when onboarding new dashboards.
- `planning/alfa_zero_nightlands_duet_storyboard.md` records how crews should reference the feed, scoreboard composites, and targeted sync cadence inside the duet playbook.
- For imagery/context, mirror `exchange/attachments/guides/nightlands_duet_playtest_packet.md` so cohorts have the scoreboard excerpts that pair with this telemetry.

## Quick Cadence Snapshot

Run the following one-liner to summarise storyboard runs and targeted sync activity by hour:

```pwsh
python - <<'PY'
from collections import Counter
import json
from pathlib import Path
feed = Path('exchange/attachments/telemetry/nightlands_duet/nightlands_duet_storyboard_sync_feed.jsonl')
rows = [json.loads(line) for line in feed.read_text(encoding='utf-8').splitlines() if line.strip()]
by_kind = Counter()
for row in rows:
    timestamp = row.get('timestamp')
    bucket = timestamp[:13] if isinstance(timestamp, str) and len(timestamp) >= 13 else 'unknown'
    by_kind[(bucket, row.get('event'))] += 1
print('Hour'.ljust(18), 'Event'.ljust(16), 'Count')
print('-' * 42)
for (bucket, event), count in sorted(by_kind.items()):
    print(bucket.ljust(18), str(event).ljust(16), count)
PY
```

### Example Output

```text
Hour               Event            Count
------------------------------------------
2025-11-12T00      storyboard_run   1
```

### Latest Pair Sanity Check

Use this helper to print the newest storyboard + targeted sync entries so you can confirm they landed before publishing a debrief:

```pwsh
python - <<'PY'
import json
from pathlib import Path
feed = Path('exchange/attachments/telemetry/nightlands_duet/nightlands_duet_storyboard_sync_feed.jsonl')
rows = [json.loads(line) for line in feed.read_text(encoding='utf-8').splitlines() if line.strip()]
for row in rows[-4:]:
    print(f"{row.get('timestamp')}  {row.get('event'):>14}  {row.get('trace_id') or row.get('summary_line')}")
PY
```

## Manual Checklist for Cohorts

1. After running the duet storyboard, execute the targeted sync helper (`sync latest` inside Alfa Zero UI).
2. Re-run the snapshot command (or the pair sanity check) above to confirm the feed reflects both the storyboard and the sync.
3. If data looks off, inspect the manifest (`nightlands_duet_telemetry_manifest.md`) to ensure new fields were added correctly before re-running the helper.
4. Capture the ASCII snapshot and include it in the session log or debrief packet if new cadence data surfaces.

## Next Evolution

- When the offline dashboard toolkit comes back online, swap this quick script into the telemetry notebook to render a proper cadence chart.
- Extend the parser to show cooldown deltas once additional runs populate the feed.
