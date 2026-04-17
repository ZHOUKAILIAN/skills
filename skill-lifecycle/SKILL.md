---
name: skill-lifecycle
description: "Full lifecycle management for skills: create new skills, fix and improve existing ones, and submit changes via PR."
---

# Skill Lifecycle

Use this skill to manage the full lifecycle of a skill: create, fix, improve, and ship via PR. For writing standards and quality criteria, refer to the `self-optimize` skill.

---

## Scenario A: Creating New Skills

### Patterns

1. **Pure Custom** — no existing skill, build from scratch (e.g., `frontier-changelog`)
2. **Reuse External** — use an existing OpenClaw skill as-is
3. **Extend External** — wrap an existing skill with customization

### Workflow

1. **Understand intent first**: Ask 2-3 clarifying questions, then restate the user's idea back to them in your own words. Get explicit confirmation before proceeding.
2. Scaffold the skill directory with `SKILL.md` + `skill.json`
3. Write the SKILL.md following the **Skill Writing Standard** in `self-optimize`
4. Implement code if needed (in a `src/` or `scripts/` directory within the skill)
5. Register in `daily/skill/SKILL.md` if it's a scheduled task
6. Test and create PR

---

## Scenario B: Fixing / Improving Existing Skills

### Workflow

1. Identify which skill is affected (by skill name or user description)
2. **Restate the problem back to the user** and confirm understanding before making changes
3. Read the skill's SKILL.md and implementation code to understand current behavior
4. Diagnose the issue
5. Fix code and/or update SKILL.md
6. If the SKILL.md violates the **Skill Writing Standard** in `self-optimize`, refactor it as part of the fix
7. Test and create PR

---

## Key Constraints

- **No secrets in code** — API keys/tokens via environment variables only
- **PR required** — all changes go through PR for human review
- **Docs-first for behavior changes** — update `docs/requirements/` or `docs/design/` before changing behavior
- **Simple bug fixes** can skip docs and go straight to code
