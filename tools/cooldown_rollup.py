"""Generate a weekly ritual cooldown rollup.

Reads telemetry JSONL records (from the alfa_03 telemetry shell by default),
computes a simple exponential moving average with a seven day half-life, and
writes a Markdown status report into the planning folder.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable

DEFAULT_SOURCES = [Path("logs") / "alfa_03" / "telemetry.jsonl"]
HALF_LIFE_DAYS = 7.0
SECONDS_PER_DAY = 86_400


@dataclass
class MetricAccumulator:
    name: str
    total_all: float = 0.0
    total_window: float = 0.0
    count_all: int = 0
    count_window: int = 0
    ema: float | None = None
    ema_timestamp: datetime | None = None
    latest_value: float | None = None
    latest_ts: datetime | None = None

    def update(self, value: float, timestamp: datetime, *, in_window: bool) -> None:
        self.total_all += value
        self.count_all += 1
        if in_window:
            self.total_window += value
            self.count_window += 1
        self.latest_value = value
        self.latest_ts = timestamp
        if self.ema is None or self.ema_timestamp is None:
            self.ema = value
            self.ema_timestamp = timestamp
            return
        delta_seconds = max((timestamp - self.ema_timestamp).total_seconds(), 0.0)
        if delta_seconds == 0:
            blending = 1.0 - math.pow(0.5, 1.0 / HALF_LIFE_DAYS)
        else:
            blending = 1.0 - math.pow(0.5, delta_seconds / (HALF_LIFE_DAYS * SECONDS_PER_DAY))
        self.ema = (1.0 - blending) * self.ema + blending * value
        self.ema_timestamp = timestamp

    def as_markdown_row(self, window_days: float) -> str:
        window_avg = self.total_window / self.count_window if self.count_window else 0.0
        ema_value = self.ema if self.ema is not None else 0.0
        latest_display = "-"
        if self.latest_value is not None and self.latest_ts is not None:
            latest_display = f"{self.latest_value:.2f} ({self.latest_ts.date().isoformat()})"
        return (
            f"| {self.name} | {self.total_window:.2f} | {window_avg:.2f} | "
            f"{ema_value:.2f} | {latest_display} |"
        )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate ritual cooldown rollup")
    parser.add_argument(
        "--source",
        action="append",
        type=Path,
        help="Telemetry JSONL file to include (default logs/alfa_03/telemetry.jsonl)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("planning"),
        help="Directory to write the Markdown rollup into (default planning/)",
    )
    parser.add_argument(
        "--window-days",
        type=float,
        default=HALF_LIFE_DAYS,
        help="Rolling window in days for totals/averages (default 7)",
    )
    return parser.parse_args()


def _read_records(paths: Iterable[Path]) -> list[dict]:
    records: list[dict] = []
    for path in paths:
        if not path.exists():
            continue
        try:
            with path.open("r", encoding="utf-8") as handle:
                for line in handle:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        record = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if isinstance(record, dict):
                        records.append(record)
        except OSError:
            continue
    return records


def _parse_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def _collect_metrics(records: list[dict], window_days: float) -> tuple[dict[str, MetricAccumulator], list[dict]]:
    metrics = {
        "activation_count": MetricAccumulator("activation_count"),
        "active_minutes": MetricAccumulator("active_minutes"),
        "unique_operators": MetricAccumulator("unique_operators"),
    }
    if not records:
        return metrics, []
    timestamps = [_parse_timestamp(record.get("ts")) for record in records]
    valid_timestamps = [stamp for stamp in timestamps if stamp is not None]
    now = max(valid_timestamps, default=datetime.now(timezone.utc))
    window_start = now - timedelta(days=window_days)

    ordered_entries: list[tuple[datetime, dict]] = []
    for record in records:
        timestamp = _parse_timestamp(record.get("ts"))
        if timestamp is None:
            continue
        ordered_entries.append((timestamp, record))

    ordered_entries.sort(key=lambda item: item[0])
    parsed_records = [record for _, record in ordered_entries]

    for timestamp, record in ordered_entries:
        in_window = timestamp >= window_start
        for field, accumulator in metrics.items():
            raw = record.get(field)
            if raw is None:
                continue
            try:
                value = float(raw)
            except (TypeError, ValueError):
                continue
            accumulator.update(value, timestamp, in_window=in_window)
    return metrics, parsed_records


def _render_report(
    metrics: dict[str, MetricAccumulator],
    records: list[dict],
    sources: list[Path],
    window_days: float,
) -> str:
    timestamp = datetime.now(timezone.utc)
    header = (
        f"# Ritual Cooldown Weekly Rollup — {timestamp.date().isoformat()}\n\n"
        "Automated summary of cooldown telemetry with a seven-day half-life EMA.\n\n"
    )
    if not records:
        return header + "No telemetry records were found for the requested sources.\n"
    sources_block = "Sources: " + ", ".join(str(path) for path in sources) + "\n\n"
    totals_block = (
        "| Metric | Window Total | Window Avg | 7d EMA | Latest |\n"
        "| -- | -- | -- | -- | -- |\n"
    )
    for accumulator in metrics.values():
        totals_block += accumulator.as_markdown_row(window_days) + "\n"

    range_info = (
        f"\nRecords processed: {len(records)}\n\n"
        "Guardrail: keep Lore-first precedence when interpreting stacked overlays;"
        " investigate spikes before raising limits.\n"
    )
    return header + sources_block + totals_block + range_info


def main() -> int:
    args = _parse_args()
    sources = args.source if args.source else DEFAULT_SOURCES
    records = _read_records(sources)
    metrics, parsed_records = _collect_metrics(records, args.window_days)
    report = _render_report(metrics, parsed_records, list(sources), args.window_days)
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"cooldown_rollup_{datetime.now(timezone.utc).strftime('%Y%m%d')}.md"
    destination = output_dir / filename
    destination.write_text(report, encoding="utf-8")
    print(f"Cooldown rollup written to {destination}")
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI
    raise SystemExit(main())
