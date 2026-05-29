---
name: frontier-changelog
description: Use when producing a daily Chinese product-intelligence digest for frontier AI IDE/CLI, agent runtime, and model changelog updates.
---

# Frontier Changelog

## Goal

Produce a Chinese product-intelligence digest of frontier AI coding tools, agent runtimes, and major model updates. The output should answer:

1. 哪些工具/模型更新了。
2. 更新了什么。
3. 这些变化解决什么问题。
4. 对用户、开发流程、agent workflow 有什么意义。
5. 哪些值得关注、升级或观望。

This skill should not produce a verbose evidence-audit report. Evidence matters, but the primary deliverable is a readable interpretation.

## Default Scope

Unless the user narrows scope, check these sources:

1. Claude Code
   - `https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md`
   - `https://github.com/anthropics/claude-code/releases`
2. Codex
   - `https://developers.openai.com/codex/changelog`
   - `https://github.com/openai/codex/releases`
3. Cursor
   - `https://cursor.com/changelog`
4. Gemini CLI
   - `https://google-gemini.github.io/gemini-cli/docs/changelogs/`
5. Antigravity
   - `https://antigravity.google/changelog`
6. OpenCode
   - `https://opencode.ai/changelog`
7. Major model vendors when relevant: OpenAI, Anthropic, Google, Meta, xAI, Mistral, and similar official sources.

Use official changelogs, GitHub releases, package registries, and official announcements. If one source is unreadable, continue with the rest and label uncertainty.

## Source-Specific Rules

### Claude Code

Claude Code often splits evidence:

- Raw `CHANGELOG.md` has version content but no date.
- GitHub Releases has release timestamps.

Join content and date by version number. For example, use the raw changelog section for `2.1.154` and the GitHub Release timestamp for `2.1.154`. If the joined version falls in the target window, treat it as confirmed.

### Codex

Codex documentation changelog can lag GitHub Releases. Always consider GitHub Releases as a first-class source, not only a fallback. If GitHub Releases is newer than the developers changelog, include the newer release and note the source difference briefly.

Split Codex CLI, Codex app, and IDE extension updates when the source mixes them.

### Cursor

If the latest Cursor changelog entry has useful content but no reliable date, include it under “日期不确定但值得看” instead of dropping it. Do not claim it is confirmed in-window.

### OpenCode

OpenCode changelog is usually date-grouped. Interpret updates by runtime themes, especially ACP, WebSocket transport, background agents, project identity, TUI, and desktop reliability.

### Gemini CLI

If the official changelog latest entry is old, say so briefly. Do not fill the digest with old details unless the user asks for history.

### Antigravity

If the source returns only a shell/title and no changelog body, mark it as unreadable briefly. Do not let unreadable sources dominate the digest.

## Time Window

Default window: yesterday 09:00 → today 09:00 Beijing time.

Do not let strict window filtering hide valuable latest updates. Use these labels:

1. `confirmed` — reliable timestamp/date and substantive body.
2. `likely` — substantive update with imprecise but plausible date.
3. `date_uncertain` — useful latest content with weak or missing date.
4. `no_recent_update` — latest visible item is older than the window.
5. `source_unreadable` — source is reachable but body is unusable.

GitHub/npm/package publish time may confirm a changelog section that itself lacks a date when the version matches.

## Interpretation Standard

For each important tool, choose the highest-impact 2-4 changes for deeper explanation. Explain:

1. 它是什么。
2. 它解决什么痛点。
3. 现在怎么变 / 怎么用。
4. 对用户、开发流程或 agent workflow 的意义。
5. 我的判断：值得升级、值得关注、可观望，或风险较高。

Smaller fixes can be summarized as quick notes. Do not translate every upstream bullet one by one.

### Command and Setting Explanations

When mentioning a command, flag, setting, mode, environment variable, or config key, explain it as an interface:

1. 它是什么入口：slash command、shell command、config、env var、UI option 等。
2. 在哪里用：TUI/chat、shell、配置文件、plugin manifest、API 等。
3. 它改变什么：model effort、transport、permissions、background behavior、rendering 等。
4. 什么时候该用。
5. 什么时候不该用 / 代价是什么。

Example boundary:

- Good: “`/effort xhigh` 是 Claude Code 里的 slash command，用来把当前任务的推理 effort 调到更高档。适合复杂重构、大 PR review、跨文件 debug；代价是更慢、更贵。”
- Bad: “`/effort xhigh` 适合最难任务。”

## Output Structure

Return the report in Chinese. Use explicit numbering so the user can refer to “1.2” or “2.3” on mobile.

Recommended shape:

```markdown
# AI 工具/模型更新解读

窗口：北京时间 ...
状态：FULL/PARTIAL

## 1. 今日值得看

### 1. Claude Code 2.1.154（confirmed）
一句话判断：...
来源：...

#### 1.1 Opus 4.8：...
...

#### 1.2 Dynamic workflows：...
...

我的判断：...

### 2. Codex CLI 0.135.0（confirmed）
...

#### 2.1 codex doctor：...
...

## 2. 日期不确定但值得看

### 4. Cursor Shared Canvases + /loop（date_uncertain）
...

## 3. 无近期更新 / 暂不可读

1. Gemini CLI：...
2. Antigravity：...

## 4. 总结判断

1. Claude Code：...
2. Codex：...
3. OpenCode：...
```

Avoid huge markdown tables in chat outputs.

## Quality Gate

Before sending, verify:

1. Important updated tools are included, especially Claude Code, Codex, and OpenCode when they have new releases.
2. Split evidence is joined correctly, especially Claude Code changelog body + GitHub release date.
3. Codex GitHub Releases were checked, not only the developers changelog.
4. Major changes are interpreted in Chinese, not left as keyword lists.
5. Important commands/settings explain what they are, where to use them, what they change, when to use them, and tradeoffs.
6. Important sections and subtopics have visible numbering such as `1`, `1.1`, `1.2`.
7. Uncertain, old, or unreadable sources are labeled briefly and do not dominate the report.

Completion means the final digest satisfies this quality gate or explicitly says which source prevented full completion.
