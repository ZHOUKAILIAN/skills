---
name: css-best-practices
description: Use when writing, reviewing, or refining CSS where layout, positioning, sizing, spacing, responsiveness, maintainability, or design-tool-to-code translation matters.
---

# CSS Best Practices

Write CSS as maintainable layout and styling rules, not as copied coordinates. UI should move correctly with containers, content, state, and viewport.

## Project Baseline

Before changing CSS, identify the project's styling system: CSS modules, scoped CSS, utilities, Tailwind, Less/Sass, tokens, components, breakpoints, and naming. Use existing primitives unless they cause the layout failure.

## Layout Standard

- Prefer document flow, flex, grid, inline layout, padding, gap, and content sizing for ordinary stacks, rows, cards, forms, lists, navigation, and button groups.
- Treat parent insets and sibling gaps as coupled layout relationships. Do not encode them as unrelated `top` / `left` offsets.
- Use grid for two-dimensional alignment. Use flex for one-direction flow, alignment, or distribution.
- Do not mirror every design-tool frame as a DOM node unless it carries layout, styling, semantics, or interaction.
- Avoid layout rules that only work for the current copy length, item count, or viewport size.

## Sizing And Units

- Prefer intrinsic sizing, `min-*` / `max-*`, `fr`, percentages, `auto`, and content-aware constraints when content can vary.
- Use fixed width or height only when the component contract requires it: icons, avatars, thumbnails, fixed-size controls, measured media, or a deliberately fixed canvas.
- Prefer project spacing tokens or existing scale values. If exact values are required for visual parity, keep them local and explain why they cannot use the token scale.
- Handle wrapping, truncation, min-width, and overflow intentionally. Do not rely on one happy-path string.

## Responsive Standard

- Verify the layout at the relevant container or viewport sizes before calling it done.
- Prefer container-aware rules for components reused in multiple parent widths.
- Follow the project's breakpoint direction. Do not mix desktop-first and mobile-first rules in one file without a reason.
- Check horizontal scroll, overlap, clipping, broken wrapping, and touch-target regressions.

## Positioning Boundary

Avoid `position:absolute`, `position:fixed`, manual `top` / `left`, and large local z-index stacks for ordinary content.

Positioning is acceptable when the element is genuinely out of flow:

- Modal masks, drawers, popovers, tooltips, dropdown menus, and anchored overlays
- Badges, notification dots, close buttons, and other small anchored affordances
- Decorative layers that intentionally overlap content
- Sticky or fixed platform/navigation chrome
- Canvas-like or game-like surfaces where coordinates are the product behavior

If positioning is necessary, keep it scoped to the smallest stable container, define the anchor, and verify affected states and viewport sizes.

## Figma And Design-Tool Input

Design-tool coordinates are measurement evidence, not implementation instructions. Convert coordinates into layout intent before writing CSS:

- Container inset becomes padding or grid/flex alignment
- Repeated vertical or horizontal spacing becomes gap
- Row text and actions become flex or grid alignment
- Repeated cards or list items become a reusable flow layout
- Intentional overlaps become documented positioning exceptions.

Wrong: copy every text, icon, and row into `position:absolute` with design-tool coordinates.
Right: use padding and gap for the container, flex or grid for rows, and positioning only for intentional out-of-flow layers.

## Completion Signal

CSS work is complete only when all applicable checks pass:

- Ordinary content participates in document flow, flex, grid, or inline layout.
- Every positioning exception is justified by an out-of-flow role and scoped to a stable anchor.
- Fixed dimensions are limited to contract-required cases or documented visual-parity constraints.
- The layout has been checked against relevant content states, item counts, and viewport or container sizes.
- No unresolved overlap, clipping, accidental horizontal scroll, or broken wrapping remains.
