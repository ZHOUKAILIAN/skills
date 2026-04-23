---
name: skill-standard
description: Meta-standard for classifying skills before applying the correct quality rubric. Use this to decide whether a skill is workflow-oriented or strategy-oriented, then switch to the matching standard.
---

# Skill Standard

This is the routing standard, not the only writing standard.

Use this skill to classify a skill into the correct category before judging its quality.
A single universal rubric is not sufficient for all SKILL.md files.

---

## Core Rule

Before evaluating or rewriting any skill, first decide what kind of skill it is.

There are at least two major categories:

1. **Workflow Skills**
   - execution-oriented
   - meant to get a task done
   - usually have concrete success/failure conditions
   - often back cron jobs, automation, API tasks, or operational flows

2. **Strategy Skills**
   - reasoning-oriented
   - meant to give a framework, doctrine, checklist, or evaluation method
   - usually guide judgment rather than execute a fixed flow
   - often support review, writing, planning, or auditing work

Do not apply one category's rubric to the other category by default.

---

## Classification Heuristic

### Choose **Workflow Skill** when the skill primarily answers:
- What concrete task should be completed?
- What assets or runtime are available to complete it?
- What counts as done?
- What should happen when runtime conditions fail?

Typical examples:
- check-in flows
- changelog collection
- auth refresh flows
- scheduled automation
- API-driven operational tasks

### Choose **Strategy Skill** when the skill primarily answers:
- How should the model think about this class of problem?
- What principles or decision criteria should it use?
- What anti-patterns should it avoid?
- When should this framework be applied or not applied?

Typical examples:
- review rubrics
- writing heuristics
- evaluation standards
- architectural judgment frameworks
- planning/doctrine/checklist skills

---

## Routing Rule

After classification:

- If it is execution-oriented, use `workflow-skill-standard`.
- If it is reasoning/framework-oriented, use `strategy-skill-standard`.

If a skill mixes both categories, identify its primary role first.
Only then decide whether to:
- keep it hybrid intentionally, or
- split it into a workflow skill plus a strategy skill.

---

## Anti-Patterns

### Wrong: workflow rubric forced onto strategy skills
Symptoms:
- over-constraining an evaluation rubric with rigid execution gates
- demanding procedural completion signals from a doctrine/checklist skill
- turning judgment frameworks into brittle pseudo-SOPs

### Wrong: strategy rubric forced onto workflow skills
Symptoms:
- goals sound good but execution contract is vague
- runtime constraints are implied instead of specified
- completion is left to model intuition
- automation can "look done" without being verifiably complete

---

## Output

When using this skill, produce:
1. the detected skill category
2. the reason for classification
3. the correct downstream standard to apply
4. if needed, whether the skill should be split into two skills

## Completion Signal

Do not stop at “this skill looks fine.”
A completed review must explicitly name the skill category and the correct standard that should govern it.
