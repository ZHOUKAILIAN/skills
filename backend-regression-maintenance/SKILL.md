---
name: backend-regression-maintenance
description: Use after backend verification to maintain reusable backend regression cases, classify P0/P1/P2/Manual coverage, and define pre-release run lists.
---

# Backend Regression Maintenance

## Goal

Turn verified backend scenarios into reusable regression coverage that protects future releases.

This skill consumes backend verification reports, evidence ledgers, proposed regression cases, existing regression files, and project conventions. It does not re-run backend verification and does not re-classify raw frontend cases from scratch.

## Core Rule

No regression case without backend evidence.

Every proposed case must have a decision ledger row that traces to verification evidence, names the backend-observable assertion, records deduplication, assigns priority with a reason, and states the writeback target or writeback blocker.

Wrong: "The frontend case is important, so add it to backend regression."

Right: "The verification evidence proved duplicate coupon claim creates only one claim row and one user coupon. Add a P0 idempotency regression case in the existing coupon service test file."

## When To Use

Use this skill after backend verification has produced a report, evidence ledger, proposed regression cases, or observed backend failures that may become long-term regression coverage.

Use it to update project regression indexes, testcase files, automated tests, release checklists, or pre-release run lists according to existing project conventions.

## When Not To Use

Do not use this skill to prove the current backend change is correct. Use `backend-service-verification` first.

Do not use it to copy frontend layout, animation, toast placement, or browser-rendering cases into backend regression unless there is a backend-observable assertion.

## Source Of Truth

Use the strongest available project-local facts:

- backend verification report and evidence ledger
- proposed regression cases
- original requirement, technical plan, PR, issue, or source test case when needed for traceability
- existing backend regression index, testcase files, automated tests, fixtures, mocks, and naming conventions
- release, CI, preflight, or pre-release checklist documentation
- project ownership or writeback policy when available

If proposed cases are missing, derive candidates from the verification report only. If the report lacks backend evidence, mark the candidate `NEEDS_REVIEW` instead of inventing a stable regression case.

## Optional Governance Context

This skill must work without the AI Coding five-layer model.

If a five-layer classifier or equivalent governance source is available and ownership, truth-source status, writeback location, split/merge decision, or public/private history would change where regression assets are written, read that source as input. Do not inline or reimplement that model here, and do not require users to install it.

If that governance source is unavailable, follow existing project testcase, test, release, and CI conventions. If the destination is obvious, proceed and record the assumption. If the destination is not obvious, produce case decisions and the run list, then mark file writeback `NEEDS_REVIEW`.

Do not discard regression decisions just because governance classification is unavailable. Block only unsafe writeback.

## Mode And Fallback Rules

Choose one active mode before proceeding:

- `maintain-assets`: use when the project has an obvious regression/test/checklist location or the user has chosen a writeback target. Update the target asset and verify the maintenance result.
- `decision-only`: use when writeback ownership, destination, or format is unclear. Produce candidate decisions and a pre-release run list, but mark file writeback `NEEDS_REVIEW`.
- `review-only`: use when the user asks only to review proposed regression coverage. Do not edit files; report decisions, gaps, and recommended writeback targets.

Fallbacks:

- If the evidence ledger is unavailable, derive candidates only from named backend evidence in the verification report and mark weak candidates `NEEDS_REVIEW`.
- If no existing regression format exists, use the concise case record format in this skill unless the user asks for a different format.
- If mechanical validation cannot run, report manual inspection evidence and the skipped check impact.

## Regression Case Eligibility

A backend regression case must have at least one backend-observable assertion:

- API/RPC/CLI response contract
- database or persisted-state check
- cache, queue, outbox, search index, file, webhook, email, notification, or worker effect
- log, trace, audit, or event evidence
- idempotency, consistency, concurrency, permission, isolation, state-machine, migration, or compatibility assertion

Reject or mark `Manual` when a case is only about frontend layout, animation, visual style, browser rendering, or toast placement with no backend fact.

Temporary run logs, scratch SQL, and local evidence can justify a candidate, but they are not themselves stable regression cases.

## Workflow

### 1. Input Evidence Gate

Before changing regression assets, read and account for:

1. backend verification report
2. execution evidence ledger
3. proposed regression cases
4. existing regression/testcase files
5. existing automated tests, fixtures, mocks, and naming conventions
6. release, CI, or pre-release run documentation
7. ownership or writeback policy when available

Anti-laziness gate: do not proceed from a summary alone when the verification report or evidence ledger is available. If the evidence ledger is absent, every candidate derived from the report starts as `NEEDS_REVIEW` until backend evidence is identified.

### 2. Candidate Accounting Gate

Create a decision ledger row for every proposed case and every backend failure that should be considered for regression.

Required fields:

```text
Candidate ID:
Source self-test case, verification item, or failure:
Evidence summary:
Backend-observable assertion:
Eligibility: eligible | manual | reject | needs_review
Decision: add | update | merge | duplicate | reject | manual | needs_review
Reason:
```

Anti-laziness gate: zero unaccounted candidates. Do not group several proposed cases under one broad "covered by regression" statement unless each candidate has its own decision row.

### 3. Deduplication Gate

Compare each eligible candidate with existing regression cases and automated tests.

Deduplicate by behavior and authoritative assertion, not just title. Check:

1. API/RPC/CLI contract
2. state or persisted-data assertion
3. invariant, idempotency, concurrency, permission, state, async, or migration assertion
4. fixture/setup overlap
5. existing test failure mode or historical bug link

Anti-laziness gate: every `duplicate` or `merge` decision must name the existing file, test, case ID, or checklist item it maps to. If the target cannot be named, the decision is `needs_review`, not `duplicate`.

### 4. Priority Gate

Assign `P0`, `P1`, `P2`, or `Manual` for every non-rejected candidate.

Use `P0` for cases that must run before every release:

- login, auth, permission, tenant isolation, or ownership boundaries
- core money, coupon, reward, order, inventory, balance, or data-write flows
- idempotency for duplicate submit/callback/retry paths that could create loss or corruption
- consistency invariants whose failure would corrupt core data
- historically fragile critical paths

Use `P1` for important module behavior that should run when the related module, data model, API, worker, queue, cache, or dependency changes.

Use `P2` for lower-frequency, edge, compatibility, migration, export, backfill, or expensive cases that should run during major releases or scheduled regression.

Use `Manual` when the case requires human confirmation, unavailable third-party systems, real external callbacks, unstable test data, or an environment that cannot be reproduced safely.

Anti-laziness gate: no batch priority assignment. Every priority needs a reason tied to business risk, data risk, release risk, historical fragility, or execution cost.

### 5. Writeback Gate

Keep the project's existing format and location. Do not introduce a new testcase directory structure if the project already has one.

For every accepted candidate, record:

```text
Target file or asset:
Change type: add | update | merge | checklist-only | manual-only
Writeback boundary: existing convention | user decision | needs_review
Automation status: automated | manual-command | manual | pending
```

If no format exists, use a concise record with:

```text
ID:
Title:
Module:
Priority: P0 | P1 | P2 | Manual
Source:
Backend assertions:
Inputs / fixtures:
Expected response:
Expected state:
Consistency / idempotency / concurrency checks:
Logs / side effects:
Automation status: automated | manual-command | manual | pending
Cleanup:
```

Anti-laziness gate: do not write temporary evidence into a formal regression suite. Promote only stable backend assertions with traceable source context.

### 6. Pre-Release Run List Gate

Generate a practical run list instead of saying "run everything":

1. all P0 cases
2. P1 cases for changed modules
3. migration/data-integrity cases when schema, backfill, or persistence changes
4. async/queue/outbox/cache cases when related infrastructure changes
5. relevant P2 cases for major releases or high-risk changes
6. Manual cases that still require human verification

Anti-laziness gate: every `P0` and every `Manual` case must appear in the run list or have a reason why it is not runnable for the current release. P1/P2 inclusion must name the changed module or release condition.

### 7. Maintenance Verification Gate

After editing files or producing the run list, verify the maintenance result.

Check:

1. every candidate has one decision row
2. every non-rejected case has priority and traceable source evidence
3. new or edited IDs are unique within the target scope
4. accepted P0 and Manual cases are represented in the pre-release run list
5. target files follow existing project format and naming conventions
6. available formatters, linters, tests, validators, or index checks have run

Anti-laziness gate: a successful write is not enough. If the index, generated list, or target test file cannot be verified mechanically, report the manual inspection evidence and remaining risk.

## Completion Standard

Report **UPDATED** only when intended file or run-list changes were made, all candidate decisions are accounted for, and maintenance verification passed or any skipped checks are explained.

Report **NO_CHANGE** only when all candidates were duplicates, rejected, manual-only, or already covered, and every such decision names the existing coverage or rejection reason.

Report **NEEDS_REVIEW** when writeback destination, evidence, deduplication, priority, or ownership is insufficient for a safe update.

For a pre-release judgment:

- Report **PASS** only if required P0 cases pass and required evidence is available.
- Report **PARTIAL** if manual cases, unavailable environments, or unexecuted required cases remain.
- Report **FAIL** if any required P0 case fails or a regression case reveals incorrect behavior.

## Gate Failure Behavior

When a gate is incomplete, first fill the missing decision rows, deduplication evidence, priority reasons, run-list entries, or maintenance checks.

If the missing item cannot be resolved safely, do not report `UPDATED` or `NO_CHANGE` as if maintenance is complete. Mark the affected candidate or writeback target `NEEDS_REVIEW`, and include the blocker in the report.

Do not convert missing evidence or unnamed duplicate coverage into a minor follow-up. A candidate without evidence, priority reason, or named duplicate target remains unresolved.

## Report Format

Use this structure:

```text
Backend Regression Maintenance Report

Result: UPDATED | NO_CHANGE | NEEDS_REVIEW

1. Inputs
   - Verification report:
   - Evidence ledger:
   - Existing regression files:
   - Project conventions:
   - Writeback policy:

2. Candidate Decision Ledger
   - Candidate ID:
   - Evidence summary:
   - Backend assertion:
   - Eligibility:
   - Decision:
   - Priority:
   - Reason:
   - Target file:

3. Deduplication Results
   - Candidate ID:
   - Existing coverage:
   - Decision:

4. Files Updated
   - File:
   - Change:
   - Verification:

5. Regression Index Summary
   - P0:
   - P1:
   - P2:
   - Manual:

6. Pre-Release Run List
   - P0 all-release cases:
   - P1 changed-module cases:
   - Required migration/data/async cases:
   - Relevant P2 cases:
   - Manual checks:

7. Skipped, Rejected, or Needs Review
   - Candidate:
   - Reason:
   - Required next decision:

8. Maintenance Verification
   - Checks run:
   - Result:
   - Skipped checks and reason:
```

## Proof Package

The final answer must include:

- input evidence inspected, including whether an evidence ledger was available
- candidate count and decision count, including `add`, `update`, `merge`, `duplicate`, `reject`, `manual`, and `needs_review`
- deduplication evidence for every duplicate or merge decision
- priority summary for P0, P1, P2, and Manual
- files or run-list artifacts changed, or the writeback blocker
- maintenance verification checks run and their result
- skipped or impossible checks with reason and impact
- final `UPDATED`, `NO_CHANGE`, or `NEEDS_REVIEW` result

## Guardrails

Do not write secrets, private user identifiers, production connection strings, raw tokens, or customer data into regression cases, reports, commits, or run lists.

Do not add tests that mutate production or shared environments. If only unsafe data is available, mark the case `Manual` or `NEEDS_REVIEW`.
