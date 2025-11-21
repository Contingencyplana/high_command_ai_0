# DSLs vs GPLs for High Command Languages

Status: working note / guardrails
Scope: emoji-first (Pivot Five), music-first (Pivot Six), synergy-first (Pivot Nine, dormant horizon)

## Purpose

- Start each *_first language as a tight domain-specific language (DSL) to ship fast, keep intent legible, and harden safety.
- Promote to a general-purpose language (GPL) only when open-ended composition is required and the ergonomics survive the added freedom.
- Provide tests for graduation so we avoid accidental GPL creep.

## DSL-first stance (why)

- Faster stabilisation: small, fixed verb/noun sets mean fewer breaking changes and clearer telemetry.
- Safety and accessibility: constrained grammars reduce blast radius and ease validation (emoji validators, motif validators).
- Tooling focus: invest in editors, translators, and validators that deeply understand the domain instead of chasing every edge case.
- Translation agility: shared JSON bindings let DSLs interoperate early without broad surface area.

## Maturity ladder

| Stage | Meaning | Allowed moves |
|-------|---------|---------------|
| DSL | Fixed lexicon and shape; single host/runtime; validators required. | Add verbs/qualifiers only with validator updates and docs. |
| Extended DSL | Adds limited modifiers (state, tempo, context tags) but still closed world. | Introduce namespacing or small config files; keep IO narrow. |
| Transition | Turing-complete or near; modules/imports under review; IO/FFI gated. | Run pilot modules, measure safety and ergonomics, tune lint/format. |
| GPL | Open composition, modules, IO/FFI, safety defenses in place, tooling parity (formatter, lints, debugger). | Ship SDKs, package format, long-term stability guarantees. |

## Graduation criteria (must be green)

- Grammar stability: N consecutive clean validator or canary runs against the full corpus (emoji after Pivot Five gates; motifs after Pivot Six gates).
- Composition: functions or macros with scoping rules; module or import story defined; deterministic execution order.
- IO and FFI: explicit policy for side effects, state, and external calls; sandbox defaults; audit hooks.
- Tooling: formatter, lints, schema docs, stepping or debug signals, minimal standard library.
- Performance envelope: latency and footprint budgets published and met on reference hardware.
- Safety: clear error model, safe defaults, and rollback paths; misuse outcomes documented.

## Guardrails to avoid accidental GPL creep

- No implicit loops, dynamic eval, or open IO until the Transition stage.
- Every new verb or qualifier ships with tests, validator updates, docs, and a rollback plan.
- Prefer embedding DSLs in a host (Python or TypeScript) over inflating the DSL to handle edge orchestration.
- Keep escape hatches declarative (for example, adapters defined in JSON) rather than arbitrary code injections.
- Freeze lexicon changes once a translation bridge is live until telemetry shows stability.

## Interop and layering

- Shared JSON schema is the Rosetta stone: emoji <-> JSON <-> music, with host adapters kept thin.
- Canonical validators must agree across modalities; translators fail closed and never silently coerce.
- Host SDKs expose the DSL as data-first with no hidden control flow.
- Telemetry quilts should log both surface tokens and normalized JSON to detect drift.

## Language snapshots

- Emoji-first (Pivot Five) - Active. Remains a DSL until the Level-0 and Level-1 lexicon is stable, canary history is clean, and a module or import story exists. GPL promotion requires scoped functions or macros, IO and FFI policy, formatter or lints or debug hooks, and a small standard library (collections, time, math) without sacrificing emoji ergonomics.
- Music-first (Pivot Six) - Exploratory. Prototype as a motif DSL mirrored to the emoji lexicon. Hold GPL ambitions until audio validators, latency budgets, and accessibility signals (audio-first missions) are proven. Any module or IO features must trail emoji by at least one maturity tier.
- Synergy-first (Pivot Nine) - Dormant horizon. Mentioned for completeness; revisit only after emoji and music reach Transition. Keep synergy experiments embedded in hosts rather than inventing new control structures.

## Non-goals (for now)

- No package manager or arbitrary user code execution inside the DSL runtimes.
- No implicit network or file IO; all side effects must be explicit adapters.
- No silent widening of grammar (for example, auto-converting unknown glyphs or notes).
- No conflation of modality concerns (emoji rules stay visual; music rules stay temporal) until shared abstractions are proven.

## Immediate actions

- Keep emoji-first strictly DSL while finishing validator coverage and telemetry gates (see new_major_pivot_5.md).
- For music-first experiments, pair every new motif with emoji or JSON round-trip tests and latency tracking.
- Park synergy-first ideas in host-level prototypes; open the DSL only after staging criteria are met.
