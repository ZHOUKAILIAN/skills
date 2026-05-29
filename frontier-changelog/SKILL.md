---
name: frontier-changelog
description: Track frontier AI IDE/CLI and model updates daily with Chinese product-intelligence interpretation.
---

# Frontier Changelog Tracking

## Goal

Gather latest updates from frontier AI coding tools and major model releases, then explain them in useful Chinese: what changed, why it matters, whether it is worth attention, and how confident the evidence is.

This skill is **not** a legal/evidence audit report. Evidence matters, but the user wants product intelligence first.

## Core Output Philosophy

Prioritize:

1. **有没有更新** — which tools/models changed.
2. **更新了什么** — concrete changes, grouped by theme.
3. **这意味着什么** — Chinese interpretation for daily use.
4. **值不值得关注/升级** — impact judgment.
5. **证据来源** — source links and confidence, concise.

Avoid dry keyword dumps like:

> doctor diagnostics / remote details / Vim mode / TUI rendering / resume flows / permissions profiles

Rewrite into human interpretation, e.g.:

> 这版重点不是新模型，而是让 Codex CLI 更稳定、更好排障、更适合长期会话。`codex doctor` 变强后，环境、Git、终端、app-server、thread 状态能一起检查；以后 Codex 抽风时，可以先让它自己体检，不用靠猜。


## Interpretation Depth Standard

The report must not merely translate feature names. For each important tool, choose **2-4 highest-impact changes** and explain them deeply. Use this 4-part pattern when possible:

1. **它是什么** — what the feature/change is.
2. **它解决什么痛点** — what was painful before.
3. **现在怎么变 / 怎么用** — how behavior changes, commands if useful.
4. **对用户/agent workflow 的意义** — why the user should care.

Do not make every bullet long. Use a two-layer style:

- **Deep interpretation** for the most important 2-4 changes.
- **Quick notes** for smaller fixes.

Example for Claude Code dynamic workflows:

> Dynamic workflows：这是 Claude Code 在往“自动项目编排器”方向走。以前你要么让一个 agent 串行做完整任务，要么手动拆任务、开多个 session。现在它可以根据目标创建 workflow，把任务拆成多个后台 agent 去跑，比如一个 agent 查代码结构，一个 agent 写实现，一个 agent 跑测试，一个 agent 做 review。你可以用 `/workflows` 查看这些后台 workflow 的运行状态。这个能力的重点不是“多开几个 agent”，而是 Claude 开始尝试自己管理任务分解、并行执行和后台推进。

Example for Codex resume flows:

> Resume flows：这解决的是“我昨天/刚才让 Codex 跑过一段任务，现在想接着干，但上下文和工作目录容易对不上”的问题。新版本把更多非交互执行 session 纳入恢复范围，并且更尊重当前指定的 cwd。也就是说，如果你用 Codex 做过一段 headless/exec 类型的任务，之后从 TUI 或另一个入口恢复时，它更可能知道之前发生过什么，也更不容易在错误目录里继续操作。

Example for Claude Code background agents fixes:

> Background agents：这次修了很多后台 agent 的“长跑问题”。比如 pinned sessions 升级后反复重启、后台 session 卡在 blocked/running/working 不退出、daemon 退出后 orphan process 吃满 CPU、subagent 绕过 worktree isolation 写到 shared checkout。这些不是花哨功能，而是决定后台 agent 能不能真正长期跑的基础修复。对想让 agent-team 长时间执行任务的人，这类稳定性比 UI 小功能更重要。

## IDE/CLI Sources

Always check these tools unless the user narrows scope:

| Tool | Primary sources |
| --- | --- |
| Claude Code | `https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md`, `https://github.com/anthropics/claude-code/releases` |
| Codex | `https://developers.openai.com/codex/changelog`, `https://github.com/openai/codex/releases` |
| Cursor | `https://cursor.com/changelog` |
| Gemini CLI | `https://google-gemini.github.io/gemini-cli/docs/changelogs/` |
| Antigravity | `https://antigravity.google/changelog` |
| OpenCode | `https://opencode.ai/changelog` |

Rules:

- Use fixed official URLs first.
- `web_fetch` for fixed URLs may run in parallel.
- `web_search` fallback/discovery stays sequential.
- Prefer official changelogs, GitHub releases, npm/package registry, and official announcements.
- If official source extraction gives only shell/navigation/empty content, mark source quality and try one reasonable official fallback (GitHub releases, raw changelog, package release page, browser snapshot if needed).

## Required Source Adapters

### Claude Code Adapter

Claude Code often splits evidence:

- Raw `CHANGELOG.md` has detailed content by version but no date.
- GitHub Releases has publish date/time.

Mandatory behavior:

1. Fetch both raw changelog and GitHub Releases.
2. Join by version number, e.g. `2.1.154`.
3. Use GitHub Release timestamp as date evidence.
4. Use raw changelog section as content evidence.
5. If joined version falls in window, mark `confirmed_in_window`.

Example interpretation style:

> Claude Code 2.1.154 是能力升级 + 后台 agent 稳定性大修：Opus 4.8 上线，dynamic workflows 能调度大量后台 agent，`claude agents` 更像真正的后台任务系统，同时修了一批 worktree isolation、后台 session 卡死、orphan process、数据外泄识别相关问题。对长期跑复杂任务的人值得关注。

### Codex Adapter

Codex official docs changelog may lag GitHub Releases.

Mandatory behavior:

1. Always fetch both developers changelog and `https://github.com/openai/codex/releases`.
2. Treat GitHub Releases as first-class evidence, not fallback-only.
3. Split `Codex CLI` and `Codex app` when mixed.
4. If GitHub release is newer than docs changelog, include it in main findings and explain source difference briefly.
5. Do not claim update from TOC/navigation text alone; require version/date/body or release body.

Example interpretation style:

> Codex CLI 0.135.0 不是新模型更新，而是长期使用体验更新：`codex doctor` 更适合排障，`/status` 能看 remote/server 细节，TUI 表格/列表/多行输出更稳，resume 会话更不容易接歪，权限 profiles 更适合多项目/多安全级别使用。

### Cursor Adapter

Cursor changelog may show latest content without explicit date.

Mandatory behavior:

- If top/latest entry has substantive content but no date, include it under **日期不确定但值得看** rather than dropping it.
- Do not overclaim it as confirmed in-window.
- Explain why it matters in product terms.

Example:

> Cursor 的 Shared Canvases 更像“agent 产物分享”，/loop 则是本地长运行 agent：让 Cursor 按计划重复跑 prompt，直到部署成功、测试通过或用户停止。日期证据弱，但功能方向值得看。

### OpenCode Adapter

OpenCode changelog is date-grouped and usually readable.

Interpret by themes:

- ACP / `acp-next`
- OpenAI WebSocket / custom base URL
- background agents
- remote project identity
- TUI/Desktop reliability

Example:

> OpenCode 这两天在补 agent runtime 基础设施：`acp-next` 能传 prompt/slash command/usage，OpenAI WebSocket path 开始成形，后台 agent 状态从 polling 转向 push updates，remote-backed project identity 更稳。

### Gemini CLI Adapter

If official changelog latest entry is old, say so briefly and do not fill the report with old details. Optionally mention latest visible version in one line.

### Antigravity Adapter

If fetch returns only title/shell content, mark unreadable briefly. Try browser snapshot or an official fallback only if the user explicitly asks for deeper investigation or the source is critical that day.

## Model Updates

Search sequentially for major model updates from OpenAI, Anthropic, Google, Meta, xAI, Mistral, etc.

For model updates, use the same product-intelligence style:

- What changed in capability/pricing/availability.
- Who should care.
- What is uncertain.

## Time Window

Default window: **yesterday 09:00 → today 09:00** (Beijing time, UTC+8).

But do **not** let strict window filtering hide important latest updates.

Use sections:

1. **今日/窗口内值得看** — confirmed or likely in target window.
2. **日期不确定但值得看** — latest observed, substantive, weak date.
3. **无近期更新/暂不可读** — short, not dominant.

Rules:

- Convert timestamps to Beijing window when possible.
- Date-only entries on yesterday/today Beijing may be `likely_in_window`.
- GitHub/npm/package publish timestamp can confirm a changelog section that itself lacks a date if version matches.
- Out-of-window items should be short unless user asks for history.

## Evidence Labels

Use concise evidence labels, not verbose audit blocks.

- `confirmed` — reliable timestamp/date and substantive body.
- `likely` — substantive latest entry, date imprecise but plausible.
- `date_uncertain` — useful latest content, no reliable date.
- `no_recent_update` — latest visible item older than window.
- `source_unreadable` — source reachable but body unusable.

Include source links under each tool, but do not let evidence metadata dominate.



## Command / Setting Explanation Standard

When a changelog mentions a command, flag, setting, mode, environment variable, or config key, the report must explain it as an interface, not just its effect.

For each important command/setting, answer:

1. **它是什么入口** — command, slash command, config, env var, UI option, etc.
2. **在哪里用** — inside TUI/chat, shell, config file, plugin manifest, API, etc.
3. **它改变什么** — model effort, transport, permissions, background behavior, rendering, etc.
4. **什么时候该用** — concrete scenarios.
5. **什么时候不该用/代价是什么** — cost, latency, risk, noise, instability, experimental status.

Example: `/effort xhigh` should not be explained only as “更适合最难任务”. Explain:

> `/effort xhigh` 是 Claude Code 里的 slash command，用来把当前会话/任务的推理 effort 调到更高档。它不是换工具，也不是打开后台 agent；它是在告诉模型“这个任务值得花更多思考预算”。适合复杂重构、跨文件 debug、架构设计、大 PR review 这类容易半路降智的任务。代价是更慢、更贵，也不适合简单改文案、查一个小 bug 这种轻任务。

Example: `OPENCODE_EXPERIMENTAL_WEBSOCKETS=true` should be explained as an environment variable that opts into experimental WebSocket transport, not simply “WebSocket 可用”.

Example: `defaultEnabled: false` should be explained as a plugin manifest setting that makes a plugin installed but not auto-enabled, reducing surprise permissions/noise until the user explicitly enables it.

## Numbering and Scanability Standard

The report must be easy to scan in Telegram/mobile. Use explicit numbering at every meaningful level.

Required numbering style:

- Main sections use numbered headings where useful: `## 1. 今日值得看`, `## 2. 日期不确定但值得看`, `## 3. 无近期更新 / 暂不可读`.
- Each tool/update uses numbered headings: `### 1. Claude Code 2.1.154（confirmed）`, `### 2. Codex CLI 0.135.0（confirmed）`.
- Each important subtopic under a tool must also be numbered: `#### 1.1 Opus 4.8`, `#### 1.2 Dynamic workflows`, `#### 1.3 Background agents`.
- If a subtopic has multiple details, use short numbered bullets: `1)`, `2)`, `3)` instead of unmarked paragraphs when it improves readability.
- The final summary should also be numbered, e.g. `1. Claude Code：...`, `2. Codex：...`, `3. OpenCode：...`.

Do not rely on visual separators alone. The user should be able to refer to “1.2” or “2.3” and know exactly which point they mean.

## Required Report Format

Return the full report in Chinese.

Recommended structure:

```markdown
# AI 工具/模型更新解读

## 1. 今日值得看

### 1. Claude Code 2.1.154（confirmed）
一句话判断：这是能力升级 + 后台 agent 稳定性大修。

#### 1.1 Opus 4.8：复杂工程任务主力模型升级
解释它是什么、解决什么痛点、怎么用、为什么值得关注。

#### 1.2 Dynamic workflows：从单 agent 往自动项目编排器走
解释任务拆解、后台 agent 并行、/workflows 查看状态，以及对 agent workflow 的意义。

#### 1.3 Background agents：修长期运行地基
解释卡死、空转、worktree isolation、后台 session 恢复等稳定性修复。

我的判断：值得关注/建议升级/可观望。
来源：...

### 2. Codex CLI 0.135.0（confirmed）
一句话判断：这是稳定性、排障和长期会话体验更新。

#### 2.1 codex doctor：出问题先自检
...

#### 2.2 Resume flows：接着干不容易接歪
...

## 2. 日期不确定但值得看

### 4. Cursor Shared Canvases + /loop（date_uncertain）

#### 4.1 Shared Canvases：分享 agent 产物，而不是聊天过程
...

#### 4.2 /loop：本地长运行 agent
...

## 3. 无近期更新 / 暂不可读

1. Gemini CLI：官方 changelog 最新可见为 ...，本窗口无新内容。
2. Antigravity：页面当前只能抽到标题，无法判断更新。
```

## Writing Rules

- Use Chinese interpretation first; English feature names can remain when they are product names or commands.
- Use explicit numbering for sections, tools, subtopics, and final summary; avoid unnumbered long blocks.
- Every important bullet should answer “它是什么 / 解决什么痛点 / 现在怎么变 / 对用户或 agent workflow 意味着什么”.
- Group raw bullets into themes; do not translate every upstream bullet one by one.
- For large changelogs, pick the most important 4-7 themes, then deeply explain the top 2-4.
- Include “我的判断” for each important tool.
- Avoid shallow one-liners for major features such as dynamic workflows, background agents, resume flows, permission profiles, MCP/plugin/runtime changes, commands/settings, or new model modes.
- When mentioning a command/config/env var such as `/effort xhigh`, `/workflows`, `OPENCODE_EXPERIMENTAL_WEBSOCKETS=true`, or `defaultEnabled: false`, explain where it is used and what knob it changes.
- Keep old/out-of-window/unreadable sections short.
- If output is for Telegram, avoid huge markdown tables.

## Quality Checklist Before Sending

Before final output, verify:

- Did I include all important updated tools, especially Claude Code/Codex/OpenCode?
- Did I join version content with release date when sources split them?
- Did I include GitHub Releases for Codex and Claude Code?
- Did I explain what changes mean in Chinese, not just list keywords?
- Did the top changes include mechanism + pain point + usage impact, not just a one-line translation?
- Did every important section/subtopic have visible numbering such as 1, 1.1, 1.2?
- Did every important command/config/env var explain what it is, where to use it, when to use it, and its tradeoff?
- Did I avoid burying useful updates under `found_but_out_of_window`?
- Did I keep uncertain items visible but clearly labeled?
- Did I keep no-update/unreadable items short?

## Failure Policy

- If one source fails, continue.
- If an official source is unreadable, say so briefly and use official fallback if available.
- Never invent dates or certainty.
- Prefer recall for substantive latest updates, but label uncertainty.
