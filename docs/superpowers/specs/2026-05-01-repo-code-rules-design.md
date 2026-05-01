# Repository Code Rules Design

Date: 2026-05-01

## Purpose

`ai-doc-driven-dev` should keep its docs-first workflow, but project-specific code standards should move out of generated documentation standards and into a dedicated `rules/` directory in the target repository.

The `rules/` directory is only for code rules. It does not replace requirement docs, technical design docs, analysis docs, or workflow instructions.

For UI-heavy repositories, the best split is usually by responsibility, not by file extension:

- layout and styling
- logic and state
- verification

That split matches how front-end changes actually fail. A CSS/layout bug is usually a geometry or overflow problem, not a CSS-only problem. A JS/state bug usually affects rendering, interaction, or data flow. A test that only rewrites the implementation is usually not a useful test.

## Target Repository Shape

When `ai-doc-driven-dev` initializes or repairs a target repository, the preferred generated structure is:

```text
<repo>/
  AGENTS.md

  rules/
    coding.md
    layout-and-styling.md
    logic-and-state.md
    verification.md
    platform-runtime.md   # required for mini program / runtime-constrained repos
    backend.md            # optional, only when a substantial backend surface exists

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
- `rules/layout-and-styling.md` is created when the repository has meaningful CSS, layout, spacing, visual hierarchy, or responsive-construction rules.
- `rules/logic-and-state.md` is created when the repository has meaningful component logic, composables, state, data flow, or event-handling rules.
- `rules/verification.md` is created when tests or proof obligations need their own rule set.
- `rules/platform-runtime.md` is created when the platform itself constrains layout, runtime behavior, asset handling, scrolling semantics, package layout, or subpackage ownership. It should be treated as required for mini program and uni-app repositories with `subPackages`.
- `rules/backend.md` is created only when the repository has a substantial backend surface that deserves its own rule file.
- `docs/requirements/` and `docs/design/` remain the canonical requirement and technical design locations.
- `docs/analysis/` is created only for investigation, audit, or analysis artifacts.
- `docs/standards/` remains optional and should not be the default location for code rules.

There is no `rules/README.md`. `AGENTS.md` owns rule discovery and indexing.

## UI-Heavy Repository Example

For a front-end-only repository such as a Vue / uni-app mini program, the first generated `rules/` shape should usually be:

```text
rules/
  coding.md
  layout-and-styling.md
  logic-and-state.md
  verification.md
  platform-runtime.md
```

Do not create `frontend.md` merely because the repository is a frontend repository. In that shape, `frontend.md` becomes a bucket that hides the real failure modes.

The preferred mapping is:

- `coding.md`: shared naming, file organization, formatting, dependency rules, and maintainability boundaries.
- `layout-and-styling.md`: CSS/SCSS, rpx/px choices, spacing, visual hierarchy, Figma-to-layout translation, overflow, wrapping, and component shell constraints.
- `logic-and-state.md`: Vue script logic, composables, stores, API calls, route payloads, event guards, loading/error/empty states, and interaction state.
- `verification.md`: how tests and manual checks prove layout, state, interaction, and runtime contracts.
- `platform-runtime.md`: mini program, uni-app, subpackages, package-size pressure, safe-area, scroll-view, native container, asset sync, and build-mode constraints.

## File Responsibilities

### `AGENTS.md`

`AGENTS.md` is the main Codex-facing entry point. It should stay short and point to the right source of truth.

It should include:

- The docs-first workflow entry.
- The requirement/design routing gate.
- A statement that code rules live in `rules/*.md`.
- A short rule index that tells Codex which rule file to read for shared code, layout and styling, logic and state, verification, platform runtime, and optional backend concerns.
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

### `rules/layout-and-styling.md`

`rules/layout-and-styling.md` contains rules for how the UI should be built and constrained.

Typical content:

- Component shell and composition boundaries.
- Flex/grid/flow choices.
- Spacing, sizing, wrapping, and overflow rules.
- Typography, color, radius, and visual hierarchy rules.
- Asset usage and icon treatment.
- Responsive and container-aware layout rules.

This file should express geometry and presentation intent, not mirror CSS line by line.

### `rules/logic-and-state.md`

`rules/logic-and-state.md` contains rules for component behavior and data flow.

Typical content:

- Component logic structure.
- Composables and reusable state helpers.
- Store boundaries and state ownership.
- API calls and async flow rules.
- Event handling and side-effect rules.
- Guard conditions and loading/error/empty state handling.

### `rules/verification.md`

`rules/verification.md` contains rules for proving the code works.

Typical content:

- Unit, integration, visual, and E2E verification boundaries.
- Test naming and scenario naming.
- Fixture, mock, and runtime stub conventions.
- Required verification commands.
- Geometry, overflow, overlap, visibility, and state-coverage assertions.
- Rules for adding tests or proofs with feature changes or bug fixes.

This file should describe observable contracts, not reproduce implementation details. If a test is mostly a copy of the code it claims to verify, the verification rule is wrong.

#### Verification Model

Verification rules should turn requirements into observable contracts:

```text
source of truth -> observable contract -> implementation -> proof
```

For layout and styling, good contracts include:

- distance from A to B
- container inset and sibling gap
- rendered width, height, or minimum touch area
- no overlap, clipping, accidental horizontal scroll, or broken wrapping
- visible state after a user action or data-state change
- scroll viewport height and bottom safe-area behavior

For logic and state, good contracts include:

- state transition from input/event A to visible result B
- API payload, route payload, or emitted event shape
- loading, empty, error, permission, and logged-out branches
- idempotency or refresh behavior after navigation return

Source-text assertions are allowed only when the source text itself is the contract, such as banning a deprecated import, requiring a specific asset path, or preventing a known forbidden API. Source-text assertions should not be the default way to prove CSS layout.

### `rules/platform-runtime.md`

`rules/platform-runtime.md` exists when the platform itself imposes real constraints that are neither generic code rules nor pure layout rules.

For mini program and uni-app repositories with `subPackages`, this file is expected, not optional. Subpackage ownership, asset placement, package-size pressure, and build-time asset synchronization are runtime constraints.

Typical content:

- `pages.json` as the page and subpackage ownership source of truth.
- Main package vs subpackage page boundaries.
- Subpackage asset placement and synchronization rules.
- Package-size pressure and asset-replacement rules.
- Mini program safe-area and scroll semantics.
- Native container interactions.
- Asset syncing and runtime packaging rules.
- Platform-specific build modes or environment contracts.

### `rules/backend.md`

`rules/backend.md` is optional and should exist only when the repository contains a substantial backend surface.

Typical content:

- API handler and service boundaries.
- Data access patterns.
- Validation and error response conventions.
- Transaction and idempotency rules.
- Background job or queue conventions.
- Backend observability rules.

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

- Existing "pattern extraction" becomes responsibility-based code rules extraction and sync.
- Extracted project-specific code conventions are written to target-repository `rules/*.md` buckets such as shared code, layout and styling, logic and state, verification, platform runtime, and any clearly justified optional backend rules.
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
3. Separate shared rules from layout/styling, logic/state, verification, runtime/platform, and any optional backend rules that the repository actually needs.
4. Use the repository's change shape to decide the split. A UI-heavy repository should not be forced into a frontend/backend bucket if layout, state, and verification are the real failure modes.
5. Create only the rule files justified by repository evidence.
6. Preserve existing project-specific rules unless they conflict with stronger code evidence or user direction.
7. Keep docs-first workflow content in `AGENTS.md` and docs, not in `rules/`.
8. Report which rule files were created, updated, skipped, or intentionally left unchanged.

If multiple code areas exist in a monorepo, the first version should still prefer the top-level `rules/` directory unless the repository already has a stronger local convention.

For mini program repositories, inspect `pages.json`, `manifest.json`, package roots such as `pagesA` / `pagesB`, asset-sync scripts, and npm scripts before deciding rule files. If development, test, or build scripts run a subpackage asset sync step, record that as a platform-runtime rule.

## Error Handling

If the repository already has code rules in another location:

- Reuse the existing location when it is clearly established and `AGENTS.md` already points there.
- Ask before moving established rules into top-level `rules/`.
- Avoid duplicating the same rule in both `docs/standards/` and `rules/`.

If the repository has no clear code conventions:

- Create minimal skeletal rule files only when the user asked to initialize rules.
- Do not invent detailed standards without code evidence.
- Mark missing evidence explicitly in the response instead of filling the gap with generic advice.

If a test file mostly restates the implementation it claims to verify:

- Convert the rule into an observable-contract rule instead of preserving the duplicate structure.
- Prefer geometry, state, rendering, and behavior assertions over implementation cloning.
- Keep CSS-related verification focused on measurable layout and visual outcomes.

If `AGENTS.md`, `CLAUDE.md`, or other instruction files conflict:

- Treat `AGENTS.md` as the Codex primary entry point.
- Align other instruction files only when they are in scope or the user asks for cross-tool compatibility.

## Testing And Verification

For the skill implementation, verification should include:

- Updating a repo with only shared code rules creates `AGENTS.md` and `rules/coding.md`.
- Updating a UI-heavy repo creates or updates `rules/coding.md`, `rules/layout-and-styling.md`, `rules/logic-and-state.md`, and `rules/verification.md`.
- Updating a repo with a substantial backend surface may also create or update `rules/backend.md`.
- Updating a runtime-constrained repo creates or updates `rules/platform-runtime.md`.
- Updating a mini program repo with `subPackages` records page ownership, subpackage asset sync, and package-size constraints in `rules/platform-runtime.md`.
- Existing requirement/design docs remain under `docs/requirements/` and `docs/design/`.
- Existing non-code standards under `docs/standards/` are preserved.
- Code rules are not written into `docs/standards/` by default.
- `AGENTS.md` indexes `rules/*.md` without duplicating their full content.
- Verification rules describe proof obligations, not implementation source code.

## Open Scope

This design does not require cross-tool compatibility in the first implementation. `CLAUDE.md`, `GEMINI.md`, and Copilot-specific instruction files can be handled later as thin compatibility entries that point to `AGENTS.md` and `rules/`.

This design does not require a `rules/README.md`.
