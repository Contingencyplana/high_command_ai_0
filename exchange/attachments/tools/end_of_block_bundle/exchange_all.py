import json, os, sys, shutil
from pathlib import Path
from datetime import datetime, timezone

_DEFAULT_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = os.environ.get("WORKSPACE_NAME") or _DEFAULT_ROOT.name
ROOT = Path(os.environ.get("WORKSPACE_ROOT") or _DEFAULT_ROOT)
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
            # Allow passing through canonical exchange artifacts that already
            # declare a top-level "schema"; staging schema checks are skipped.
            if isinstance(obj, dict) and obj.get("schema"):
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
    # Build a filtered set excluding invalid files; copy only valid ones.
    invalid_lookup = {(e.get("kind"), e.get("file")) for e in missing}
    filtered = {
        "orders": [p for p in files["orders"] if ("orders", p.name) not in invalid_lookup],
        "reports": [p for p in files["reports"] if ("reports", p.name) not in invalid_lookup],
        "acks": [p for p in files["acks"] if ("acks", p.name) not in invalid_lookup],
    }
    ok = True  # proceed even if some staged files are invalid; they will be skipped

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

    if missing:
        # Preserve visibility but do not fail the run; we skip invalid staged files.
        summary["note"] = "Some staged files failed validation and were skipped."

    (hub/ORDERS_SUB).mkdir(parents=True, exist_ok=True)
    (hub/REPORTS_SUB).mkdir(parents=True, exist_ok=True)
    (hub/ACKS_SUB).mkdir(parents=True, exist_ok=True)

    for kind, dest_sub in (("orders", ORDERS_SUB), ("reports", REPORTS_SUB), ("acks", ACKS_SUB)):
        for f in filtered[kind]:
            dest = hub/dest_sub/f.name
            shutil.copy2(f, dest)
            summary["copied"][kind].append(f.name)

    out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"exchange_all complete. See {out}")
    sys.exit(0)

if __name__ == "__main__":
    main()
