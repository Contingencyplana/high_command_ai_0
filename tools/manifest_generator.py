"""Generate high-rank (K–P) manifests from rank_path metadata.

Scans JSON files under given roots, aggregates counts by higher ranks
(kilo, lima, mike, november, oscar, papa), and writes summaries to
`high_command_ai_0/manifests/`.

Usage:
    python tools/manifest_generator.py \
        --roots exchange/orders/completed exchange/reports/archived contract_samples/cases \
        --out high_command_ai_0/manifests

Notes:
- Files without a rank_path are skipped quietly.
- This is a minimal stub intended to make the automation path tangible; extend
  as needed to include rollups by workspace/juliett/golf as follow-ons.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Mapping


HIGH_RANKS = ("kilo", "lima", "mike", "november", "oscar", "papa")


def _iso_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _iter_json_files(roots: list[Path]) -> list[Path]:
    files: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        if root.is_file() and root.suffix.lower() == ".json":
            files.append(root)
        else:
            files.extend(p for p in root.rglob("*.json") if p.is_file())
    return files


def _load_json(path: Path) -> Mapping[str, object] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def build_aggregates(files: list[Path]) -> Dict[str, Counter]:
    agg: Dict[str, Counter] = {rank: Counter() for rank in HIGH_RANKS}
    for path in files:
        data = _load_json(path)
        if not isinstance(data, Mapping):
            continue
        rp = data.get("rank_path")
        if not isinstance(rp, Mapping):
            continue
        for rank in HIGH_RANKS:
            ident = rp.get(rank)
            if isinstance(ident, str) and ident.strip():
                agg[rank][ident] += 1
    return agg


def write_manifests(agg: Dict[str, Counter], out_dir: Path, *, roots: list[Path]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    index: dict = {
        "generated_at": _iso_now(),
        "roots": [str(r) for r in roots],
        "ranks": {},
    }
    for rank, counter in agg.items():
        entries = sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))
        payload = {
            "generated_at": _iso_now(),
            "rank": rank,
            "total_identifiers": len(entries),
            "identifiers": [
                {"id": ident, "count": count} for ident, count in entries
            ],
        }
        (out_dir / f"{rank}.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        index["ranks"][rank] = {
            "identifiers": len(entries),
            "total_count": int(sum(counter.values())),
            "path": f"{rank}.json",
        }
    (out_dir / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate K–P rank manifests")
    parser.add_argument(
        "--roots",
        nargs="*",
        default=[
            "exchange/orders/completed",
            "exchange/reports/archived",
            "contract_samples/cases",
        ],
        help="Directories/files to scan for JSON payloads",
    )
    parser.add_argument(
        "--out",
        default="high_command_ai_0/manifests",
        help="Output directory for manifests",
    )
    args = parser.parse_args(argv)

    roots = [Path(r) for r in args.roots]
    out_dir = Path(args.out)

    files = _iter_json_files(roots)
    agg = build_aggregates(files)
    write_manifests(agg, out_dir, roots=roots)
    print(f"[manifests] wrote {out_dir} (ranks: {', '.join(HIGH_RANKS)})")
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI
    raise SystemExit(main())

