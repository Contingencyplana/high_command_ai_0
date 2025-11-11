"""Ops Readiness Pack

Runs a lightweight preflight:
  1) Exchange heartbeat
  2) Contract tests (fail-fast)
  3) Offline sync (quiet, latest=1)
  4) Schema sweep across exchange payloads
  5) Hybrid shadow check (no writes)

Emits a labeled one-page summary and exits non-zero on failure.

Usage:
  python -m tools.ops_readiness
  python -m tools.ops_readiness --no-fail-fast --latest 3
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import textwrap
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass
class StepResult:
    name: str
    status: str  # OK | FAIL | WARN
    returncode: int
    duration_ms: int
    stdout: str
    stderr: str


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _run_cmd(args: list[str], cwd: Path | None = None, timeout: int | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(cwd or REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def run_heartbeat() -> StepResult:
    start = _now()
    proc = _run_cmd([sys.executable, "-m", "tools.exchange_heartbeat"])  # returns 0/1/2
    end = _now()
    status = "OK" if proc.returncode == 0 else ("WARN" if proc.returncode == 2 else "FAIL")
    return StepResult(
        name="Exchange Heartbeat",
        status=status,
        returncode=proc.returncode,
        duration_ms=int((end - start).total_seconds() * 1000),
        stdout=proc.stdout.strip(),
        stderr=proc.stderr.strip(),
    )


def read_config_mode() -> StepResult:
    start = _now()
    cfg_path = REPO_ROOT / "exchange" / "config.json"
    mode = "local"
    online_enabled = False
    offline_write_kinds: list[str] = ["report"]
    try:
        import json as _json

        raw = _json.loads(cfg_path.read_text(encoding="utf-8"))
        if isinstance(raw, dict):
            mode = str(raw.get("mode", mode))
            online = raw.get("online", {})
            if isinstance(online, dict):
                online_enabled = bool(online.get("enabled", False))
                kinds = online.get("offline_write_kinds", offline_write_kinds)
                if isinstance(kinds, list):
                    offline_write_kinds = [str(k).lower() for k in kinds]
        status = "OK"
        rc = 0
        stdout = f"mode={mode}, online.enabled={online_enabled}, offline_write_kinds={offline_write_kinds}"
        stderr = ""
    except Exception as exc:  # pragma: no cover - defensive
        status = "WARN"
        rc = 0
        stdout = ""
        stderr = f"Could not read config: {exc}"
    end = _now()
    return StepResult(
        name="Config Mode",
        status=status,
        returncode=rc,
        duration_ms=int((end - start).total_seconds() * 1000),
        stdout=stdout,
        stderr=stderr,
    )


def run_contracts(fail_fast: bool) -> StepResult:
    start = _now()
    args = [sys.executable, "-m", "tools.contract_test_runner"]
    if fail_fast:
        args.append("--fail-fast")
    proc = _run_cmd(args)
    end = _now()
    status = "OK" if proc.returncode == 0 else "FAIL"
    return StepResult(
        name="Contract Tests",
        status=status,
        returncode=proc.returncode,
        duration_ms=int((end - start).total_seconds() * 1000),
        stdout=proc.stdout.strip(),
        stderr=proc.stderr.strip(),
    )


def run_offline_sync(latest: int, quiet: bool) -> StepResult:
    start = _now()
    args = [sys.executable, "-m", "tools.offline_sync_exchange", "--latest", str(latest)]
    if quiet:
        args.append("--quiet")
    proc = _run_cmd(args)
    end = _now()
    status = "OK" if proc.returncode == 0 else "FAIL"
    return StepResult(
        name="Offline Sync",
        status=status,
        returncode=proc.returncode,
        duration_ms=int((end - start).total_seconds() * 1000),
        stdout=proc.stdout.strip(),
        stderr=proc.stderr.strip(),
    )


def run_schema_sweep() -> StepResult:
    """Validate exchange payloads (orders/reports/acks) with schema validator.

    Treat missing files as WARN (not a failure) to keep readiness permissive
    when a given category has no artifacts yet.
    """
    start = _now()
    roots = [
        REPO_ROOT / "exchange" / "orders" / "pending",
        REPO_ROOT / "exchange" / "orders" / "dispatched",
        REPO_ROOT / "exchange" / "orders" / "completed",
        REPO_ROOT / "exchange" / "reports" / "inbox",
        REPO_ROOT / "exchange" / "reports" / "outbox",
        REPO_ROOT / "exchange" / "reports" / "archived",
        REPO_ROOT / "exchange" / "reports" / "archived" / "inbox_backlog",
        REPO_ROOT / "exchange" / "acknowledgements" / "pending",
        REPO_ROOT / "exchange" / "acknowledgements" / "logged",
    ]

    files: list[str] = []
    for root in roots:
        if root.exists():
            files.extend(str(p) for p in sorted(root.glob("*.json")))

    if not files:
        end = _now()
        return StepResult(
            name="Schema Sweep (Exchange)",
            status="WARN",
            returncode=0,
            duration_ms=int((end - start).total_seconds() * 1000),
            stdout="No exchange payload files found; skipping validation",
            stderr="",
        )

    proc = _run_cmd([sys.executable, "-m", "tools.schema_validator", *files])
    end = _now()
    status = "OK" if proc.returncode == 0 else "FAIL"
    return StepResult(
        name="Schema Sweep (Exchange)",
        status=status,
        returncode=proc.returncode,
        duration_ms=int((end - start).total_seconds() * 1000),
        stdout=proc.stdout.strip(),
        stderr=proc.stderr.strip(),
    )


def run_hybrid_shadow() -> StepResult:
    """Exercise the hybrid comms adapter in shadow mode (dry run)."""
    start = _now()
    try:
        import json as _json
        from tools.comm_adapter import CommAdapter  # local import to avoid test coupling

        adapter = CommAdapter()
        payload = {"schema": "ops-hybrid-shadow@1.0", "generated_at": _now().strftime("%Y-%m-%dT%H:%M:%SZ")}
        out = adapter.send(kind="report", payload=payload, trace_id="ops-readiness", dry_run=True)
        stdout = _json.dumps(out, indent=2)
        status = "OK"
        rc = 0
        stderr = ""
    except Exception as exc:  # pragma: no cover - defensive
        stdout = ""
        stderr = str(exc)
        status = "FAIL"
        rc = 1
    end = _now()
    return StepResult(
        name="Hybrid Shadow Check",
        status=status,
        returncode=rc,
        duration_ms=int((end - start).total_seconds() * 1000),
        stdout=stdout.strip(),
        stderr=stderr.strip(),
    )


def _write_summary(steps: list[StepResult], destination: Path) -> None:
    lines: list[str] = []
    ts = _now().isoformat().replace("+00:00", "Z")
    lines.append(f"Ops Readiness Summary — {ts}")
    lines.append("")
    for step in steps:
        lines.append(f"[{step.status}] {step.name} ({step.duration_ms} ms)")
        if step.stdout:
            snippet = "\n".join(step.stdout.splitlines()[:12])
            if snippet:
                lines.append(textwrap.indent(snippet, prefix="  "))
        if step.stderr:
            lines.append(textwrap.indent("stderr:", prefix="  "))
            lines.append(textwrap.indent("\n".join(step.stderr.splitlines()[:6]), prefix="    "))
        lines.append("")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Ops Readiness preflight")
    parser.add_argument("--no-fail-fast", action="store_true", help="Run all steps even if one fails")
    parser.add_argument("--latest", type=int, default=1, help="Limit offline sync to N most recent files")
    parser.add_argument("--quiet-sync", action="store_true", help="Quiet mode for offline sync")
    args = parser.parse_args(argv)

    steps: list[StepResult] = []
    exit_code = 0

    # 0) Config mode visibility
    cfg = read_config_mode()
    steps.append(cfg)

    # 1) Heartbeat
    hb = run_heartbeat()
    steps.append(hb)
    if hb.returncode != 0:
        exit_code = 1
        if not args.no_fail_fast:
            summary_path = REPO_ROOT / "logs" / "ops_readiness" / "summary.txt"
            _write_summary(steps, summary_path)
            print(f"[FAIL] {hb.name}\n" + (hb.stdout or hb.stderr or ""))
            return exit_code

    # 2) Contracts (fail-fast)
    ct = run_contracts(fail_fast=True)
    steps.append(ct)
    if ct.returncode != 0:
        exit_code = 1
        if not args.no_fail_fast:
            summary_path = REPO_ROOT / "logs" / "ops_readiness" / "summary.txt"
            _write_summary(steps, summary_path)
            print(ct.stdout)
            return exit_code

    # 3) Offline sync (quiet)
    sync = run_offline_sync(latest=max(1, args.latest), quiet=True or args.quiet_sync)
    steps.append(sync)
    if sync.returncode != 0:
        exit_code = 1

    # 4) Schema sweep for frontline feedback
    sweep = run_schema_sweep()
    steps.append(sweep)
    if sweep.status == "FAIL":
        exit_code = 1

    # 5) Hybrid shadow check (no writes)
    hybrid = run_hybrid_shadow()
    steps.append(hybrid)
    if hybrid.status == "FAIL":
        exit_code = 1

    # Write summary artifact
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    summary_path = REPO_ROOT / "logs" / "ops_readiness" / f"summary-{stamp}.txt"
    _write_summary(steps, summary_path)

    # Mirror a terse one-pager to stdout
    print((REPO_ROOT / "logs" / "ops_readiness").as_posix())
    for step in steps:
        print(f"[{step.status}] {step.name} ({step.duration_ms} ms)")
    print("Consult: exchange/attachments/guides/multi_layer_playbook.md for layering checklist")

    return exit_code


if __name__ == "__main__":  # pragma: no cover - CLI
    raise SystemExit(main())
