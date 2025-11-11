from __future__ import annotations

import json
from pathlib import Path


def load_adapter():
    # Local import to avoid test collection import-time side effects
    from tools.comm_adapter import CommAdapter  # type: ignore

    return CommAdapter()


def test_plan_report_shadow(tmp_path: Path):
    adapter = load_adapter()
    payload = {"schema": "factory-report@1.0", "order_id": "o", "reported_by": "tester", "timestamp_reported": "2025-01-01T00:00:00Z", "status": "ok"}
    out = adapter.send(kind="report", payload=payload, trace_id="t-1", dry_run=True)
    assert out["kind"] == "report"
    planned = out["offline"]["planned"]
    assert "exchange/reports/outbox" in planned["dir"].replace("\\", "/")
    assert out["offline"]["wrote"] is False
    # Online plan should echo channel info and enabled flag
    online = out["online"]["planned"]
    assert online["channel"] in ("git", "http")
    assert "trace_id" in online


def test_plan_ack_shadow(tmp_path: Path):
    adapter = load_adapter()
    payload = {
        "schema": "signal-ack@1.0",
        "ack_id": "a-1",
        "referenced_id": "o-1",
        "sender": "tester",
        "receiver": "hc",
        "timestamp_sent": "2025-01-01T00:00:00Z",
        "status": "acknowledged",
    }
    out = adapter.send(kind="ack", payload=payload, trace_id="t-ack", dry_run=True)
    planned = out["offline"]["planned"]
    assert "exchange/outbox/acknowledgements/logged" in planned["dir"].replace("\\", "/")
    assert out["offline"]["wrote"] is False


def test_plan_order_shadow(tmp_path: Path):
    adapter = load_adapter()
    payload = {"schema": "high-command-order@1.0", "order_id": "o-2", "issued_by": "hc", "target": "all", "priority": "low", "timestamp_issued": "2025-01-01T00:00:00Z", "summary": "t", "directives": [], "requires_ack": False}
    out = adapter.send(kind="order", payload=payload, trace_id="t-order", dry_run=True)
    planned = out["offline"]["planned"]
    assert "exchange/outbox/orders" in planned["dir"].replace("\\", "/")
    assert out["offline"]["wrote"] is False

