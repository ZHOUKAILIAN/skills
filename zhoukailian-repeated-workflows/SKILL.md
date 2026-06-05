---
name: zhoukailian-repeated-workflows
description: Use when Zhou Kailian asks for recurring CrewPals, Figma, Feishu/Lark, agent-team, debugging, testing, PR, data consistency, or skill-writing work that should be routed through known local workflows.
---

# Zhou Kailian Repeated Workflows

## Core Rule

Classify the project context before classifying the workflow. Personal infrastructure repositories and CrewPals work repositories have different truth sources, release habits, and privacy boundaries. Then load the narrower skill that owns the work, and apply `zhoukailian-development-preferences` when personal engineering preferences affect scope, verification, or communication.

This router is based on local history scans from 2026-05-27 and 2026-06-05. The 2026-06-05 pass reviewed the recent two-week Claude Code and Codex history, filtered out tool output and continuation noise, and found repeated clusters around CrewPals release work, running-data consistency, CST investigation, endpoint verification, Figma/UI restoration, agent-team gate failures, Feishu docs/Base work, skill repair, and database/index decisions.

## Active Mode

Choose one active mode before substantial work:

- `route-task`: default mode. Classify context, choose the owning route, load the narrower skill, and execute that workflow.
- `recover-thread`: use when the latest message is "继续", status-only, an interruption marker, a continuation wrapper, or tool/background output. Recover the active human goal from the surrounding task, branch/worktree, goal state, or artifacts before acting.
- `extract-workflow`: use when the user asks to summarize repeated work or improve skills from history. Use conversation history only as evidence; the target skill files and `skill-standard` own the final content.
- `release-handoff`: use when the user asks to push, open a PR, cut a release branch, merge, or tell them what deployment/database step to take. Verify the code state first, then separate code handoff from manual operations.

If more than one mode could own the next action, pick the mode that owns the source of truth first and name any secondary handoff.

## History Signal Hygiene

Do not treat these as new requirements by themselves: `Continue working toward the active thread goal`, `<turn_aborted>`, background command output, pasted tool results, pasted skill bodies, or local-command caveats. Use them as execution context only after finding the actual human request they refer to.

If the active goal cannot be recovered from local context, summarize the likely current state and ask for the missing target instead of guessing.

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
| Backend endpoint, `new-api`, `curl`, service startup, runtime acceptance, or "自己端到端验证" | Use `backend-service-verification`; unit tests or code inspection alone do not close backend acceptance. After verification, use `backend-regression-maintenance` only when reusable regression coverage needs to be maintained. |
| Slow query, SQL plan, index choice, `ALTER TABLE`, DDL, data repair, or "我应该操作什么数据库" | Use read-only data/log inspection skills when available, usually `mysql-readonly`, `redis-readonly`, `aliyun-sls-query`, `cst`, or `crewpals-sports-metrics-investigation` depending on the source. Produce a proposed SQL/runbook with risk, rollback, and verification. Do not execute production or shared-environment writes without explicit approval. |
| CrewPals group timeline, social diary, existing-data migration, backfill, reconcile script, manual feed/activity repair, or cron pressure | Use `ai-doc-driven-dev` for owning requirement/design routing when semantics change, then `backend-service-verification` for API/script/job acceptance. Account for source rows, generated rows, dry-run results, idempotency, rollback, and runtime load. |
| Agent-team gate failure, missing stage artifact, `max_stage_runs`, blocked delivery, prompt/skill injection, or "为什么交付失败" | Use `agent-team-traceability`; build the trace ledger from runtime artifacts before proposing state-machine or prompt fixes. |
| OpenClaw, Bug扫描, Feishu robot, scheduled agent task, or agent not responding | Treat as personal/infrastructure unless it directly mutates CrewPals data. Use `agent-team-traceability` plus repository/process logs; keep credentials out of docs and commits. |
| Code review request or review feedback | Use `code-reviewer` for review; use `receiving-code-review` before changing code from review comments. |
| Branch, worktree, push, PR/MR, release branch, merge, deployment handoff | Use `using-git-worktrees` when isolation is needed, `verification-before-completion` before success claims, and `finishing-a-development-branch` when deciding PR/merge/cleanup. Report branch, diff scope, verification, PR/link if created, and any manual server/database steps separately. |

## Red Flags

- "This is just a push/PR." Check the diff and verification state before shipping.
- "The user pasted a continuation or tool output, so that must be the task." Recover the human goal first.
- "The SQL looks obvious." Inspect schema/query path and provide rollback/verification before any shared-environment DDL or data repair.
- "The endpoint returned 200." Verify response fields plus authoritative state, logs, or side effects when backend behavior matters.
- "The failure summary says blocked." Inspect the underlying stage artifact, state file, and prompt before explaining an agent-team failure.

## Workflow

1. Name the project context and selected route in a short update before substantial work.
2. Load the route skill and any required preference skill.
3. Establish the source of truth for that context: personal repo docs/tests/traces, or CrewPals Figma node data/code/docs/logs/database/Feishu/runtime evidence.
4. Execute with scope accounting when the task has multiple states, records, files, nodes, or environments.
5. Verify with the route's required evidence. Missing verification blocks completion unless the user explicitly accepts a lower-confidence report.

## Guardrails

- Do not store raw conversation history, credentials, tokens, user identifiers, customer data, or production secrets in generated skills or reports.
- Stop and ask before production writes, destructive actions, package publishing, or broad deletion.
- Treat database DDL, data backfills, cron/job triggers, and production script runs as write operations even when the user phrases them as "看下" or "我应该怎么做".
- If a request matches multiple routes, choose the route that owns the source of truth in the current project context first, then hand off to secondary skills.

## Completion Signal

The workflow is complete only when the selected route has produced its required artifact or code change, all in-scope items are accounted for, verification evidence is named, and skipped checks or unresolved risks are reported.
