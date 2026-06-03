---
name: backend-service-verification
description: Use when verifying a backend requirement or service-side change by authoring and executing API/RPC/CLI end-to-end self-tests with service evidence.
---

# Backend Service Verification

## Goal

Prove whether a backend change is complete by authoring and executing service-side end-to-end self-tests, then verifying the response, authoritative state, logs, and side effects behind the judgment.

End-to-end in this skill means crossing the real service boundary: API, RPC, CLI command, job trigger, webhook handler, or the project's equivalent backend entrypoint. It does not mean browser/UI automation unless browser behavior is only being used to discover the backend request.

This skill is for backend verification only. It does not verify frontend layout, visual style, animation, browser rendering, or toast placement except to extract the backend facts behind those user-visible assertions.

## Core Rule

No `PASS` without executed backend probes and an evidence ledger.

Every backend fact, derived risk, required negative path, and proposed regression case must trace to a self-authored test case and a reproducible probe artifact such as a `curl` command, RPC call, CLI invocation, focused integration test, SQL query, log query, cache/queue inspection, or project-native equivalent.

Wrong: "The endpoint returned 200, so backend verification passed."

Right: "The self-test created an isolated record through the API, the response matched the contract, the authoritative row exists with expected fields, the related count invariant holds, duplicate submit produced no second row, and the audit log contains the expected event."

## When To Use

Use this skill when the task is to verify a backend requirement, API/RPC/CLI behavior, service-side bug fix, data-write flow, async worker behavior, or full-stack/QA test case that needs backend evidence.

Use it when the agent should actively create backend self-test cases, build executable probes, call the service, and inspect logs, database, cache, queue, files, audit records, or other authoritative side effects.

Use it when source test cases are written from a frontend or QA perspective and need to be decomposed into backend facts before service-side end-to-end verification.

## When Not To Use

Do not use this skill for purely visual frontend checks, copy/layout review, browser-only behavior, or design restoration unless those checks imply backend state or service behavior.

Do not use it to maintain long-term regression assets after verification. Hand the `Proposed Regression Cases` section to `backend-regression-maintenance`.

## Required Inputs

Before executing probes, establish or mark blocked:

- target requirement, change, bug, PR, endpoint, route, RPC method, CLI command, worker, or backend behavior under verification
- target environment: local, test, staging, production, or supplied snapshot
- base URL, service startup command, RPC target, CLI entrypoint, or job trigger method
- authentication method, test account, tenant, fixture, or safe identity
- whether write operations and external side effects are allowed
- authoritative state stores and lookup strategy for records touched by the test
- cleanup strategy for every mutation

If any of these inputs cannot be established safely, continue only for plan-only or evidence-review-only work, or mark the affected executable checks `BLOCKED`.

## Source Of Truth

Use the strongest available project-local facts:

- requirement, acceptance criteria, product notes, issue, PR, or technical plan
- source QA/frontend/full-stack test cases
- API/RPC/CLI contracts, OpenAPI specs, protobufs, request validators, route definitions, or captured frontend requests
- implementation code, migrations, schemas, models, fixtures, factories, and existing tests
- runtime configuration, service startup docs, dependency docs, CI scripts, release docs, sample requests, or local dev scripts
- authoritative state: database records, persisted files, cache keys, outbox rows, queue messages, search index records, generated artifacts, or external-system test doubles
- runtime evidence: responses, logs, traces, audit records, worker output, side effects, cleanup evidence, and command output

Do not treat model memory, summaries, "looks correct", code inspection alone, or HTTP 200 alone as source-of-truth evidence for executed verification.

## Optional Governance Context

This skill must work without the AI Coding five-layer model.

If a five-layer classifier or equivalent governance source is available and artifact ownership, truth-source status, writeback location, or public/private history would change the verification output or repository writes, read that source as input. Do not inline or reimplement that model here, and do not require users to install it.

If that governance source is unavailable, continue with project-local discovery. Use existing project conventions for obvious destinations, keep temporary run evidence local, and mark ambiguous writeback decisions as `needs boundary decision` instead of guessing.

Do not block backend verification just because the five-layer model is unavailable. Block repository writeback only when the destination or ownership is unsafe to assume.

## Mode And Fallback Rules

Choose one active mode before proceeding:

- `plan-only`: use when the user asks only for a verification plan. Stop after self-test cases and probe artifacts are drafted, mark all items `NOT_RUN`, and do not claim backend behavior passed.
- `execute-verification`: use by default when the user asks to verify, test, prove, or check completion. Discover the service boundary, author self-test cases, create executable probes, execute safe probes, inspect authoritative state, and fill the evidence ledger.
- `evidence-review-only`: use when the environment cannot be run but reports, logs, database snapshots, command output, or prior probe outputs are available. Review only the supplied evidence and report `PARTIAL` unless the evidence fully satisfies the completion standard.

Fallbacks:

- If startup, credentials, test data, dependency access, or write permission is unsafe or unavailable, mark affected executable checks `BLOCKED` or `NOT_RUN`; do not invent evidence.
- If a mechanical check cannot run, use manual inspection evidence only when the inspected source is named and the gap impact is reported.
- If repository writeback ownership is unclear, continue verification but mark writeback `needs boundary decision`.
- If a project-native integration test is more reliable than a raw `curl`, use it, but still record the exact request, fixture, assertion, authoritative state check, and command output.

## Workflow

### 1. Source Inventory Gate

Before planning verification, enumerate the source materials and mark each as `read`, `missing`, `unavailable`, or `not applicable`.

Required inventory groups:

1. requirement or acceptance source
2. technical plan or implementation intent
3. source test cases, if provided
4. API/RPC/CLI contract, captured request, route definition, or job trigger
5. implementation code path
6. schema, model, migration, fixture, factory, or authoritative state definition
7. project startup, dependency, test, local-dev, or CI convention
8. authentication, tenant, permission, or test identity convention
9. log, trace, queue, cache, worker, audit, external side-effect, or cleanup convention when relevant

Anti-laziness gate: do not write "docs reviewed" or "project conventions checked" without naming the files, commands, endpoints, routes, or sources inspected. If a source group is missing, record the impact before proceeding.

### 2. Environment And Safety Gate

Before executing any probe, classify the environment and side effects.

Record:

```text
Environment:
Service startup or target base URL:
Auth or test identity source:
Allowed mutation scope:
External side effects possible:
Data isolation strategy:
Cleanup strategy:
Blocked operations:
Safety decision: safe_to_execute | plan_only | evidence_review_only | blocked
```

Safety rules:

- Production or shared-environment writes require explicit user approval before execution.
- Do not send real emails, notifications, payments, webhooks, or external callbacks unless the user explicitly approved that side effect.
- Redact secrets, cookies, authorization headers, passwords, tokens, private user identifiers, and full production connection strings from reports.
- If isolated data cannot be prepared, mark mutating probes `BLOCKED` or convert them to plan-only checks.

Anti-laziness gate: do not execute a `curl`, RPC, CLI, SQL mutation, worker trigger, or cleanup command until the environment and mutation scope are recorded.

### 3. Source Test Case Decomposition Gate

Treat user-provided QA, frontend, or full-stack cases as source material, not backend cases to copy directly.

For every original case, create a decomposition row:

```text
Original case ID:
Original assertion:
Frontend-only assertions:
Backend-verifiable facts:
Full-stack/manual assertions:
Derived backend risks:
Unknowns:
Status: covered | not backend-applicable | blocked
Reason:
```

Anti-laziness gate: zero unaccounted original cases. If one original case implies multiple backend facts, split them into separate self-test cases instead of testing only the obvious happy path.

Wrong: "Click Save shows success toast, so call the save API once."

Right: "The case implies create/update behavior. Verify response contract, authoritative persisted state, related records, duplicate submit behavior, and any required audit or async side effect."

### 4. Backend Risk Derivation Gate

Actively derive service-side risks from requirements, plan, code, schema, and source test cases. Do this even when the original cases do not mention the risk.

For each risk category, record `applies`, `not applicable`, or `unknown`, with evidence and next action:

1. idempotency or duplicate execution
2. data consistency invariants
3. concurrency or race conditions
4. permissions, roles, ownership, or tenant isolation
5. state transitions and terminal states
6. transactions, rollback, or partial failure
7. async jobs, queues, outbox, webhooks, retries, or workers
8. cache reads, writes, invalidation, or stale data
9. audit logs, business logs, traceability, and secret redaction
10. migrations, backfills, compatibility, or data repair
11. quotas, counters, balances, inventory, rewards, coupons, or limited resources

Anti-laziness gate: no batch `N/A`. Every category needs a cited reason from requirement, code, schema, or project convention. Every `applies` or `unknown` category needs a self-test case, blocker, or explicit out-of-scope decision.

### 5. Self-Test Case Authoring Gate

Before executing, author one backend end-to-end self-test case per backend fact, applicable risk, unknown risk, and important negative path.

Each self-test case must include:

```text
Self-test case ID:
Source case, requirement, code path, or risk:
Backend behavior under test:
Preconditions and isolated test data:
Entrypoint: API | RPC | CLI | worker trigger | webhook handler | other
Request method/path or command:
Headers/auth strategy, redacted:
Request body, params, or fixture:
Expected response status, schema, fields, or error code:
Expected authoritative state:
Expected logs, traces, audit rows, cache/queue/outbox effects, or worker effects:
Negative/idempotency/concurrency/permission/state checks:
Cleanup:
PASS criterion:
```

If the project already has integration or E2E test conventions, prefer a focused test in that convention when it is safe and proportionate. If a durable test is not needed or would be too heavy, create a temporary probe such as `curl` plus SQL/log/cache checks.

Anti-laziness gate: "test the endpoint" is not a self-test case. The case must be specific enough that another agent could execute the request and inspect the expected state without guessing.

### 6. Probe Artifact Gate

For every self-test case, create or record executable probe artifacts before claiming execution.

Acceptable probe artifacts include:

- exact `curl` command with redacted secrets
- RPC invocation, GraphQL operation, CLI command, worker trigger, or webhook replay command
- focused project-native integration/E2E test command
- SQL query or read-only data inspection command
- log, trace, audit, cache, queue, outbox, file, or search-index inspection command
- cleanup command or cleanup verification query

Each probe artifact must include:

```text
Probe ID:
Self-test case ID:
Executable request or command:
Expected output:
Authoritative state query:
Runtime evidence query:
Cleanup or cleanup verification:
Safety notes:
```

Anti-laziness gate: one broad command may support many rows, but it must be mapped to each self-test case. A command that is not mapped to a case, expected result, and evidence source does not prove that case.

### 7. Execution Evidence Gate

Execute the probe artifacts using the project's discovered conventions. If execution is unsafe or impossible, mark the affected case `BLOCKED` or `NOT_RUN` with the reason.

For every self-test case, maintain an evidence ledger:

```text
Self-test case ID:
Probe ID:
Expected result:
Request or command executed:
Response evidence:
Authoritative state evidence:
Runtime evidence: log | trace | audit | cache | queue | worker | file | other
Observed data:
Status: PASS | FAIL | NOT_RUN | BLOCKED | OUT_OF_SCOPE
Reason:
Cleanup evidence:
```

Evidence rules:

- API/RPC/CLI checks must include contract-relevant response status, schema, error code, or returned fields.
- Authoritative state checks must inspect the source of truth, not only returned data.
- Consistency checks must verify the actual invariant from authoritative data.
- Idempotency checks must prove duplicate execution does not duplicate business effects.
- Concurrency checks must inspect final authoritative state, not only individual responses.
- Permission checks must include allowed and denied access when relevant.
- State-machine checks must include legal transitions, illegal transitions, and terminal-state protection when relevant.
- Async and side-effect checks must verify the trigger record plus eventual effect or documented pending state.
- Log, trace, and audit checks count only when they prove a business event, link request to downstream work, and avoid leaking secrets.

Anti-laziness gate: code inspection, a large test-suite pass, or a single happy-path `curl` can support evidence, but none of them replaces the ledger. Map runtime evidence back to every self-test case. Details that are not mapped are not verified.

## Completion Standard

Report **PASS** only when all applicable conditions are met:

1. source inventory is complete or gaps are documented as non-blocking
2. environment, auth, data isolation, side effects, and cleanup are classified as safe for executed probes
3. every original source test case is decomposed or marked not backend-applicable with reason
4. every backend fact is mapped to a self-test case
5. every risk category is individually classified with evidence
6. every applicable or unknown risk is verified, blocked, or explicitly scoped out
7. every required self-test case has a probe artifact
8. every required probe artifact was executed in a safe environment
9. the evidence ledger has no `NOT_RUN` or `BLOCKED` row for required scope
10. every required response, authoritative state, runtime evidence, and cleanup check passed
11. every required invariant, idempotency, concurrency, permission, state, async, side-effect, log, trace, or audit check passed
12. important negative paths are verified or explicitly scoped out

Report **PARTIAL** when evidence is incomplete, an environment is unavailable, safe execution is blocked, a required item is `NOT_RUN` or `BLOCKED`, or an applicable risk is only planned but not executed.

Report **FAIL** when observed behavior violates the requirement, technical plan, API contract, authoritative state, invariant, or safety boundary.

Anti-laziness gate: do not downgrade missing execution evidence into "low risk" and still report `PASS`. Missing required evidence is `PARTIAL`; contradictory evidence is `FAIL`.

## Gate Failure Behavior

When a gate is incomplete, first try to fill the missing source references, self-test case fields, probe artifacts, ledger rows, or execution evidence.

If the missing item cannot be filled safely, do not continue to a `PASS` result. Mark the affected item `NOT_RUN`, `BLOCKED`, or `OUT_OF_SCOPE` with reason, then report `PARTIAL` unless observed evidence already requires `FAIL`.

Do not convert a failed gate into a vague residual risk. The failed item must appear in the report's evidence ledger or gaps section.

## Proposed Regression Cases

Propose regression cases only from executed self-test cases, verified backend facts, observed failures, or documented manual checks.

Each proposed case must include:

```text
Candidate ID:
Source self-test case:
Probe and evidence summary:
Backend assertion:
Suggested priority: P0 | P1 | P2 | Manual
Why it should or should not become long-term regression coverage:
```

The `Proposed Regression Cases` section is the handoff input for `backend-regression-maintenance`.

## Report Format

Use this structure:

```text
Backend Service Verification Report

Result: PASS | PARTIAL | FAIL

1. Source Inventory
   - Source:
   - Status:
   - Evidence or location:
   - Gap impact:

2. Environment and Safety
   - Environment:
   - Target base URL or service entrypoint:
   - Auth/test identity:
   - Mutation and side-effect scope:
   - Data isolation and cleanup:
   - Safety decision:

3. Original Test Case Decomposition
   - Original case ID:
   - Frontend-only assertions:
   - Backend facts:
   - Full-stack/manual assertions:
   - Derived backend risks:
   - Status and reason:

4. Risk Coverage Matrix
   - Risk category:
   - Applies / not applicable / unknown:
   - Evidence:
   - Self-test case or out-of-scope reason:

5. Self-Test Cases
   - Self-test case ID:
   - Backend behavior:
   - Request or command:
   - Expected response:
   - Expected authoritative state:
   - Expected runtime evidence:
   - Cleanup:
   - PASS criterion:

6. Probe Artifacts
   - Probe ID:
   - Self-test case ID:
   - Executable request or command:
   - State/log/cache/queue queries:
   - Cleanup check:

7. Execution Evidence Ledger
   - Self-test case ID:
   - Probe ID:
   - Request or command executed:
   - Response evidence:
   - Authoritative state evidence:
   - Runtime evidence:
   - Observed data:
   - Status:
   - Reason:
   - Cleanup evidence:

8. Gaps and Risks
   - Not verified:
   - Reason:
   - Impact:

9. Final Judgment
   - Result:
   - Why:

10. Proposed Regression Cases
   - Candidate ID:
   - Source self-test case:
   - Probe and evidence summary:
   - Suggested priority:
```

## Proof Package

The final answer must include:

- source inventory count and any missing or unavailable source groups
- environment and safety decision, including whether writes or external side effects were executed
- original source test case count, decomposed count, and not-backend-applicable count
- risk matrix count by `applies`, `not applicable`, and `unknown`
- self-test case count and probe artifact count
- evidence ledger count by `PASS`, `FAIL`, `NOT_RUN`, `BLOCKED`, and `OUT_OF_SCOPE`
- redacted commands, calls, queries, logs, traces, code paths, or files used as evidence
- skipped or impossible checks with reason and impact
- cleanup status
- final `PASS`, `PARTIAL`, or `FAIL` judgment with the blocking evidence behind it

## Guardrails

Do not print raw secrets, cookies, authorization headers, passwords, tokens, private transcripts, private user identifiers, or full production connection strings.

Do not write to production, mutate shared data, trigger external callbacks, or send emails/notifications unless the user explicitly asked for that environment and side effect.

If safe isolated data cannot be prepared, mark the affected checks `BLOCKED` or `Manual`; do not fabricate data evidence.
