---
name: agent-team-traceability
description: Use when inspecting, designing, or fixing agent-team or AI_Team workflow traceability, skill injection, stage prompts, artifacts, state files, or PRD/Dev/QA/Acceptance handoffs.
---

# Agent Team Traceability

## Goal

Make an agent-team or AI_Team run reproducible and debuggable across Product, Dev, QA, Acceptance, and human decision stages. The user expects to see what entered each stage, which skills were used, what prompt reached the executor, what artifact came out, and why a later gate passed or failed.

## Source Of Truth

- Runtime code that builds prompts, contracts, state transitions, and skill injection.
- Session artifacts under the active `.agent-team` or runtime artifact directory.
- Codex session logs, command output, trace files, stage contracts, state JSON/YAML, and generated PRD/design/QA/acceptance reports.
- User-facing summaries are supporting evidence only; inspect the underlying stage input/output when available.

## Trace Ledger

For each workflow stage, account for:

- original user request or feedback that entered the run
- stage name and role owner
- input artifact or prompt source
- selected skills with local path or remote URL
- actual prompt or stdin sent to the executor
- generated artifact path
- state transition before and after the stage
- verification result or human decision
- memory/context changes that affected later stages

## Workflow

1. Identify the session ID, artifact directory, current stage, and requested question or failure.
2. Build the trace ledger before proposing fixes. Mark missing entries explicitly.
3. Separate human documents from machine control. PRD, technical plan, QA report, and acceptance report can be Markdown; workflow state, contracts, trace, and skill injection should be JSON/YAML or validated structured data.
4. Prefer engineering controls for state, schema, and transitions. Do not rely on a model to return perfect control JSON when code can validate or derive it.
5. Keep skill selection generic and configurable. Do not hard-code Figma review, code review, or other domain skills into the workflow when the skill manager or project preference file should own that choice.
6. For `--auto`, preserve trace output and stage transitions even when intermediate human confirmation is skipped. Product/CEO alignment and final human acceptance remain explicit stops unless the user changes that contract.

## Anti-Shortcuts

- Wrong: answer from `workflow_summary.md` only.
- Right: inspect the actual prompt, selected skills, state file, and produced artifact for the relevant stage.

- Wrong: create both a preference YAML and injection JSON with overlapping ownership.
- Right: define one owner or make one a generated trace output.

- Wrong: report that a stage ran without showing its input and output.
- Right: name the artifact path or trace entry that proves it.

## Completion Signal

The task is complete only when the trace ledger answers the user's question, missing trace fields are reported or fixed, and any code change is verified with a minimal workflow run or a targeted contract/state test.
