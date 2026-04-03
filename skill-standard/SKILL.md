---
name: skill-standard
description: The authoritative quality standard for writing SKILL.md files. Use this to evaluate, audit, or improve any skill's content.
---

# Skill Standard

The authoritative reference for what makes a skill well-written. Use this when writing a new skill, auditing an existing one, or improving SKILL.md content quality.

---

## Skill Writing Standard

**Every SKILL.md MUST follow these principles:**

### 1. Semantically Clear, No Ambiguity

Every word in a SKILL.md must have a single clear meaning. Avoid vague terms that could be interpreted multiple ways.

- ✅ "Search for major AI model releases (new versions from OpenAI, Anthropic, Google, Meta)"
- ❌ "Update model" (update which model? update how? update the AI model itself, or update info about models?)

### 2. Goal-Oriented, Not Step-by-Step

Tell the AI **what** to achieve, not **how** to execute. The AI can figure out commands, file discovery, and execution order on its own.

- ✅ "Complete the daily check-in and fetch sign record to verify"
- ❌ "Run `python3 -m checkin.xiaojuchongdian.src.main run --task xiaoju.checkin --verify-record`"

### 3. Declare Available Tools, Don't Dictate Usage

If the skill has programmatic assets (scripts, CLI tools, APIs), describe **what they do** and **where they are** relative to the skill. Let the AI read the code and decide how to use them.

- ✅ "Entry point: `main.py`. Read the file to understand usage."
- ❌ "Run `python3 -m checkin.xiaojuchongdian.src.main status --task xiaoju.checkin`"

### 4. Portable Paths Only

Never hardcode absolute or repo-root-relative paths. Use paths relative to the skill itself.

- ✅ "Located in the `scripts/` directory of this skill"
- ❌ "Location: `checkin/xiaojuchongdian/skill/get-params/scripts/`"

### 5. Know What AI Can and Cannot Do

**AI can figure out on its own** (don't over-specify):
- How to run a Python/Shell/Node script after reading it
- Which subcommands or flags a CLI supports
- How to parse JSON output
- How to find files in a directory
- Error handling and retry logic

**AI needs to be told** (must specify):
- The goal and success criteria
- What programmatic assets exist and their purpose
- Key constraints (auth requirements, idempotency, user interaction needed)
- Dependencies on other skills (by skill name, not path)

### 6. Reference by Skill Name, Not Path

Skills depend on each other by **name**. OpenClaw resolves names to locations.

- ✅ "Use the `xiaoju-get-params` skill to refresh credentials"
- ❌ "Switch to `checkin/xiaojuchongdian/skill/get-params/SKILL.md`"

### 7. Declare Dependencies in skill.json

External or sub-skill dependencies must be declared in `skill.json` under `sub_skills` (by skill name), so OpenClaw can auto-install them.

### 8. Declare Explicit Completion Signals

For any task, define an explicit completion signal tied to a verifiable standard — not to the model's own sense of sufficiency. **"Looks done" is not done. Completion means the defined criteria are met and verified.**

**Warning Signs** — if you think any of these, pause and take the correct action:

| Thought | Reality | Correct Action |
|---|---|---|
| "I've read enough to understand" | Read = read every item in scope. Partial reads are not reads. | Enumerate all items, then read each one. |
| "I've seen most of the nodes/files" | Most ≠ all. | List all items first, then process them in order. |
| "This looks like a standard structure" | Assumptions replace reading. | Read the actual content before drawing conclusions. |
| "The fix is small, checking is overkill" | Small fixes break adjacent behavior. | Verify the full scope before and after the fix. |
| "I've covered the main cases" | Main cases ≠ all cases. | Explicitly check for edge items before closing. |
| "I've completed the task" | Completion ≠ verified to the highest standard. Reading all nodes does not mean spacing, hierarchy, and every property has been validated. | Validate every property against the full spec before declaring done. |

**How to write completion signals in a skill:**
- ✅ "Read all child nodes before generating output. Do not assume the structure from partial traversal."
- ✅ "Verify every item in the list is processed. Log skipped items explicitly."
- ❌ (no completion signal stated — model decides when it's done)
