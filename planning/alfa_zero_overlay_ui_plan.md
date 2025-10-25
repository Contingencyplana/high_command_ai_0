# Alfa Zero Overlay UI Plan

## 1. Objectives

- Provide an interactive overlay interface that maps the 16x16 Alfa Zero grid to dispatchable emoji chains via `OverlayBridge`.
- Surface translator feedback to operators in near real time (payload previews, status, telemetry hooks).
- Prepare the codebase for future integration with a graphical client while keeping a CLI fallback for automated testing.

## 2. Scope

- Implement a thin UI layer (initially terminal-based) that renders the grid, handles cell selection, and invokes `OverlayBridge.dispatch_cell`.
- Display confirmation payload metadata (chain name, template, outcomes, outbox file path) after each dispatch.
- Provide quick access to cell descriptions and available commands (help screen, list view).
- Support extensibility for additional cell mappings and future overlay modules.

Out of scope for this iteration:

- Networking or multiplayer synchronization.
- Full graphical rendering (reserved for later pivot).
- Persisted analytics dashboards (placeholder hooks only).

## 3. High-Level Design

- **UI Controller** (`alfa_zero_ui.py`): orchestrates rendering and input. Uses curses (or rich/textual if available) with a graceful fallback to simple ANSI printing.
- **Bridge Adapter**: wraps `OverlayBridge` calls, capturing payload summaries for UI display.
- **Telemetry Hook**: optional callback interface the UI can emit to (e.g., future logging, web socket bridge).

Component Diagram:

```text
User -> UI Controller -> Bridge Adapter -> OverlayBridge -> Emoji Translator -> Payload Outbox
             ^                  |
             |                  v
        Telemetry Sink <- Payload Summary
```

## 4. Implementation Steps

1. **Scaffold UI module**
   - Create `golf_00/delta_00/alfa_00/alfa_zero_ui.py` with command-line entry point.
   - Detect terminal capabilities; choose between curses and basic mode.
2. **Render grid**
   - Render 16x16 grid with coordinate headers; highlight mapped cells.
   - Provide legends for Heartday/Heartnight annotations (placeholder data for now).
3. **Handle input**
   - Accept keyboard navigation (arrow keys/WASD) and dispatch command (Enter/Space).
   - Provide command palette: `m` to show mappings, `i` for cell info, `q` to quit.
4. **Integrate bridge**
   - Instantiate `OverlayBridge` once per session.
   - On dispatch, call `dispatch_cell`, capture output path, and load payload summary for display.
5. **Feedback display**
   - Show last dispatched cell, chain name, description, outcomes, and outbox file.
   - Log errors prominently with remediation tips.
6. **Telemetry hook**
   - Add optional `--telemetry` flag to log payload metadata to JSONL or stdout.
   - Structure data for future overlay monitoring.
7. **Testing and validation**
   - Unit-test bridge adapter to ensure payload summaries serialize correctly.
   - Smoke-test both UI modes (curses and fallback) by simulating dispatch of mapped cells.

## 5. Future Enhancements

- Integrate actual graphical overlay client (e.g., PyGame, web UI) using the same adapter layer.
- Hook telemetry into analytics dashboards in `exchange/reports`.
- Extend cell mapping visualization to include emotional cosmology overlays (Heartday/Heartnight).

## 6. Open Questions

- Do we have constraints on terminal dependencies (e.g., allow `rich` library)?
- Should telemetry emit to existing exchange ledger formats or a new channel?
- How will the UI integrate with planned "real overlay" front-ends (determine API shape early)?
