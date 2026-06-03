---
name: backend-service-verification
description: Use when verifying a backend requirement or service-side change from requirements, technical plans, and QA/frontend/full-stack test cases with real service evidence.
---

# Backend Service Verification

## Goal

Prove whether a backend change is complete by deriving a backend verification plan, executing the service-side checks, and reporting observable evidence.

This skill is for backend verification only. It does not verify frontend layout, visual style, animation, browser rendering, or toast placement except to extract the backend facts behind those user-visible assertions.

## Source Test Cases Are Input, Not Backend Cases

User-provided QA, frontend, or full-stack test cases are source material. Do not copy them directly as backend cases.

For each original case, decompose it into:

1. frontend-only assertions
2. backend-verifiable facts
3. full-stack or manual assertions
4. derived backend risks
5. unknowns that need clarification

Backend verification must combine the original cases with the requirement, technical plan, API contracts, database model, logs, queues, cache, and project conventions.

Wrong: "The frontend case says click Save and see a success toast, so backend passes if the API returns 200."

Right: "The case implies a create operation. Verify the response, authoritative database row, audit/log event, duplicate-submit behavior, and any stated consistency invariant."

## Relationship With `five-layer-classifier`

`five-layer-classifier` decides asset responsibility, truth-source status, repository boundary, and writeback location. This skill uses those decisions to design and execute backend verification. It does not replace the classifier.

Use `five-layer-classifier` before or during this skill when any of these are unclear:

1. whether the verification artifact is product definition, implementation reality, project landing, shared governance, local evidence, or research
2. whether a report, testcase, fixture, script, or run log should be written into the product repo, control repo, local workspace, or nowhere
3. whether a temporary validation result is allowed to become a formal truth source
4. whether a mixed artifact should be split before writeback
5. whether public/private history policy changes the destination

The classifier output must affect this skill's plan:

- Layer 1 findings define intended product semantics and acceptance criteria.
- Layer 2 findings identify current implementation reality, executable tests, schemas, fixtures, and runtime behavior to verify.
- Layer 3 findings identify project startup, packaging, CI, and default run conventions.
- Layer 4 findings identify shared verification gates, report formats, and release rules.
- Layer 5 findings identify local-only evidence that may support the current run but must not be promoted without an explicit decision.

This skill is a Layer 4 verification-governance skill under the AI Coding five-layer model. Do not treat it as a project-specific runbook. It must adapt to any project by discovering that project's verification conventions.

Default layer responsibilities:

1. Requirements and product semantics usually belong to Layer 1.
2. Source code, tests, schemas, fixtures, and runtime scripts usually belong to Layer 2.
3. Project default startup, packaging, and repository layout usually belong to Layer 3.
4. Shared verification policy, gates, and reusable verification reports belong to Layer 4.
5. Temporary run logs, scratch queries, local env notes, and one-off validation artifacts belong to Layer 5 unless promoted.

Before writing a verification plan, testcase, or report into the repository, decide whether it is current runtime reality, shared verification governance, or local temporary evidence. If the boundary is ambiguous, classify first instead of guessing.

## Project-Specific Discovery

Every project has its own verification style. Discover it before designing or running checks.

Look for project-local sources such as:

- README or developer setup docs
- testing or verification docs
- package scripts, Make targets, task runners, or CI config
- service entrypoints and config examples
- database migrations/schema/model definitions
- existing tests and test fixtures
- logging, tracing, queue, cache, and worker conventions

Use discovered conventions. If startup, test data, credentials, or database access are unclear and a wrong guess would change results or touch unsafe data, stop and ask.

## Backend Verification Plan

Before executing, produce a concise plan covering:

1. backend scope and explicit non-scope
2. decomposed source test cases
3. five-layer placement for verification artifacts and temporary evidence
4. derived backend verification cases
5. service startup and dependency readiness
6. isolated test data and cleanup strategy
7. API/RPC/CLI calls to execute
8. database or persisted-state checks
9. log/trace checks
10. side effects: queue, outbox, cache, webhook, file, email, notification, or worker behavior
11. failure paths and edge cases
12. done criteria for PASS/PARTIAL/FAIL

If the user only asks for a plan, stop after the plan and mark it as not executed.

## Required Backend Risk Derivation

Actively derive service-side risks from the requirement and technical plan, even when the original test cases do not mention them.

Check whether the change involves:

1. idempotency or duplicate execution
2. data consistency invariants
3. concurrency or race conditions
4. permissions, roles, ownership, or tenant isolation
5. state transitions and terminal states
6. transactions, rollback, or partial failure
7. asynchronous jobs, queues, outbox, webhooks, retries, or workers
8. cache reads, writes, invalidation, or stale data
9. audit logs, business logs, traceability, and secret redaction
10. migrations, backfills, compatibility, or data repair
11. quotas, counters, balances, inventory, rewards, coupons, or limited resources

For every applicable risk, add a verification item or explicitly mark it out of scope with the reason.

## Verification Dimensions

### API or Service Behavior

Verify the externally observable backend contract: status codes, response schema, error codes, permission errors, validation errors, and idempotent replay or duplicate-submit responses.

HTTP 200 or command exit code alone is not evidence of correctness.

### Authoritative State

Verify the authoritative persisted state, not only returned data.

Depending on the project, this can include relational tables, document stores, cache keys, files, event/outbox rows, search index records, or generated artifacts.

A database check is complete only when expected business state is observed in the authoritative records and enough related records are checked to prove the behavior.

### Consistency Invariants

When the plan or data model implies relationships such as totals, balances, counts, inventory, rewards, or formulas like `A = B + C`, verify the invariant from authoritative data.

Examples:

- total equals sum of details plus fees minus discounts
- remaining inventory equals previous inventory minus successful claims plus returns
- balance equals initial balance plus credits minus debits
- completed count never exceeds total count
- one business entity has only one active state when uniqueness is required

Do not report PASS if required cross-record invariants were not checked.

### Idempotency

If the operation can be retried, submitted twice, receive duplicate callbacks, or use request IDs or idempotency keys, verify duplicate execution behavior.

Expected evidence may include:

1. exactly one business row or one intended state transition
2. no duplicate side effects
3. stable final state
4. expected duplicate/replay response
5. idempotency key or deduplication record when the design uses one

### Concurrency

If the operation touches limited resources, counters, balances, inventory, claims, locks, status transitions, or uniqueness constraints, evaluate concurrency risk.

When applicable, run or design concurrent verification and check final authoritative state, not only individual request responses.

Evidence should show no oversell, duplicate claim, double charge, negative counter, illegal state, unhandled deadlock, or lost update.

### Permissions and Isolation

For user, role, organization, or tenant scoped behavior, verify allowed and denied access. Include cross-tenant or cross-owner reads/writes when relevant.

### State Machines

If the feature has states, verify legal transitions, illegal transitions, terminal-state protection, retry behavior, and rollback or recovery expectations.

### Async and Side Effects

If behavior crosses queues, workers, outbox, webhooks, emails, notifications, search indexes, caches, or scheduled jobs, verify both the triggering record and the eventual effect or documented pending state.

### Logs, Traces, and Audit

Logs are verification evidence when they prove the expected business event, connect request to downstream work through request/trace IDs, show no relevant errors, and redact sensitive fields.

Do not print raw secrets, cookies, authorization headers, passwords, tokens, private transcripts, or full production connection strings.

## Completion Standard

Report **PASS** only when all applicable conditions are met:

1. artifact placement follows the five-layer boundary, or unresolved placement is reported
2. service startup and dependency readiness are verified or not required
3. original test cases have been decomposed into backend scope and non-scope
4. backend facts from the source cases are covered
5. derived backend risks are covered or explicitly scoped out
6. happy path evidence is observed
7. important negative paths are verified or explicitly scoped out
8. authoritative state is checked
9. required consistency invariants are checked
10. idempotency and concurrency are checked when applicable
11. side effects and async behavior are checked when applicable
12. logs/traces/audit are checked when applicable
13. test data cleanup is completed or documented

Report **PARTIAL** when evidence is incomplete, a required environment is unavailable, or an applicable risk is only designed but not executed.

Report **FAIL** when observed behavior violates the requirement, plan, contract, state, invariant, or safety boundary.

## Report Format

Use this structure:

```text
Backend Service Verification Report

Result: PASS | PARTIAL | FAIL

1. Source Materials
   - Requirement:
   - Technical plan:
   - Source test cases:
   - Project verification docs/conventions:
   - Five-layer placement decisions:

2. Original Test Case Decomposition
   - Original case:
   - Frontend-only assertions:
   - Backend facts:
   - Full-stack/manual assertions:
   - Derived backend risks:

3. Backend Verification Plan
   - Scope / non-scope:
   - Artifact layer / writeback boundary:
   - Startup/dependencies:
   - Test data:
   - Calls to execute:
   - State checks:
   - Consistency invariants:
   - Idempotency:
   - Concurrency:
   - Permissions/state/async/logs:
   - Cleanup:

4. Execution Evidence
   - Commands or calls:
   - Responses:
   - Persisted-state evidence:
   - Log/trace evidence:
   - Side effects:

5. Gaps and Risks
   - Not verified:
   - Reason:
   - Impact:

6. Final Judgment
   - Result:
   - Why:

7. Proposed Regression Cases
   - P0 candidates:
   - P1 candidates:
   - P2 candidates:
   - Manual candidates:
```

The `Proposed Regression Cases` section is the handoff input for `backend-regression-maintenance`.
