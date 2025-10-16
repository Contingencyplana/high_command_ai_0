# 🛰️ command_exchange_protocol.md — High Command Signal Network

*Doctrine Scroll — `high_command_ai_0/planning/`*

---

## 🌍 Purpose

Codifies the shared communications substrate that links High Command (`high_command_ai_0`) and all field workspaces (e.g., `toysoldiers_ai_*`). Defines directory structure, message lifecycles, and JSON schemas so every order, report, and acknowledgement remains traceable and machine-readable.

---

## 🛠️ 1. Transport Layer

| Layer | Current Implementation | Upgrade Path | Notes |
|-------|------------------------|--------------|-------|
| Storage | Dedicated git repository `high_command_exchange` mounted by every workspace | Object store or secure document DB | Keeps orders/reports immutable and auditable. |
| Access | Git submodule or checkout at `exchange/` inside each workspace | Dedicated sync daemon or API client | Allows offline work with eventual sync. |
| Auth | GitHub SSH/HTTPS credentials | Secrets broker or service principal | Same credentials as doctrine repos for now. |
| Telemetry | `tools/exchange_watcher.py` (local polling utility) | Push-based notification service | Provides lightweight automation for detecting new artefacts. |

**Directory Layout (`exchange/`)**

```plaintext
exchange/
 ├─ orders/
 │   ├─ pending/
 │   └─ dispatched/
 ├─ reports/
 │   ├─ inbox/
 │   └─ archived/
 ├─ acknowledgements/
 │   ├─ pending/
 │   └─ logged/
 └─ ledger/
     ├─ journal.md
     └─ index.json
```

- `orders/` holds outbound directives from High Command.
- `reports/` stores field submissions awaiting review plus long-term archive.
- `acknowledgements/` tracks delivery confirmations to prevent silent loops.
- `ledger/` keeps a rolling human-auditable summary and machine index.

📌 *Version Control:* The `exchange/` directory is initialized as its own git repository so it can be promoted to the shared `high_command_exchange` submodule. Each workspace should add a remote and synchronize this repo independently of the doctrine codebase.

---

## 🧾 2. Message Schemas

All payloads are versioned JSON documents encoded in UTF-8, newline-terminated. Keys use `snake_case`. Timestamps are ISO 8601 UTC.

### 2.1 Order Schema (`orders/pending/*.json`)

```json
{
  "schema": "high-command-order@1.0",
  "order_id": "order-2025-10-12-001",
  "issued_by": "high_command_ai_0",
  "target": "toysoldiers_ai_0",
  "priority": "standard",
  "timestamp_issued": "2025-10-12T16:20:00Z",
  "summary": "Initialize git repository and confirm readiness",
  "directives": [
    {
      "step": 1,
      "action": "run_command",
      "command": "git init",
      "notes": "Execute at workspace root"
    }
  ],
  "dependencies": [],
  "requires_ack": true,
  "expires_at": "2025-10-15T00:00:00Z",
  "attachments": [
    {
      "type": "markdown",
      "path": "attachments/setup_notes.md"
    }
  ]
}
```

Valid `priority` values: `standard`, `urgent`, `hold`. Orders move from `pending/` to `dispatched/` after receipt is logged.

### 2.2 Report Schema (`reports/inbox/*.json`)

```json
{
  "schema": "field-report@1.0",
  "report_id": "report-2025-10-12-017",
  "origin": "toysoldiers_ai_0",
  "relates_to": "order-2025-10-12-001",
  "timestamp_submitted": "2025-10-12T16:35:00Z",
  "status": "completed",
  "summary": "Repository initialized with .gitignore staged",
  "metrics": {
    "execution_time_s": 45,
    "files_touched": 2,
    "entropy_index": 0.12
  },
  "artifacts": [
    {
      "type": "git_status",
      "path": "artifacts/git_status.txt"
    }
  ],
  "follow_up": [
    {
      "suggestion": "Define shared .gitignore template",
      "priority": "standard"
    }
  ]
}
```

`status` values: `completed`, `blocked`, `partial`, `aborted`.

### 2.3 Acknowledgement Schema (`acknowledgements/pending/*.json`)

```json
{
  "schema": "signal-ack@1.0",
  "ack_id": "ack-2025-10-12-003",
  "referenced_id": "order-2025-10-12-001",
  "sender": "toysoldiers_ai_0",
  "receiver": "high_command_ai_0",
  "timestamp_sent": "2025-10-12T16:21:30Z",
  "status": "received",
  "notes": "Order queued for execution"
}
```

Valid `status` values: `received`, `in-progress`, `completed`, `declined`.

---

## 🔄 3. Message Lifecycle

1. **Draft** — High Command composes JSON order with unique `order_id`.
2. **Commit** — Order placed in `orders/pending/` and committed to exchange repo.
3. **Sync** — Field workspace pulls exchange repo, reads new orders.
4. **Acknowledge** — Field posts `signal-ack@1.0`; order moves to `dispatched/`.
5. **Execute** — Field carries out directives, logs artifacts.
6. **Report** — Field submits `field-report@1.0`; High Command reviews and moves report to `reports/archived/`.
7. **Close-Out** — High Command issues closure note in `ledger/journal.md` and updates `ledger/index.json`.

📡 *Automation Hook:* Field workspaces should run `python -m tools.exchange_watcher --watch` (or equivalent scheduling) so new orders, pending acknowledgements, and inbox reports surface immediately without manual polling.

Every state transition must leave a git commit trail for full auditability.

---

## 📚 4. Indexing & Retrieval

`ledger/index.json` contains a compact manifest for fast lookups:

```json
{
  "version": "1.0.0",
  "orders": {
    "order-2025-10-12-003": {
      "status": "closed",
      "order_path": "orders/dispatched/order-2025-10-12-003.json",
      "ack_path": "acknowledgements/logged/order-2025-10-12-003-ack.json",
      "report_path": "reports/archived/order-2025-10-12-003-report.json"
    }
  },
  "acks": {
    "order-2025-10-12-003-ack": "acknowledgements/logged/order-2025-10-12-003-ack.json"
  },
  "reports": {
    "order-2025-10-12-003-report": "reports/archived/order-2025-10-12-003-report.json"
  }
}
```

Automation scripts should regenerate the index after each sync to guarantee references are current.

---

## 🛡️ 5. Governance

- **Unique IDs:** All message IDs are deterministic: `type-YYYY-MM-DD-###`.
- **Time Discipline:** Clocks sync via UTC; drift beyond 5 seconds triggers warning.
- **Human Checkpoint:** Orders with `priority = urgent` require human sign-off recorded in `ledger/journal.md`.
- **Retention:** Reports stay in `archived/` indefinitely; attachments may be pruned via rolling hash audit after 90 days.
- **Encryption (Future):** When secrets emerge, encapsulate attachments with workspace-specific keys and store only fingerprints in the exchange repo.
- **Governance Collateral:** Every workspace interacting with the exchange must surface `LICENSE`, `CODE_OF_CONDUCT.md`, and `CONTRIBUTING.md` aligned with High Command’s templates; include links in `exchange/README.md`.

---

## 6. Automation Aides

- **Exchange Watcher (`tools/exchange_watcher.py`):** Polls the exchange tree, tracks the last-seen snapshot, and prints new orders, pending acknowledgements, and inbox reports. Supports one-shot checks or continuous monitoring via `--watch`.
- **Schema Validator (`tools/schema_validator.py`):** Validates payloads against canonical schemas prior to commit; integrate into CI or pre-commit flows.
- **Forge Logs:** Events recorded in `logs/forge.log` provide cross-reference between doctrine automation and exchange activity.

---

## 🚀 7. Immediate Tasks

1. **Deploy exchange watcher scheduling** — Embed the watcher in each field workspace (cron, scheduled task, or daemon) so operators receive near-real-time order prompts.
2. **Maintain governance parity** — Whenever doctrine evolves (licenses, conduct, contribution flow), issue orders to downstream workspaces and log completion in the ledger.
3. **Plan Toyfoundry integration** — Define manufacturing pipeline requirements and map how Toyfoundry will consume exchange directives and report production telemetry.

With these actions, High Command and field theatres operate from a shared doctrine, automated alerting, and evolving strategic roadmap.
