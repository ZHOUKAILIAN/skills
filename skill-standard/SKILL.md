---
name: skill-standard
description: Use before and after creating, editing, auditing, reviewing, syncing, or shipping any skill artifact, including SKILL.md, skill.json, assets, scripts, templates, examples, and installed skill copies.
---

# Skill Standard

Use this as the quality gate for every skill change. A good skill reduces repeated model failure modes with the minimum clear rules needed to change behavior. It should not become a speculative process document.

This standard is self-contained; task-skill requirements live in this file.

## Trigger Rule

Use this skill before the first edit to any skill artifact and again before considering the work complete.

Skill artifacts include:

- `SKILL.md`
- `skill.json`
- skill-local `assets/`, `scripts/`, `templates/`, `examples/`, `references/`, or `evals/`
- generated review copies or rationale docs that explain a skill
- installed skill copies under local agent or Codex skill directories
- repository index or lifecycle docs when the change alters skill behavior or routing

Wrong: edit a skill first, then check whether it satisfies the standard.

Right: read the current skill artifacts, classify the skill type, apply the standard while editing, then run the audit checklist before reporting completion.

## Skill Type Gate

Before judging or editing a skill, classify the target as one primary type:

| Type | Purpose | Examples |
| --- | --- | --- |
| Task skill | Helps the agent complete a concrete class of work and produce a verifiable artifact or task outcome | Figma restoration, customer-service troubleshooting, E2E coverage generation, backend verification |
| Controller skill | Governs how the agent chooses, sequences, delegates, gates, or verifies work across tasks | Skill lifecycle, docs-first workflow, debugging discipline, skill-use policy |

Reference or constraint skills are task skills when they define artifact quality or task-local checks. They are controller skills when they mostly govern process, routing, or verification across other skills.

If a skill mixes both types, choose an explicit active mode before applying type-specific completion checks. Do not force one completion rule across materially different modes.

## Universal Standard

Every skill must satisfy these rules regardless of type.

### 1. Discovery Metadata Is Trigger-Only

The frontmatter `description` and `skill.json.description` must describe when to use the skill, not summarize the workflow.

Good: "Use when investigating a customer service issue that requires logs, code, data, and root-cause explanation."

Bad: "Use to ask questions, query logs, read code, query database, write Feishu report, then ask whether to fix."

Why: workflow summaries in metadata tempt the agent to act from metadata instead of reading the full skill.

### 2. Semantically Clear, No Ambiguity

Every important term must have one clear meaning. Avoid vague verbs when a wrong interpretation would change behavior.

Good: "Search for major AI model releases from OpenAI, Anthropic, Google, and Meta."

Bad: "Update model."

### 3. One Skill, One Behavior Boundary

A skill should own one coherent behavior boundary. Split when two parts have different triggers, safety rules, source-of-truth requirements, or completion signals.

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

Tell the agent which facts it must establish before acting: source of truth, required inputs, target environment, code location, write permission, ownership boundary, credentials, or user approval.

Do not over-specify facts the agent can safely discover after reading the repo or helper script, such as basic CLI flags, JSON parsing, file search, or ordinary retry mechanics.

### 7. Define Stop-And-Ask Boundaries

If a silent assumption would change scope, behavior, target files, data writes, credentials, user-visible output, ownership, or safety, the skill must tell the agent to surface the ambiguity instead of guessing.

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

Use this section for skills that execute concrete work and produce a verifiable task artifact or outcome.

### Required Shape

A task skill should usually contain:

- `Goal`: the artifact or outcome the task must produce.
- `When To Use` and `When Not To Use`: routing boundaries.
- `Required Inputs`: information needed before safe execution.
- `Source Of Truth`: authoritative facts, docs, data, design, logs, or code.
- `Mode And Fallback Rules`: preferred path, allowed fallbacks, and stop conditions.
- `Workflow`: ordered phases or a decision tree.
- `Local Anti-Laziness Gates`: task-specific checks that block known shortcuts.
- `Available Assets`: scripts, templates, references, APIs, CLIs, or helpers, when present.
- `Guardrails`: read/write boundaries, credentials, environment, approval, and safety limits.
- `Success Criteria` or `Completion Standard`: objective conditions that prove the artifact is acceptable.
- `Verification`: how those criteria are checked.
- `Proof Package`: what evidence the final answer must report.

Only include sections that matter for the task. If a skill has no assets, it does not need an `Available Assets` section.

### Source Of Truth

Every task skill must name the authority for facts and acceptance.

Examples:

- official docs for API guidance
- Figma node data for exact design restoration
- user-provided Feishu records for change scope
- runtime logs, code, and database records for incident investigation
- rendered artifact output for documents, slides, sheets, images, and web pages

Screenshots, summaries, memory, and model guesses can support the task only when the skill says they are acceptable sources.

### Local Anti-Laziness Gates

Anti-laziness rules must live inside the task skill near the workflow they gate. The task skill must name the exact shortcut and the exact check.

For each task skill, ask:

1. What shortcut would let the agent falsely claim completion?
2. What observable artifact proves the shortcut did not happen?
3. What mechanical or manual check can inspect that artifact?
4. What must happen if the check fails?

Good: "Every Feishu record must be mapped to a journey or marked no-E2E-applicable with reason before tests are generated."

Bad: "Cover the important records."

### Scope Accounting

Use scope accounting when the task processes multiple nodes, pages, records, slides, rows, files, routes, screenshots, tests, cases, or user journeys.

The task skill should require an item ledger or equivalent accounting with:

- stable item identity
- group or parent when hierarchy matters
- expected count or source count when available
- status for each item: processed, verified, excluded, blocked, or not applicable
- reason for every excluded, blocked, skipped, or not-applicable item
- completion proof for every processed item

Default stance: zero unaccounted in-scope items. If partial coverage is acceptable, the skill must define the allowed gap explicitly.

### Gate Artifacts

Use gate artifacts when a later phase depends on evidence from an earlier phase.

Good gate artifacts include:

- node ledger before design implementation
- rendered page or slide screenshots before visual delivery
- spreadsheet recalculation output before workbook delivery
- DOM snapshot before browser actions
- log/code/database evidence table before root-cause reporting
- test discovery summary before generating new tests

Gate artifacts are not decorative. A later phase must use them to decide whether to continue.

### Mechanical Verification

Use mechanical checks whenever the task has a checkable artifact:

- scripts or validators
- renderers
- linters or type checks
- formula recalculators
- screenshots or visual diffs
- DOM snapshots
- log queries
- SQL or API count checks
- file existence and content checks

If a mechanical check is not possible, the task skill must define the manual inspection evidence required instead.

### Failed-Gate Behavior

Every task skill must say what happens when verification fails.

Allowed outcomes:

- fix the specific failed criterion and re-run the check
- stop and report `not ready`, including the failed criterion and evidence

Not allowed:

- mention the failure and still claim completion
- continue into the next phase when the failed gate was meant to block that phase
- convert a failed check into vague residual risk without explaining why the task can still be considered complete

### Proof Package

The final answer for a task skill must report evidence, not confidence.

The proof package should include:

- artifact produced or changed
- source-of-truth inputs inspected
- scope counts when the task is multi-item
- verification checks run and their pass/fail status
- skipped or impossible checks with reason
- failed gates and whether they were fixed, re-run, or left as blockers
- residual risk only when it affects confidence in completion

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

Good: "`skill-lifecycle` owns create/improve/sync/ship flow; `skill-standard` owns the quality gate."

Bad: repeat the full contents of `skill-standard` inside `skill-lifecycle`.

### Active Mode Is Mandatory For Multi-Entry Skills

If the skill has multiple workflows, select one active mode before acting. Completion checks apply only to that mode.

Good: create mode, improve mode, sync mode, shipping mode.

Bad: apply all mode checks to every invocation.

### Red Flags Should Target Agent Rationalizations

Controller skills should name the specific shortcut they prevent.

Good: "This is just a quick fix" -> still route the doc owner first.

Bad: generic advice such as "be careful" or "think deeply."

### Handoffs Must Be Explicit

If the controller depends on another skill or phase, name when the handoff happens and what the next skill owns.

Good: "`skill-lifecycle` owns create/improve/sync/ship flow; `skill-standard` owns the quality gate."

Bad: "Use other relevant standards as needed."

## Audit Checklist

An audit or improvement pass using this standard is complete only when all applicable checks are done:

- The skill type is classified as task, controller, or mixed. Mixed skills have an explicit active mode.
- `SKILL.md` frontmatter and `skill.json` names/descriptions are checked for consistency.
- Descriptions are trigger-only and do not summarize workflow.
- Skill dependencies are checked against `skill.json.sub_skills`; undeclared required dependencies are fixed or the dependency is removed.
- Bundled assets, scripts, templates, references, examples, or helper files are documented by purpose when present.
- Paths are portable and skill-local unless the skill is explicitly environment-specific.
- Stop-and-ask boundaries exist where silent assumptions would change scope, behavior, writes, ownership, safety, or file targets.
- Completion signals exist and fit the skill type and active mode.
- Task skills have a concrete artifact or outcome, required inputs when needed, source of truth, local anti-laziness gates, mode/fallback rules, guardrails, output format, artifact verification, failed-verification behavior, and a proof package.
- Controller skills have a core rule, priority or interaction model, active mode when needed, gates, red flags, handoff rules, and process verification.
- Each major rule traces to a real failure mode, safety boundary, or success condition.
- Findings include concrete file references, or the audit explicitly states that no findings were found in scope.

Do not end an audit after a few style observations. End it after metadata, dependency surface, assets, portability, ambiguity boundaries, type-specific structure, completion logic, and reported findings have all been checked for the requested scope.
