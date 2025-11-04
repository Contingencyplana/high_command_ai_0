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

The fixtures intentionally capture only the stable fields that matter for the
contract. Dynamic values (timestamps, telemetry batch identifiers) are asserted
indirectly by the test runner and therefore do not need to appear in the JSON.

## Editing Guidelines

- Keep emoji chains short and focused on Level-0 templates so drift is obvious.
- When adding a new case, extend the test runner expectations to cover any new
  schema surface.
- Run `python -m tools.contract_test_runner` after editing fixtures to verify
  all cases still pass.
