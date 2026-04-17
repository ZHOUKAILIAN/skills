# Legacy Plugin Mapping

This file records how the old `claude-community-plugins/plugins/ai-doc-driven-dev` plugin was migrated into this skills repository.

The first migration pass split the workflow into multiple skills. That was later collapsed into one public skill because the behavior is most useful as a single entry point.

## Migrated Components

| Legacy plugin component | Current location | Notes |
| --- | --- | --- |
| `.claude-plugin/plugin.json` | `ai-doc-driven-dev/skill.json` | Converted from Claude plugin metadata to skill metadata. |
| `skills/doc-detector/SKILL.md` | `ai-doc-driven-dev/SKILL.md` | Folded into the main skill as the documentation analysis and routing phase. |
| `skills/doc-generator/SKILL.md` | `ai-doc-driven-dev/SKILL.md` | Folded into the main skill as the requirement/design update and generation phase. |
| `skills/doc-workflow-enforcer/SKILL.md` | `ai-doc-driven-dev/SKILL.md` | Folded into the main skill as the workflow enforcement phase. |
| `skills/pattern-extractor/SKILL.md` | `ai-doc-driven-dev/SKILL.md` | Folded into the main skill as the pattern extraction phase. |
| `knowledge/templates/YYYYMMDD-feature-name.md` | `ai-doc-driven-dev/assets/templates/requirements-template.md` | Reworked into a reusable requirement template with change-history and correction sections. |
| `knowledge/templates/YYYYMMDD-feature-name-technical-design.md` | `ai-doc-driven-dev/assets/templates/technical-design-template.md` | Reworked into a reusable design template with route decision and bug/follow-up impact sections. |
| `knowledge/templates/claude-md-template.md` | `ai-doc-driven-dev/assets/templates/claude-md-template.md` | Updated to require document routing before creating new docs. |
| `knowledge/templates/agents-md-template.md` | `ai-doc-driven-dev/assets/templates/agents-md-template.md` | Updated to prohibit default standalone bug docs. |
| `knowledge/patterns/*.json` | `ai-doc-driven-dev/assets/patterns/*.json` | Preserved as pattern hints, not target-project standards. |

## Folded Workflows

| Legacy command or agent | Current replacement |
| --- | --- |
| `commands/init-doc-driven-dev.md` | `ai-doc-driven-dev` workflow: Initialize Docs-First Development |
| `commands/update-doc-driven-dev.md` | `ai-doc-driven-dev` workflow: Update an Existing Docs-First Setup |
| `commands/update-standards.md` | `ai-doc-driven-dev` workflow: documentation analysis plus approved updates |
| `agents/doc-flow-initializer.md` | `ai-doc-driven-dev` initialization workflow |
| `agents/doc-flow-updater.md` | `ai-doc-driven-dev` update workflow |
| `agents/doc-workflow-transformer.md` | `ai-doc-driven-dev` single-entry coordinator skill |
| `agents/codebase-style-analyzer.md` | `ai-doc-driven-dev` pattern extraction phase |
| `agents/project-standards-analyzer.md` | `ai-doc-driven-dev` pattern extraction phase |

## Intentional Changes

- The current repository stores reusable skills, not Claude plugin commands, so command shortcut metadata was not copied.
- The old workflow allowed agents to treat bug fixes as new documentation work. The migrated workflow adds a hard routing gate: bug fixes, regressions, optimizations, and follow-up changes update the original requirement/design pair when one exists.
- Templates now include explicit places for change history, corrections, route decisions, and bug/follow-up impact so existing feature docs can evolve without fragmentation.
- The public surface is intentionally one skill. Internal phases remain inside `ai-doc-driven-dev/SKILL.md` instead of being exposed as separate standalone skills.
