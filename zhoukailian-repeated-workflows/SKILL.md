---
name: zhoukailian-repeated-workflows
description: Use when Zhou Kailian asks for recurring CrewPals, Figma, Feishu/Lark, agent-team, debugging, testing, PR, data consistency, or skill-writing work that should be routed through known local workflows.
---

# Zhou Kailian Repeated Workflows

## Core Rule

Classify the project context before classifying the workflow. Personal infrastructure repositories and CrewPals work repositories have different truth sources, release habits, and privacy boundaries. Then load the narrower skill that owns the work, and apply `zhoukailian-development-preferences` when personal engineering preferences affect scope, verification, or communication.

This router is based on a 2026-05-27 scan of local Codex history: 770 session files, 6062 real user messages, and repeated clusters around CrewPals debugging, Figma/UI restoration, Feishu docs, agent-team traceability, E2E verification, PR workflow, and running-data consistency.

## Project Context Routing

| Project context | Signals | Default truth sources | Default workflow boundary |
| --- | --- | --- | --- |
| Personal / infrastructure | `agent-team-runtime`, `ai-team-runtime`, `skills`, `mySelf` repos, agent runtime, skill repo, workflow engine | Repo README/docs, tests, runtime trace/state artifacts, local design notes, changelog, GitHub PRs | Do not require CrewPals Feishu, SLS/MySQL, test/prod env, or customer-data workflows unless explicitly requested. |
| CrewPals work | `crewpals-mp`, `group_pals`, CrewPals worktrees, CST/customer issues, running metrics, Feishu product docs | Active requirement/design docs, Feishu, code, API/schema, SLS/MySQL/Redis, screenshots, E2E checks | Apply CrewPals docs-first, environment-aware investigation, privacy, and verification habits. |
| Reusable skill extraction | Work summary, repeated workflow, skill repo, cross-project process | Source history only as evidence; target skill files and `skill-standard` as final owner | Generalize the pattern and remove CrewPals-only or personal-only assumptions unless the skill is explicitly scoped. |

## Routing Table

| User signal | Route |
| --- | --- |
| Figma URL, node ID, 1:1, UI restoration, popup/page/component visual work | Use `figma-design-audit` first. Implement only after the audit is ready, using `css-best-practices` for CSS/layout decisions. Use `figma-restoration-review` only for read-only post-implementation review. |
| Read-only Figma fidelity check or "review this restoration" | Use `figma-restoration-review`; report differences with Figma node values, derived numeric targets, implementation measurements, and priority. |
| CrewPals customer issue, bug, logs, SLS, MySQL, Redis, user state, prod/test symptoms | Use `cst` or the environment-specific read-only skills. Produce root cause, evidence, impact, and next action. |
| Running data consistency, pace, distance, best record, FIT files, Garmin, Coros, Huawei, pause, abnormal speed, charts | Use `crewpals-sports-metrics-investigation`: map frontend, backend, stored data, display surfaces, and metric definition; verify representative records end to end. |
| Feishu document, wiki, Base, sheet, approval, or report artifact | Use the matching `lark-*` skill. In CrewPals work, prefer Chinese docs with tables and PlantUML/Mermaid for process-heavy explanations. |
| Requirement/design docs, canonical docs, documentation drift, bug routed back to feature docs | Use `ai-doc-driven-dev` for docs-first projects. For personal infrastructure repos, follow the repo's native design/test/changelog conventions instead of forcing a CrewPals requirement/design pair. |
| agent-team, run, PRD/dev/QA/acceptance, prompt trace, skill injection, stage handoff, workflow state | Use `agent-team-traceability` for inspection/design/fixes; for runtime execution, follow the target repo's own run instructions and state artifacts. |
| Skill creation, skill extraction from history, skill repair, skill sync | Use `skill-lifecycle` and `skill-standard`; keep task-specific gates inside the skill being edited. |
| E2E coverage from Feishu bug/feature records | Use `e2e-coverage-guard`; account for every in-scope record or mark it not applicable with reason. |
| Code review request or review feedback | Use `code-reviewer` for review; use `receiving-code-review` before changing code from review comments. |
| Branch, worktree, push, PR/MR, release handoff | Use existing git/worktree practices; verify before push/PR and report branch plus checks. |

## Workflow

1. Name the project context and selected route in a short update before substantial work.
2. Load the route skill and any required preference skill.
3. Establish the source of truth for that context: personal repo docs/tests/traces, or CrewPals Figma node data/code/docs/logs/database/Feishu/runtime evidence.
4. Execute with scope accounting when the task has multiple states, records, files, nodes, or environments.
5. Verify with the route's required evidence. Missing verification blocks completion unless the user explicitly accepts a lower-confidence report.

## Guardrails

- Do not store raw conversation history, credentials, tokens, user identifiers, customer data, or production secrets in generated skills or reports.
- Stop and ask before production writes, destructive actions, package publishing, or broad deletion.
- If a request matches multiple routes, choose the route that owns the source of truth in the current project context first, then hand off to secondary skills.

## Completion Signal

The workflow is complete only when the selected route has produced its required artifact or code change, all in-scope items are accounted for, verification evidence is named, and skipped checks or unresolved risks are reported.
