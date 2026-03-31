---
name: figma-popup-sheet-restoration
description: |
  Use when the Figma restoration boundary is a popup, modal, sheet, bottom sheet, drawer, or overlay-style module that needs exact shell, spacing, and state restoration.
---

# Figma Popup Sheet Restoration

Audit and restore popup-style modules with strict attention to overlay, sheet shell, header chrome, content stack, bottom actions, and safe-area geometry.

## Goal

Restore popup and sheet modules with exact structure and spacing, especially the vertical relationships that commonly drift during implementation.

## When To Use

- bottom sheet
- modal popup
- drawer-like panel
- overlay dialog
- popup with title bar and close action
- popup with bottom CTA or safe-area treatment

## Success Criteria

Do not claim popup fidelity unless all of the following are true:

1. Overlay and sheet container are both accounted for.
2. Header shell, title, and close action are audited.
3. Main content stack is vertically closed.
4. Row or option states are explicitly listed.
5. Bottom action area and safe-area treatment are either included or explicitly out of scope.

## Popup Audit Shape

Always identify these regions when present:

- overlay or mask
- sheet container
- header row
- close action
- primary content rows
- selection or input rows
- bottom CTA area
- safe area or home indicator

## Hard Gates

### Gate 1: Do not collapse overlay and sheet into one box

Audit the overlay and the sheet container separately when both are present.

### Gate 2: Title row is not just text

For popup headers, read:

- title text
- close affordance
- header shell background
- top inset inside the sheet

### Gate 3: Vertical closure is mandatory

For the popup content stack, prove:

- top inset
- header height
- row heights
- row-to-row gaps
- bottom inset
- optional CTA or safe-area block

### Gate 4: Selected and unselected rows are separate states

If the popup contains selectable rows, do not treat selected and unselected appearances as the same state.

## Output Contract

Report:

- popup boundary
- shell structure map
- top inset and bottom inset
- row stack formula
- selected vs unselected state differences
- whether bottom CTA and safe area are in scope

## Failure Modes To Prevent

- Treating the popup as a flat white rectangle
- Ignoring overlay opacity and sheet shell
- Auditing only the row content while skipping the header or close affordance
- Computing left and right alignment but not top and bottom spacing
- Treating selected and unselected rows as one visual state
- Forgetting the safe area or home indicator when it is visually part of the module

## Practical Rule

If a popup looks simple, verify it twice. Popup drift usually comes from shell geometry, not from the obvious text nodes.
