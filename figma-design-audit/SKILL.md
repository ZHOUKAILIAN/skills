---
name: figma-design-audit
description: Use when a user provides a Figma URL, fileKey, or node-id and you need to exhaustively read Figma nodes, classify visible layers, derive design geometry, and produce audit artifacts before implementation.
---

# Figma Design Audit

## Goal

Produce a complete, read-only Figma audit package for a requested design boundary. The audit owns Figma facts: visible node coverage, terminal-depth traversal, node classification, geometry targets, visual specs, state examples, business-source questions, and unresolved blockers.

This skill does not write CSS, edit project code, choose implementation primitives, or perform final restoration acceptance review.

## Source Of Truth

Figma is the source of truth for visual facts: node tree, visibility, geometry, typography, colors, assets, visual hierarchy, and visual state examples.

Figma is not automatically the source of truth for business content, data fields, permissions, conditional branches, sorting, filtering, counts, copy ownership, or which records should render. Resolve those from user instructions, product requirements, existing implementation, API contracts, schema, runtime data, or another explicit business source.

When Figma visual evidence conflicts with PRD, existing implementation, API/schema, or another business source, record the conflict explicitly. Do not silently choose one source and continue. Unresolved conflicts that affect implementation or acceptance are blockers and require user or owner decision.

Wrong: hardcode sample names, counts, tabs, or selected rows because they are visible in Figma.
Right: record the sample as a visual example, resolve the business source, and ask the user only if available sources cannot answer it.

## Required Inputs

- A Figma URL, `fileKey`, `node-id`, or an explicit Figma boundary from the user.
- The requested audit boundary: component, frame, screen, popup, flow step, variant set, or state list.
- Any known business source the user wants prioritized, such as PRD, existing route/component, API contract, or owner document.
- An artifact location when the user needs durable files; otherwise report the audit inline with the same required sections.

If the Figma boundary is ambiguous, first inspect the available Figma metadata. Ask only when multiple plausible boundaries remain and choosing one would change scope.

If the user provides a list of states, treat it as the required seed state list, not as proof that the state set is complete. Audit every user-provided state, then actively look for additional states in Figma variants, visible alternate frames, interaction-proxy nodes, existing code branches, product requirements, schema, and analogous UI. Add confirmed states to the manifest. Only ask the user about remaining state gaps after available sources have been checked and the gap affects implementation or acceptance.

## When To Use

- The user provides a Figma URL, `fileKey`, or `node-id`.
- The user asks to read all child nodes, states, assets, variables, or specs before coding.
- A Figma restoration task needs an audit package before CSS implementation.
- A prior Figma audit may be incomplete and needs terminal-depth coverage or blocker cleanup.

## When Not To Use

- The user is asking how to implement CSS from an already-complete audit: use `css-best-practices`.
- The user wants a read-only comparison of existing UI against Figma: use `figma-restoration-review`.
- The task does not involve Figma node data.

## Mode And Fallback Rules

Preferred mode: use Figma MCP node data and metadata to traverse the boundary. If Figma MCP is unavailable, unauthenticated, or cannot read the requested node, stop and report `not ready`; do not fabricate values from images, memory, or visual guesses.

The current Figma restoration workflow does not support screenshot-based audit or acceptance. The required evidence is Figma node data and derived values that can be compared numerically against the implementation.

## Programmatic Assets

- `assets/templates/figma-audit-readme-template.md`: boundary audit report template.
- `assets/templates/figma-all-child-nodes-template.md`: exhaustive node ledger template.
- `assets/templates/figma-node-snapshot-template.json`: structured Figma node snapshot template used to prove every visible node was recursively read to a closed child tree.
- `assets/templates/figma-verification-template.md`: audit-gate verification template for proving the Figma audit package is handoff-ready.
- `scripts/verify_figma_audit.py`: checks the minimum audit contract for the README, node ledger, and Figma node snapshot.

Use the templates when the task needs durable audit artifacts. Use the verifier before marking the audit ready for CSS implementation.

## Workflow

1. Establish the audit boundary from the user request and the available Figma metadata.
2. Read the boundary to terminal depth and classify every visible node.
3. Resolve geometry, state, and business-source questions from Figma, code, docs, schema, runtime data, or user instructions.
4. Record blocking questions only after the available sources have been checked.
5. Write the audit README, node ledger, Figma node snapshot, and manifest or verification artifact when needed.
6. Run `scripts/verify_figma_audit.py --readme <README> --ledger <ALL_CHILD_NODES> --figma-snapshot <FIGMA_NODE_SNAPSHOT>` on durable artifacts.
7. If any gate fails, fix the specific failed item or stop and report `not ready`; do not hand off to CSS while blockers remain.

## Success Criteria

- The boundary is explicit and stable.
- Every in-scope visible node is read to terminal depth or explicitly excluded with reason.
- Every visible node has a classification and handling decision.
- Every implementation-affecting spacing or size value is derived from named Figma geometry.
- Vertical and horizontal closure pass for each major container.
- Every implementation-affecting state and business branch has a source or an explicit blocker.
- All blocking questions are grouped, resolved when possible, and empty before implementation handoff.
- The audit artifacts pass the local verifier with a Figma node snapshot.

## Verification

- Mechanical check: `scripts/verify_figma_audit.py --readme <README> --ledger <ALL_CHILD_NODES> --figma-snapshot <FIGMA_NODE_SNAPSHOT>`
- Snapshot check: the verifier compares every in-scope visible node id in `figma-node-snapshot.json` against the ledger. Missing, duplicate, unreadable, blocked, unknown, or unexpanded visible nodes fail verification.
- Tree closure check: every visible snapshot node must include `child_count` and `child_ids`; every `child_id` must exist in the snapshot; child parent links must point back to the parent; all visible nodes must be reachable from `root_node` through `child_ids`.
- Manual check: confirm the README includes source priority, blocking questions, geometry closure, state matrix, and readiness status; confirm the ledger includes every in-scope visible node and its terminal proof.
- Failure handling: if verification fails, repair the specific gap and rerun; if the gap cannot be resolved from available sources, report `not ready` with the failed gate and evidence.

## Required Audit Outputs

Before handoff to CSS implementation, produce:

- A restoration manifest when the task includes more than one screen, component boundary, state, variant, or flow step.
- A boundary README with scope, source priority, read basis, node classification, derived geometry, vertical and horizontal design closure, state matrix, business-source map, blocking questions, verification summary, and readiness status.
- A source conflict register when Figma visual facts and PRD, existing code, API/schema, runtime data, or user instructions disagree.
- A Figma node snapshot JSON listing every in-scope visible node read from Figma, including id, parent id, name, type, visibility, read status, child count, and child ids.
- A complete node ledger listing every in-scope visible node with classification, geometry, child count, expansion status, terminal proof, exclusion reason, or blocker reason.
- A blocking questions list when implementation-affecting uncertainty remains after available source checks.

If these artifacts are missing or fail verification, the audit is not ready for implementation.

## Exhaustive Node Read Gate

The audit is not complete until every in-scope visible node under the restoration boundary has been read to terminal depth.

Do not sample repeated items. Do not infer child structure from siblings. Do not stop at a frame, group, component, instance, icon wrapper, slot wrapper, or design-system shell just because the outer layer looks complete. Do not use images or screenshots as a substitute for node traversal.

Every visible node must appear in the node ledger with:

- Node id, parent id, name, type, visibility, depth, x, y, width, and height.
- Classification: `renderable-ui`, `platform-native`, `interaction-proxy`, or `annotation-demo-only`.
- Child count from the current read.
- Expansion status and expansion basis.
- Terminal proof, exclusion reason, or blocker reason.

Allowed ledger statuses:

- `expanded`: children were read and recorded.
- `terminal`: no readable child nodes remain.
- `excluded`: visible but outside product scope, with a reason.
- `blocked`: should be read but cannot be read with current access, tooling, or source data.

If any in-scope visible node remains `unknown`, `unexpanded`, or `blocked`, the audit cannot be marked ready for CSS implementation.

The node-read proof is the Figma node snapshot, not the README prose. The snapshot must be produced from recursive Figma reads, not manually invented, sampled, or inferred from sibling patterns. The snapshot must contain every in-scope visible node discovered during traversal, each node's `child_count`, and the exact `child_ids` returned by the read. `scripts/verify_figma_audit.py` must prove snapshot-vs-ledger coverage and snapshot child-tree closure before the audit can claim terminal coverage.

## Node Classification Gate

Classify every in-scope visible node before deciding how it should be handled:

- `renderable-ui`: product code should render this UI.
- `platform-native`: the host platform, runtime container, browser, operating system, or mini-program shell provides it.
- `interaction-proxy`: a static design representation of behavior, transition, gesture, selected state, expanded state, or temporary overlay.
- `annotation-demo-only`: notes, arrows, preview chrome, phone frames, presentation shells, or demo-only layers.

The audit must answer two questions for every visible node:

1. Is this node visually present in the design boundary?
2. Should it be rendered by product code, delegated to platform/runtime, converted into behavior/state, or excluded with rationale?

If classification cannot be resolved from Figma, code, platform conventions, or task context, add a blocking question.

## Geometry Audit Gate

Figma coordinates are design measurement evidence, not CSS implementation instructions.

Use Figma `x`, `y`, `width`, and `height` to derive target geometry:

- Parent insets.
- Sibling gaps.
- Element dimensions.
- Vertical and horizontal design closure for major containers.
- Typography, color, radius, shadow, asset, and state target values when exposed by Figma.

For every spacing or size value that may affect implementation, record the container, reference nodes, formula, and result.

Design closure belongs to the Figma audit:

- Vertical: `top inset + internal gaps + content heights + bottom inset = container height`.
- Horizontal: `left inset + internal gaps + content widths + right inset = container width`.

If closure does not pass, keep reading or mark the blocker. Do not decide CSS primitives here. CSS translation belongs to `css-best-practices`.

## Resolve-Before-Asking Gate

Do not ask the user about an unknown until you have tried to resolve it from available sources.

Critical rule: after available sources have been checked, any remaining uncertainty that affects implementation or acceptance is a blocker. Guessing is prohibited. Do not continue from inference, convention, likely intent, visual similarity, or "probably correct" assumptions when the fact cannot be proven by Figma data, code, docs, schema, runtime data, or a user answer.

Before adding an item to `Blocking Questions`, check whether it can be resolved from:

- Figma node tree, component/instance expansion, variables, styles, and metadata.
- Existing implementation code, component props, stores, hooks, API clients, schemas, fixtures, or seeded data.
- Product requirement, technical design, task text, or explicit user instruction.
- Existing analogous UI or interaction flow named by the user.
- Runtime or test data when available and in scope.

Ask the user when both are true:

1. The unknown affects implementation or acceptance.
2. It cannot be resolved from available sources.

Record each blocking question with:

- What is unknown.
- Why it matters.
- Sources checked.
- Decision needed from the user.

Do not interrupt the user one item at a time. During audit, collect blocking questions. After the first complete audit pass, ask the user one grouped batch of concise questions. After the user answers, update the audit artifacts and rerun the audit gate. If answers reveal new blockers, ask one follow-up batch.

The audit cannot hand off to CSS implementation while any blocking question remains unresolved.

## Source Conflict Gate

Figma owns visual facts. PRD, code, API/schema, runtime data, and user instructions may own product behavior and business facts. When those sources disagree, the audit must expose the disagreement instead of resolving it by preference.

Record each conflict with:

- Figma evidence: node id, value, visual state, or geometry.
- Business evidence: PRD line, code path, API/schema field, runtime value, or user instruction.
- Conflict impact: visual only, behavior, data binding, condition, copy ownership, acceptance, or implementation target.
- Proposed decision owner when known.
- Status: resolved, non-blocking, or blocking.

If a conflict affects implementation or acceptance and no explicit source priority or owner decision resolves it, mark it as blocking. Do not hand off to CSS implementation until the conflict is resolved or explicitly accepted as non-blocking.

## State Coverage Gate

State scope has two layers:

1. User-provided seed states: every state the user named must be represented in the restoration manifest and state matrix.
2. Discovered states: every implementation-affecting state discovered from Figma, code, product docs, schema, or analogous flows must be added, marked not applicable with evidence, or converted into a grouped blocking question.

Do not assume the user's state list is exhaustive. Do not assume a Figma visual state is business-owned. For each state, record the Figma node or source, visual delta, business trigger or source, implementation target, and whether code must change.

If a discovered state cannot be confirmed from available sources, include one grouped question after the audit pass. The audit is not ready while a required state is missing, silently skipped, or marked as unknown.

## Guardrails

- Read Figma and related source material only. Do not edit project code, CSS, component files, tests, design tokens, or product docs as part of this skill.
- Do not choose implementation primitives such as flex, grid, absolute positioning, fixed positioning, CSS variables, or unit conversion strategy. That belongs to `css-best-practices`.
- Do not perform final implementation acceptance review. That belongs to `figma-restoration-review` after implementation exists.
- Do not turn Figma sample content into product-owned business logic without a business source or resolved user answer.

## Image Boundary

Screenshot-based audit and visual diff are out of scope for the current restoration workflow. Do not request or require screenshots for Figma audit readiness.

The mandatory evidence is Figma node data, derived target values, and later implementation measurements that can be compared numerically. Do not use "looks close" as an audit result.

## Handoff Boundary

This skill ends when the Figma audit package is complete and ready for implementation handoff.

After this audit:

- Use `css-best-practices` to translate audited target geometry into maintainable CSS or project styling primitives.
- Use `figma-restoration-review` only for read-only acceptance review after implementation exists.

Do not put CSS layout strategy into this audit except to name values that must be preserved.

## Completion Signal

The audit is complete only when all conditions are true:

1. Boundary and source priority are explicit.
2. Every in-scope visible node appears in the ledger.
3. Every in-scope visible node is `terminal`, `expanded`, or `excluded`; no node is `unknown`, `unexpanded`, or unresolved `blocked`.
4. Every shell-capable node has expansion basis and terminal proof, or a blocking question has been answered and recorded.
5. Every visible node has a classification and handling decision.
6. Derived geometry includes named reference nodes and formulas for implementation-affecting sizes, insets, and gaps.
7. Vertical and horizontal design closure pass for each major in-scope container, or any exception is resolved and recorded.
8. State matrix covers all in-scope Figma visual states and separates business-driven states from visual examples.
9. Business-affecting content and branches have source coverage, or resolved user answers are recorded.
10. Blocking questions are empty or explicitly answered.
11. `scripts/verify_figma_audit.py` passes for generated README, ledger, and Figma node snapshot artifacts.

If any item is missing, report `not ready for CSS implementation` with the failed gate and evidence.

## Proof Package

When reporting audit completion or `not ready`, include:

- Artifact paths or inline sections produced.
- Boundary count, visible node count, terminal/expanded/excluded/blocked counts, and any skipped out-of-scope count.
- Figma node snapshot path and snapshot-vs-ledger coverage result.
- Figma reads and business sources inspected.
- Geometry closure status for each major container.
- Blocking questions asked and resolution status, or `none`.
- Verification command and result for `scripts/verify_figma_audit.py` when durable artifacts exist.
