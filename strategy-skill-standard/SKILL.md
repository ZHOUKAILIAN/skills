---
name: strategy-skill-standard
description: Quality standard for reasoning-oriented skills that provide frameworks, rubrics, heuristics, or decision guidance.
---

# Strategy Skill Standard

Use this standard for skills whose primary job is to shape how the model thinks.

These skills are not execution contracts first.
They are judgment frameworks.
Their quality depends on clarity of scope, principles, and decision boundaries.

---

## What a Strategy Skill Must Do

A strategy skill must define:
- what kind of problem it helps with
- when it should be used
- when it should not be used
- what principles or criteria should guide judgment
- what anti-patterns or traps to avoid

If it does not define those boundaries, it will sprawl and be misapplied.

---

## Strategy Writing Standard

### 1. Purpose and scope must be explicit
State the class of decisions this skill is for.
Do not pretend to be universal if the framework is only useful in a narrow domain.

### 2. Principles over pseudo-procedure
A strategy skill should provide decision rules, criteria, and heuristics.
Do not force it into fake operational steps unless the strategy genuinely requires staged analysis.

### 3. Tell the model what to notice
A good strategy skill highlights the important dimensions to evaluate.
Examples:
- evidence quality
- ambiguity level
- tradeoff boundaries
- common failure modes
- escalation conditions

### 4. Define applicability boundaries
The skill must explain when to use it and when another skill or framework is more appropriate.
Without this, strategy skills become vague universal advice.

### 5. Anti-patterns are first-class content
A strong strategy skill explicitly names the common wrong moves.
This is often more important than adding more principles.

### 6. Do not fake workflow completion signals
A strategy skill usually should not pretend to have operational completion gates like a workflow skill.
Its completion signal should instead be tied to whether the correct reasoning frame was applied and the relevant criteria were evaluated.

### 7. Abstraction must stay grounded
The framework should be reusable, but still concrete enough to guide real decisions.
If everything sounds wise but nothing changes behavior, the skill is too abstract.

---

## Anti-Patterns

- reads like motivational advice instead of a usable framework
- no scope boundary, so it applies to everything and therefore nothing
- no anti-patterns, so misuse is invisible
- over-converted into rigid steps that kill judgment
- vague slogans replace decision criteria

---

## Review Output

When auditing a strategy skill, report:
1. the intended decision domain
2. whether scope is clear
3. whether principles are concrete enough to guide judgment
4. whether anti-patterns are explicit
5. whether applicability boundaries are defined
6. the exact ambiguity or overreach, if any

## Completion Signal

A strategy skill review is complete only when you can state what problems the skill is for, what decision criteria it provides, and where its boundary stops.
