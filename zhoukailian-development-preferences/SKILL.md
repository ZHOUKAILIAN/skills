---
name: zhoukailian-development-preferences
description: Use when working with Zhou Kailian on coding, debugging, product documentation, repository workflow, or technical decisions where personal engineering preferences affect scope, verification, or communication.
---

# Zhou Kailian Development Preferences

## Core Rule

Treat work for Zhou Kailian as evidence-driven engineering. Prefer explicit source-of-truth files, structured state, traceable handoffs, and runnable verification over prompt-only discipline or model memory.

This skill is derived from a local Codex history scan on 2026-05-27. It is preference guidance, not permission to override the user's newest instruction, project rules, or safety boundaries.

## Default Preferences

- Read the repo, docs, logs, and existing patterns before proposing architecture or writing code.
- Prefer engineering controls over prompt reliance. If JSON/YAML/state-machine validation can enforce a behavior, use that rather than asking a model to remember it.
- Use Markdown for human-facing PRDs, technical plans, reports, and Feishu docs. Use JSON/YAML for machine state, contracts, skill injection, trace data, and workflow control.
- Avoid duplicate control files. If two configs represent the same truth, consolidate or clearly define ownership before changing behavior.
- Keep docs in Chinese by default for PRD, technical plan, investigation report, and handoff artifacts unless the repository convention requires English.
- Use flowcharts, PlantUML/Mermaid, tables, and explicit examples for process or architecture explanations. Explain unfamiliar English terms in Chinese.
- Do not add a `Non-Goals` or `非目标` section unless the user asks for it or the existing template requires it.
- For existing features or regressions, update the owning requirement/design docs instead of creating standalone bugfix docs by default.
- Preserve traceability for multi-stage work: original user input, stage handoff, selected skills with source path or URL, actual prompt sent to agents, produced artifacts, verification output, and final decision.
- For implementation work, create or use the requested branch/worktree, keep changes scoped, and do not revert unrelated user changes.
- For backend/API work, unit tests alone are usually insufficient. Prefer starting the service or calling the target endpoint with representative data when feasible.
- For bug investigation, produce symptoms, root cause, impact, evidence, and fix/next action. Do not stop at a plausible explanation.
- For completion claims, report verification commands and results. If a check was skipped, say why.

## Communication Defaults

- Be direct and concrete. State what was inspected, what changed, how it was verified, and what risk remains.
- Use exact file paths, branch names, task IDs, dates, environment names, and artifact links when they are relevant and safe to share.
- Give short progress updates during long work. Do not fill space with generic reassurance.
- Ask only when a silent assumption would change scope, write location, credentials, environment, branch, user-visible behavior, or safety.

## Guardrails

- Do not write secrets, account credentials, raw tokens, private user identifiers, or customer data into skills, docs, reports, commits, or final summaries.
- Do not write to production, mutate databases, trigger external side effects, or publish packages without explicit user intent for that action.
- Do not treat a model-generated summary as the source of truth when the underlying code, logs, database, trace, or document is available.

## Completion Signal

Work is ready to report only when the requested artifact or code change exists, the relevant source of truth was checked, verification has run or been explicitly blocked, and the final response includes changed artifacts, evidence, skipped checks, and residual risk.
