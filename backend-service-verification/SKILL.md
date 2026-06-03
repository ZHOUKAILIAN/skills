---
name: backend-service-verification
description: Use when verifying a backend requirement or service-side change from requirements, technical plans, and QA/frontend/full-stack test cases with real service evidence.
---

# Backend Service Verification

## Goal

Prove whether a backend change is complete by deriving backend-verifiable facts, executing service-side checks, and reporting the data evidence behind the judgment.

This skill is for backend verification only. It does not verify frontend layout, visual style, animation, browser rendering, or toast placement except to extract the backend facts behind those user-visible assertions.

## Core Rule

No `PASS` without an evidence ledger.

Every backend fact, derived risk, and required negative path must have a ledger row with an expected result, evidence source, executed action or inspected source, observed data, status, and reason for any non-`PASS` status.

Wrong: "The endpoint returned 200, so backend verification passed."

Right: "The create request returned the expected schema, the authoritative row exists with the expected fields, the related count invariant holds, duplicate submit produced no second row, and the audit log contains the expected event."

## When To Use

Use this skill when the task is to verify a backend requirement, API/RPC/CLI behavior, service-side bug fix, data-write flow, async worker behavior, or full-stack/QA test case that needs backend evidence.

Use it when source test cases are written from a frontend or QA perspective and need to be decomposed into backend facts.

## When Not To Use

Do not use this skill for purely visual frontend checks, copy/layout review, browser-only behavior, or design restoration unless those checks imply backend state or service behavior.

Do not use it to maintain long-term regression assets after verification. Hand the `Proposed Regression Cases` section to `backend-regression-maintenance`.

## Source Of Truth

Use the strongest available project-local facts:

- requirement, acceptance criteria, product notes, issue, PR, or technical plan
- source QA/frontend/full-stack test cases
- API/RPC/CLI contracts, OpenAPI specs, protobufs, request validators, or route definitions
- implementation code, migrations, schemas, models, fixtures, and existing tests
- runtime configuration, service startup docs, dependency docs, CI scripts, or release docs
- authoritative state: database records, persisted files, cache keys, outbox rows, queue messages, search index records, or generated artifacts
- runtime evidence: responses, logs, traces, audit records, worker output, side effects, and cleanup evidence

Do not treat model memory, summaries, "looks correct", or HTTP 200 alone as source-of-truth evidence.

## Optional Governance Context

This skill must work without the AI Coding five-layer model.

If a five-layer classifier or equivalent governance source is available and artifact ownership, truth-source status, writeback location, or public/private history would change the verification output or repository writes, read that source as input. Do not inline or reimplement that model here, and do not require users to install it.

If that governance source is unavailable, continue with project-local discovery. Use existing project conventions for obvious destinations, keep temporary run evidence local, and mark ambiguous writeback decisions as `needs boundary decision` instead of guessing.

Do not block backend verification just because the five-layer model is unavailable. Block repository writeback only when the destination or ownership is unsafe to assume.

## Mode And Fallback Rules

Choose one active mode before proceeding:

- `plan-only`: use when the user asks only for a verification plan. Stop after the plan, mark all items `NOT_RUN`, and do not claim backend behavior passed.
- `execute-verification`: use by default when the user asks to verify, test, prove, or check completion. Produce the plan, execute safe checks, and fill the evidence ledger.
- `evidence-review-only`: use when the environment cannot be run but reports, logs, database snapshots, or prior outputs are available. Review only the supplied evidence and report `PARTIAL` unless the evidence fully satisfies the completion standard.

Fallbacks:

- If startup, credentials, test data, or dependency access is unsafe or unavailable, mark affected items `BLOCKED` or `NOT_RUN`; do not invent evidence.
- If a mechanical check cannot run, use manual inspection evidence only when the inspected source is named and the gap impact is reported.
- If repository writeback ownership is unclear, continue verification but mark writeback `needs boundary decision`.

## Workflow

### 1. Source Inventory Gate

Before planning verification, enumerate the source materials and mark each as `read`, `missing`, `unavailable`, or `not applicable`.

Required inventory groups:

1. requirement or acceptance source
2. technical plan or implementation intent
3. source test cases, if provided
4. API/RPC/CLI contract or route definition
5. implementation code path
6. schema, model, migration, fixture, or authoritative state definition
7. project startup, dependency, test, or CI convention
8. log, trace, queue, cache, worker, or side-effect convention when relevant

Anti-laziness gate: do not write "docs reviewed" or "project conventions checked" without naming the files, commands, or sources inspected. If a source group is missing, record the impact before proceeding.

### 2. Source Test Case Decomposition Gate

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

Anti-laziness gate: zero unaccounted original cases. If one original case implies multiple backend facts, split them into separate verification items instead of testing only the obvious happy path.

Wrong: "Click Save shows success toast, so call the save API once."

Right: "The case implies create/update behavior. Verify response contract, authoritative persisted state, related records, duplicate submit behavior, and any required audit or async side effect."

### 3. Backend Risk Derivation Gate

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

Anti-laziness gate: no batch `N/A`. Every category needs a cited reason from requirement, code, schema, or project convention. Every `applies` or `unknown` category needs a verification item, blocker, or explicit out-of-scope decision.

### 4. Verification Plan Gate

Before executing, produce a concise plan with one verification item per backend fact or applicable risk.

Each item must include:

```text
Verification item ID:
Source case or risk:
Expected backend behavior:
Data setup and isolation:
Action to execute or source to inspect:
Evidence sources:
Authoritative state checks:
Invariant, idempotency, concurrency, permission, state, async, log, or side-effect checks:
Cleanup:
PASS criterion:
```

If the user only asks for a plan, stop after the plan and mark every item `NOT_RUN`.

Anti-laziness gate: the plan must name concrete evidence sources. "Run backend verification" is not a plan. "Check DB" is not enough unless the authoritative table/store, record identity, or lookup strategy is named.

### 5. Execution Evidence Gate

Execute the plan using the project's discovered conventions. If execution is unsafe or impossible, mark the affected item `BLOCKED` or `NOT_RUN` with the reason.

For every item, maintain an evidence ledger:

```text
Item ID:
Expected result:
Action performed:
Evidence source: response | database | cache | queue | log | trace | audit | file | code | test output | other
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

Anti-laziness gate: one large command or one broad test suite run can support many rows, but it does not replace the ledger. Map the command output or runtime evidence back to each item. Details that are not mapped are not verified.

## Completion Standard

Report **PASS** only when all applicable conditions are met:

1. source inventory is complete or gaps are documented as non-blocking
2. every original source test case is decomposed or marked not backend-applicable with reason
3. every backend fact is mapped to a verification item
4. every risk category is individually classified with evidence
5. every applicable or unknown risk is verified, blocked, or explicitly scoped out
6. the evidence ledger has no `NOT_RUN` or `BLOCKED` row for required scope
7. every required authoritative state check passed
8. every required invariant, idempotency, concurrency, permission, state, async, side-effect, log, trace, or audit check passed
9. important negative paths are verified or explicitly scoped out
10. test data cleanup is completed or documented

Report **PARTIAL** when evidence is incomplete, an environment is unavailable, a required item is `NOT_RUN` or `BLOCKED`, or an applicable risk is only planned but not executed.

Report **FAIL** when observed behavior violates the requirement, technical plan, API contract, authoritative state, invariant, or safety boundary.

Anti-laziness gate: do not downgrade missing evidence into "low risk" and still report `PASS`. Missing required evidence is `PARTIAL`; contradictory evidence is `FAIL`.

## Gate Failure Behavior

When a gate is incomplete, first try to fill the missing ledger rows, source references, or execution evidence.

If the missing item cannot be filled safely, do not continue to a `PASS` result. Mark the affected item `NOT_RUN`, `BLOCKED`, or `OUT_OF_SCOPE` with reason, then report `PARTIAL` unless observed evidence already requires `FAIL`.

Do not convert a failed gate into a vague residual risk. The failed item must appear in the report's evidence ledger or gaps section.

## Proposed Regression Cases

Propose regression cases only from verified backend facts, observed failures, or documented manual checks.

Each proposed case must include:

```text
Candidate ID:
Source verification item:
Evidence summary:
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

2. Original Test Case Decomposition
   - Original case ID:
   - Frontend-only assertions:
   - Backend facts:
   - Full-stack/manual assertions:
   - Derived backend risks:
   - Status and reason:

3. Risk Coverage Matrix
   - Risk category:
   - Applies / not applicable / unknown:
   - Evidence:
   - Verification item or out-of-scope reason:

4. Verification Plan
   - Item ID:
   - Expected backend behavior:
   - Evidence sources:
   - Data setup and cleanup:
   - PASS criterion:

5. Execution Evidence Ledger
   - Item ID:
   - Action performed:
   - Observed data:
   - Status:
   - Reason:
   - Cleanup evidence:

6. Gaps and Risks
   - Not verified:
   - Reason:
   - Impact:

7. Final Judgment
   - Result:
   - Why:

8. Proposed Regression Cases
   - Candidate ID:
   - Source verification item:
   - Evidence summary:
   - Suggested priority:
```

## Proof Package

The final answer must include:

- source inventory count and any missing or unavailable source groups
- original source test case count, decomposed count, and not-backend-applicable count
- risk matrix count by `applies`, `not applicable`, and `unknown`
- evidence ledger count by `PASS`, `FAIL`, `NOT_RUN`, `BLOCKED`, and `OUT_OF_SCOPE`
- commands, calls, queries, logs, traces, code paths, or files used as evidence
- skipped or impossible checks with reason and impact
- cleanup status
- final `PASS`, `PARTIAL`, or `FAIL` judgment with the blocking evidence behind it

## Guardrails

Do not print raw secrets, cookies, authorization headers, passwords, tokens, private transcripts, private user identifiers, or full production connection strings.

Do not write to production, mutate shared data, trigger external callbacks, or send emails/notifications unless the user explicitly asked for that environment and side effect.

If safe isolated data cannot be prepared, mark the affected checks `BLOCKED` or `Manual`; do not fabricate data evidence.
