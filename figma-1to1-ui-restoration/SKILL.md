---
name: figma-1to1-ui-restoration
description: |
  Use when a user provides a Figma URL or node ID and wants an existing UI aligned or a new UI implemented with exact 1:1 fidelity, especially when they ask to read all child nodes, states, assets, and specs before coding. Applies to components, popups, pages, partial modules, and both new implementations and refinements of an existing rough implementation.
---

# Figma 1:1 UI Restoration

Treat this work as scoped design auditing plus implementation convergence, not as "look at a screenshot and recreate it from memory".

## Positioning

This is the general orchestration skill for high-fidelity Figma restoration.

Use it to:

- define the boundary
- decide whether the task is refinement or new implementation
- decide which specialized audit skill must be invoked
- collect audit artifacts, verification evidence, and implementation results into one traceable flow

When a task clearly matches a specialized sub-skill, invoke that sub-skill as part of the workflow instead of keeping every concern inside this file:

- Use `figma-shell-expansion-audit` when the boundary contains important `instance`, component shell, icon wrapper, or other metadata-insufficient nodes.
- Use `figma-popup-sheet-restoration` when the boundary is a popup, modal, sheet, bottom sheet, or drawer-like container with overlay, header, content stack, and bottom action area.

## Goal

Given a Figma node boundary, fully read the real visible structure inside that boundary, derive the layout semantics from geometry, then converge the existing or new implementation until it matches the audited structure exactly enough to be traceable and verifiable.

## Success Criteria

Do not claim exact restoration unless all of the following are true:

1. The restoration boundary is explicit.
2. The boundary ledger covers every relevant visible node inside scope.
3. Every in-bound node is recursively expanded until it has no child nodes, instead of stopping at an instance shell, outer frame, or apparently complete visible layer.
4. Spacing is expressed as derived layout values, not guessed CSS terms.
5. Vertical spacing is closed mathematically:
   - `top inset + internal gaps + content heights + bottom inset = container height`
6. State differences are audited and translated into code branches where required.
7. Tests and broader verification have both been run.

If any item is missing, the audit is incomplete and implementation is not yet ready.

## Core Terms

Use these meanings consistently.

- `boundary`: the exact subtree or module included in the task
- `visible node`: a node that materially affects rendered output inside the boundary
- `terminal node`: a node that has no remaining implementation-relevant internal structure after required metadata traversal and shell expansion checks
- `shell node`: an outer frame, instance, or metadata wrapper whose internal visible structure still matters
- `derived spacing`: a layout value inferred from geometry, not a native Figma field
- `vertical closure check`: the accounting step that proves top inset, bottom inset, content heights, and internal gaps fully explain the container height
- `boundary coverage`: whether all in-scope visible nodes have been accounted for
- `terminal coverage`: whether every in-bound node has been expanded until there is no remaining implementation-relevant internal structure, unless that subtree is explicitly out of scope

## Hard Gates

These gates are mandatory.

### Gate 1: No Figma MCP, no audit

If Figma MCP is unavailable or unauthenticated, stop and provide setup instructions. Do not fabricate specs from screenshots, memory, or guesses.

### Gate 2: No ledger, no implementation

Do not write tests or production code until the node ledger is complete for the current boundary.

### Gate 3: No shell-only reads

Do not stop at the root screenshot, outer frame, or instance shell when the real visible structure is inside it.

If a node is an instance, component set, shell frame, or metadata rectangle:

- decide whether the visible implementation-critical structure is inside it
- if yes, continue reading child structure until there are no child nodes left
- record that the outer node was only a shell

### Gate 3.5: No non-terminal nodes in scope

Within the current boundary, keep reading until each node reaches a terminal state in metadata traversal.

This means:

- use `get_metadata` as the recursive source of truth for child expansion
- if a node still has child nodes, it is not fully read yet
- do not stop merely because the current level looks visually sufficient
- only stop recursion when the node has no child nodes left, or the boundary explicitly excludes that subtree

### Gate 3.6: Instance metadata is not completion proof

Do not treat `instance` or other shell-capable nodes as terminal merely because `get_metadata(node)` shows no children.

For nodes such as:

- `instance`
- component-like reusable shells
- icon wrappers
- slot-like wrapper nodes

You must also inspect `get_design_context(node)` when the node affects implementation.

If `get_design_context(node)` reveals internal structure, nested node ids, asset layers, text layers, or layout-critical descendants:

- treat the node as a shell
- record that metadata alone was insufficient
- use the revealed structure in the audit

Only mark such a node as terminal when both conditions are true:

1. metadata traversal is exhausted for the current boundary
2. design-context expansion did not reveal any additional implementation-relevant internal structure that remains unaudited

### Gate 4: No guessed spacing

Do not describe spacing as if Figma exposed `margin`, `padding`, or CSS `gap` directly.

Instead:

- read raw `x`, `y`, `width`, and `height`
- derive layout semantics from node relationships
- state which nodes were used for the derivation

### Gate 5: No vertical closure, no 1:1 claim

Do not claim exact restoration until top inset, bottom inset, content heights, and internal vertical gaps are accounted for with a closure equation.

### Gate 6: No unresolved critical unknowns

If a critical node is still marked `unknown`, `shell`, or unexpanded, do not start implementation. Either expand it or explicitly narrow the boundary first.

## Failure Modes To Prevent

Treat each item below as a concrete failure, not a style preference.

- Reading only the root screenshot and then starting implementation
- Recording only outer bounds while skipping the internal visible subtree
- Stopping at a node that still has child nodes in metadata
- Marking an instance as terminal only because metadata returned no children
- Listing width and height but never deriving top inset or bottom inset
- Computing only horizontal spacing while leaving vertical spacing implicit
- Saying "padding is about 16" without naming the reference nodes and formula
- Treating metadata bounds as the final shell when the real visible shell is inside the instance
- Claiming "all child nodes were read" while important nodes remain `unknown` or unexpanded
- Translating Figma directly into CSS terms without proving the geometry relationships first

## When To Use

- The user provides a Figma URL, `fileKey`, or `node-id`
- The user gives node IDs and wants them read to the deepest visible level
- The user says there is already a rough version and wants it aligned to Figma
- The user wants an existing page, popup, component, list, or card refined to match Figma exactly
- The user wants a new component or page implemented from Figma
- The user cares about font sizes, line heights, colors, insets, derived gaps, shell geometry, and state differences
- The user explicitly asks to read the full node information before development

## When Not To Use

- The user only wants a loose visual direction
- There is no Figma node and exact restoration is not required
- The real task is new product design rather than restoring an existing design

## Prerequisites

- A working Figma MCP connection is required for the strict 1:1 workflow
- The user should provide either:
  - A Figma URL containing `fileKey` and `node-id`
  - Or a currently selected node if the environment exposes a desktop Figma MCP server
- Exact restoration should not proceed from screenshots alone when node-level audit data is required

## Inputs

Extract as much as possible from the conversation before asking follow-up questions:

- Figma URL or `fileKey + nodeId`
- Access mode
  - Remote Figma MCP with URL parsing
  - Desktop Figma MCP with current selection, if available in the environment
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
3. A derived spacing audit
4. A verification plan
5. Existing implementation location or new implementation entry point
6. Test and code changes
7. Verification results

If the project allows analysis docs, prefer writing the audit into the project under `docs/analysis/`.

Suggested directory:

```text
docs/analysis/YYYYMMDD-figma-node-<root-node>-audit/
|- README.md
|- ALL_CHILD_NODES.md
`- VERIFICATION.md
```

If you do not want to start from scratch every time, prefer the bundled templates:

```text
assets/templates/figma-audit-readme-template.md
assets/templates/figma-all-child-nodes-template.md
assets/templates/figma-verification-template.md
```

## Programmatic Assets

This skill includes reusable assets:

- Templates in `assets/templates/`
- Audit verifier in `scripts/verify_figma_audit.py`

Read these assets and decide how to use them for the current task. Do not ignore them when the task needs audit artifacts or verification.

## Sub-Skills

This skill depends on:

- `figma-shell-expansion-audit`
- `figma-popup-sheet-restoration`

Invoke them when their scope matches the task. Do not duplicate their detailed shell or popup-specific logic here when the specialized skill is clearly the right fit.

## Workflow

### 0. Ensure Figma MCP is available before the audit

Before boundary definition or development, confirm how the Figma data will be read.

- If Figma MCP tools are already available and authenticated, continue to Step 1
- If the user provided a Figma URL, extract `fileKey` and `node-id` from it
- If the environment exposes a desktop Figma MCP server and the user is working from the current selection, use that mode instead of forcing a URL

If any Figma MCP call fails because the server is missing or unauthenticated, stop and set it up first:

1. Add the Figma MCP server:
   - `codex mcp add figma --url https://mcp.figma.com/mcp`
2. Enable the remote MCP client:
   - Set `[features].rmcp_client = true` in `config.toml`
   - Or run `codex --enable rmcp_client`
3. Authenticate:
   - `codex mcp login figma`
4. Restart Codex, then retry the task

If setup is required, finish the answer with the setup instructions and tell the user to retry after restart. Do not pretend the audit already happened.

### 1. Define the restoration boundary first

Before development, make the boundary explicit:

- Are you restoring only the root node, or its subtree?
- Are all states required?
- Are hover, active, selected, disabled, empty, full, or similar variants required?
- Are popup chrome, bottom bars, safe areas, or home indicators included?
- Is responsive or platform adaptation included?

If the user says "read until node X" or "all child nodes under this node", record that as the boundary rule and use it for every later read and code decision.

If the boundary is a popup, sheet, modal, drawer, or overlay module, invoke `figma-popup-sheet-restoration` before continuing the detailed audit.

### 2. Decide whether this is a refinement or a new implementation

Search the existing code first:

- Use `rg` for visible text, class names, component names, or page names
- If a rough version exists, refine that file directly
- Only create a parallel implementation if the user explicitly wants a new component or extraction

If the user says "just modify the original one", do not create a parallel implementation.

### 3. Follow project-specific documentation rules first

If the project has `AGENTS.md`, `CLAUDE.md`, requirement docs, or design docs:

- Read the relevant constraints first
- Reuse approved docs when possible
- Only add docs when the project requires them and they are missing

Do not bypass the project's workflow.

### 4. Build a complete node ledger with Figma MCP

Before development begins, complete at least one full read pass.

If the boundary contains shell-capable nodes that are likely to fool metadata traversal, invoke `figma-shell-expansion-audit` before declaring terminal coverage.

Read in this order:

1. `get_metadata(root)`
2. `get_design_context(root)`
3. `get_screenshot(root)`

Then expand until all important nodes inside the boundary are covered:

- Use `get_metadata` recursively to enumerate child nodes
- Call `get_design_context` on important child nodes
- Add `get_metadata(child)` where needed
- Add `get_screenshot(child)` where local visual confirmation helps
- Add `get_variable_defs` when variables or tokens matter
- Read recursively until each in-bound branch reaches nodes with no child nodes
- For instance or shell-capable nodes, use `get_design_context` to verify whether metadata-only traversal is sufficient
- Clearly mark which nodes are terminal, shell nodes, or intentionally out of scope

The ledger is not complete until:

- every critical visible node in the boundary has a status
- every in-bound traversed node is either terminal or explicitly excluded by the boundary rule
- important nodes are no longer ambiguous about whether they are shells or terminal descendants
- shell-capable nodes are not marked terminal without a shell expansion check
- unresolved nodes are either expanded or explicitly excluded by the boundary rule

Do not stop at the root screenshot.

### 5. Derive spacing from geometry instead of inventing CSS terms

Figma usually gives geometry, not implementation semantics.

Always derive spacing from node relationships:

- `top inset = first visible child.y - container.y`
- `bottom inset = (container.y + container.height) - (last visible child.y + last visible child.height)`
- `left inset = first visible child.x - container.x`
- `right inset = (container.x + container.width) - (last visible child.x + last visible child.width)`
- `sibling vertical gap = next.y - (current.y + current.height)`
- `sibling horizontal gap = next.x - (current.x + current.width)`

When using any derived value:

- name the container node
- name the reference child or sibling nodes
- write the formula in audit language
- separate raw geometry from the derived semantic label

Do not write "margin is 16" unless you have first shown which nodes produce that `16`.

### 6. Perform a vertical closure check

At least once for each major container, prove that the vertical structure closes.

Required accounting:

- top inset
- every visible child height in the main stack
- every internal vertical gap
- bottom inset
- container height

Required conclusion:

- the numbers either close exactly
- or you state the mismatch and keep reading because the audit is not complete yet

If the numbers do not close, do not start implementation.

### 7. Extract the right level of detail during the audit

Always try to capture:

- Root geometry and position
- Key child structure map
- Vertical rhythm expressed as derived values
- Horizontal insets expressed as derived values
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

### 8. Build a dedicated state matrix

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

### 9. Audit document structure

`README.md` should usually include:

- Boundary Rule
- Scope
- Read Basis
- Quick Facts
- Structure Map
- Root Geometry
- Derived Spacing
- Vertical Closure Check
- Shell vs Real Visible Bounds
- Unexpanded Nodes
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
- Depth
- Status
- Whether it was expanded
- Expansion basis
- Why it was not expanded, if not
- Completion proof
- Notes

Prefer starting from `assets/templates/figma-all-child-nodes-template.md`.

If audit files were written, validate them with the bundled verifier before implementation. If validation fails, the audit is still incomplete.

### 10. Choose between refining the original implementation and building fresh

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

### 10.5. Enforce the audit contract before implementation

If the task produced `README.md` and `ALL_CHILD_NODES.md` audit files:

- run the bundled verifier against those files
- treat any verifier failure as a hard stop
- do not begin tests or production code until the verifier passes

The verifier is meant to enforce engineering gates, not just narrative reminders.

### 10.6. Define the verification contract before claiming fidelity

Do not treat a single test type as proof of 1:1 restoration.

For high-confidence restoration, verify through multiple independent signals:

1. `structure check`
   - the audited boundary and terminal coverage are complete
   - shell nodes and excluded subtrees are explicitly accounted for
2. `geometry check`
   - key dimensions, insets, gaps, and alignment points are asserted from rendered output
   - use strict tolerances, usually `0px` when the platform allows it and at most `1px` when rendering differences are known
3. `content check`
   - text, typography, icon presence, asset wiring, and state branches match the audit
4. `visual diff check`
   - compare the implementation screenshot against the Figma screenshot at the same viewport, scale, and state
   - do not compare different crop regions or mismatched device scales
5. `state coverage check`
   - every in-scope Figma state has a matching implementation state and verification result

If one of these signals is missing, do not describe the result as `99% restored`.

### 10.7. Use visual regression as the final confidence layer

Visual regression is the last gate, not the first one.

Before visual diffing:

- lock viewport size
- lock device scale if the toolchain exposes it
- lock font loading and wait for the settled state
- lock the exact state and boundary crop
- remove or freeze dynamic data where possible

When reporting the result:

- state which screenshot was compared to which Figma node
- state the compared state name
- state the crop or viewport rule
- state the diff result in a measurable way
- call out any intentionally ignored regions

Do not use "looks close" as a verification result.

### 10.8. Use acceptance thresholds, not vague confidence

Prefer measurable gates such as:

- terminal coverage: `100%`
- vertical closure: `pass`
- key geometry tolerance: `<= 1px`
- required state coverage: `100%`
- visual diff status: `pass`

If a threshold is not met, report the failure directly. Do not soften it into "mostly restored".

### 11. Translate Figma numbers into project conventions

Do not copy values blindly.

Check the project's measurement system first:

- Web usually stays in `px`
- Uni-app / mini programs often map a `375px` frame to `750rpx`

If the file already uses `rpx`, translate using the project's established scale. If the file follows a different unit convention, stay consistent with that file.

### 12. Confirm assets and dependencies before coding

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

### 13. Use TDD for implementation

Whenever code changes are needed:

1. Update or add tests first
2. Run them once and confirm the new assertions fail for the expected reason
3. Then modify production code
4. Re-run the same tests until green
5. Then run broader verification

The key is not "tests were written". The key is "the new checks were seen failing first, then passing".

### 14. What to test

Prefer tests that lock down Figma geometry and state details:

- Header height and typography
- Close button size
- Double-shell card geometry
- Top inset and bottom inset
- Internal vertical gaps
- Horizontal insets
- CTA width and height
- State styling
- Real divider structure
- Presence of required state branches
- Correct asset wiring

Include node IDs in test names when practical for easier traceability.

### 15. Code change principles

- Prefer editing the original implementation rather than creating a parallel one
- Preserve existing business logic whenever possible
- Tighten structure and styling with minimal markup changes
- Use precise patches instead of rewriting entire files casually
- If the current code is just a rough version, continue tightening that exact implementation

### 16. Final verification

Always do at least two layers:

1. Targeted tests
2. A build or broader project verification command

For exact restoration work, prefer at least four layers:

1. Audit contract verifier
2. Geometry and content assertions
3. Visual diff for each important state
4. Build or broader project verification command

If `npm` or `node` is not on the default PATH:

- Find the working binary first
- Run verification with the full path

Do not skip verification just because the environment PATH is odd.

### 17. Visual final pass

When time allows, do one final visual check:

- Compare against the Figma screenshot
- Check small rhythm details, not only major blocks
- Check state switching
- Check scroll areas, safe areas, and popup shells
- Recheck top and bottom spacing, not just left and right alignment

## Suggested Response Structure

When reporting results, cover:

1. What the restoration boundary was
2. Which nodes were read and whether they reached terminal no-children state
3. Whether any shell nodes required deeper expansion
4. How derived spacing was computed
5. Whether the vertical closure check passed
6. Where the original implementation lives, or whether a new implementation was created
7. Which states are now covered
8. Which geometry, typography, state, and asset details changed
9. Which verification commands were run and what happened
10. Any remaining visual risk not yet covered
11. Whether the work met the threshold for `99% restored`

If implementation did not start because the audit contract is incomplete, say that explicitly instead of softening the failure.

## Practical Reminders

- If Figma MCP is missing or login has expired, stop after the setup instructions and tell the user to retry after restart
- If the user asks "did you read to the deepest layer?", answer in terms of boundary coverage and terminal coverage, not vague reassurance
- If the user asks for full child coverage, report whether every in-bound node reached a terminal no-children state
- If shell-capable nodes were present, report whether terminal status came from metadata only or from metadata plus design-context expansion
- If the user asks whether typography can be read, answer specifically: size, line height, weight, color, tracking, and related text specs
- If the user says "read all nodes before development", treat that as a strict gate
- If a rough implementation already exists, do not default to building a second version
- For complex pages, do not stop at the root node; expand important states and instance internals
- If any in-bound node still has child nodes in metadata, keep reading
- If a shell-capable node shows no children in metadata, verify it with design context before calling it terminal
- If Figma does not expose a direct spacing field, derive it from geometry and record the formula
- The value of 1:1 restoration is auditability, so always leave a traceable ledger, spacing derivation trail, and verification trail

## Example Tasks

- "Read `node-id=150-27773` and all child nodes under it until `150-27833`. I need font sizes, spacing, and exact specs before we compare."
- "Align the current UI to Figma. It only has a rough implementation right now, and the spacing, typography, and shells all need tightening."
- "There should already be a rough version of this component. Modify the original one directly. Do not create a new one."
- "Implement this popup from Figma, but read all nodes, states, assets, and variables before you start development."
- "This is not just for one page. Use the same workflow for all future Figma restoration tasks."
