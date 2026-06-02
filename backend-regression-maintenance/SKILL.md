---
name: backend-regression-maintenance
description: Use after backend verification to maintain reusable backend regression cases, classify P0/P1/P2/Manual coverage, and define pre-release run lists.
---

# Backend Regression Maintenance

## Goal

Turn verified backend scenarios into a reusable regression asset that protects future releases.

This skill does not re-run backend verification and does not re-classify raw frontend cases from scratch. It consumes backend verification reports, proposed regression cases, existing regression files, and project conventions to update the long-term backend regression suite.

## Inputs

Use available materials such as:

1. backend verification report
2. proposed regression cases
3. original requirement and technical plan when needed for traceability
4. existing backend regression index or testcase files
5. existing automated test files and naming conventions
6. release or CI documentation

If proposed cases are missing, derive them from the verification report only. If the report lacks backend evidence, mark the case `NEEDS_REVIEW` instead of inventing a stable regression case.

## Regression Case Eligibility

A backend regression case must have at least one backend-observable assertion:

- API/RPC/CLI response contract
- database or persisted-state check
- cache, queue, outbox, search index, file, webhook, email, notification, or worker effect
- log, trace, audit, or event evidence
- idempotency, consistency, concurrency, permission, isolation, state-machine, or migration assertion

Reject or mark `Manual` when a case is only about frontend layout, animation, visual style, browser rendering, or toast placement with no backend fact.

## Maintenance Procedure

1. Read the verification report and proposed regression cases.
2. Discover the project’s existing regression/testcase organization before editing.
3. Compare proposed cases with existing cases to avoid duplicates.
4. Add, update, merge, reject, or mark cases for review.
5. Assign priority: P0, P1, P2, or Manual.
6. Preserve traceability to the requirement, source test case, PR, issue, or verification report.
7. Update the regression index or module file used by the project.
8. Produce a pre-release run list.

Do not introduce a new testcase directory structure if the project already has one. Follow the project’s existing organization unless the user asks for a new structure.

## Priority Rules

### P0 — Every Release

Use P0 for backend cases that must run before every release:

- login, auth, permission, tenant isolation, or ownership boundaries
- core money, coupon, reward, order, inventory, balance, or data-write flows
- idempotency for duplicate submit/callback/retry paths that could create loss or corruption
- consistency invariants whose failure would corrupt core data
- historically fragile critical paths

P0 failure blocks a PASS pre-release judgment.

### P1 — Related Module Changes

Use P1 for important module-level behavior that should run when the related module, data model, API, worker, queue, cache, or dependency changes.

### P2 — Periodic or Major Release

Use P2 for lower-frequency, edge, compatibility, migration, export, backfill, or expensive cases that should run during major release or scheduled regression.

### Manual — Documented but Not Automated

Use Manual when the case requires human confirmation, unavailable third-party systems, real external callbacks, unstable test data, or an environment that cannot be reproduced safely.

Manual cases remain visible in the release checklist and must not be silently dropped.

## Case Record Fields

Keep the project’s existing format. If no format exists, use a concise record with:

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

## Pre-Release Run List

Generate a practical run list instead of saying “run everything”:

1. all P0 cases
2. P1 cases for changed modules
3. migration/data-integrity cases when schema, backfill, or persistence changes
4. async/queue/outbox/cache cases when related infrastructure changes
5. relevant P2 cases for major releases or high-risk changes
6. Manual cases that still require human verification

Report **PASS** only if required P0 cases pass and required evidence is available.

Report **PARTIAL** if manual cases, unavailable environments, or unexecuted required cases remain.

Report **FAIL** if any required P0 case fails or a regression case reveals incorrect behavior.

## Report Format

Use this structure:

```text
Backend Regression Maintenance Report

Result: UPDATED | NO_CHANGE | NEEDS_REVIEW

1. Inputs
   - Verification report:
   - Existing regression files:
   - Project conventions:

2. Case Decisions
   - Proposed case:
   - Decision: add | update | merge | duplicate | reject | manual | needs_review
   - Priority:
   - Reason:
   - Target file:

3. Files Updated
   - ...

4. Regression Index Summary
   - P0:
   - P1:
   - P2:
   - Manual:

5. Pre-Release Run List
   - P0 all-release cases:
   - P1 changed-module cases:
   - Required migration/data/async cases:
   - Manual checks:

6. Skipped or Rejected
   - Reason:

7. Follow-ups
   - Cases needing automation:
   - Missing environment/docs:
```
