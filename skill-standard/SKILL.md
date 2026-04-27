---
name: skill-standard
description: Use when evaluating, auditing, or improving SKILL.md content against the repository's skill authoring standard.
---

# Skill Standard

Route skill writing, auditing, or improvement work to the right standard before judging content.

A good skill reduces repeated model failure modes with the minimum set of clear rules needed to change behavior. This skill is the dispatcher for that review, not the place to expand every type-specific rule.

## Dispatch Rule

If a type-specific standard applies, use it before making final judgments.

Do not rely on memory of the standard. Standards change. Load the relevant sub-skill when its type applies.

| Skill type | Use this standard | When |
| --- | --- | --- |
| Task skill | `task-standard` | The skill executes work and produces a verifiable artifact or task outcome |
| Controller skill | This file for now | The skill governs routing, sequencing, gates, or verification across tasks |

If the target skill is mixed, choose the active mode first. Apply `task-standard` to task modes and the controller section here to controller modes. Do not force one checklist across modes.

## Dispatch Flow

```text
User asks to write/audit/improve a skill
  -> Read SKILL.md and skill.json
  -> Classify primary type
     -> Task skill? Apply task-standard
     -> Controller skill? Apply controller section in this file
     -> Mixed? Select active mode, then apply the matching standard
  -> Apply universal standard
  -> Report findings or make the smallest needed fix
```

## Red Flags

These thoughts mean stop and dispatch:

| Thought | Correct action |
| --- | --- |
| "This is obviously a task skill, I can judge it from the generic checklist." | Load or apply `task-standard`. |
| "The task skill says be careful, that is enough." | Check for task-local gates, verification, and proof package. |
| "This skill has several modes, but one completion signal is fine." | Require active mode and mode-specific completion checks. |
| "The dependency is mentioned in prose, so skill.json is optional." | Declare the dependency in `skill.json.sub_skills`. |
| "I can add detailed task rules to skill-standard." | Put task-specific rules in the task skill or in `task-standard`. |

## Skill Type Gate

Before judging a skill, classify it as one primary type:

| Type | Purpose | Examples |
| --- | --- | --- |
| Task skill | Helps the agent complete a concrete class of work and produce a task artifact | Figma restoration, customer-service troubleshooting, E2E coverage generation, CSS review |
| Controller skill | Changes how the agent chooses, sequences, gates, or verifies work across tasks | Skill lifecycle, docs-first workflow, debugging discipline, skill-use policy |

Reference or constraint skills are usually task skills with a narrow artifact: they provide standards that must be applied while doing work. If a skill mostly tells the agent how to govern its own process, audit it as a controller skill.

If a skill mixes both types, require an explicit active mode before applying type-specific completion checks. Do not force one completion rule across materially different modes.

## Universal Standard

Every `SKILL.md` must satisfy these rules regardless of type.

### 1. Discovery Metadata Is Trigger-Only

The frontmatter `description` and `skill.json.description` must describe when to use the skill, not summarize the whole workflow.

Good: "Use when investigating a customer service issue that requires logs, code, data, and root-cause explanation."
Bad: "Use to ask questions, query logs, read code, query database, write Feishu report, then ask whether to fix."

Why: workflow summaries in metadata tempt the agent to act from metadata instead of reading the full skill.

### 2. Semantically Clear, No Ambiguity

Every important term must have one clear meaning. Avoid vague verbs when a wrong interpretation would change behavior.

Good: "Search for major AI model releases from OpenAI, Anthropic, Google, and Meta."
Bad: "Update model."

### 3. One Skill, One Behavior Boundary

A skill should own one coherent behavior boundary. Split when two parts have different triggers, different safety rules, or different completion signals.

Good: one read-only Figma review skill and one implementation/restoration skill.
Bad: one Figma skill that sometimes reviews, sometimes edits, sometimes creates tests, with one vague completion rule.

### 4. Declare Assets And Tools By Purpose

If the skill has scripts, templates, references, examples, CLIs, APIs, or generated artifacts, name what each asset does and when to use it.

Good: "`scripts/verify_figma_audit.py` checks the audit README and node ledger contract."
Bad: "Scripts are available."

Do not turn asset declarations into brittle command recipes unless the exact command is the stable interface.

### 5. Portable Paths And Dependencies

Use skill-local paths such as `scripts/`, `assets/templates/`, and `references/`. Do not hardcode absolute paths or one user's workspace layout.

Reference other skills by skill name. If a skill requires another skill, declare it in `skill.json` under `sub_skills`.

Good: "Use `css-best-practices` before writing CSS."
Bad: "Open the CSS skill from a user-specific absolute path."

### 6. State What The Agent Must Not Guess

Tell the agent the facts it must establish before acting: source of truth, required inputs, target environment, code location, write permission, ownership boundary, or user approval.

Do not over-specify things the agent can safely discover after reading the repo or helper script: basic CLI flags, JSON parsing, file search, or ordinary retry mechanics.

### 7. Define Stop-And-Ask Boundaries

If a silent assumption would change scope, behavior, target files, data writes, credentials, user-visible output, or ownership, the skill must tell the agent to stop and ask.

Good: "If multiple ownership candidates exist, present them and ask which one should own the change."
Bad: "Pick the most likely owner and continue" when the owner determines which canonical doc is edited.

### 8. Declare Explicit Completion Signals

Completion must be tied to verifiable criteria, not the model's sense that it is done.

Good: "Every in-scope visible node has terminal-depth coverage and every spacing value has named geometry proof."
Bad: "The UI looks close."

For multi-mode skills, completion signals must be scoped to the active mode.

### 9. No Speculative Complexity

Each rule should close a real failure mode, protect a safety boundary, or define a required success condition. If a section would not change what the agent does on a real task, cut it.

### 10. Prefer Short Wrong/Right Contrasts

Use short contrasts for non-obvious rules. They are more useful than long tutorial prose.

Good: "Wrong: create standalone bugfix docs. Right: update the owning requirement/design pair."
Bad: multiple paragraphs explaining the philosophy without changing the next action.

## Task Skill Standard

Use `task-standard` for detailed rules when writing, auditing, or improving a task skill.

A task skill executes a concrete class of work and produces a verifiable task artifact. This file only defines the routing and quality gate; `task-standard` owns the detailed task-skill standard.

When a target skill is a task skill, use `task-standard` before editing or closing the audit.

At this level, the audit only needs to confirm that the task skill has:

- A concrete artifact or outcome.
- Objective success criteria.
- A named source of truth.
- Task-local anti-laziness gates near the workflow they control.
- Verification and failed-verification behavior.
- A proof package requirement for the final output.

If any of those are missing, invoke or apply `task-standard` and fix the task skill there instead of expanding this general standard.

## Controller Skill Standard

Use this section for skills that govern how the agent sequences, routes, delegates, or verifies work.

### Required Shape

A controller skill should usually contain:

- `Core Rule`: the behavior change that must happen.
- `Priority`: how it interacts with user instructions, project rules, and other skills.
- `Active Mode`: which branch of the process is currently in force.
- `Gates`: checks that must happen before the next phase.
- `Red Flags`: thoughts or shortcuts that indicate the agent is about to violate the process.
- `Handoff Rules`: which skill, phase, or user decision comes next.
- `Completion Signal`: proof that the process was followed.

### Control The Decision, Not The Artifact

Controller skills should focus on sequencing and guardrails. They should not duplicate the detailed task instructions of the skills they route to.

Good: "Choose improve mode, read current skill artifacts, fix the smallest verified failure, then apply `skill-standard`."
Bad: repeat the full contents of `skill-standard` inside `skill-lifecycle`.

### Active Mode Is Mandatory For Multi-Entry Skills

If the skill has multiple workflows, select one active mode before acting. Completion checks apply only to that mode.

Good: create mode, improve mode, sync mode, shipping mode.
Bad: apply all mode checks to every invocation.

### Red Flags Should Target Agent Rationalizations

Controller skills should name the specific shortcut they prevent.

Good: "This is just a quick fix" -> still route the doc owner first.
Good: "The first few nodes show the pattern" -> keep reading every in-scope node.
Bad: generic advice such as "be careful" or "think deeply."

### Handoffs Must Be Explicit

If the controller depends on another skill or phase, name when the handoff happens and what the next skill owns.

Good: "`skill-lifecycle` owns create/improve/sync/ship flow; `skill-standard` owns the quality gate."
Bad: "Use other relevant standards as needed."

## Audit Checklist

An audit or improvement pass using this standard is complete only when all applicable checks are done:

- The skill type is classified as task or controller. Mixed skills have an explicit active mode.
- The relevant type-specific standard was applied: `task-standard` for task skills; controller section here for controller skills.
- `SKILL.md` frontmatter and `skill.json` names/descriptions are checked for consistency.
- Descriptions are trigger-only and do not summarize workflow.
- Skill dependencies are checked against `skill.json.sub_skills`.
- Bundled assets, scripts, templates, references, or helper files are documented by purpose.
- Paths are portable and skill-local unless the skill is explicitly environment-specific.
- Stop-and-ask boundaries exist where silent assumptions would change scope, behavior, writes, ownership, or file targets.
- Completion signals exist and fit the skill type and active mode.
- Task skills were checked against `task-standard` and have required inputs, objective success criteria, source of truth, local anti-laziness gates, workflow, progressive references, mode/fallback rules, guardrails, output format, artifact verification, verification-failure handling, and a proof package.
- Controller skills have core rule, priority or interaction model, active mode when needed, gates, red flags, handoff rules, and process verification.
- Each major rule traces to a real failure mode, safety boundary, or success condition.
- Findings include concrete file references, or the audit explicitly states that no findings were found in scope.

Do not end an audit after a few style observations. End it after metadata, dependency surface, assets, portability, ambiguity boundaries, type-specific structure, completion logic, and reported findings have all been checked for the requested scope.
