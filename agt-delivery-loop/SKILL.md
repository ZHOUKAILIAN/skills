---
name: agt-delivery-loop
description: Use when Zhou Kailian wants a requirement executed through AGT as a traceable delivery loop, or wants AGT blockers reviewed and rerouted with human decision points.
---

# AGT Delivery Loop

## Core Rule

Run user requirements through AGT as an engineering delivery loop, not as a one-shot model answer. AGT may use GPT, DS, OpenAI-compatible gateways, or `local_fallback`, but the source of truth for completion is runtime state, artifacts, code, commands, tests, logs, and external handoff evidence.

The loop must keep moving until the requirement is delivered, explicitly blocked for a user decision, or safely handed off with concrete remaining actions.

## Priority

- The user's newest instruction wins over this skill.
- Use `zhoukailian-development-preferences` for Zhou Kailian's evidence, scope, and communication defaults.
- Use `agent-team-traceability` whenever an existing AGT run is blocked, stale, confusing, or needs explanation from prompt/state/artifact evidence.
- Use narrower task skills for domain work. This skill controls the AGT loop; it does not replace backend, Figma, CST, Feishu, database, release, or code-review skills.

Wrong: AGT says "done", so report completion.
Right: inspect delivery state, execution state, changed artifacts, verification output, and handoff status before reporting completion.

## Active Mode

Choose one active mode before acting:

- `start-requirement`: the user gives a new requirement and asks AGT to do it.
- `continue-loop`: an AGT session already exists and needs to continue, retry, verify, or finish.
- `review-blocker`: AGT has a problem, blocker, timeout, confusing state, missing artifact, or failed verification, and the user wants to go through it.
- `handoff-only`: implementation is already complete and the work needs PR, merge, release, deploy, Feishu comment, or final status handoff.

If the user's request could mean either "run AGT" or "do it directly in Codex", choose AGT only when the user explicitly says AGT, agent-team, loop, session, workflow, or asks for the engineering system to own the demand.

## Source Of Truth

For an AGT run, inspect available runtime evidence before interpreting state:

- AGT CLI output such as `agt run`, `agt status`, `agt status --json`, and `agt inspect`.
- Session files under the active state root: `session.json`, `delivery-workflow.json`, `execution-workflow.json`, `events.jsonl`, `tool-calls.jsonl`, `agents/*.json`, `artifacts/index.jsonl`, and `prompt_traces/`.
- The target repository's code, docs, tests, git branch, worktree, and package or service commands.
- Domain evidence from the narrower task skill: API responses, logs, DB/SLS/Redis read results, Figma node data, Feishu docs, PR checks, deployment status, or release output.

Model summaries, chat text, screenshots, and memory can help orient the investigation, but they are not completion evidence when the underlying AGT state or task artifact is available.

## Requirement Loop

### 1. Normalize The Requirement

Before starting or continuing AGT, establish:

- the target repo or project context
- the user's requested outcome
- whether the task is read-only, code-changing, release/handoff, or external-write work
- the preferred AGT profile when it is obvious: `quick` for small changes, `investigate` for read-only investigation, `full` for cross-module or release-sensitive work
- the narrower task skill that owns domain verification

Stop and ask if the target repo, external write permission, production data action, release target, or human-facing artifact destination is ambiguous.

### 2. Start Or Continue AGT

- Prefer the installed `agt` command when available.
- Use `agt run --continue` or a known `session_id` when the task is already in progress.
- Use `--from` or `--from-dir` when the requirement already lives in a doc or folder.
- Preserve the AGT session id, repo root, state root, branch, and worktree identity in your notes and final proof package.
- If AGT cannot be started because installation, config, auth, or model routing is broken, switch to `review-blocker` and inspect the local AGT/runtime evidence before proposing changes.

### 3. Watch The Delivery State

Read delivery status first and execution state second:

- `done`: verify the task artifact and handoff evidence before reporting success.
- `blocked`: classify the blocker, inspect the relevant prompt/run/artifact, then either fix the loop input/config or take it back to the user.
- `waiting_human`: summarize the decision, evidence, and consequences; ask the user for a concrete go/no-go/rework decision.
- `needs_verification` or verification gaps: run or request the domain verification required by the owning task skill.
- stale running state: inspect heartbeat, latest events, tool calls, and active process state before restarting or reworking.

Wrong: rerun AGT blindly after any blocked state.
Right: inspect `agt inspect` or the session files, classify why it blocked, then decide whether to continue, rework, fix config, or ask the user.

### 4. Route Problems Back To Human Review

Take the issue back to Zhou Kailian when any of these happens:

- AGT changes the scope or target behavior beyond the user's request.
- AGT needs approval for production writes, data repair, release, deployment, merge, package publish, Feishu bot/comment side effects, or destructive cleanup.
- AGT has repeated the same blocker after a retry or rework.
- AGT's result conflicts with code, tests, logs, DB/SLS evidence, Figma, Feishu docs, or PR/deploy state.
- The next step is a product/technical decision rather than execution.

The review package must include the session id, current phase/stage, blocker or decision, evidence path or command result, and a recommended next action.

### 5. Complete The Handoff

Do not report completion until the owning task skill's verification is satisfied. For code work, include git branch, commit, PR or push status when relevant. For read-only work, include the evidence and conclusion. For external operations that require user action, separate in-scope completion from manual remaining steps.

## Blocker Classification

Use this classification before deciding the next action:

| Blocker | Meaning | Next action |
| --- | --- | --- |
| `missing_input` | Requirement, repo, environment, credential, or target is not known | Ask the user only for the missing decision |
| `tool_or_runtime` | `agt`, model routing, sandbox, package install, or local command failed | Inspect runtime logs/state and fix or report the precise setup gap |
| `skill_routing` | Required task skill, prompt injection, or route config is missing | Use `agent-team-traceability`, then fix routing or hand back the missing prerequisite |
| `implementation` | Code or artifact change failed | Inspect changed files and executor output, then continue or rework the failing stage |
| `verification` | Tests, API checks, logs, visual review, or data checks failed or were skipped | Run the required check or report `needs_verification` |
| `human_decision` | A scope, risk, release, product, or external-write decision is required | Present evidence and ask for go/no-go/rework |

## Red Flags

- "AGT completed, so the demand is done." Completion still needs artifact and verification evidence.
- "The model can decide the release/deploy/data write." External side effects require explicit user intent.
- "The blocker summary is enough." Inspect the prompt, run, artifact, event, or state file behind it.
- "Just switch models." Model changes can help execution, but routing, state, verification, and handoff evidence still decide correctness.
- "This is only a small demand." Small tasks can use `quick`, but still need a closed loop and proof package.

## Handoff Rules

- Hand off to `agent-team-traceability` for any AGT state, prompt, skill-injection, artifact, or stage-transition diagnosis.
- Hand off to `backend-service-verification` for service/API behavior that requires real request or runtime proof.
- Hand off to `ai-doc-driven-dev` when a requirement/design source must be created or updated.
- Hand off to Figma, CST, Feishu/Lark, data, code-review, or release skills when their route owns the domain evidence.
- Return to the user only for decisions that cannot be inferred safely: scope changes, external writes, merge/release/deploy approval, production data actions, or repeated AGT blockers.

## Completion Signal

The AGT delivery loop is complete only when:

- the active mode was named or obvious from the user request
- the AGT session id, repo root, state root, branch or worktree are known when AGT was run
- delivery and execution state were checked when available
- every blocked or waiting-human state was classified and resolved, or reported with a concrete user decision request
- the owning task skill's verification passed, or the final answer says exactly which verification is still missing and why
- the final proof package reports changed artifacts or read-only evidence, commands/checks run, handoff status, and residual risk

Do not claim AGT delivered the requirement from a model summary alone.
