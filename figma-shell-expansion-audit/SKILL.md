---
name: figma-shell-expansion-audit
description: |
  Use when a Figma restoration boundary contains instances, component shells, icon wrappers, or other nodes whose metadata may look terminal while implementation-relevant internal structure still exists.
---

# Figma Shell Expansion Audit

Audit shell-capable Figma nodes until their internal implementation-relevant structure is no longer ambiguous.

## Goal

Prevent false completion caused by shell nodes whose metadata appears empty but whose real structure is only visible through design-context expansion.

## Success Criteria

Do not claim a shell-capable node is complete unless all of the following are true:

1. The node is explicitly identified as shell-capable or explicitly ruled out as shell-capable.
2. Metadata traversal has been exhausted for the current boundary.
3. Design-context expansion has been checked for the node when the node affects implementation.
4. The ledger records `Expansion basis` and `Completion proof`.
5. Terminal status is supported by evidence, not by assumption.

## Shell-Capable Nodes

Treat these as shell-capable by default:

- `instance`
- component-like reusable containers
- icon wrappers
- slot wrappers
- named design-system shells
- any node whose screenshot or root design context suggests internal structure not visible in metadata

## Hard Gates

### Gate 1: Metadata is not enough for shells

Do not mark a shell-capable node terminal only because `get_metadata(node)` shows no child nodes.

### Gate 2: Design-context expansion is required when the node affects implementation

If a shell-capable node changes layout, text, iconography, state, spacing, or user-visible chrome, inspect `get_design_context(node)`.

### Gate 3: Record the proof

For every shell-capable node in scope, the audit ledger must record:

- whether the node was expanded
- which source established completion
- what evidence proved that no remaining implementation-relevant structure was missing

## Workflow

1. Identify shell-capable nodes inside the current boundary.
2. Use `get_metadata` to detect obvious structural children.
3. Use `get_design_context` on shell-capable nodes that influence implementation.
4. Compare metadata-only understanding against expanded understanding.
5. Mark the node as `shell` until completion proof exists.
6. Only then allow `terminal` status.

## Output Contract

For each shell-capable node, report:

- node id
- why it is shell-capable
- whether metadata alone was sufficient
- whether design context revealed more structure
- expansion basis
- completion proof
- final terminal decision

## Failure Modes To Prevent

- Marking an `instance` terminal only because metadata returned no children
- Treating root-level design context as proof for every shell without checking the actual node
- Recording `Expanded = yes` without saying what expanded it
- Recording `Terminal = yes` without `Completion proof`
- Ignoring shell expansion for icons or small wrappers because they look visually simple

## Practical Rule

If there is any doubt whether a node is truly terminal, keep it non-terminal and expand it. The cost of one extra expansion is lower than the cost of a false 1:1 claim.
