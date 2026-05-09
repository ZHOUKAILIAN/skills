# Five-Layer Model Reference

## Core Rule

Classify by responsibility first, then by carrying boundary. Never classify by directory name, file name, document type, or perceived importance alone.

## Layers

| Layer | Question answered | Typical contents | Domain |
| --- | --- | --- | --- |
| Layer 1: product definition | What is the product? | goals, core objects, product semantics, long-term operating model, product contracts | product domain |
| Layer 2: product implementation | What is currently implemented? | source code, tests, runtime scripts, build outputs that express current reality, current technical debt | product domain |
| Layer 3: project landing | How does this project carry and run the product by default? | default entry points, repository organization, packaging shell, artifact locations, project status baselines | project bridge domain |
| Layer 4: repository governance | How does the repository collaborate, verify, hand off, and close work? | branch discipline, Task Packet, preflight, merge gates, handoff protocol, role protocol, risk gates | engineering reuse domain |
| Layer 5: local development control | What keeps the current local scene alive? | live handoff, task board, temporary logs, local notes, session memory, transient validation drafts | engineering reuse domain |
| Outside five layers | Does this mainly research, compare, argue, or support writing? | research drafts, comparison notes, external-background summaries, article drafts | research archive |

## Ordered Classification Questions

Ask in this order:

1. Does the asset define the product body, stable product semantics, product goals, product architecture, or official product contracts?
2. Does it carry current implementation reality: source, tests, runtime behavior, scripts, generated runtime contracts, or known current technical debt?
3. Does it define this project's default way to host, package, organize, release, or represent the product in this repository?
4. Does it define shared repository collaboration, verification, handoff, role boundaries, preflight, merge, closure, or protected-document gates?
5. Does it only preserve current local work continuity: live session state, task instance state, temporary logs, scratch validation, or local agent memory?
6. If none fit, is it research, comparison, argumentation, writing, or external background? Classify it outside the five layers.

## Default Carrying Boundaries

| Classification | Default carrying boundary | Formal truth source | Public-history default |
| --- | --- | --- | --- |
| Layer 1 | product repo formal area | yes, if adopted by the project | usually yes |
| Layer 2 | product repo formal area | yes for current runtime reality | usually yes, except secrets/generated/private artifacts |
| Layer 3 | split by responsibility; project bridge until clarified | yes only for adopted project defaults | policy-dependent |
| Layer 4 | control repo formal area, or shared repo during transition | yes for shared governance | usually private or sanitized |
| Layer 5 | current working directory; optional control repo local-control copy for recovery | no, unless promoted through governance | no |
| Outside five layers | research archive | no, unless later promoted | no or policy-dependent |

Product runtime belongs to Layer 2 by default, not the control repo. Shared governance belongs to Layer 4. Layer 5 copies in a control repo are private recovery material, not formal shared truth.

## Conflict Priority

- Layer 1 is the authority for intended product semantics. Layer 2 is the authority for current runtime reality. When they conflict, report drift instead of silently rewriting one from the other.
- Layer 3 must contain only adopted project defaults. Experiments, comparisons, and proposed defaults stay in Layer 5 or research until adopted.
- Layer 4 governance controls shared execution even when local notes disagree.
- Layer 5 preserves current continuity but does not override Layers 1-4.
- Research material supports reasoning but does not decide active execution unless promoted into an active project document.

## Common Examples

| Asset | Layer | Boundary | Reason |
| --- | --- | --- | --- |
| Product architecture index | Layer 1 | product repo formal area | defines product architecture or product semantics |
| `src/`, `tests/`, runtime scripts | Layer 2 | product repo formal area | expresses current implementation reality |
| Default entry point or packaging shell | Layer 3 | split by responsibility | describes how this project carries the product |
| `STATUS`, `BACKLOG`, `ROADMAP` | Layer 3 if adopted execution baseline; otherwise Layer 5 | project bridge or local-control | project reality/status is not product definition |
| Task Packet template | Layer 4 | control repo formal area | shared work contract |
| Handoff protocol template | Layer 4 | control repo formal area | shared continuity protocol |
| Live handoff or current task card | Layer 5 | local-control | current scene continuity |
| Temporary logs and scratch validation notes | Layer 5 | local-control | transient evidence for current work |
| Research comparison or article draft | outside five layers | research archive | supports argumentation, not current execution |

## Route Discipline

For project work, route before acting:

```text
request
  -> route_resolve
  -> baseline_set
  -> scope_bind
  -> hard_gates
  -> execute
  -> verify
  -> writeback_decision
```

For this skill, `route_resolve` means choosing project-scan, file-set, review, or agent-guide mode. `baseline_set` means identifying the active project docs and the five-layer model. `hard_gates` means applying the red lines before migration, deletion, public-history, or product/control repo conclusions.

## Red Lines

- Directory names are signals, not conclusions.
- File type names such as design, proposal, ADR, contract, or status do not determine the layer.
- Current implementation reality must not be silently promoted to long-term product definition.
- Handoff, live task state, temporary logs, and local agent memory must not be promoted to formal truth sources.
- Layer 5 assets must not be physically deleted only because they are not public.
- Research drafts must not be promoted to shared governance without explicit adoption.
- Physical repository splitting is the last step: file classification first, formal entry consolidation second, public/private policy third, physical split fourth.
