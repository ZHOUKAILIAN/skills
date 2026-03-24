---
name: figma-1to1-ui-restoration
description: |
  General Figma restoration workflow: fully read the Figma nodes, child nodes, states, assets, and key specs within the target scope before starting development or code changes, then converge the implementation to true 1:1 fidelity. Use this skill whenever the user says things like "align to Figma", "restore 1:1", "implement this from Figma", "read all child nodes under this node", "tighten the rough version", or "read the full node information before development". It applies to components, popups, pages, partial modules, and both new implementations and refinements of an existing rough implementation.
---

# General Figma 1:1 Restoration Workflow

Treat this work as scoped design auditing plus implementation convergence, not as "look at a screenshot and recreate it from memory".

Default goals:

1. Define the restoration boundary first
2. Fully read every relevant node inside that boundary
3. Find the existing implementation or decide the correct new entry point
4. Only then write tests and production code
5. Lock the result with verification

## First Principle

**Before development starts, all relevant node information inside the target boundary must be read.**

"All relevant nodes" includes:

- The user-specified root node
- All child nodes inside the current task boundary
- Important state nodes
- Visible real structure inside key instances
- Assets, text, typography, colors, sizes, spacing, radius, and variables that affect implementation

If the scope is too large, define the boundary first and then read everything inside that boundary. Do not start coding while still relying on guesses.

## When To Use

- The user provides a Figma URL, `fileKey`, or `node-id`
- The user gives node IDs and wants them read to the deepest visible level
- The user says there is already a rough version and wants it aligned to Figma
- The user wants an existing page, popup, component, list, or card refined to match Figma exactly
- The user wants a new component or page implemented from Figma
- The user cares about font sizes, line heights, colors, padding, gaps, shell geometry, and state differences
- The user explicitly asks to read the full node information before development

## When Not To Use

- The user only wants a loose visual direction
- There is no Figma node and exact restoration is not required
- The real task is new product design rather than restoring an existing design

## Inputs

Extract as much as possible from the conversation before asking follow-up questions:

- Figma URL or `fileKey + nodeId`
- Child nodes or states the user explicitly calls out
- Target boundary
  - Single component
  - Popup or sheet
  - Partial module
  - Full page
- Target code file or page
- Target platform
  - Web
  - Uni-app / mini program
  - React / Vue / other
- Task mode
  - New implementation
  - Directly modifying an existing rough implementation
  - Multiple states in scope
- Whether the user explicitly wants the original implementation edited in place

## Outputs

At minimum, produce:

1. A boundary definition
2. A Figma audit
3. Existing implementation location or new implementation entry point
4. Test and code changes
5. Verification results

If the project allows analysis docs, prefer writing the audit into the project under `docs/analysis/`.

Suggested directory:

```text
docs/analysis/YYYYMMDD-figma-node-<root-node>-audit/
├── README.md
└── ALL_CHILD_NODES.md
```

If you do not want to start from scratch every time, prefer the bundled templates:

```text
assets/templates/figma-audit-readme-template.md
assets/templates/figma-all-child-nodes-template.md
```

## Workflow

### 0. Define the restoration boundary first

Before development, make the boundary explicit:

- Are you restoring only the root node, or its subtree?
- Are all states required?
- Are hover, active, selected, disabled, empty, full, or similar variants required?
- Are popup chrome, bottom bars, safe areas, or home indicators included?
- Is responsive or platform adaptation included?

If the user says "read until node X" or "all child nodes under this node", record that as the boundary rule and use it for every later read and code decision.

### 1. Decide whether this is a refinement or a new implementation

Search the existing code first:

- Use `rg` for visible text, class names, component names, or page names
- If a rough version exists, refine that file directly
- Only create a parallel implementation if the user explicitly wants a new component or extraction

If the user says "just modify the original one", do not create a parallel implementation.

### 2. Follow project-specific documentation rules first

If the project has `AGENTS.md`, `CLAUDE.md`, requirement docs, or design docs:

- Read the relevant constraints first
- Reuse approved docs when possible
- Only add docs when the project requires them and they are missing

Do not bypass the project's workflow.

### 3. Build a complete node ledger with Figma MCP

Before development begins, complete at least one full read pass.

Read in this order:

1. `get_metadata(root)`
2. `get_design_context(root)`
3. `get_screenshot(root)`

Then expand until all important nodes inside the boundary are covered:

- Call `get_design_context` on important child nodes
- Add `get_metadata(child)` where needed
- Add `get_screenshot(child)` where local visual confirmation helps
- Add `get_variable_defs` when variables or tokens matter
- Read down to the deepest visible leaf level
- Clearly mark which nodes are leaves, outer frames, or instance shells

**Hard rule: do not write production code until the boundary node inventory is complete.**

Do not stop at the root screenshot.

### 4. Extract the right level of detail during the audit

Always try to capture:

- Root geometry and position
- Key child structure map
- Vertical rhythm
- Horizontal insets
- Typography: size, line height, weight, tracking, color
- Icon sizes
- Button sizes, radius, and colors
- State differences
  - Default
  - Selected
  - Full
  - Disabled
  - Empty
  - Hover / pressed / focus when relevant to platform
- All visible text
- Images, icons, illustrations, or SVG assets
- Design tokens or variables
- Whether metadata bounds differ from the instance's real visible shell

Pay special attention to misleading outer bounds, for example:

- Metadata shows `8px`
- But the instance actually contains a `24px` shell

In cases like that, implementation should follow the real internal structure, not the metadata rectangle alone.

### 5. Build a dedicated state matrix

A single screenshot summary is not enough.

If the component or page has multiple states, list at least:

- State name
- Node ID
- Whether geometry changes
- Whether copy changes
- Whether colors change
- Whether shell structure changes
- Which differences must become code branches

Recommended format:

```text
| State | Node | Key differences | Must change in code |
| --- | --- | --- | --- |
| default | ... | ... | yes |
| selected | ... | ... | yes |
| disabled | ... | ... | yes |
```

### 6. Audit document structure

`README.md` should usually include:

- Boundary Rule
- Scope
- Read Basis
- Quick Facts
- Structure Map
- Root Geometry
- Vertical Rhythm
- State Matrix
- Asset Inventory
- Detailed Read
- Current Read Outcome

Prefer starting from `assets/templates/figma-audit-readme-template.md`.

`ALL_CHILD_NODES.md` should contain the full ledger:

- Node ID
- Parent
- Name
- Relative x/y
- Width / height
- Notes

Prefer starting from `assets/templates/figma-all-child-nodes-template.md`.

### 7. Choose between refining the original implementation and building fresh

There are two modes:

1. Tighten an existing rough implementation
2. Build a new implementation from Figma

If a rough implementation already exists:

- Preserve the existing business logic
- Tighten structure, styling, and state branches first
- Do not rewrite everything just because a fresh file looks cleaner

If no implementation exists:

- Create the new component or page
- But still complete the node ledger before coding

### 8. Translate Figma numbers into project conventions

Do not copy values blindly.

Check the project's measurement system first:

- Web usually stays in `px`
- Uni-app / mini programs often map a `375px` frame to `750rpx`

If the file already uses `rpx`, translate using the project's established scale. If the file follows a different unit convention, stay consistent with that file.

### 9. Confirm assets and dependencies before coding

If the restoration includes:

- SVGs
- Images
- Icons
- Illustrations
- Variables or tokens

Confirm first whether you should:

- Reuse existing project assets
- Use assets returned by Figma
- Download and wire Figma assets into the project

Do not ship a placeholder asset implementation while pretending the design is fully restored.

### 10. Use TDD for implementation

Whenever code changes are needed:

1. Update or add tests first
2. Run them once and confirm the new assertions fail for the expected reason
3. Then modify production code
4. Re-run the same tests until green
5. Then run broader verification

The key is not "tests were written". The key is "the new checks were seen failing first, then passing".

### 11. What to test

Prefer tests that lock down Figma geometry and state details:

- Header height and typography
- Close button size
- Double-shell card geometry
- Gap, padding, and insets
- CTA width and height
- State styling
- Real divider structure
- Presence of required state branches
- Correct asset wiring

Include node IDs in test names when practical for easier traceability.

### 12. Code change principles

- Prefer editing the original implementation rather than creating a parallel one
- Preserve existing business logic whenever possible
- Tighten structure and styling with minimal markup changes
- Use precise patches instead of rewriting entire files casually
- If the current code is just a rough version, continue tightening that exact implementation

### 13. Final verification

Always do at least two layers:

1. Targeted tests
2. A build or broader project verification command

If `npm` or `node` is not on the default PATH:

- Find the working binary first
- Run verification with the full path

Do not skip verification just because the environment PATH is odd.

### 14. Visual final pass

When time allows, do one final visual check:

- Compare against the Figma screenshot
- Check small rhythm details, not only major blocks
- Check state switching
- Check scroll areas, safe areas, and popup shells

## Suggested Response Structure

When reporting results, cover:

1. What the restoration boundary was
2. Which nodes were read and whether they reached leaf level
3. Where the original implementation lives, or whether a new implementation was created
4. Which states are now covered
5. Which geometry, typography, state, and asset details changed
6. Which verification commands were run and what happened
7. Any remaining visual risk not yet covered

## Practical Reminders

- If the user asks "did you read to the deepest layer?", answer in terms of boundary coverage and leaf-node coverage, not vague reassurance
- If the user asks whether typography can be read, answer specifically: size, line height, weight, color, tracking, and related text specs
- If the user says "read all nodes before development", treat that as a strict gate
- If a rough implementation already exists, do not default to building a second version
- For complex pages, do not stop at the root node; expand important states and instance internals
- The value of 1:1 restoration is auditability, so always leave a traceable ledger and verification trail

## Example Tasks

- "Read `node-id=150-27773` and all child nodes under it until `150-27833`. I need font sizes, spacing, and exact specs before we compare."
- "Align the current UI to Figma. It only has a rough implementation right now, and the spacing, typography, and shells all need tightening."
- "There should already be a rough version of this component. Modify the original one directly. Do not create a new one."
- "Implement this popup from Figma, but read all nodes, states, assets, and variables before you start development."
- "This is not just for one page. Use the same workflow for all future Figma restoration tasks."
