# Documentation Front

Purpose
- Make doctrine and plans clear, parseable, and actionable for humans and AI tooling.

Standards
- Use Safety Notes sections on planning docs linking to concrete policies/gates.
- Prefer structured templates (RFC, runbooks, decision memos) and schemas where applicable.
- Plain, concise language; stable headings; predictable file names.

Tooling & Links
- Templates: planning/templates/
- Policies: policies/*; Exchange interfaces: exchange/interfaces.md
- Schemas: exchange/schemas/*.schema.json

Acceptance Checks
- New planning docs include “Safety Notes (valiant_citadel_ai_0)” with concrete links.
- Required runbooks/policies present; validator passes.
- Docs support watcher/gates without ambiguity.
