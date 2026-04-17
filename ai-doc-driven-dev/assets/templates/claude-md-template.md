# Project Documentation Workflow

This project follows a documentation-driven development workflow.

## Development Workflow

All code changes follow this sequence:

1. Route the work item to documentation.
2. Update existing requirement/design docs when the work belongs to an existing feature.
3. Create new requirement/design docs only when the work is a new feature boundary.
4. Get user approval for documentation changes.
5. Implement code based on approved documentation.
6. Verify code and documentation remain synchronized.

## Document Routing Gate

Before creating any new document, check whether the work belongs to existing docs:

- Requirement docs: `docs/requirements/`
- Technical designs: `docs/design/`
- Standards: `docs/standards/`
- Analysis and investigations: `docs/analysis/`

Bugs, regressions, optimizations, and follow-up changes usually update the original requirement/design pair. Do not create standalone bug documents by default.

Create a new requirement/design pair only when:

- The work introduces a new user goal or feature boundary.
- No existing requirement/design pair owns the behavior.
- The user explicitly asks for a separate incident or investigation record.

## Document Naming Convention

- Requirement: `docs/requirements/YYYYMMDD-feature-name.md`
- Technical design: `docs/design/YYYYMMDD-feature-name-technical-design.md`
- Same-day filename conflicts: append `-v2`, `-v3`

Same-day suffixes resolve filename conflicts only. They are not a substitute for updating an existing feature document.

## Documentation Structure

```text
docs/
├── requirements/     # Canonical feature requirements and user journeys
├── design/           # Paired technical designs
├── standards/        # Coding, testing, architecture, and workflow standards
└── analysis/         # Project analysis and investigation notes
```

## Visual Documentation

- Use Mermaid diagrams for architecture, data flow, state transitions, and sequence flows.
- Use Markdown tables for data structures, APIs, configurations, requirements, and acceptance criteria.
- Update diagrams and tables inline when behavior changes.

## Reference Documents

- Requirements: `docs/requirements/`
- Technical designs: `docs/design/`
- Project standards: `docs/standards/`
- Project analysis: `docs/analysis/`
