---
name: ai-doc-driven-dev
description: |
  Use when a project needs docs-first workflow setup or repair, documentation drift review, canonical requirement/design updates, requirement/design generation, or bug and follow-up changes that must be routed back into existing feature documentation.
---

# AI Documentation-Driven Development

Keep project requirements, technical design, workflow rules, and implementation aligned through one canonical documentation workflow.

## Core Principle

Documentation is a living source of truth for a feature or user journey. A bug fix, regression, optimization, or follow-up change that belongs to an existing feature must update that feature's original requirement and technical design documents.

Do not create a new document just because the current work item is a bug or small change. Create a new requirement/design pair only when the work represents a new user goal, a new feature boundary, or no existing document can reasonably own it.

## Goals

1. Establish a docs-first workflow in project instruction files.
2. Detect whether the current docs are complete and paired.
3. Extract project-specific coding and architecture standards from real code.
4. Update canonical requirement/design and workflow documents in place when they already exist.
5. Generate requirement/design documents only when no existing owner can reasonably own the work.
6. Prevent documentation fragmentation by routing follow-up work to the original docs.

## Available Assets

Use the files bundled inside this skill when the target project does not already define its own standards:

- Templates in `assets/templates/`
  - `requirements-template.md`: default requirement template for a new feature or for normalizing an existing requirement doc
  - `technical-design-template.md`: default paired technical design template
  - `claude-md-template.md`: default lightweight workflow entry template for projects that use `CLAUDE.md`
  - `agents-md-template.md`: default AI execution-rules template for projects that use `AGENTS.md`
- Pattern hints in `assets/patterns/`
  - `frontend-patterns.json`: common frontend signals to inspect when extracting real project standards
  - `backend-patterns.json`: common backend signals to inspect when extracting real project standards

## Document Routing Gate

Run this gate before generating or modifying docs:

1. Classify the work item as one of:
   - New feature or new user journey
   - Change to an existing feature or journey
   - Bug fix or regression in an existing feature or journey
   - Technical refactor with user-visible behavior unchanged
   - Operational incident or investigation note
2. Detect the project's current documentation locations before assuming a directory layout.
3. Search the detected requirement, design, standards, analysis, and instruction-file locations for ownership candidates.
   Default candidates in projects that follow this skill's bundled convention are:
   - `docs/requirements/`
   - `docs/design/`
   - `docs/standards/`
   - `docs/analysis/`
   - root instruction files when workflow rules are involved
4. Match by feature name, user journey, module, route, API, business entity, acceptance criteria, issue ID, or user-visible behavior.
5. Present the selected owner document pair to the user when the route is not obvious.
6. Update the existing pair when ownership is clear.
7. Create a new pair only when no existing pair owns the work.

## Workflow Surface

This single skill covers six concerns:

1. Documentation routing
2. Documentation analysis
3. Canonical update of existing requirement/design and workflow artifacts
4. Requirement and technical design generation when no owner exists
5. Workflow enforcement in project instruction files
6. Pattern extraction for the project's standards docs

## Documentation Analysis

Inspect the full documentation surface before deciding what to change. Detect the project's actual doc and instruction locations first.

Common candidates include:

- requirement docs
- technical design docs
- standards docs
- analysis or investigation docs
- workflow instruction files such as `CLAUDE.md`, `AGENTS.md`, or `GEMINI.md`
- README files that define workflow or feature scope
- requirement and design templates that shape future doc creation behavior

Classify requirement/design pairs, naming drift, missing pairs, contradictory docs, and possible owners for the current work item.

## Requirement and Design Actions

Choose one route and apply it consistently:

| Route | Action |
| --- | --- |
| Existing pair | Update both existing requirement and design docs |
| Existing requirement only | Update requirement and create the missing design |
| Existing design only | Update design and create the missing requirement |
| New pair | Create a new requirement/design pair |
| Incident-only | Create or update an incident note only if the user explicitly asks |
| No docs applicable | Report why the change does not need docs |

When updating existing docs:

- Revise the normative behavior, not just append a loose note.
- Update acceptance criteria for user-visible fixes.
- Add change history only where it helps preserve context.
- Keep requirement and technical design synchronized.
- Link bugs, regressions, tickets, or incident references back to the canonical feature docs.

When creating a new pair, the default filenames are:

- Requirement: `docs/requirements/YYYYMMDD-feature-name.md`
- Technical design: `docs/design/YYYYMMDD-feature-name-technical-design.md`

Use those filenames only when the project follows this skill's bundled convention or the user approves adopting it. Otherwise, reuse the project's existing naming and location rules.

Same-day suffixes such as `-v2` solve filename conflicts only. They are not a substitute for updating an existing feature document.

## Update Capability

Use the update capability when the project already has canonical artifacts and the task is to revise them rather than open parallel docs.

Common update requests include:

- update, revise, refresh, amend, or sync an existing requirement/design pair
- fold a bug fix, regression, or follow-up into the original feature docs
- update workflow entry files, README files, templates, or standards docs after process drift
- bring implementation-facing docs back in sync after clarified scope or approved design changes

For update requests:

- Prefer modifying the existing canonical files in place.
- Update every workflow surface that teaches the same rule when those surfaces are in scope.
- State which files were updated and which related canonical files were intentionally left unchanged.
- Do not create replacement docs, override docs, or standalone bugfix docs just because the user asked to "update" something.

## Workflow Enforcement

When the project lacks clear rules, create or repair workflow entry files so they enforce:

- Documentation routing before new docs are created
- Requirement/design pairing
- User approval before implementation
- Alignment across active workflow surfaces so README files, templates, and instruction files do not contradict each other
- Separation of responsibilities
  - `CLAUDE.md`: lightweight workflow entry and navigation when the project uses that file
  - `AGENTS.md`: AI execution rules and guardrails when the project uses that file
  - standards docs: detailed coding, testing, and architecture guidance in the project's chosen standards location
  - README or docs overview files: contributor-facing workflow summaries when they influence how work is started
  - requirement/design templates: defaults for future canonical docs so bug fixes do not reopen the fragmentation pattern

Preserve project-specific instruction content. Do not rewrite or move existing instruction files without user approval when the change is substantive.

## Pattern Extraction

When standards are missing or stale, extract dominant conventions from real code rather than imposing generic defaults.

Look for repeated evidence in:

- file and directory naming
- module and feature boundaries
- API and data flow structure
- error handling and logging
- test organization
- configuration and environment management
- documentation and template conventions

Treat bundled pattern JSON files as hints for what to inspect, not as project standards to copy blindly.

## Typical Use Cases

- initialize docs-first development in a new repo
- repair or modernize an existing docs-first setup
- decide whether a bug belongs to an existing requirement
- update an existing requirement/design pair after clarified scope, regression, or follow-up work
- update README files, templates, or workflow entry files so future runs follow the corrected process
- update the canonical requirement/design pair for a regression or optimization
- generate a missing requirement/design pair
- extract standards into the project's standards docs

## Active Mode

After analysis, narrow the task to one active mode:

- routing-only review
- documentation drift analysis
- canonical update
- requirement/design generation
- workflow enforcement
- pattern extraction

Apply completion signals only for the active mode.

## Completion Signals

The task is complete only when the active mode's completion checks are satisfied:

- Routing-only review:
  - The work item has been classified.
  - Existing owner candidates have been checked in the detected project locations.
  - The result names the owning doc pair, the ambiguity, or the reason no owner exists.
- Documentation drift analysis:
  - Relevant documentation and instruction locations have been checked.
  - Missing pairs, naming drift, or contradictions are identified.
  - The result lists the highest-priority fixes without inventing new docs.
- Canonical update:
  - The change has been routed to existing canonical files in the detected project locations.
  - Existing requirement/design docs, workflow files, README files, templates, or standards docs in scope have been updated in place.
  - Requirement and technical design documents are synchronized when both exist or when a missing paired doc had to be created.
  - The result states which canonical files were updated, which missing paired files were created, and which related files were intentionally left unchanged.
- Requirement/design generation:
  - No existing canonical owner reasonably owns the work, or the user explicitly approved creating a new pair.
  - The new requirement/design pair uses the project's existing naming and location rules, or an approved bundled default.
  - The result states why generation was chosen instead of updating an existing canonical file.
- Workflow enforcement:
  - The project's workflow entry files, workflow-facing README files, templates, and standards locations have been identified.
  - Proposed or applied workflow rules include the routing gate before new docs are created.
  - Conflicting workflow surfaces have been aligned or explicitly left unchanged by user decision.
  - The result states which instruction files, overview files, and templates were updated, created, preserved, or left for approval.
- Pattern extraction:
  - Standards are derived from evidence in the actual project.
  - Dominant conventions and important exceptions are separated.
  - The result states which standards docs should be created or updated.

## Non-Goals

- Do not replace product ownership or user approval.
- Do not generate standalone bug docs by default.
- Do not write implementation code before the docs route and required document updates are approved.
- Do not invent project standards when the codebase does not provide evidence.
