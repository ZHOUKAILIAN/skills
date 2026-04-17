# AI Agent Workflow Rules

## Mandatory Process

Follow this workflow for all code changes:

1. Understand the requested change.
2. Route the work item to the correct documentation owner.
3. Update or create requirement/design docs according to the route.
4. Wait for user approval of documentation changes.
5. Implement code.
6. Verify implementation against approved docs.
7. Update docs again if implementation differs from the approved design.

## Document Routing Rules

Before creating a new requirement or design document:

1. Search existing docs for the owning feature or user journey.
2. Match by feature name, user journey, route, API, module, entity, issue ID, and expected behavior.
3. If an existing requirement/design pair owns the work, update that pair.
4. If only one side of the pair exists, update it and create the missing paired document.
5. If no existing docs own the work, create a new pair.

Bug fixes, regressions, optimizations, and follow-up changes must not create standalone bug documents by default. They update the original requirement/design pair unless the user explicitly requests a separate incident record.

## Documentation Standards

### Naming

- Requirement: `docs/requirements/YYYYMMDD-feature-name.md`
- Technical design: `docs/design/YYYYMMDD-feature-name-technical-design.md`
- Same-day conflicts: append `-v2`, `-v3`

### Pairing

- Every requirement should have one paired technical design.
- Every technical design should point back to its requirement.
- Bug-fix updates must keep both sides synchronized.

### Content

- Requirements describe user-visible behavior, scope, edge cases, and acceptance criteria.
- Technical designs describe architecture, data flow, API/state changes, risks, and verification.
- Follow-up changes revise normative sections instead of adding disconnected notes.

## Prohibited Actions

- Writing code before documentation routing.
- Creating new docs before checking existing ownership.
- Creating standalone bug docs by default.
- Leaving requirements and technical designs inconsistent.
- Deleting or overwriting user documentation without approval.
- Using placeholder-only documents as if they were approved specs.

## Verification

Before claiming a task is ready for implementation:

- The route decision is explicit.
- Updated or created docs are named in the response.
- Requirement and design docs are paired.
- No unresolved placeholders remain unless the user asked for a scaffold.
