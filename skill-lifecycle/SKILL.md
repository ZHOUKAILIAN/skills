---
name: skill-lifecycle
description: Use when creating, improving, installing, syncing, or shipping a skill and you need one workflow that covers SKILL.md, skill.json, bundled assets, and release handoff.
---

# Skill Lifecycle

Manage a skill from first draft through repair, installation sync, and shipping. Use `skill-standard` as the quality gate for every content change.

## Active Mode

Choose one active mode before editing:

1. Create a new skill
2. Improve or repair an existing skill
3. Reuse or adapt an external skill
4. Sync an installed skill copy with a repository version
5. Ship an already-updated skill through branch, commit, push, or PR work

If the request could mean more than one mode, name the ambiguity and ask before changing files.

## Core Rules

- Keep the write scope on skill artifacts: `SKILL.md`, `skill.json`, skill-local assets, scripts, templates, and installation copies when requested.
- Do not assume repo-specific registry files, product-doc locations, or marketplace manifests exist. Detect them first and update them only if the current repo actually uses them.
- Do not assume every skill change needs product requirements or technical design docs. Only update broader project workflow docs when the user explicitly wants the skill process changed there and the repo contains those docs.
- Keep new rules minimal. A lifecycle fix should close a real failure mode, not add speculative process.
- If the skill references another skill as a dependency, declare it in `skill.json` under `sub_skills`.

## Create Mode

When creating a new skill:

1. Confirm the user goal, target behavior change, and whether one skill is enough or a split is justified.
2. Create the skill directory with `SKILL.md` and `skill.json`.
3. Write trigger-only metadata first so discovery works before deeper content exists.
4. Add only the assets or helper code the skill actually needs, and explain each asset's purpose in `SKILL.md`.
5. Apply `skill-standard` before considering the new skill complete.

## Improve Mode

When repairing or improving an existing skill:

1. Read the current `SKILL.md`, `skill.json`, and any bundled assets or helper code that shape behavior.
2. Verify the reported problem against the current files before editing.
3. Fix the smallest set of content or asset changes that closes the verified failure mode.
4. If the skill violates `skill-standard`, bring the affected sections up to standard as part of the fix.

Wrong: rewrite the whole skill because one section is weak.
Right: fix the broken routing, metadata, asset declaration, or completion logic and keep the rest stable.

## External Reuse Mode

When reusing an external skill:

1. Read the upstream skill completely before adapting it.
2. Keep only the parts that fit the local runtime, toolchain, and workflow.
3. Remove or rewrite environment-specific paths, commands, and assumptions.
4. Re-check discovery metadata, dependencies, asset declarations, and completion signals after adaptation.

## Sync Mode

Use sync mode when the repository version and the installed copy have drifted.

- Compare the repository skill directory with the installed skill directory before copying anything.
- Sync only the requested skills or the skills touched by the current fix.
- If installation would overwrite a locally customized copy, stop and surface that conflict instead of silently replacing it.
- After syncing, verify that the installed files match the repository files you intended to deploy.

## Shipping Mode

Use shipping mode after the content changes are complete.

- Verify the diff before staging.
- Commit only the intended skill changes.
- Push or open a PR when the user asks for release handoff.
- If the user asked only for local fixes, stop after verified local completion.

## Completion Signals

The lifecycle task is complete only when all applicable checks for the active mode are satisfied:

- The active mode is explicit, or any unresolved mode ambiguity has been surfaced to the user.
- Every changed skill has both `SKILL.md` and `skill.json`, and their names and descriptions match where required.
- Descriptions remain trigger-only; they describe when to use the skill, not its workflow.
- Declared dependencies are present in `skill.json`, and undeclared skill dependencies are not introduced.
- Bundled assets or helper files are either documented with purpose or removed from the scope of the change.
- New or edited rules are portable and do not hardcode environment-specific paths, branches, commands, or unrelated project-doc conventions unless the skill is explicitly environment-specific.
- The changed skill has a verifiable completion signal that fits its actual modes or task type.
- Verification has run for the edited artifacts: diff hygiene, JSON validity, and any targeted checks needed for the reported failure mode.
- If sync mode was requested, the installed copy matches the intended repository version after the sync.
- If shipping mode was requested, the final git state is reported accurately: local only, committed, pushed, or PR opened.

Do not stop after scaffolding files, after editing only `SKILL.md`, or after committing without verification. Stop when the skill content, metadata, dependency surface, verification result, and requested handoff all line up.
