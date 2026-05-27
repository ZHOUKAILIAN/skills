---
name: zhoukailian-ui-aesthetic-preferences
description: Use when designing, implementing, reviewing, or restoring UI for Zhou Kailian, especially Figma 1:1 work, frontend CSS, mini-program pages, popups, charts, or visual polish tasks.
---

# Zhou Kailian UI Aesthetic Preferences

## Core Rule

Separate visual source of truth from business source of truth. Figma defines style, geometry, states, and layout intent; existing business logic, product rules, API contracts, and real data define what should be shown.

Use `css-best-practices` when writing CSS. Use `figma-1to1-ui-restoration` for implementation from Figma and `figma-restoration-review` for read-only visual acceptance when applicable.

## Source Of Truth

- Figma node data, screenshots, variables, and measured geometry for visual values.
- Existing code, product docs, APIs, logs, and data contracts for behavior and conditional content.
- Runtime screenshots on the target viewport/device for final visual evidence.

## Aesthetic Defaults

- Prefer exact, restrained product UI over decorative layouts. Operational tools should be dense, scannable, and predictable.
- Match geometry, spacing, font size, color, radii, shadow, image crop, icon placement, and text wrapping to the design unless a business rule requires a documented deviation.
- Reuse existing components, tokens, and design-system patterns before creating one-off styles.
- Keep CSS standards technology-oriented, not Figma-scenario-oriented. A shared standard should discuss layout, flex/grid, positioning, responsiveness, and component reuse rather than one specific restoration task.
- Avoid hard-coding a single Figma case into reusable components unless the component is explicitly variant-bound.
- Avoid nested cards, marketing-style hero sections for tools, over-rounded panels, one-note palettes, and generic purple/blue gradient aesthetics.
- Use icons for tool actions when an icon exists. Keep button labels short and ensure text never clips on mobile.

## Workflow

1. Identify every target state and viewport before implementation. Common states include logged out, first screen after login, loading/pagination, detail view, empty state, and error state.
2. Build a state matrix with state ID, Figma node/case, trigger, input data, expected rendering, and verification method.
3. Compare Figma against business logic. If they conflict, document the conflict and ask before silently choosing one.
4. Implement with existing components and responsive constraints. Prefer layout primitives over absolute positioning unless the design truly requires fixed geometry.
5. Verify with runtime screenshots and, for Figma restoration, a visual diff or review report that lists blocking/high-priority differences and their resolution.

## Anti-Shortcuts

- Wrong: assume the static Figma text or sample data is the real product content.
- Right: use Figma for style and locate the code/API rule that decides dynamic content.

- Wrong: say "looks close" after code inspection only.
- Right: inspect the rendered page on the target viewport and compare against the design.

- Wrong: create broad CSS rules for a one-off Figma screen.
- Right: use component-scoped styles unless the rule is a real reusable standard.

## Completion Signal

UI work is ready only when all in-scope states are accounted for, the runtime screen was inspected, important visual differences are recorded or fixed, and the final response names the screenshots, checks, or review evidence used.
