---
name: figma-1to1-ui-restoration
description: Use when a user provides a Figma URL, fileKey, or node-id and wants an exact 1:1 UI implementation or restoration for a component, popup, page, or partial module.
---

# Figma 1:1 UI Restoration

## Core Rule

Treat this skill as the coordinator for exact Figma-to-code restoration. It does not own the detailed Figma audit rules, CSS implementation rules, or final read-only review rules. It routes the task through the right owner skill and blocks phase changes when the previous phase has not produced verifiable evidence.

## Priority

User intent sets the top-level goal, but phase ownership is fixed: `figma-design-audit` owns Figma facts, `css-best-practices` owns implementation strategy, and `figma-restoration-review` owns read-only acceptance review. This skill only sequences those phases and stops handoff when the required evidence is missing.

## Active Mode

Use this skill only when the user wants implementation or restoration, not read-only review.

If the user asks only to inspect Figma before coding, use `figma-design-audit`. If the user asks only to compare an existing implementation against Figma, use `figma-restoration-review`.

## Workflow

1. Run the Figma fact-gathering phase with `figma-design-audit`.
2. Do not write application code until the Figma audit says `Ready for implementation: yes` and has no unresolved blocking questions.
3. Run the implementation phase with `css-best-practices`, using the audited Figma values as measurement evidence and the project codebase as the implementation context.
4. Preserve product-owned business logic unless a PRD, API/schema, existing source of truth, or explicit user answer changes it.
5. After implementation exists, use `figma-restoration-review` for read-only acceptance review when the user asks for review, the task requires fidelity sign-off, or the implementation has high visual risk.

## Handoff Gates

### Audit To Implementation

The handoff from `figma-design-audit` to `css-best-practices` is allowed only when:

- Every in-scope visible node has terminal-depth coverage or a recorded exclusion.
- Every visible node is classified as `renderable-ui`, `platform-native`, `interaction-proxy`, or `annotation-demo-only`.
- Geometry values are derived from Figma node data with named reference nodes and closure checks.
- Business-affecting Figma samples are mapped to a source or resolved user answer.
- Blocking questions are empty or explicitly answered.
- The audit verifier passes when durable audit artifacts exist.

If the audit is `not ready`, keep working in the audit phase or ask the grouped blocking questions produced by `figma-design-audit`.

### Implementation To Review

The handoff from implementation to `figma-restoration-review` is allowed only after the relevant source files are changed and runnable or inspectable. The review skill is read-only and should report deviations, not patch code.

## Ownership Boundaries

| Area | Owner skill |
| --- | --- |
| Figma node traversal, visible node classification, measurement evidence, state examples, blocking questions | `figma-design-audit` |
| CSS/layout/styling implementation strategy, unit conversion, flow vs absolute positioning, maintainability | `css-best-practices` |
| Post-implementation fidelity review and deviation checklist | `figma-restoration-review` |
| This skill | Phase sequencing, handoff gates, and final proof package |

## Red Flags

- "The screenshot looks clear enough" -> return to `figma-design-audit`; screenshots do not replace node traversal or geometry derivation.
- "The Figma audit has blockers, but the likely answer is obvious" -> resolve from sources or ask the grouped questions before implementation.
- "Figma x/y means every node should be absolutely positioned" -> use `css-best-practices`; Figma coordinates are measurement evidence, not CSS strategy.
- "Review found deviations, so fix them inside the review skill" -> switch back to implementation mode; `figma-restoration-review` is read-only.

## Completion Signal

This coordinated restoration is complete only when:

- The Figma audit phase is complete or its blocker status is explicitly reported.
- Implementation changes, if requested, follow `css-best-practices` and preserve business-source decisions.
- Any requested or high-risk fidelity review has been run with `figma-restoration-review`, or skipped with reason.
- The final response reports the audit artifacts, implementation files changed, verification commands/results, unresolved blockers, and review outcome if run.
