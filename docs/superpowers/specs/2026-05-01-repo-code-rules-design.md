# Repository Code Rules Design

Date: 2026-05-01

## Purpose

`ai-doc-driven-dev` should keep its docs-first workflow, but project-specific code standards should move out of generated documentation standards and into a dedicated `rules/` directory in the target repository.

The `rules/` directory is only for code rules. It does not replace requirement docs, technical design docs, analysis docs, or workflow instructions.

## Target Repository Shape

When `ai-doc-driven-dev` initializes or repairs a target repository, the preferred generated structure is:

```text
<repo>/
  AGENTS.md

  rules/
    coding.md
    frontend.md
    backend.md
    testing.md

  docs/
    requirements/
      YYYYMMDD-feature-name.md

    design/
      YYYYMMDD-feature-name-technical-design.md

    analysis/
      YYYYMMDD-topic-analysis.md

    standards/
      non-code-standard.md
```

Generation is conditional:

- `AGENTS.md` is the Codex entry point.
- `rules/coding.md` is created when code rules are initialized or extracted.
- `rules/frontend.md` is created only when the repository has frontend code or frontend-specific conventions.
- `rules/backend.md` is created only when the repository has backend code or backend-specific conventions.
- `rules/testing.md` is created only when testing conventions are detected or need separate rules.
- `docs/requirements/` and `docs/design/` remain the canonical requirement and technical design locations.
- `docs/analysis/` is created only for investigation, audit, or analysis artifacts.
- `docs/standards/` remains optional and should not be the default location for code rules.

There is no `rules/README.md`. `AGENTS.md` owns rule discovery and indexing.

## File Responsibilities

### `AGENTS.md`

`AGENTS.md` is the main Codex-facing entry point. It should stay short and point to the right source of truth.

It should include:

- The docs-first workflow entry.
- The requirement/design routing gate.
- A statement that code rules live in `rules/*.md`.
- A short rule index that tells Codex which rule file to read for implementation, frontend work, backend work, and tests.
- A reminder that `rules/` contains code rules only.

It should not include:

- Full coding standards copied from `rules/`.
- Long requirement or technical design templates.
- Project-specific code details that belong in `rules/`.

### `rules/coding.md`

`rules/coding.md` contains shared code conventions that apply across the repository.

Typical content:

- File and directory naming.
- Module boundaries.
- Shared architecture rules.
- Error handling and logging conventions.
- Configuration and environment rules.
- Dependency and abstraction rules.
- Cross-cutting maintainability rules.

### `rules/frontend.md`

`rules/frontend.md` contains frontend-only conventions.

Typical content:

- Component structure.
- State management.
- API call boundaries.
- Styling conventions.
- Accessibility expectations.
- Frontend test conventions when they are tightly coupled to frontend code.

### `rules/backend.md`

`rules/backend.md` contains backend-only conventions.

Typical content:

- API handler and service boundaries.
- Data access patterns.
- Validation and error response conventions.
- Transaction and idempotency rules.
- Background job or queue conventions.
- Backend observability rules.

### `rules/testing.md`

`rules/testing.md` contains repository testing conventions when they deserve their own file.

Typical content:

- Unit, integration, and E2E test boundaries.
- Test file naming.
- Fixture and mock conventions.
- Required verification commands.
- Rules for adding tests with feature changes or bug fixes.

### `docs/requirements/`

Requirement documents remain the source of truth for user-visible behavior, acceptance criteria, scope, and edge cases.

### `docs/design/`

Technical design documents remain paired with requirements and describe implementation architecture, data flow, APIs, risks, and verification.

### `docs/analysis/`

Analysis documents are optional and used for investigations, audits, migrations, or research notes that are not canonical feature requirements.

### `docs/standards/`

`docs/standards/` is optional. It may contain non-code project standards such as documentation process, release process, business terminology, or operational conventions.

It should not be used as the default code-standard location after `rules/` is introduced.

## `ai-doc-driven-dev` Skill Changes

The skill should keep its current docs-first responsibilities:

- Documentation routing.
- Requirement/design pairing.
- Canonical requirement and design updates.
- Requirement/design generation when no owner exists.
- Workflow enforcement through project instruction files.

The code-standard responsibility changes:

- Existing "pattern extraction" becomes code rules extraction and sync.
- Extracted project-specific code conventions are written to target-repository `rules/*.md`.
- The skill does not store project-specific code rules inside its own `SKILL.md`.
- The skill does not generate a generic all-in-one code standards document under `docs/standards/` by default.

The skill may keep pattern hint assets such as:

```text
ai-doc-driven-dev/
  assets/
    patterns/
      frontend-patterns.json
      backend-patterns.json
```

These assets are only inspection hints. They are not copied directly into target repositories as rules.

The skill may optionally include skeletal rule templates later, but those templates must be empty structure only. They must not contain concrete project code standards.

## Active Modes

`ai-doc-driven-dev` should continue to narrow each task to one active mode.

Recommended active modes after this change:

- `routing-only review`
- `documentation drift analysis`
- `canonical update`
- `requirement/design generation`
- `workflow enforcement`
- `code rules extraction`
- `code rules sync`

`code rules extraction` creates or updates `rules/*.md` from repository evidence.

`code rules sync` updates existing `rules/*.md` when code conventions drift or when the user asks to refresh code standards.

## Rules Extraction Behavior

When extracting code rules, the skill should:

1. Detect the repository type and major code areas.
2. Inspect real code before writing rules.
3. Separate shared rules from frontend, backend, and testing rules.
4. Create only the rule files justified by repository evidence.
5. Preserve existing project-specific rules unless they conflict with stronger code evidence or user direction.
6. Keep docs-first workflow content in `AGENTS.md` and docs, not in `rules/`.
7. Report which rule files were created, updated, skipped, or intentionally left unchanged.

If multiple code areas exist in a monorepo, the first version should still prefer the top-level `rules/` directory unless the repository already has a stronger local convention.

## Error Handling

If the repository already has code rules in another location:

- Reuse the existing location when it is clearly established and `AGENTS.md` already points there.
- Ask before moving established rules into top-level `rules/`.
- Avoid duplicating the same rule in both `docs/standards/` and `rules/`.

If the repository has no clear code conventions:

- Create minimal skeletal rule files only when the user asked to initialize rules.
- Do not invent detailed standards without code evidence.
- Mark missing evidence explicitly in the response instead of filling the gap with generic advice.

If `AGENTS.md`, `CLAUDE.md`, or other instruction files conflict:

- Treat `AGENTS.md` as the Codex primary entry point.
- Align other instruction files only when they are in scope or the user asks for cross-tool compatibility.

## Testing And Verification

For the skill implementation, verification should include:

- Updating a repo with only shared code rules creates `AGENTS.md` and `rules/coding.md`.
- Updating a frontend repo creates or updates `rules/coding.md` and `rules/frontend.md`.
- Updating a backend repo creates or updates `rules/coding.md` and `rules/backend.md`.
- Updating a full-stack repo separates shared, frontend, backend, and testing conventions.
- Existing requirement/design docs remain under `docs/requirements/` and `docs/design/`.
- Existing non-code standards under `docs/standards/` are preserved.
- Code rules are not written into `docs/standards/` by default.
- `AGENTS.md` indexes `rules/*.md` without duplicating their full content.

## Open Scope

This design does not require cross-tool compatibility in the first implementation. `CLAUDE.md`, `GEMINI.md`, and Copilot-specific instruction files can be handled later as thin compatibility entries that point to `AGENTS.md` and `rules/`.

This design does not require a `rules/README.md`.
