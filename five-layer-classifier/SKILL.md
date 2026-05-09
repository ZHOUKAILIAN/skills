---
name: five-layer-classifier
description: "Use when classifying a project, repository, directory, or file set under the AI Coding five-layer governance model, including file-level responsibility, truth-source, product/control repo, local-control, research-archive, public/private, migration, split, or downgrade decisions."
---

# Five Layer Classifier

## Goal

Produce a verifiable classification artifact for project assets:

1. A file-level or file-group classification table.
2. A high-risk misclassification list.
3. Migration, split, local-retention, downgrade, or "do not formalize yet" recommendations.
4. When useful, an agent guide that says what to read first, what to trust, and where to write back.

## Boundaries

Use this skill to classify project assets and governance boundaries. Do not use it as:

- A generic file cleanup script.
- A replacement for project-specific product requirements, technical designs, or governance docs.
- A permission to migrate, delete, publish, or physically split repositories without a separate user request.
- A way to invent a new layer taxonomy when the five-layer model is sufficient.

## Required Inputs

Establish these before classifying:

- Target scope: repository root, directories, files, or file groups. If absent, default to the current working directory for a project-wide audit.
- Purpose: file governance, pre product/control repo split audit, public/private audit, or agent orientation. If absent, default to file governance.
- Output destination: chat response unless the user asks for a file.
- Public/private policy and canonical project docs when the user expects public-history or truth-source decisions. If unavailable, mark those fields as `needs policy` instead of guessing.

Stop and ask if the target scope is unsafe or unclear enough that classification would touch the wrong project. Do not ask only because the purpose is omitted; use the default above.

## Source Of Truth

- Use `references/five-layer-model.md` for the portable five-layer model, route discipline, red lines, and default boundary rules.
- Use `references/classification-report-template.md` for the output shape.
- Use active project docs and file contents as the project-specific source of truth. Directory names, file names, and document types are only signals.
- Treat research drafts as background unless the user explicitly says they are the current canonical rule.
- For projects with their own agent rules, obey stricter local rules in addition to this skill.

## Available Assets

- `scripts/inventory_project.py`: builds a deterministic file ledger with path, size, extension, path signals, and first Markdown heading. Use it for project-wide or large-scope audits before classifying.
- `references/five-layer-model.md`: compact reference for layers, domains, repository boundaries, conflict priority, red lines, and common examples.
- `references/classification-report-template.md`: Markdown template for the classification table, risk list, and final proof package.

## Workflow

### 1. Route The Request

Resolve the mode before scanning:

- `project-scan`: classify a repository or broad directory range.
- `file-set`: classify named files or small file groups.
- `review`: review or repair an existing classification table.
- `agent-guide`: produce a reading order, truth-source map, and writeback map from an existing or newly generated table.

Bind the task with this order: request -> scope -> purpose -> baseline docs -> hard gates -> classify.

Fallbacks:

- If `scripts/inventory_project.py` cannot run, use `rg --files` or another local file listing command and report the fallback.
- If project-specific public/private policy is missing, continue classification but mark public-history fields as `needs policy`.
- If a file's responsibility cannot be established from available content, mark it `needs human decision` instead of guessing.

### 2. Build A Scope Ledger

For project-scan or broad scopes, run:

```bash
python3 <skill>/scripts/inventory_project.py <scope> --root <repo-root>
```

Use the ledger to account for every in-scope file or declared file group. Exclude generated/vendor/cache folders only when the exclusion is visible in the ledger or final proof package.

For small file sets, `rg --files` and direct reads are enough, but still keep an explicit list of in-scope paths.

### 3. Inspect Responsibility Before Judging

For each file or group, inspect enough content to answer the responsibility question. Open headings, templates, schemas, source entry points, or representative files as needed.

Wrong: classify `docs/*.md` as product definition because it is a document.
Right: classify by what the file governs: product semantics, runtime reality, project defaults, shared workflow, local session continuity, or research.

### 4. Classify In Fixed Order

Use the ordered questions in `references/five-layer-model.md`:

1. Does it define the product body? Layer 1.
2. Does it carry current product implementation reality? Layer 2.
3. Does it define how this project lands or packages the product? Layer 3.
4. Does it govern shared collaboration, verification, handoff, or closure? Layer 4.
5. Does it only keep the current local development scene alive? Layer 5.
6. If none fit, is it research, comparison, argumentation, writing, or external background? Outside the five layers.

Assign one primary layer. If one file has two primary responsibilities, recommend `split` instead of forcing a false single owner.

After the layer, decide domain, formal truth-source status, default carrying boundary, public-history recommendation, action, and reason.

### 5. Apply Red Lines

Block these shortcuts before producing the final result:

- Do not classify by directory name, file extension, or document type alone.
- Do not promote handoff, task cards, local logs, or current-session notes to formal truth sources.
- Do not promote research drafts to shared governance unless the project has explicitly adopted them.
- Do not recommend physically deleting Layer 5 local scene assets just because a public repo should not contain them.
- Do not discuss physical product/control repo splitting until the classification table and formal-entry boundaries exist.
- Do not treat "in a repo" as "in a formal carrying area"; local-control copies are not formal shared truth.

If a red line is triggered, put it in the high-risk list and revise the affected rows.

## Output

Use the report template unless the user requests a different shape. The final answer or artifact must include:

- Scope and mode.
- File-level or file-group classification table.
- High-risk misclassification list.
- Recommended migration, split, downgrade, local-retention, and not-yet-formalized objects.
- Stable formal entries discovered.
- Proof package: source inputs inspected, scope count or grouping rule, exclusions, verification checks, and unresolved policy gaps.

## Verification

Before completion:

- Every in-scope file or declared group is accounted for as classified, excluded, blocked, or needs-human-decision.
- Every classified row has a primary layer, carrying boundary, public-history recommendation, action, and reason.
- Every `待拆分` or `needs-human-decision` row explains the mixed responsibility or missing policy.
- Red-line checks have been applied and failures are either fixed or reported as blockers.
- If the result is file-group level rather than file-level, state that clearly and do not claim file-level coverage.

If verification fails, fix the specific failed rows and rerun the check. If the failure depends on missing policy, ownership, or source-of-truth decisions, stop with `not ready` and list the blocker.

## Success Criteria

The task is complete only when the classification artifact states scope, accounts for every in-scope item or group, applies the red lines, and includes a proof package that makes remaining uncertainty explicit.
