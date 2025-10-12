# Contributing Guide

Thank you for supporting the High Command AI workspace. To keep SHAGI safe and disciplined, please follow the workflow below when proposing changes:

## 1. Prepare Your Environment

1. Install dependencies: `pip install -r requirements.txt`.
2. Initialize the exchange submodule if you need to work with orders: `git submodule update --init --recursive`.
3. Run `python -m tools.forge.cli validate` to ensure templates and configs are healthy.

## 2. Coding Standards

- Prefer small, documented scrolls or scripts over monolithic changes.
- Use Forge commands (`forge init-alfa`, `forge hydrate`, etc.) instead of manual file generation when possible.
- Keep comments purposeful—focus on doctrine, safety, or non-obvious logic.
- Follow the schema definitions in `planning/command_exchange_protocol.md` when emitting payloads.

## 3. Testing and Validation

- Run `pytest` before submitting patches.
- Validate any exchange payloads with `python tools/schema_validator.py <path>`.
- If you modify Forge, include CLI dry-run output or relevant logs in your notes.

## 4. Commit Discipline

- Reference the relevant order/report IDs in commit messages when responding to directives.
- Do not rebase shared branches without coordination; prefer merge commits for audit trails.
- Keep commits scoped and descriptive (e.g., `Order 2025-10-12-003: automate receiver scheduling`).

## 5. Pull Requests

1. Outline the change, the motivating order, and validation steps in the PR description.
2. Request review from another High Command maintainer.
3. Ensure the CI (tests, validators) passes before merging.

## 6. Safety Procedures

- Respect lock files (`forge.lock`, `safety.lock`); do not remove them without authorization.
- Escalate immediately if you observe entropy spikes or schema violations in the exchange.
- For urgent fixes, coordinate via the exchange repository so all theatres stay informed.

By contributing, you agree to abide by the Code of Conduct and the SHAGI safety doctrine.
