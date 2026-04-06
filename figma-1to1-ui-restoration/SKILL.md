---
name: figma-1to1-ui-restoration
description: |
  Use when a user provides a Figma URL or node ID and wants exact 1:1 UI restoration. Applies to components, popups, pages, and partial modules. Requires exhaustive node traversal, geometry-derived spacing, and multi-layer verification.
---

# Figma 1:1 UI Restoration

Given a Figma node boundary, exhaustively read every visible node to terminal depth, derive all layout values from geometry, then implement or refine the code until it demonstrably matches the audited structure.

## Goal

Read every visible node inside the restoration boundary until no child nodes remain, derive spacing from geometry with named reference nodes, then converge implementation until multi-layer verification passes. The standard is data-backed fidelity — not "looks about right".

## When To Use

- The user provides a Figma URL, `fileKey`, or `node-id`
- The user wants existing UI aligned to match Figma exactly
- The user wants a new component, page, popup, or module implemented from Figma
- The user asks to read all child nodes, states, assets, and specs before coding

## When Not To Use

- The user only wants a loose visual direction without exact restoration
- No Figma node is available

## Programmatic Assets

This skill includes reusable assets in `assets/templates/` and a verifier script in `scripts/`. Read them to understand their purpose and use them when the task needs audit artifacts or verification.

## Constraints

### Figma MCP is mandatory

If Figma MCP is unavailable or unauthenticated, stop immediately. Tell the user to configure it. Do not fabricate specs from screenshots, memory, or guesses.

### Boundary before everything

Make the restoration boundary explicit before any development: which nodes, which states, which variants are in scope. If the boundary is a popup/sheet/modal/drawer, audit overlay and sheet container separately.

### Complete node ledger before implementation

Do not write tests or production code until the node ledger is complete. Every in-scope visible node must be recursively expanded until it has no child nodes — do not stop at an instance shell, outer frame, or apparently complete layer.

The ledger is not complete until:

- Every in-scope visible node has a terminal/shell/excluded status
- No node is left as "unknown" or "unexpanded"
- Shell-capable nodes are not marked terminal without expansion proof

### Shell nodes require expansion proof

Nodes of type `instance`, component-like reusable containers, icon wrappers, slot wrappers, and named design-system shells must not be marked terminal merely because metadata shows no children. Design-context expansion is required when the node affects implementation. Only mark such a node terminal when both metadata traversal is exhausted AND design-context expansion reveals no additional unaudited structure.

If in doubt, expand. One extra expansion costs less than a false fidelity claim.

### Spacing must be derived from geometry with proof

Figma does not expose CSS semantics. Derive insets and gaps from raw `x`, `y`, `width`, `height` of parent and child nodes. For every spacing value used in implementation:

- Name the container node and the reference child/sibling nodes
- Write the derivation formula
- Do not say "padding is 16" without showing which nodes produce that 16

### Vertical closure is required

For each major container, prove: `top inset + internal gaps + content heights + bottom inset = container height`. If the numbers do not close, keep reading — the audit is not complete. Do not start implementation until closure passes.

### Refine before rewriting

Search the existing codebase first. If a rough version exists, refine that file directly. Only create a new implementation if none exists or the user explicitly requests it.

### Follow project conventions

Check the project's measurement system (px, rpx, rem, etc.) and stay consistent with existing code. Do not copy Figma pixel values blindly into a project that uses different units.

## Key Information To Capture

Every audit must cover:

- Root geometry and position
- Full child structure map with depth
- Derived vertical and horizontal spacing (with formulas)
- Typography: size, line height, weight, tracking, color
- Colors, borders, radius, shadows
- Icon and button sizes
- State differences (default, selected, disabled, hover, empty, full, etc.) as a state matrix
- All visible text, images, icons, SVG assets
- Design tokens or variables
- Shell vs real visible bounds discrepancies

## Verification

Do not claim restoration based on a single signal. All five layers are required:

1. **Structure** — boundary and terminal coverage are 100% complete
2. **Geometry** — key dimensions, insets, gaps asserted from rendered output (tolerance ≤1px)
3. **Content** — text, typography, icons, assets, and state branches match the audit
4. **Visual diff** — implementation screenshot vs Figma screenshot at same viewport, scale, and state
5. **State coverage** — every in-scope state has a matching implementation and verification result

Use measurable thresholds. Do not use "looks close" as a verification result.

## Completion Signal

The task is complete only when ALL of the following are verified:

1. The restoration boundary is explicit and recorded.
2. Every in-scope visible node has been read to terminal depth (no child nodes remaining).
3. Every shell-capable node has expansion basis and completion proof recorded.
4. Spacing is derived with named reference nodes and formulas.
5. Vertical closure passes for each major container.
6. State matrix covers all in-scope states.
7. All five verification layers (structure, geometry, content, visual diff, state) have been run.
8. No unresolved critical unknowns remain in the ledger.

If any item is missing, say so explicitly — do not soften it into "mostly restored".

## Popup / Sheet / Modal / Drawer

When the boundary is an overlay-style module, also ensure:

- Overlay/mask and sheet container are audited separately
- Header shell, title, and close action are accounted for
- Main content stack vertical closure passes
- Row or option states are explicitly listed (selected vs unselected are separate states)
- Bottom action area and safe-area treatment are either included or explicitly out of scope
