import json, os, sys, shutil
from pathlib import Path
from datetime import datetime, timezone

WORKSPACE = "high_command_ai_0"
ROOT = Path(__file__).resolve().parents[1]
LOGS = ROOT / "logs"

ORDERS_SUB = Path("exchange/orders/dispatched")
REPORTS_SUB = Path("exchange/reports/archived")
ACKS_SUB = Path("exchange/acknowledgements/logged")

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

def collect_staged():
    return {
        "orders": list((ROOT/"outbox"/"orders").glob("*.json")),
        "reports": list((ROOT/"outbox"/"reports").glob("*.json")),
        "acks": list((ROOT/"outbox"/"acks").glob("*.json")),
    }

def validate(files_by_kind):
    missing = []
    def fields_for(kind):
        return {
            "orders": ["id","workspace","title","status","created_at","attachments"],
            "acks": ["order_id","ack_id","workspace","ack_timestamp","notes"],
            "reports": ["order_id","report_id","workspace","summary","created_at","artifacts"],
        }[kind]
    for kind, files in files_by_kind.items():
        req = fields_for(kind)
        for f in files:
            try:
                obj = json.loads(f.read_text(encoding="utf-8"))
            except Exception:
                missing.append({"kind": kind, "file": f.name, "missing": ["invalid_json"]})
                continue
            miss = [k for k in req if obj.get(k) is None]
            if miss:
                missing.append({"kind": kind, "file": f.name, "missing": miss})
    return missing

def main():
    hub = read_hub_path()
    if not hub:
        print("No hub path. Set SHAGI_EXCHANGE_PATH or edit exchange/config.json.", file=sys.stderr)
        sys.exit(2)
    files = collect_staged()
    missing = validate(files)
    ok = len(missing) == 0

    summary = {
        "timestamp_utc": iso_now(),
        "workspace": WORKSPACE,
        "hub_path": str(hub),
        "validated_ok": ok,
        "validation_errors": missing,
        "copied": {"orders": [], "reports": [], "acks": []},
    }

    LOGS.mkdir(parents=True, exist_ok=True)
    out = LOGS/"exchange_all.json"

    if not ok:
        out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(f"Validation failed. See {out}")
        sys.exit(1)

    (hub/ORDERS_SUB).mkdir(parents=True, exist_ok=True)
    (hub/REPORTS_SUB).mkdir(parents=True, exist_ok=True)
    (hub/ACKS_SUB).mkdir(parents=True, exist_ok=True)

    for kind, dest_sub in (("orders", ORDERS_SUB), ("reports", REPORTS_SUB), ("acks", ACKS_SUB)):
        for f in files[kind]:
            dest = hub/dest_sub/f.name
            shutil.copy2(f, dest)
            summary["copied"][kind].append(f.name)

    out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"exchange_all complete. See {out}")
    sys.exit(0)

if __name__ == "__main__":
    main()
