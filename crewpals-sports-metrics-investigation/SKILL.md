---
name: crewpals-sports-metrics-investigation
description: Use when investigating CrewPals running or sports metric discrepancies such as pace, distance, duration, best records, abnormal data, FIT imports, device sync, or frontend/backend display mismatches.
---

# CrewPals Sports Metrics Investigation

## Goal

Find the divergence point for CrewPals sports data and produce either a root-cause report, a scoped fix, or a verified follow-up plan. Common cases include distance, pace, duration, pause, abnormal speed, best record, personal stats, group/activity stats, FIT import, and watch-sync inconsistencies.

## Required Inputs

- Environment: prod, test, local, or unknown.
- User-visible surface: summary, segment, chart, detail, personal stats, group, activity, challenge, best list, thumbnail, or API.
- Expected vs actual behavior, with task/user/group/time identifiers redacted in reports when possible.
- Whether the task is read-only investigation, data seeding, code fix, or end-to-end verification.

Ask before production writes, data mutation, or destructive cleanup. Read-only log, DB, Redis, code, and API inspection can proceed when credentials and environment are available.

## Source Of Truth

- `crewpals-mp` frontend code for device sync, upload, display, and UI calculations.
- `group_pals` backend code for ingestion, persistence, async jobs, aggregation, API assembly, and metric definitions.
- Read-only MySQL, Redis, SLS logs, API responses, FIT files, and Feishu requirements when available.
- Runtime screenshots are supporting evidence only; they do not replace data and code tracing.

## Workflow

1. Scope every affected surface and metric. Record units, rounding, inclusion/exclusion rules, privacy rules, and whether abnormal or paused data should count.
2. Trace the pipeline: device/FIT source -> frontend sync/upload -> backend save -> async processing/aggregation -> API response -> UI rendering/cache.
3. Compare source data, stored data, API output, and UI output. Identify the first layer where values diverge.
4. Check ordering and freshness issues: async point batches, finish events, cache keys, image/SVG URL reuse, stale aggregation, and frontend rendering cache.
5. If changing code, update the owning requirement/design docs when they exist, implement the smallest fix, and add regression coverage around the metric definition.
6. Verify with representative records or files through the endpoint/UI path that originally exposed the discrepancy.

## Anti-Shortcuts

- Wrong: compare two UI screens and infer backend logic.
- Right: trace the exact metric from input data through storage, API assembly, and UI rendering.

- Wrong: treat all "abnormal" data as one rule.
- Right: state separately how abnormal speed, pause, signal loss, privacy, and best-record exclusion affect each surface.

- Wrong: trust a single task record after a fix.
- Right: verify at least one representative positive case and one case that should remain excluded when feasible.

## Success Criteria

- The report names the divergence layer and supporting evidence.
- Code fixes preserve existing public/private and abnormal-data semantics unless the user asked to change them.
- Verification exercises the user-visible path, not only an isolated helper, unless runtime access is blocked and reported.

## Proof Package

Final output must include inspected source-of-truth inputs, affected surfaces, divergence point, files changed if any, verification commands or API/UI checks, skipped checks with reasons, and remaining risk.
