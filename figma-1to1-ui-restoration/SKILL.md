---
name: figma-1to1-ui-restoration
description: |
  Use when a user provides a Figma URL, fileKey, or node-id and wants an exact 1:1 UI implementation or restoration for a component, popup, page, or partial module.
---

# Figma 1:1 UI Restoration

Given a Figma node boundary, exhaustively read every visible node to terminal depth, derive all layout values from geometry, then implement or refine the code until it demonstrably matches the audited structure.

## Goal

Read every visible node inside the restoration boundary until no child nodes remain, derive spacing from geometry with named reference nodes, then converge implementation until multi-layer verification passes. The standard is data-backed fidelity — not "looks about right".

## Governing Rule

When the user asks for exact restoration, this skill governs fidelity decisions. In that mode, Figma is the primary visual source of truth. Existing design-system components, project tokens, or prior code may be reused only after proving they preserve the audited geometry, structure, and state coverage.

## When To Use

- The user provides a Figma URL, `fileKey`, or `node-id`
- The user wants existing UI aligned to match Figma exactly
- The user wants a new component, page, popup, or module implemented from Figma
- The user asks to read all child nodes, states, assets, and specs before coding

## Programmatic Assets

This skill includes reusable assets in `assets/templates/` and a verifier script in `scripts/`. Read them to understand their purpose and use them when the task needs audit artifacts or verification.

The verifier script checks the minimum audit contract for the boundary README and node ledger. Use it to confirm the audit is structurally complete before claiming the task is ready for implementation or verification.

## Required Audit Outputs

Before implementation, produce audit artifacts for the restoration boundary:

- A boundary README that records scope, node classification decisions, derived spacing, vertical closure, shell-node notes, state matrix, verification status, and unresolved unknowns
- A complete node ledger listing every in-scope visible node with expansion status and completion proof

If these artifacts are missing, the audit is not complete.

## Constraints

### Figma MCP is mandatory

If Figma MCP is unavailable or unauthenticated, stop immediately. Tell the user to configure it. Do not fabricate specs from screenshots, memory, or guesses.

### Classify nodes before deciding how to implement them

Every in-scope visible node must be classified before implementation. Use one of these classes:

- **Renderable UI** — implement as app-rendered UI
- **Platform-native** — provided by the host platform, runtime container, or operating system
- **Interaction-proxy** — a static design representation of behavior, transition, gesture, selection, expansion, or another interactive state
- **Annotation / demo-only** — notes, arrows, preview chrome, phone frames, or presentation-only layers

Do not treat all visible nodes as static pixels to recreate. The audit must answer both:

1. Is this node visually present in the design?
2. Should this node be rendered by product code, delegated to the platform, converted into behavior, or excluded as annotation?

### Platform-native nodes must not be blindly cloned

Host-native UI such as WeChat capsule buttons, OS status bars, home indicators, browser chrome, system keyboards, container-provided nav chrome, or runtime-safe-area affordances may appear in Figma as visual context. These are not automatically part of the product surface.

When a node is platform-native:

- Do not recreate it as ordinary business UI unless the product explicitly owns a custom version
- Record it as `platform-native` in the audit with the reason
- Map it to platform configuration, runtime behavior, safe-area handling, or explicit out-of-scope treatment

### Interaction-proxy nodes must become behavior, not frozen pixels

Some Figma layers exist only to communicate interaction: pressed states, selection samples, open sheets, swipe hints, picker wheels, hotspot shells, transient overlays, or expanded examples. These may look like static nodes in MCP output, but they should often be translated into state, transitions, or trigger behavior rather than copied as always-visible UI.

When a node is an interaction-proxy:

- Record the state or behavior it represents
- Link it to the relevant state-matrix entry
- Do not leave it as a permanently rendered static layer unless the product actually shows it that way

### Boundary before everything

Make the restoration boundary explicit before any development: which nodes, which states, which variants are in scope. If the boundary is a popup/sheet/modal/drawer, audit overlay and sheet container separately.

### State matrix before implementation

List every in-scope state before writing code. This includes selection states, visibility states, empty/populated states, loading states, permission states, popup open/closed states, and any user-specific branches such as "my row" vs ordinary rows.

Do not implement from a default screenshot alone. If a state exists in the boundary and affects layout, content, or styling, it must appear in the state matrix.

### Complete node ledger before implementation

Do not write tests or production code until the node ledger is complete. Every in-scope visible node must be recursively expanded until it has no child nodes — do not stop at an instance shell, outer frame, or apparently complete layer.

The ledger is not complete until:

- Every in-scope visible node has a terminal/shell/excluded status
- No node is left as "unknown" or "unexpanded"
- Shell-capable nodes are not marked terminal without expansion proof

### Shell nodes require expansion proof

Nodes of type `instance`, component-like reusable containers, icon wrappers, slot wrappers, and named design-system shells must not be marked terminal merely because metadata shows no children. Design-context expansion is required when the node affects implementation. Only mark such a node terminal when both metadata traversal is exhausted AND design-context expansion reveals no additional unaudited structure.

If in doubt, expand. One extra expansion costs less than a false fidelity claim.

### Screenshot supports the audit, but does not replace it

Use screenshots for visual comparison and state matching. Do not use a screenshot as justification to skip node traversal, skip shell expansion, or guess spacing values.

### Spacing must be derived from geometry with proof

Figma does not expose CSS semantics. Derive insets and gaps from raw `x`, `y`, `width`, `height` of parent and child nodes. For every spacing value used in implementation:

- Name the container node and the reference child/sibling nodes
- Write the derivation formula
- Do not say "padding is 16" without showing which nodes produce that 16

### Follow `css-best-practices` before writing CSS

Use `css-best-practices` to translate audited Figma geometry into maintainable CSS. Figma coordinates are measurement evidence; they are not permission to recreate every layer with absolute coordinates. Record any positioning exception with the reason, anchor, and affected state.

### Vertical closure is required

For each major container, prove: `top inset + internal gaps + content heights + bottom inset = container height`. If the numbers do not close, keep reading — the audit is not complete. Do not start implementation until closure passes.

### Refine before rewriting

Search the existing codebase first. If a rough version exists, refine that file directly. Only create a new implementation if none exists or the user explicitly requests it.

### Inventory existing interaction component owners before rebuilding controls

When the Figma boundary contains an interactive control or an open transient state, search for existing product components that already own that behavior before creating new UI. This applies to date/time pickers, picker wheels, sheets, modals, drawers, popovers, tabs, segmented controls, and form controls with existing state logic.

For each matching candidate, record:

- Component path and name
- Behavior it owns
- Visual and state gaps against the Figma audit
- Reuse decision: direct reuse, prop/wrapper adapter, style variant, or rejected with proof

Do not duplicate picker, sheet, modal, or control behavior while an existing owner can preserve the interaction contract and meet the audited visual target through props, a wrapper, an adapter, or a variant. If visual parity conflicts with behavior ownership, prefer extending the existing behavior owner with the smallest variant unless the audit proves it cannot satisfy the required states.

Wrong: Figma shows an open month picker, so the implementation creates a new picker component from the visible wheel layers.
Right: The audit identifies the existing date picker and shared sheet components, keeps the behavior owner, and adds only the required variant or adapter to match the audited shell.

### Follow project conventions

Check the project's measurement system (px, rpx, rem, etc.) and stay consistent with existing code. Do not copy Figma pixel values blindly into a project that uses different units.

### Reuse existing code only with parity proof

Reusing an existing component is allowed only when it can be shown to preserve the audited structure, geometry, assets, and states. If reuse forces the implementation away from the audited result, do not reuse it.

### Figma values outrank project defaults in exact-restoration mode

When the user explicitly wants 1:1 restoration, do not silently snap spacing, sizes, radii, typography, or assets back to design-system defaults. Any deviation from the Figma audit must be explicit, justified, and recorded as a deviation.

### Unknowns must remain visible

If any in-scope node, state, or geometry relationship remains unresolved, record it as an explicit unknown or blocker. Do not close the task with softened language such as "mostly matched" or "close enough".

## Key Information To Capture

Every audit must cover:

- Root geometry and position
- Full child structure map with depth
- Derived vertical and horizontal spacing (with formulas)
- CSS strategy required by `css-best-practices`
- Typography: size, line height, weight, tracking, color
- Colors, borders, radius, shadows
- Icon and button sizes
- State differences (default, selected, disabled, hover, empty, full, etc.) as a state matrix
- All visible text, images, icons, SVG assets
- Design tokens or variables
- Shell vs real visible bounds discrepancies
- Node classification result for each special node: renderable, platform-native, interaction-proxy, or annotation/demo-only
- Handling decision for non-renderable nodes: delegated to platform, converted into behavior/state, or excluded with rationale
- Existing interaction component owner inventory for behavior-heavy UI, including accepted reuse/adaptation or rejection proof
- Reuse or deviation decisions, with proof when existing code or tokens are kept

## Verification

Do not claim restoration based on a single signal. The baseline five layers are required, plus the component reuse check when the boundary contains behavior-heavy UI:

1. **Structure** — boundary and terminal coverage are 100% complete
2. **Geometry** — key dimensions, insets, gaps asserted from rendered output (tolerance ≤0.5px)
3. **Content** — text, typography, icons, assets, and state branches match the audit
4. **Visual diff** — implementation screenshot vs Figma screenshot at same viewport, scale, and state
5. **State coverage** — every in-scope state has a matching implementation and verification result
6. **Component reuse** — existing interaction component owners are recorded, and any new behavior-heavy component is justified by behavior or parity proof

Geometry verification must include a `css-best-practices` check. Any `absolute` or `fixed` positioning in the restored boundary must have a recorded reason tied to an out-of-flow layer.

Use measurable thresholds. Do not use "looks close" as a verification result.

Record the outcome for each layer. If a layer could not be run, say why and keep the task open.

## Completion Signal

The task is complete only when ALL of the following are verified:

1. The restoration boundary is explicit and recorded.
2. Every in-scope visible node has been read to terminal depth (no child nodes remaining).
3. Every shell-capable node has expansion basis and completion proof recorded.
4. Spacing is derived with named reference nodes and formulas.
5. Vertical closure passes for each major container.
6. State matrix covers all in-scope states.
7. All required verification layers (structure, geometry, content, visual diff, state, and component reuse when applicable) have been run.
8. CSS strategy satisfies `css-best-practices`, and every `absolute` or `fixed` positioned element has a justified out-of-flow reason.
9. No unresolved critical unknowns remain in the ledger.
10. Any reused component or token has parity proof, or the deviation is explicitly recorded.
11. Any behavior-heavy control has an existing component inventory, with reuse/adaptation accepted or rejection justified.
12. Every non-renderable node has an explicit handling decision: platform delegation, behavior translation, or justified exclusion.

If any item is missing, say so explicitly — do not soften it into "mostly restored".

## Popup / Sheet / Modal / Drawer

When the boundary is an overlay-style module, also ensure:

- Overlay/mask and sheet container are audited separately
- Header shell, title, and close action are accounted for
- Main content stack vertical closure passes
- Row or option states are explicitly listed (selected vs unselected are separate states)
- Bottom action area and safe-area treatment are either included or explicitly out of scope
