"""End-to-end contract tests for emoji-runtime and factory-order payloads.

The runner promotes canonical emoji chains through the composer translator and
factory adapter. It asserts that the resulting emoji-runtime payloads and
factory orders match curated expectations in ``contract_samples/``.

Usage::

    python -m tools.contract_test_runner           # run all cases
    python -m tools.contract_test_runner --list    # list available cases
    python -m tools.contract_test_runner --case basic_ritual_victory
"""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence

from golf_00.delta_00.alfa_04 import emoji_translator, factory_adapter
from golf_00.delta_00.alfa_00.overlay_bridge import build_bridge

REPO_ROOT = Path(__file__).resolve().parents[1]
SAMPLES_ROOT = REPO_ROOT / "contract_samples"
CASES_DIR = SAMPLES_ROOT / "cases"


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


@dataclass
class FactoryOrderExpectations:
    summary: str
    priority: str
    target: str
    requires_ack: bool
    details_contains: Sequence[str]
    overlay_id: str | None = None
    overlay_layer: str | None = None


@dataclass
class EmojiRuntimeExpectations:
    summary: str
    intent: dict
    spoken: Sequence[str]
    overlay_id: str | None = None
    overlay_layer: str | None = None


@dataclass
class AdapterConfig:
    order_id: str
    issued_by: str
    target: str
    priority: str
    requires_ack: bool


@dataclass
class ContractCase:
    name: str
    description: str
    emoji_chain: Sequence[str]
    adapter: AdapterConfig
    expectations_runtime: EmojiRuntimeExpectations
    expectations_factory: FactoryOrderExpectations
    source_path: Path
    overlay: "OverlayCaseConfig | None" = None


@dataclass
class CaseResult:
    name: str
    passed: bool
    errors: List[str]


@dataclass
class OverlayCaseConfig:
    overlay_id: str
    layer_kind: str
    trace_id: str
    description: str | None = None


def _as_list(value: Sequence[str] | Iterable[str]) -> List[str]:
    return [str(item) for item in value]


def load_cases() -> List[ContractCase]:
    if not CASES_DIR.exists():
        raise FileNotFoundError(f"Contract case directory missing: {CASES_DIR}")

    cases: List[ContractCase] = []
    for path in sorted(CASES_DIR.glob("*.json")):
        raw = _load_json(path)
        adapter = AdapterConfig(**raw["adapter"])
        runtime_raw = raw["expectations"]["emoji_runtime"]
        factory_raw = raw["expectations"]["factory_order"]
        overlay_config = None
        overlay_raw = raw.get("overlay")
        if overlay_raw:
            overlay_config = OverlayCaseConfig(
                overlay_id=overlay_raw["overlay_id"],
                layer_kind=overlay_raw["layer_kind"],
                trace_id=overlay_raw.get("trace_id", "overlay-trace"),
                description=overlay_raw.get("description"),
            )
        runtime = EmojiRuntimeExpectations(
            summary=runtime_raw["summary"],
            intent=runtime_raw["intent"],
            spoken=tuple(runtime_raw.get("spoken", [])),
            overlay_id=runtime_raw.get("overlay_id"),
            overlay_layer=runtime_raw.get("overlay_layer"),
        )
        factory = FactoryOrderExpectations(
            summary=factory_raw["summary"],
            priority=factory_raw["priority"],
            target=factory_raw["target"],
            requires_ack=factory_raw["requires_ack"],
            details_contains=tuple(factory_raw.get("details_contains", [])),
            overlay_id=factory_raw.get("overlay_id"),
            overlay_layer=factory_raw.get("overlay_layer"),
        )
        case = ContractCase(
            name=raw["name"],
            description=raw.get("description", ""),
            emoji_chain=tuple(raw["emoji_chain"]),
            adapter=adapter,
            expectations_runtime=runtime,
            expectations_factory=factory,
            source_path=path,
            overlay=overlay_config,
        )
        cases.append(case)
    if not cases:
        raise RuntimeError(f"No contract cases found in {CASES_DIR}")
    return cases


def _compare_intent(expected: dict, actual: dict) -> List[str]:
    errors: List[str] = []
    for key, value in expected.items():
        actual_value = actual.get(key)
        if key == "qualifiers":
            actual_value = _as_list(actual_value or [])
        if key == "secondary_outcome":
            if actual.get(key) != value:
                errors.append(f"intent.{key} expected {value!r}, got {actual.get(key)!r}")
            continue
        if actual_value != value:
            errors.append(f"intent.{key} expected {value!r}, got {actual_value!r}")
    return errors


def _validate_runtime(case: ContractCase, payload: dict) -> List[str]:
    errors: List[str] = []
    if payload.get("schema") != "emoji-runtime@1.0":
        errors.append("emoji_runtime.schema mismatch")
    if _as_list(payload.get("glyph_chain", [])) != list(case.emoji_chain):
        errors.append("glyph_chain does not match sample chain")
    if payload.get("summary") != case.expectations_runtime.summary:
        errors.append(
            "emoji_runtime.summary expected "
            f"{case.expectations_runtime.summary!r}, got {payload.get('summary')!r}"
        )
    spoken = _as_list(payload.get("spoken", []))
    if spoken != list(case.expectations_runtime.spoken):
        errors.append(f"spoken expected {case.expectations_runtime.spoken!r}, got {spoken!r}")
    intent = payload.get("intent")
    if not isinstance(intent, dict):
        errors.append("emoji_runtime.intent missing or not an object")
        return errors
    errors.extend(_compare_intent(case.expectations_runtime.intent, intent))
    if case.expectations_runtime.overlay_id is not None:
        actual_overlay_id = payload.get("overlay_id")
        if actual_overlay_id != case.expectations_runtime.overlay_id:
            errors.append(
                f"overlay_id expected {case.expectations_runtime.overlay_id!r}, got {actual_overlay_id!r}"
            )
        stub = payload.get("telemetry_stub") if isinstance(payload.get("telemetry_stub"), dict) else {}
        stub_overlay_id = stub.get("overlay_id") if isinstance(stub, dict) else None
        if stub_overlay_id != case.expectations_runtime.overlay_id:
            errors.append(
                f"telemetry_stub.overlay_id expected {case.expectations_runtime.overlay_id!r}, got {stub_overlay_id!r}"
            )
    if case.expectations_runtime.overlay_layer is not None:
        actual_layer = payload.get("overlay_layer")
        if actual_layer != case.expectations_runtime.overlay_layer:
            errors.append(
                f"overlay_layer expected {case.expectations_runtime.overlay_layer!r}, got {actual_layer!r}"
            )
        stub = payload.get("telemetry_stub") if isinstance(payload.get("telemetry_stub"), dict) else {}
        stub_layer = stub.get("overlay_layer") if isinstance(stub, dict) else None
        if stub_layer != case.expectations_runtime.overlay_layer:
            errors.append(
                f"telemetry_stub.overlay_layer expected {case.expectations_runtime.overlay_layer!r}, got {stub_layer!r}"
            )
    return errors


def _validate_factory_order(case: ContractCase, payload: dict, order: dict) -> List[str]:
    errors: List[str] = []
    if order.get("schema") != "factory-order@1.0":
        errors.append("factory_order.schema mismatch")
    if order.get("order_id") != case.adapter.order_id:
        errors.append(
            f"factory_order.order_id expected {case.adapter.order_id!r}, got {order.get('order_id')!r}"
        )
    if order.get("priority") != case.expectations_factory.priority:
        errors.append(
            "factory_order.priority expected "
            f"{case.expectations_factory.priority!r}, got {order.get('priority')!r}"
        )
    if order.get("summary") != case.expectations_factory.summary:
        errors.append(
            "factory_order.summary expected "
            f"{case.expectations_factory.summary!r}, got {order.get('summary')!r}"
        )
    if order.get("target") != case.expectations_factory.target:
        errors.append(
            f"factory_order.target expected {case.expectations_factory.target!r}, got {order.get('target')!r}"
        )
    if order.get("requires_ack") is not case.expectations_factory.requires_ack:
        errors.append(
            "factory_order.requires_ack expected "
            f"{case.expectations_factory.requires_ack!r}, got {order.get('requires_ack')!r}"
        )

    directives = order.get("directives")
    if not isinstance(directives, list) or not directives:
        errors.append("factory_order.directives missing")
    else:
        directive = directives[0]
        action_expected = case.expectations_runtime.intent.get("action")
        if directive.get("action") != action_expected:
            errors.append(
                f"factory_order.directive.action expected {action_expected!r}, got {directive.get('action')!r}"
            )
        details = directive.get("details", "")
        for snippet in case.expectations_factory.details_contains:
            if snippet not in details:
                errors.append(f"factory_order.directive.details missing snippet: {snippet!r}")

    extensions = order.get("extensions")
    if not isinstance(extensions, dict):
        errors.append("factory_order.extensions missing")
    elif extensions.get("emoji_runtime_payload") != payload:
        errors.append("factory_order.extensions.emoji_runtime_payload does not match source payload")

    return errors


def run_case(case: ContractCase) -> CaseResult:
    payload = None
    cleanup_outbox: tempfile.TemporaryDirectory | None = None
    original_auto_flag = os.environ.get("OVERLAY_AUTO_PROMOTE_FACTORY_ORDERS")
    try:
        if case.overlay:
            os.environ["OVERLAY_AUTO_PROMOTE_FACTORY_ORDERS"] = "0"
            cleanup_outbox = tempfile.TemporaryDirectory()
            bridge = build_bridge(cleanup_outbox.name)
            destination = bridge.dispatch_raw_chain(
                case.emoji_chain,
                chain_name=case.name,
                description=case.overlay.description,
                trace_id=case.overlay.trace_id,
                overlay_id=case.overlay.overlay_id,
                layer_kind=case.overlay.layer_kind,
            )
            payload_path = Path(destination)
            payload = json.loads(payload_path.read_text(encoding="utf-8"))
        else:
            payload = emoji_translator.translate_chain(case.emoji_chain)
    except Exception as exc:  # pragma: no cover - defensive guard
        return CaseResult(case.name, False, [f"translator error: {exc}"])
    finally:
        if cleanup_outbox is not None:
            cleanup_outbox.cleanup()
        if original_auto_flag is None:
            os.environ.pop("OVERLAY_AUTO_PROMOTE_FACTORY_ORDERS", None)
        else:
            os.environ["OVERLAY_AUTO_PROMOTE_FACTORY_ORDERS"] = original_auto_flag

    errors = _validate_runtime(case, payload)

    if not errors:
        order = factory_adapter.emoji_runtime_to_factory_order(
            payload,
            order_id=case.adapter.order_id,
            issued_by=case.adapter.issued_by,
            target=case.adapter.target,
            priority=case.adapter.priority,
            requires_ack=case.adapter.requires_ack,
        )
        errors.extend(_validate_factory_order(case, payload, order))

    return CaseResult(case.name, not errors, errors)


def run_contract_tests(selected: Sequence[str] | None = None, *, fail_fast: bool = False) -> List[CaseResult]:
    cases = load_cases()
    if selected:
        selected_set = {name.lower() for name in selected}
        cases = [case for case in cases if case.name.lower() in selected_set]
        if not cases:
            raise ValueError(f"Requested cases not found: {', '.join(selected)}")

    results: List[CaseResult] = []
    for case in cases:
        result = run_case(case)
        results.append(result)
        if fail_fast and not result.passed:
            break
    return results


def _format_result(result: CaseResult) -> str:
    if result.passed:
        return f"[PASS] {result.name}"
    lines = [f"[FAIL] {result.name}"]
    lines.extend(f"  - {error}" for error in result.errors)
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run emoji/factory contract tests.")
    parser.add_argument("--case", action="append", dest="cases", help="Run a specific case by name.")
    parser.add_argument("--list", action="store_true", help="List available cases and exit.")
    parser.add_argument("--fail-fast", action="store_true", help="Stop after the first failing case.")
    args = parser.parse_args(argv)

    cases = load_cases()

    if args.list:
        for case in cases:
            print(f"{case.name}: {case.description}")
        return 0

    selected = args.cases
    results = run_contract_tests(selected or None, fail_fast=args.fail_fast)

    exit_code = 0
    for result in results:
        print(_format_result(result))
        if not result.passed:
            exit_code = 1
    return exit_code


if __name__ == "__main__":  # pragma: no cover - CLI
    raise SystemExit(main())
