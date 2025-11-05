"""Run a Level-0 emoji translator canary over sample chains.

Loads `golf_00/delta_00/alfa_04/sample_chains.json`, translates each chain
via `emoji_translator.py`, validates the resulting emoji-runtime payload
against the schema, and optionally promotes to factory-order and validates.

Results are appended to `logs/canary/emoji_translator/results.jsonl`.

Usage:
  python tools/run_emoji_canary.py [--promote]

Exit code is non-zero if any translation or validation fails when not skipped.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in [here.parent] + list(here.parents):
        if (parent / ".git").exists():
            return parent
    return here.parent


def load_module(name: str, path: Path):
    import importlib.util

    spec = importlib.util.spec_from_file_location(name, path)
    if not spec or not spec.loader:
        raise ImportError(f"Cannot import {name} from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module


@dataclass
class Result:
    chain_name: str
    status: str
    details: str | None = None
    factory_status: str | None = None
    output_len: int | None = None


def validate_payload(schema_validator, payload: dict) -> None:
    schema_validator.validate_payload(payload)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run emoji translator canary")
    parser.add_argument("--promote", action="store_true", help="Also validate factory-order promotion")
    args = parser.parse_args()

    root = repo_root()
    logs_dir = root / "logs" / "canary" / "emoji_translator"
    logs_dir.mkdir(parents=True, exist_ok=True)
    results_path = logs_dir / "results.jsonl"

    translator = load_module("emoji_translator", root / "golf_00" / "delta_00" / "alfa_04" / "emoji_translator.py")
    sample_path = root / "golf_00" / "delta_00" / "alfa_04" / "sample_chains.json"
    samples: Dict[str, str] = json.loads(sample_path.read_text(encoding="utf-8"))

    schema_validator = load_module("schema_validator", root / "tools" / "schema_validator.py")

    adapter = None
    if args.promote:
        adapter = load_module("factory_adapter", root / "golf_00" / "delta_00" / "alfa_04" / "factory_adapter.py")

    failures = 0
    with results_path.open("a", encoding="utf-8") as out:
        for name, chain in samples.items():
            res = Result(chain_name=name, status="success")
            try:
                payload = translator.translate_chain(chain)
                # Basic required fields
                if payload.get("schema") != "emoji-runtime@1.0":
                    raise ValueError("emoji payload missing schema or wrong schema")
                if not isinstance(payload.get("glyph_chain"), list):
                    raise ValueError("missing glyph_chain list")
                if not isinstance(payload.get("intent"), dict):
                    raise ValueError("missing intent dict")
                # Schema validation
                validate_payload(schema_validator, payload)
                res.output_len = len(json.dumps(payload))
            except Exception as exc:
                res.status = "failure"
                res.details = str(exc)
                failures += 1

            # Optional factory promotion validation
            if res.status == "success" and adapter is not None:
                try:
                    oid = adapter.derive_order_id(name, payload.get("created_at"))
                    order = adapter.emoji_runtime_to_factory_order(
                        payload,
                        order_id=oid,
                        issued_by="canary",
                        target="toyfoundry_ai_0",
                        priority="realtime",
                        requires_ack=False,
                    )
                    # Inject schema if not present (adapter returns with schema set)
                    validate_payload(schema_validator, order)
                    res.factory_status = "ok"
                except Exception as exc:
                    res.factory_status = f"failure: {exc}"
                    failures += 1

            out.write(json.dumps(res.__dict__, ensure_ascii=False))
            out.write("\n")

    if failures:
        print(f"[canary] {failures} failure(s)")
        return 1
    print("[canary] all sample chains passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

