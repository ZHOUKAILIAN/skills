---
name: skill-standard
description: Use when evaluating, auditing, or improving SKILL.md content against the repository's skill authoring standard.
---

# Skill Standard

Use this as the single authoring and audit standard for skills in this repository. A good skill reduces a repeated model failure mode with the smallest clear rules needed to change behavior, then defines how completion is proven.

## Core Rule

A skill is acceptable only when its trigger, behavior boundary, source of truth, stop conditions, and completion proof are explicit enough that another agent can use it without guessing.

Wrong: "Be careful and produce high quality work."
Right: "Read the source artifact, account for every in-scope item, run the verifier, and report pass/fail evidence."

## Review Workflow

1. Read the target `SKILL.md`, `skill.json`, and any skill-local assets that shape behavior.
2. Classify the active behavior as task, controller, reference, or mixed.
3. Apply the universal standard to every skill.
4. Apply the relevant type addendum in this file.
5. Make the smallest fix that closes the verified failure mode.
6. Verify metadata, dependency surface, paths, and completion signals before closing.

If the skill is mixed, choose the active mode before judging it. Do not force one completion signal across materially different modes.

## Skill Types

| Type | Purpose | Examples |
| --- | --- | --- |
| Task skill | Executes work and produces a verifiable artifact or task outcome | Figma restoration, customer-service troubleshooting, E2E coverage generation |
| Controller skill | Governs sequencing, routing, gates, or handoffs across work | Skill lifecycle, docs-first workflow, debugging discipline |
| Reference skill | Provides standards or constraints to apply inside another task | CSS rules, style guides, API usage rules |
| Mixed skill | Contains multiple modes with different outputs or gates | Create/review/sync/ship lifecycle skills |

Reference skills usually need task-like proof for the artifact they constrain. If a reference skill mainly controls sequencing, audit that part as controller behavior.

## Universal Standard

Every `SKILL.md` must satisfy these rules regardless of type.

### 1. Discovery Metadata Is Trigger-Only

The frontmatter `description` and `skill.json.description` must describe when to use the skill, not summarize the workflow.

Good: "Use when investigating a customer service issue that requires logs, code, data, and root-cause explanation."
Bad: "Use to ask questions, query logs, read code, query database, write Feishu report, then ask whether to fix."

### 2. Semantically Clear, No Ambiguity

Every important term must have one clear meaning. Avoid vague verbs when a wrong interpretation would change behavior.

Good: "Search for major AI model releases from OpenAI, Anthropic, Google, and Meta."
Bad: "Update model."

### 3. One Skill, One Behavior Boundary

A skill should own one coherent behavior boundary. Split only when two parts have different triggers, safety rules, or completion signals that would make one skill confusing.

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

## Task Skill Addendum

Use this section when a skill executes work and produces a verifiable artifact or task outcome.

### Required Shape

A task skill should usually contain:

- `Goal`: the artifact or outcome the task must produce.
- `When To Use` and `When Not To Use`: routing boundaries.
- `Required Inputs`: information needed before safe execution.
- `Source Of Truth`: authoritative facts, docs, data, design, logs, code, or user instructions.
- `Mode And Fallback Rules`: preferred path, allowed fallbacks, and stop conditions.
- `Workflow`: ordered phases or a decision tree.
- `Local Anti-Laziness Gates`: task-specific checks that block known shortcuts.
- `Available Assets`: scripts, templates, references, APIs, CLIs, or helpers.
- `Guardrails`: read/write boundaries, credentials, environment, approval, and safety limits.
- `Success Criteria`: objective conditions that prove the artifact is acceptable.
- `Verification`: how those criteria are checked.
- `Proof Package`: what evidence the final answer must report.

Only include sections that materially change behavior. A narrow task skill can combine related sections when the checks stay clear.

### Source Of Truth

Every task skill must name the authority for facts and acceptance.

Examples:

- Official docs for API guidance.
- Figma node data for exact design restoration.
- User-provided Feishu records for change scope.
- Runtime logs, code, and database records for incident investigation.
- Rendered artifact output for documents, slides, sheets, images, and web pages.

Screenshots, summaries, memory, and model guesses can support the task only when the skill says they are acceptable sources.

### Local Gates

Anti-laziness gates must live near the workflow they block. The shared standard can name the pattern; the task skill must name the exact shortcut and exact check.

For each task skill, ask:

1. What shortcut would let the agent falsely claim completion?
2. What observable artifact proves the shortcut did not happen?
3. What mechanical check can inspect that artifact?
4. What must happen if the check fails?

Good: "Node ledger verification must pass before Figma implementation starts."
Bad: "Inspect the design carefully."

### Gate Patterns

Use only the gate patterns that fit the task.

Scope accounting: require an item ledger when the task processes multiple nodes, pages, records, slides, rows, files, routes, screenshots, tests, or user journeys. The ledger needs stable identity, status, exclusion or blocked reasons, and completion proof. Default stance: zero unaccounted in-scope items.

Gate artifacts: when a later phase depends on earlier evidence, require a concrete artifact such as a node ledger, rendered screenshot set, recalculation output, DOM snapshot, log evidence table, or test discovery summary. Later phases must consume that artifact.

Mechanical verification: use validators, renderers, linters, type checks, recalculators, screenshots, visual diffs, DOM snapshots, log queries, SQL/API count checks, or file-content checks when practical. If not practical, define the manual inspection evidence required.

Failed-gate behavior: when verification fails, either fix the failed criterion and re-run the check, or stop and report `not ready` with evidence. Do not continue past a blocking gate and still claim completion.

### Modes And Fallbacks

If a task can run in multiple modes, choose one mode before execution.

Fallback rules must say:

- preferred path
- fallback trigger
- whether user approval is required
- whether fallback changes output quality, safety, credentials, or verification
- what to do if fallback is unavailable

Fallback is never permission to bypass the source of truth, safety boundary, or completion signal.

### Success Criteria And Proof Package

Success criteria must be objective enough to check.

Good: "All in-scope records are accounted for, generated tests follow existing naming conventions, and skipped execution is reported with reason."
Bad: "Write a useful report."

The final output must report evidence, not confidence:

- Artifact produced or changed.
- Source-of-truth inputs inspected.
- Scope counts when the task is multi-item.
- Verification checks run and pass/fail status.
- Skipped or impossible checks with reason.
- Failed gates and whether they were fixed, re-run, or left as blockers.
- Residual risk only when it affects confidence in completion.

## Controller Skill Addendum

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

Controller skills should focus on sequencing and guardrails. They should not duplicate detailed task instructions that belong in the task skill being routed to.

Good: "`skill-lifecycle` owns create/improve/sync/ship flow; `skill-standard` owns the quality gate."
Bad: repeat the full contents of a downstream task workflow inside the controller.

### Active Mode Is Mandatory For Multi-Entry Skills

If the skill has multiple workflows, select one active mode before acting. Completion checks apply only to that mode.

Good: create mode, improve mode, sync mode, shipping mode.
Bad: apply all mode checks to every invocation.

### Red Flags Should Target Agent Rationalizations

Controller skills should name the specific shortcut they prevent.

Good: "This is just a quick fix" -> still route the doc owner first.
Good: "The first few nodes show the pattern" -> keep reading every in-scope node.
Bad: generic advice such as "be careful" or "think deeply."

## Red Flags

These thoughts indicate the standard is about to be weakened:

| Thought | Correct action |
| --- | --- |
| "The metadata is enough; the body can explain the rest." | Keep metadata trigger-only and put workflow in `SKILL.md`. |
| "The task skill says be careful, that is enough." | Add task-local gates, verification, and proof package requirements. |
| "This skill has several modes, but one completion signal is fine." | Require active mode and mode-specific completion checks. |
| "The dependency is mentioned in prose, so skill.json is optional." | Declare the dependency in `skill.json.sub_skills`. |
| "This rule is generally good advice." | Keep it only if it closes a real failure mode or success condition. |

## Audit Checklist

An audit or improvement pass using this standard is complete only when all applicable checks are done:

- The skill type is classified as task, controller, reference, or mixed.
- Mixed skills have an explicit active mode before type-specific checks are applied.
- `SKILL.md` frontmatter and `skill.json` names/descriptions are checked for consistency.
- Descriptions are trigger-only and do not summarize workflow.
- Skill dependencies are checked against `skill.json.sub_skills`.
- Bundled assets, scripts, templates, references, or helper files are documented by purpose.
- Paths are portable and skill-local unless the skill is explicitly environment-specific.
- Stop-and-ask boundaries exist where silent assumptions would change scope, behavior, writes, ownership, or file targets.
- Completion signals exist and fit the skill type and active mode.
- Task skills have required inputs, objective success criteria, source of truth, local anti-laziness gates, workflow, mode/fallback rules, guardrails, artifact verification, verification-failure handling, and a proof package.
- Controller skills have core rule, priority or interaction model, active mode when needed, gates, red flags, handoff rules, and process verification.
- Each major rule traces to a real failure mode, safety boundary, or success condition.
- Findings include concrete file references, or the audit explicitly states that no findings were found in scope.

Do not end an audit after a few style observations. End it after metadata, dependency surface, assets, portability, ambiguity boundaries, type-specific structure, completion logic, and reported findings have all been checked for the requested scope.
