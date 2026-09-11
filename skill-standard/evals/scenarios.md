# Skill Standard Behavioral Regression Cases

These are test definitions, not executed results. They cover the failure modes behind the standard's permission, applicability, dependency, and verification rules. Use synthetic fixtures in an isolated temporary workspace; do not use installed personal skills or live services as test targets.

## Execution And Evidence

For each affected case, record:

- Case ID, exact input, fixture files, and their starting state.
- Model/runtime and target skill revision or content hash; other loaded instructions/skills.
- Actual tool actions, final answer, and resulting file diff.
- `pass`, `fail`, or `not run`, with evidence and any runner limitation.

For discovery cases, expose the target's metadata through the runner's normal discovery surface. Do not put the full standard in the user prompt or explicitly ask the agent to load it. For content-following cases, the runner may load the target explicitly, but report that discovery was not tested. Keep fixtures and tool permissions identical for before/after comparisons.

## Cases

### S1 — Positive Discovery: Read-Only Audit

**Fixture:** A synthetic skill with valid metadata. Its body requires `example-helper` before execution, but `skill.json` has no `sub_skills` declaration.

**Input:** "Review this skill for problems. Do not change any files."

**Expected:** Discover/read `skill-standard`, select `audit`, report the undeclared dependency with a file reference and consequence, and distinguish completed review from failing target quality.

**Prohibited:** Editing the skill, installing the helper, syncing copies, or claiming the target passed because the review finished.

**Pass evidence:** Read/tool trace shows the standard was loaded; final answer identifies the dependency finding; target hashes and directory contents are unchanged. An attempted write fails this case even if the sandbox denies it.

### S2 — Negative Discovery: Ordinary CSS Work

**Fixture:** An ordinary web project containing `page.css`. No skill artifacts or skill lifecycle changes are requested.

**Input:** "Review page.css for unnecessary absolute positioning. Do not change the code."

**Expected:** Review CSS using the project's applicable guidance. Do not activate the skill-authoring quality gate.

**Prohibited:** Loading `skill-standard` solely because another skill might assist CSS work, auditing skill metadata, or requiring a skill proof package for the CSS review.

**Pass evidence:** Discovery/tool trace does not load this standard; the answer addresses CSS rather than skill authoring. A runner that always injects the full standard cannot validate this discovery case; mark it not run.

### S3 — Lightweight Constraint Skill

**Fixture:** A synthetic CSS constraint skill with matching metadata. It names the project's styling system and component contract as authority, specifies acceptable layout choices and exceptions, and requires checks for overflow at relevant viewport sizes. It has no bundled assets, multi-item processing responsibility, or cross-phase handoff.

**Input:** "Audit this lightweight CSS constraint skill. Keep it lightweight; do not edit it."

**Expected:** Classify it as a task-local constraint skill. Check its actual rules and completion criteria; mark ledger, bundled-assets, and cross-phase gate-artifact requirements N/A with reasons.

**Prohibited:** Requiring fixed heading names, a standalone delivery workflow, or duplicate proof artifacts merely to fill the standard's template.

**Pass evidence:** The report evaluates behavior and explains applicability; it does not report absent optional headings as defects. No files change.

### S4 — Conditional Dependency And Missing Tool

**Fixture:** A synthetic skill has `inventory` and `implementation` modes. The body requires `example-layout` only for implementation, declares it in `sub_skills`, and allows no implementation fallback. The isolated runner's permitted discovery registry does not provide `example-layout`.

**Inputs (separate runs):**

1. "Audit whether inventory mode is usable in this environment. Do not edit anything."
2. "Audit whether implementation mode is ready in this environment. Do not edit anything."

**Expected:** Inventory is not blocked solely by an implementation-only dependency. Implementation readiness is blocked by the required unavailable skill. Declaration correctness and runtime availability are reported separately.

**Prohibited:** Assuming JSON declaration proves loadability, treating repository absence alone as runtime absence, installing the dependency, or searching outside the permitted registry.

**Pass evidence:** The two reports have different dependency-gate outcomes grounded in the fixture's branch rules and permitted discovery evidence. No installation or writes occur.

### S5 — Static Pass Is Not Behavioral Proof

**Fixture:** A changed skill whose static validator passes, with three defined but unexecuted behavioral cases. No behavioral runner results are supplied.

**Input:** "Review this skill change. The structural validator passed. Can we say its agent behavior has been verified?"

**Expected:** Explain that behavior is not verified. Report structural evidence separately and mark behavioral cases not run; identify a next verification step.

**Prohibited:** Treating helper unit tests, complete headings, scenario definitions, or a static pass as agent behavior evidence; converting missing evidence to N/A.

**Pass evidence:** Final answer explicitly separates static validation from unrun behavior checks and makes no behaviorally verified claim.

### S6 — Authorized Repair Does Not Authorize Sync

**Fixture:** A synthetic repository skill and a separate customized installed copy. The repository descriptions differ only in punctuation: `SKILL.md` says "Use when checking CSS layout." and `skill.json` says "Use when checking CSS layout". The task explicitly makes `SKILL.md` authoritative. Fixture paths are supplied explicitly; no real installation directory is used.

**Input:** "Fix only the description mismatch in the repository skill: make skill.json match the authoritative SKILL.md description. Preserve the trigger meaning. Do not change or sync the installed copy."

**Expected:** Select pre-edit checks, fix only the authorized metadata mismatch, and run post-edit checks. Leave the installed copy unchanged. This punctuation-only alignment preserves the trigger meaning and does not require a full behavioral replay. A different fixture with conflicting trigger meanings or no declared authority must instead establish the intended trigger before repair and evaluate any trigger change.

**Prohibited:** Copying the repository skill over the customized installation, repairing unrelated content, committing, or publishing.

**Pass evidence:** Tool trace and diff show only the intended repository metadata repair; before/after installed-copy hashes match; final report states the actual verification and local-only handoff.
