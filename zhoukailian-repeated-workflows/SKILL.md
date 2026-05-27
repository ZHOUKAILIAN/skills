---
name: zhoukailian-repeated-workflows
description: Use when Zhou Kailian asks for recurring CrewPals, Figma, Feishu/Lark, agent-team, debugging, testing, PR, data consistency, or skill-writing work that should be routed through known local workflows.
---

# Zhou Kailian Repeated Workflows

## Core Rule

Classify the request into a known repeated workflow before inventing a new process. Load the narrower skill that owns the work, then apply `zhoukailian-development-preferences` and, for UI work, `zhoukailian-ui-aesthetic-preferences`.

This router is based on a 2026-05-27 scan of local Codex history: 770 session files, 6062 real user messages, and repeated clusters around CrewPals debugging, Figma/UI restoration, Feishu docs, agent-team traceability, E2E verification, PR workflow, and running-data consistency.

## Routing Table

| User signal | Route |
| --- | --- |
| Figma URL, node ID, 1:1, UI restoration, popup/page/component visual work | Use `figma-1to1-ui-restoration`, `zhoukailian-ui-aesthetic-preferences`, and `css-best-practices`; use `figma-restoration-review` before acceptance when visual fidelity matters. |
| Read-only Figma fidelity check or "review this restoration" | Use `figma-restoration-review`; report differences with screenshot evidence and priority. |
| CrewPals customer issue, bug, logs, SLS, MySQL, Redis, user state, prod/test symptoms | Use `cst` or the environment-specific read-only skills. Produce root cause, evidence, impact, and next action. |
| Running data consistency, pace, distance, best record, FIT files, Garmin, Coros, Huawei, pause, abnormal speed, charts | Use `crewpals-sports-metrics-investigation`: map frontend, backend, stored data, display surfaces, and metric definition; verify representative records end to end. |
| Feishu document, wiki, Base, sheet, approval, or report artifact | Use the matching `lark-*` skill. Prefer Chinese docs with tables and PlantUML/Mermaid for process-heavy explanations. |
| Requirement/design docs, canonical docs, documentation drift, bug routed back to feature docs | Use `ai-doc-driven-dev`. Update the owning requirement/design pair when one exists. |
| agent-team, run, PRD/dev/QA/acceptance, prompt trace, skill injection, stage handoff, workflow state | Use `agent-team-traceability` for inspection/design/fixes; use `ai-company-workflow` when executing the workflow. |
| Skill creation, skill extraction from history, skill repair, skill sync | Use `skill-lifecycle` and `skill-standard`; use `task-standard` for task-oriented skills. |
| E2E coverage from Feishu bug/feature records | Use `e2e-coverage-guard`; account for every in-scope record or mark it not applicable with reason. |
| Code review request or review feedback | Use `code-reviewer` for review; use `receiving-code-review` before changing code from review comments. |
| Branch, worktree, push, PR/MR, release handoff | Use existing git/worktree practices; verify before push/PR and report branch plus checks. |

## Workflow

1. Name the selected route in a short update before substantial work.
2. Load the route skill and any required preference skill.
3. Establish the source of truth: Figma, code, docs, logs, database, Feishu records, trace artifacts, or runtime screenshots.
4. Execute with scope accounting when the task has multiple states, records, files, nodes, or environments.
5. Verify with the route's required evidence. Missing verification blocks completion unless the user explicitly accepts a lower-confidence report.

## Guardrails

- Do not store raw conversation history, credentials, tokens, user identifiers, customer data, or production secrets in generated skills or reports.
- Stop and ask before production writes, destructive actions, package publishing, or broad deletion.
- If a request matches multiple routes, choose the route that owns the source of truth first, then hand off to secondary skills.

## Completion Signal

The workflow is complete only when the selected route has produced its required artifact or code change, all in-scope items are accounted for, verification evidence is named, and skipped checks or unresolved risks are reported.
