import json, os, sys
from pathlib import Path
from datetime import datetime, timezone

WORKSPACE = "high_command_ai_0"
ROOT = Path(__file__).resolve().parents[1]
LOGS = ROOT / "logs"

def iso_now():
    return datetime.now(timezone.utc).isoformat()

def read_hub_path():
    env = os.environ.get("SHAGI_EXCHANGE_PATH")
    if env:
        return Path(env)
    cfg = ROOT / "exchange" / "config.json"
    try:
        if cfg.exists():
            obj = json.loads(cfg.read_text(encoding="utf-8"))
            hp = obj.get("hub_path")
            if hp:
                return Path(hp)
    except Exception:
        pass
    return None

def staged_missing_fields(root: Path):
    checks = []
    def needs(obj, fields):
        return [f for f in fields if obj.get(f) is None]
    kinds = [
        ("order",  root/"outbox"/"orders",  ["id","workspace","title","status","created_at","attachments"]),
        ("ack",    root/"outbox"/"acks",    ["order_id","ack_id","workspace","ack_timestamp","notes"]),
        ("report", root/"outbox"/"reports", ["order_id","report_id","workspace","summary","created_at","artifacts"]),
    ]
    for kind, d, fields in kinds:
        if not d.exists():
            continue
        for f in d.glob("*.json"):
            try:
                obj = json.loads(f.read_text(encoding="utf-8"))
            except Exception:
                checks.append({"kind": kind, "file": f.name, "missing": ["invalid_json"]})
                continue
            missing = needs(obj, fields)
            checks.append({"kind": kind, "file": f.name, "missing": missing})
    return checks

def main():
    hub = read_hub_path()
    files_expect = [ROOT/"RUNBOOK.md"]
    docs_present = {str(p): p.exists() for p in files_expect}
    staged_checks = staged_missing_fields(ROOT)
    has_missing = any(c["missing"] for c in staged_checks)
    hub_ok = bool(hub and hub.exists())
    summary = {
        "timestamp_utc": iso_now(),
        "workspace": WORKSPACE,
        "python": sys.version.split()[0],
        "hub_path": str(hub) if hub else None,
        "hub_exists": hub_ok,
        "docs_present": docs_present,
        "staged_checks": staged_checks,
        "ok": hub_ok and all(docs_present.values()) and not has_missing,
    }
    LOGS.mkdir(parents=True, exist_ok=True)
    out = LOGS/"ops_readiness.json"
    out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"ops_readiness written to {out}")
    sys.exit(0 if summary["ok"] else 1)

if __name__ == "__main__":
    main()
