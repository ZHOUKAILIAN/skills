---
name: task-standard
description: Use when writing, auditing, or improving task-oriented skills that produce verifiable artifacts and need task-local gates to prevent shortcutting or false completion claims.
---

# Task Standard

Task skills help the agent complete a concrete class of work. A good task skill does not ask the agent to "do a good job"; it defines the artifact, the source of truth, the gates that prevent shortcuts, and the proof required before completion.

Use this skill for task-oriented skills such as document generation, spreadsheet editing, design implementation, browser testing, customer-service investigation, data seeding, API research, code generation, and coverage generation.

## Core Rule

Completion is not a statement. Completion is a verified match between the produced artifact and the skill's success criteria.

Wrong: "Done."
Right: "Produced X, verified it with Y, skipped Z because ..., remaining risk is ..."

## Required Shape

A task skill should usually contain:

- `Goal`: the artifact or outcome the task must produce.
- `When To Use` and `When Not To Use`: routing boundaries.
- `Required Inputs`: information needed before safe execution.
- `Source Of Truth`: the authoritative facts, docs, data, design, logs, or code.
- `Mode And Fallback Rules`: preferred path, allowed fallbacks, and stop conditions.
- `Workflow`: ordered phases or a decision tree.
- `Local Anti-Laziness Gates`: task-specific checks that block known shortcuts.
- `Available Assets`: scripts, templates, references, APIs, CLIs, or helpers.
- `Guardrails`: read/write boundaries, credentials, environment, approval, and safety limits.
- `Success Criteria`: objective conditions that prove the artifact is acceptable.
- `Verification`: how those criteria are checked.
- `Proof Package`: what evidence the final answer must report.

## Local Anti-Laziness Gates

Anti-laziness rules must live inside the task skill, near the workflow they gate. The shared standard can name the pattern; the task skill must name the exact shortcut and the exact check.

For each task skill, ask:

1. What shortcut would let the agent falsely claim completion?
2. What observable artifact proves the shortcut did not happen?
3. What mechanical check can inspect that artifact?
4. What must happen if the check fails?

Good: "Node ledger verification must pass before Figma implementation starts."
Bad: "Inspect the design carefully."

Good: "Render every slide to PNG and fix visual QA failures before delivery."
Bad: "Make the deck look good."

Good: "Every Feishu record must be mapped to a journey or marked no-E2E-applicable with reason before tests are generated."
Bad: "Cover the important records."

## Gate Patterns

Use only the gate patterns that fit the task. Do not copy all of them into every skill.

### Scope Accounting

Use when the task processes multiple nodes, pages, records, slides, rows, files, routes, screenshots, tests, or user journeys.

The task skill should require an item ledger or equivalent accounting with:

- Stable item identity.
- Group or parent when hierarchy matters.
- Expected count or source count when available.
- Status for each item: processed, verified, excluded, blocked, or not applicable.
- Reason for every excluded, blocked, skipped, or not-applicable item.
- Completion proof for every processed item.

Default stance: zero unaccounted in-scope items. If partial coverage is acceptable, the skill must define the allowed gap explicitly.

### Gate Artifacts

Use when the task has phases and a later phase depends on evidence from an earlier phase.

Good gate artifacts include:

- Node ledger before design implementation.
- Rendered page or slide screenshots before visual delivery.
- Spreadsheet recalculation output before workbook delivery.
- DOM snapshot before browser actions.
- Log/code/database evidence table before root-cause reporting.
- Test discovery summary before generating new tests.

Gate artifacts are not decorative. A later phase must use them to decide whether to continue.

### Mechanical Verification

Use mechanical checks whenever the task has a checkable artifact:

- scripts or validators
- renderers
- linters or type checks
- formula recalculators
- screenshots or visual diffs
- DOM snapshots
- log queries
- SQL or API count checks
- file existence and content checks

If a mechanical check is not possible, the skill must define the manual inspection evidence required instead.

### Failed-Gate Behavior

Every task skill must say what happens when verification fails.

Allowed outcomes:

- Fix the specific failed criterion and re-run the check.
- Stop and report `not ready`, including the failed criterion and evidence.

Not allowed:

- Mention the failure and still claim completion.
- Continue into the next phase when the failed gate was meant to block that phase.
- Convert a failed check into vague residual risk without explaining why the task can still be considered complete.

## Modes And Fallbacks

If a task can run in multiple modes, choose one mode before execution.

Examples:

- Read-only review vs code implementation.
- Built-in tool vs CLI fallback.
- Generate-only vs generate-and-run.
- Local artifact creation vs project-bound asset update.

Fallback rules must be explicit:

- preferred path
- fallback trigger
- whether user approval is required
- whether the fallback changes output quality, safety, credentials, or verification
- what to do if fallback is unavailable

Fallback is never permission to bypass the source of truth, safety boundary, or completion signal.

## Source Of Truth

Every task skill must name the authority for facts and acceptance.

Examples:

- Official docs for API guidance.
- Figma node data for exact design restoration.
- User-provided Feishu records for change scope.
- Runtime logs, code, and database records for incident investigation.
- Rendered artifact output for documents, slides, sheets, images, and web pages.

Screenshots, summaries, memory, and model guesses can support the task only when the skill says they are acceptable sources.

## Success Criteria

Success criteria must be objective enough that the agent can check them.

Good:

- "All in-scope records are accounted for, generated tests follow existing naming conventions, and skipped execution is reported with reason."
- "The final report includes Symptoms, Action, Code Problem, Why it happened, Impact, and Evidence, with each section backed by named evidence."
- "The rendered artifact has no clipped text, unresolved overlap, missing assets, or formula errors."

Bad:

- "Implement cleanly."
- "Make it high quality."
- "Write a useful report."

## Proof Package

The final answer for a task skill must report evidence, not confidence.

The proof package should include:

- Artifact produced or changed.
- Source-of-truth inputs inspected.
- Scope counts when the task is multi-item.
- Verification checks run and their pass/fail status.
- Skipped or impossible checks with reason.
- Failed gates and whether they were fixed, re-run, or left as blockers.
- Residual risk only when it affects confidence in completion.

## Audit Completion Signal

A task-skill audit is complete only when:

- The task skill's artifact or outcome is concrete.
- Trigger and non-trigger cases are clear.
- Required inputs and source of truth are named.
- Modes and fallbacks are explicit when more than one path exists.
- Workflow phases include task-local anti-laziness gates for known shortcuts.
- Multi-item work has scope accounting or an explicit reason it does not need it.
- Gate artifacts are consumed by later phases rather than decorative.
- Mechanical verification is used where practical.
- Verification failure loops back or stops with `not ready`.
- Success criteria are objective.
- Final output requires a proof package.
- Any missing standard is reported with a concrete file location and suggested fix.
