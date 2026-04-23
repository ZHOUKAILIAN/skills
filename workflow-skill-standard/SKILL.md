---
name: workflow-skill-standard
description: Quality standard for execution-oriented skills that run tasks, automation, APIs, or operational workflows.
---

# Workflow Skill Standard

Use this standard for skills whose primary job is to get something done.

These skills are execution contracts.
They must be clear enough that the model and runtime can complete the task without inventing missing rules.

---

## What a Workflow Skill Must Do

A workflow skill must define:
- the task goal
- the available assets or runtime used to complete it
- the critical constraints
- the dependency relationships
- the completion signal
- the failure boundary

If any of those are vague, the skill is incomplete.

---

## Workflow Writing Standard

### 1. Goal-first, execution-focused
State the task outcome clearly.
The goal must describe what the task accomplishes in the real world, not just what command might run.

### 2. Describe assets, not hand-holding commands
Declare the programmatic assets that exist and what they can do.
Do not over-script exact execution unless a literal command is itself part of the contract.

### 3. Runtime contract must be explicit
If the task depends on auth, env, local files, APIs, services, or scheduling context, say so clearly.
Do not rely on implied runtime assumptions.

Examples of runtime contract items:
- required auth fields
- config source of truth
- isolated runtime behavior
- idempotency expectations
- side-effect boundaries

### 4. Dependencies must be named
If the skill relies on another skill, reference it by skill name.
Its `skill.json` must declare that dependency when applicable.

### 5. Success must be externally verifiable
A workflow skill must define completion in terms of observable state.
Do not let the model decide that “it probably worked.”

Good completion signals:
- platform state confirms today is signed
- output contains validated record data
- required downstream artifact exists and passes checks

Bad completion signals:
- task ran without crashing
- output looks plausible
- model thinks enough steps were done

### 6. Failure states must be explicit
A workflow skill must say what failure looks like.
Examples:
- missing required config
- invalid credentials
- platform rejected the action
- verification failed

### 7. Idempotency must be stated when relevant
If repeated execution is safe, say so.
If repeated execution is unsafe, say so.
Do not leave this implicit.

### 8. Recovery path must be clear
If the normal path can fail due to known preconditions, specify the recovery route.
Example:
- use `xiaoju-get-params` when auth is missing or invalid

---

## Anti-Patterns

- commands dominate the skill while runtime assumptions stay vague
- success means “the script was called” instead of “the platform state was verified”
- missing distinction between execution start and execution qualification
- no defined behavior when credentials/config are unavailable
- cron/isolated runtime assumptions left implicit

---

## Review Output

When auditing a workflow skill, report:
1. whether the goal is clear
2. whether runtime contract is explicit
3. whether dependencies are declared
4. whether completion signal is verifiable
5. whether failure/recovery paths are defined
6. the exact ambiguity or gap, if any

## Completion Signal

A workflow skill review is complete only when you have checked goal, runtime contract, dependency model, success criteria, and failure criteria explicitly.
