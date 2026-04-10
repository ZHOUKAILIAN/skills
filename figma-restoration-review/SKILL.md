---
name: figma-restoration-review
description: |
  Review an existing UI implementation against a Figma design for restoration fidelity. Use when a user provides a Figma URL or node ID and wants to verify how closely their code matches the design. Outputs a structured deviation checklist — does not modify code.
---

# Figma Restoration Review

Given a Figma design reference and an existing implementation, systematically compare every auditable dimension and produce a structured deviation checklist ranked by severity. This skill is read-only — it never modifies source code.

## Goal

Identify every gap between the Figma source of truth and the current implementation, report each gap with measurable evidence (expected vs actual), and rank them so the developer knows what to fix first. "Looks close" is not a review result — every claim must be backed by node data or measurement.

## When To Use

- The user provides a Figma URL, `fileKey`, or `node-id` and wants to **review** an existing implementation
- The user asks to audit, check, or verify how closely their code matches a Figma design
- The user wants a deviation report, fidelity check, or restoration quality review
- The user wants to know what is wrong or missing before a design sign-off

## When NOT To Use

- The user wants to **implement** or **build** UI from Figma — use the `figma-1to1-ui-restoration` skill instead
- The user wants code changes or fixes applied — this skill only reports deviations

## Relationship to `figma-1to1-ui-restoration`

The `figma-1to1-ui-restoration` skill governs development — it produces audit artifacts, derives geometry, and implements code. This skill governs **acceptance review** — it reads the same Figma data and compares it against what already exists. The two skills share the same fidelity standard and tolerance thresholds but serve different stages of the workflow.

## Constraints

### Figma MCP is mandatory

If Figma MCP is unavailable or unauthenticated, stop immediately. Tell the user to configure it. Do not fabricate specs from screenshots, memory, or guesses.

### Read-only — never modify code

This skill produces a deviation checklist only. Do not edit, create, or delete any source files. If the user wants fixes applied, tell them to use `figma-1to1-ui-restoration` or apply the fixes manually.

### Read the implementation before reviewing

Read the actual source files that render the UI under review. Do not rely on assumptions about what the code does — open the files, trace the component tree, and extract the real values used in the implementation.

### Derive Figma values from geometry — read ALL nodes first, then calculate

Follow the same geometry-derivation approach as `figma-1to1-ui-restoration`: derive spacing from raw `x`, `y`, `width`, `height` of parent and child nodes. Do not assume spacing from visual appearance alone.

**Figma node trees are often asymmetric.** Child nodes under the same parent may have different depths, different sub-structures, or inconsistent grouping. Do not assume sibling nodes share the same structure. The correct process is:

1. Read **every** visible child node to terminal depth — do not stop early because the first few siblings look similar.
2. Collect the full set of absolute coordinates (`x`, `y`, `width`, `height`) for every terminal node.
3. **Only after all nodes are read**, compute spacing, insets, and gaps by comparing coordinates between adjacent nodes and their parent.

Computing spacing from a partial node read will produce wrong numbers. If a node has not been read yet, its spacing has not been derived yet — period.

### Geometry review must be strict

Geometry is the highest-stakes dimension. Apply these rules without exception:

- Every spacing value in the implementation must be traceable to a Figma geometry derivation (parent coord minus child coord, sibling coord difference, etc.).
- Name both reference nodes for every derivation — e.g., "gap between NodeA (y + height = 120) and NodeB (y = 132) = 12 px".
- If the Figma layout uses irregular spacing (different gaps between visually similar siblings), each gap must be derived and checked individually. Do not average or approximate.
- Vertical closure check: for key containers, verify `top inset + sum of child heights + sum of gaps + bottom inset = container height`. If it does not close, the node read is incomplete — go back and re-read.
- Horizontal closure check: apply the same logic horizontally for row-like containers.

## Review Dimensions

Every review must cover all five dimensions. Do not skip a dimension — if it cannot be evaluated, say why.

### 1. Structure

Compare the DOM / component hierarchy against the Figma node tree. Check for:
- Missing or extra structural nodes
- Incorrect nesting or hierarchy order
- Components that should exist but are absent
- Wrapper or container mismatches

### 2. Geometry

Compare dimensions, spacing, insets, and gaps. Tolerance: **<= 0.5 px is pass; > 0.5 px is a deviation**.

- Width and height of key containers and elements
- Horizontal and vertical padding / insets (derive from Figma geometry with named reference nodes)
- Gaps between sibling elements
- Absolute position offsets where applicable

### 3. Style

Compare visual styling properties:
- Colors (background, text, border, shadow) — compare as hex/rgba
- Font family, size, weight, line-height, letter-spacing
- Border radius
- Box shadow / drop shadow parameters
- Opacity
- Border width, style, color

### 4. Content

Compare rendered content against Figma:
- Text strings and copy
- Icon identity and size
- Image resources and aspect ratios
- Placeholder or empty-state content

### 5. State Coverage

Check that every in-scope interactive or conditional state is implemented:
- Default, hover, pressed, disabled, focused, selected states
- Empty vs populated data states
- Loading / skeleton states
- Error states
- Permission-gated or user-specific branches (e.g., "own item" vs "other's item")

If states exist in the Figma design but have no corresponding implementation, report each as a deviation.

## Deviation Checklist Format

Present findings as a structured list. Each deviation entry must include:

| Field | Description |
|---|---|
| **Severity** | `critical`, `major`, or `minor` |
| **Dimension** | One of: Structure, Geometry, Style, Content, State |
| **Figma Reference** | Node name or node-id in the Figma file |
| **Expected** | The value or behavior specified by the Figma design |
| **Actual** | The value or behavior found in the implementation |
| **Location** | Source file path + line number, or CSS selector / component name |

### Severity Definitions

- **`critical`** — Structural element missing or not implemented; state entirely absent; visually obvious error (color completely wrong, > 2 px geometry deviation, wrong icon or image)
- **`major`** — Geometry deviation between 0.5–2 px; font property mismatch (wrong weight, size, or line-height); border-radius or shadow missing; minor structural reorder that affects layout
- **`minor`** — Geometry deviation <= 0.5 px that technically exceeds tolerance but is barely perceptible; subtle letter-spacing or opacity difference; non-critical asset variation

## Review Process

1. **Establish the Figma boundary** — Confirm the target node-id or URL. Identify which nodes and states are in scope for this review.

2. **Read the Figma node tree** — Use Figma MCP to traverse all visible child nodes to terminal depth within the boundary. Derive geometry values from node coordinates.

3. **Read the implementation** — Open the source files that render the corresponding UI. Trace the component tree and extract actual values (dimensions, colors, fonts, structure, assets, states).

4. **Compare dimension by dimension** — For each of the five review dimensions, systematically compare the Figma audit data against the implementation data. Record every deviation.

5. **Classify and rank deviations** — Assign severity to each deviation per the definitions above. Sort the final checklist by severity (critical first, then major, then minor).

6. **Produce the deviation checklist** — Output the structured checklist. Include a summary count (e.g., "3 critical, 5 major, 2 minor").

7. **State unknowns explicitly** — If any node could not be evaluated (e.g., a state that requires runtime interaction to verify), record it as an unresolved item rather than silently skipping it.

## Completion Signal

The review is complete only when ALL of the following are true:

1. The review boundary is explicit and recorded.
2. Every in-scope visible Figma node has been read to terminal depth.
3. The implementation source files have been read (not assumed).
4. All five review dimensions (structure, geometry, style, content, state) have been evaluated — or explicitly marked as unevaluable with a reason.
5. Every deviation is recorded with severity, dimension, expected vs actual, and location.
6. No in-scope node or state has been silently skipped.
7. A summary count of deviations by severity is provided.

If any item is missing, say so explicitly — do not close the review with "mostly matches" or "looks close".
