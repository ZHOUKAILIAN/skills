---
name: e2e-coverage-guard
description: |
  Use when the user provides a Feishu link (Base table or Doc) with bugs, features, requirements, or optimizations and wants E2E coverage checked or filled for affected user journeys.
---

# E2E Coverage Guard

For every code change tracked in Feishu, identify the user journey it belongs to, and ensure that journey has complete E2E coverage.

## Core Insight

A bug is not an isolated event — it is a symptom of an incomplete user journey test. A feature is not a standalone addition — it extends or creates a user journey. The right unit of E2E testing is the **journey**, not the individual change record.

This means:

- Do NOT create one test per bug. Instead, find which journey the bug belongs to, and make sure that journey is fully covered.
- If a journey's E2E test is complete, no bug in that journey should be possible without the test catching it.
- A new bug means the journey test has a gap. Fill the gap in the journey, not bolt on an isolated test.

## Goal

Given a Feishu link and a target project:

1. Read change records from the Feishu source.
2. Map each change to the user journey it affects.
3. Assess the E2E coverage of each affected journey (not each individual record).
4. For journeys with gaps, generate or extend E2E tests to close the gaps.
5. Output a summary by journey.

## Success Criteria

- Every change record is mapped to a user journey.
- Every affected journey is classified: **Fully covered**, **Gap filled**, **Skipped**, or **No E2E applicable**.
- Generated tests are organized by journey, not by individual bug/feature.
- Generated tests follow the project's existing E2E conventions (framework, naming, directory, patterns).
- Generated tests include traceable references back to the Feishu source.
- No duplicate or fragmented tests — one journey, one test file (or one describe block).

## Core Terms

- **User journey**: a complete end-to-end flow from the user's perspective. Examples: "user registers and logs in", "user adds item to cart and checks out", "user submits a form and sees confirmation". A journey has a starting point, a sequence of user actions, and an expected end state.
- **Journey map**: the mapping from change records to user journeys. Multiple changes often map to the same journey.
- **Journey coverage**: whether the E2E test for a journey exercises all critical paths, including the path that the change record describes.

## Available Tools

### Feishu access: lark-cli

Use `lark-cli` to read from Feishu. It supports both Base tables and Docs.

- **Base tables**: `lark-cli base` subcommands — list fields, list/filter records.
- **Docs**: `lark-cli docs` subcommands — get doc content.

Run `lark-cli base --help` or `lark-cli docs --help` to discover the exact commands and flags. Do not guess — read the help output.

If lark-cli is not authenticated, guide the user through `lark-cli config init` and `lark-cli auth login --recommend`.

### Source type detection

Determine source type from the URL the user provides:

- `/base/` in URL → Base table
- `/docx/`, `/docs/`, `/wiki/` in URL → Doc
- Ambiguous → ask the user

## Inputs

Ask the user for anything not already known:

| Input | Required | Notes |
|-------|----------|-------|
| Feishu URL | Yes | Base or Doc link |
| Record filter | If Base | View name, field filter, or specific record IDs |
| Section filter | No | For Docs: heading keyword to scope which sections to process |
| Target project path | Yes | The codebase to check and generate tests in |

Auto-detect from the project (do not ask unless detection fails):
- E2E test framework and version
- E2E test directory and file naming convention
- Existing test patterns (page objects, selectors, fixtures, assertions)

## Workflow

### 1. Read change records

**From Base**: list the table fields first to understand the schema, then pull records with the user's filter. Adapt to whatever column names the table uses.

**From Doc**: read the doc content. Treat each heading-level section (H2/H3) as one change record. If the doc structure is unclear (no headings, mixed topics), ask the user to identify the relevant sections.

Parse each record into a change summary with whatever fields are available:

- Title, type (bug/feature/requirement/optimization), module or feature area
- Description of the change and user-visible behavior
- Acceptance criteria (if available)
- For bugs: reproduction steps, expected result, actual result
- Source reference: record ID (Base) or section heading + doc URL (Doc)

### 2. Map changes to user journeys

This is the critical step. Do not skip it.

1. **Identify the user journey** each change belongs to. Ask: "What is the user trying to do when this bug/feature is triggered?" The answer is the journey.
2. **Group changes by journey**. Multiple bugs and features often belong to the same journey (e.g., three bugs in the checkout flow all belong to the "user checks out" journey).
3. **Name each journey clearly**: use the format "user [verb] [object]" (e.g., "user submits loan application", "user edits profile settings").
4. **Define the journey's critical path**: the sequence of user actions from start to end, including the happy path and the key edge cases revealed by the change records.

If a change cannot be mapped to a user journey (e.g., pure backend infra), mark it as **No E2E applicable**.

Present the journey map to the user for confirmation before proceeding.

### 3. Assess journey coverage

For each affected journey:

1. **Find existing E2E tests** that cover this journey. Search by journey-related keywords in test file names, describe/test/it blocks, and page navigation logic.
2. **Read the existing tests** to understand what steps and assertions they already cover.
3. **Compare against the journey's critical path** (including the edge cases revealed by the change records). Identify which steps or assertions are missing.
4. **Classify**:
   - **Fully covered** — the existing test already exercises the full journey including the scenarios from the change records. Nothing to do.
   - **Has gaps** — the existing test covers part of the journey but misses the scenarios from the change records. Extend it.
   - **Not covered** — no existing test covers this journey. Create one.

### 4. Fill coverage gaps

For each journey with gaps:

- **If extending an existing test**: add the missing steps/assertions to the existing test file. Keep the test coherent as a single journey, not a collection of unrelated checks.
- **If creating a new test**: write a complete journey test that covers the full flow, not just the individual bug scenario. The change records inform which edge cases to include, but the test should make sense as a standalone journey.

Generated tests must:

- Follow the project's E2E test profile exactly (framework, selectors, fixtures, assertions)
- Include source reference comments linking back to the Feishu records that motivated the test
- Test the full journey flow, with the specific change scenarios as assertions within that flow

### 5. Report

Print a summary organized by journey:

```
Journey: user submits loan application
  Status: Gap filled
  Test file: e2e/loan-application.spec.ts
  Changes covered:
    - [Bug] 输入为空时崩溃 (recXXXX) → added empty input assertion
    - [Feature] 新增证件类型选择 (recYYYY) → added ID type selection step
    - [Bug] 提交后页面白屏 (recZZZZ) → added success page assertion

Journey: user views order history
  Status: Fully covered (existing test)
  Test file: e2e/order-history.spec.ts
  Changes covered:
    - [Optimization] 订单列表加载优化 (recAAAA) → already tested

Journey: database index optimization
  Status: No E2E applicable (no user-visible behavior)
  Changes:
    - [Optimization] 优化查询索引 (recBBBB)
```

## Hard Gates

1. **No Feishu access → stop.** The Feishu artifact is the source of truth. Do not fabricate change descriptions from chat or memory.
2. **No code found → skip.** Do not generate tests with invented selectors or guessed routes. Mark as Skipped.
3. **No existing tests → ask first.** If the project has zero E2E tests, ask the user which framework and base setup to use before generating anything.
4. **Journey map before generation.** Always map changes to journeys and get user confirmation before writing any test code.
5. **Generate only, do not run.** This skill produces test files. The user decides when to run them.

## Edge Cases

- **Chinese descriptions**: test function names in English, comments and references in the original language.
- **Screenshots without text**: ask the user for a text description. Do not interpret screenshots.
- **User provides both Base and Doc**: process in sequence, de-duplicate by title — prefer the Base record (more structured).
- **Doc mixes topics** (meeting notes + changes + discussion): only process sections describing concrete code changes.
- **A change spans multiple journeys**: list it under each relevant journey. The test in each journey covers its own aspect.
- **Journey is too broad** (e.g., "user uses the app"): break it into sub-journeys at the page or feature level. A journey should be testable in one E2E test file.
