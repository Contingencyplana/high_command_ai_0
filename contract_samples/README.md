# Contract Samples

This directory contains canonical emoji-runtime chains and their expected
factory-order projections. The data is consumed by
`tools/contract_test_runner.py` to verify that High Command and Toyfoundry stay
in lockstep on the payload contract.

## Layout

- `cases/` holds JSON fixtures. Each file defines a single contract case with:
  - the emoji chain to translate
  - adapter metadata to promote the payload into a factory-order
  - expectations for both the emoji-runtime payload and the resulting order

Current Level-0 coverage includes:

- `basic_ritual_victory.json` — core forge craft success baseline.
- `guarded_delivery_warning.json` — guarded delivery with qualifier emphasis.
- `signal_loop_gain.json` — signal loop scenario with gain outcome.
- `conditional_repeat_again.json` — conditional repeat with secondary outcome.
- `automation_path_happy_flow.json` — Order 044 automation comfort flow (forge delivers ally with target qualifier).

The fixtures intentionally capture only the stable fields that matter for the
contract. Dynamic values (timestamps, telemetry batch identifiers) are asserted
indirectly by the test runner and therefore do not need to appear in the JSON.

## Editing Guidelines

- Keep emoji chains short and focused on Level-0 templates so drift is obvious.
- When adding a new case, extend the test runner expectations to cover any new
  schema surface.
- Run `python -m tools.contract_test_runner` after editing fixtures to verify
  all cases still pass.

## Drafts

- Use `contract_samples/drafts/` for work-in-progress templates. Files here are
  not executed by the runner. When a draft is ready, move it into `cases/` and
  run the targeted case first, e.g.:

  - Template seed: `contract_samples/drafts/automation_path_happy_flow.json.template`
  - Promote under `cases/automation_path_happy_flow.json`
  - Validate: `python -m tools.contract_test_runner --case automation_path_happy_flow`
