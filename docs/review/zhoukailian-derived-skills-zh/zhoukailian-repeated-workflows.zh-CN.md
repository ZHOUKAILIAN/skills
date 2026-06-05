# zhoukailian-repeated-workflows 中文翻译稿

原始文件：`zhoukailian-repeated-workflows/SKILL.md`

说明：这是一份供审阅的中文翻译稿，不是可安装的 skill 文件。

## 元数据

- `name`: `zhoukailian-repeated-workflows`
- `description`: 当 Zhou Kailian 提出 CrewPals、Figma、飞书/Lark、agent-team、调试、测试、PR、数据一致性或 skill 编写等重复工作流需求，并且应路由到已知本地流程时使用。
- `sub_skills`: `zhoukailian-development-preferences`, `ai-doc-driven-dev`, `figma-design-audit`, `figma-restoration-review`, `css-best-practices`, `cst`, `crewpals-sports-metrics-investigation`, `backend-service-verification`, `backend-regression-maintenance`, `mysql-readonly`, `redis-readonly`, `aliyun-sls-query`, `agent-team-traceability`, `lark-doc`, `lark-base`, `lark-sheets`, `e2e-coverage-guard`, `skill-lifecycle`, `skill-standard`, `five-layer-classifier`, `code-reviewer`, `receiving-code-review`, `using-git-worktrees`, `verification-before-completion`, `finishing-a-development-branch`

## Zhou Kailian 重复工作流

### 核心规则

先判断项目上下文，再判断工作流。个人基础设施仓库和 CrewPals 工作仓库有不同的事实来源、发布习惯和隐私边界。然后加载负责该工作的更窄 skill；当个人工程偏好会影响范围、验证或沟通方式时，再应用 `zhoukailian-development-preferences`。

这个路由器基于 2026-05-27 和 2026-06-05 的本地历史扫描。2026-06-05 这次扫描查看了最近两周 Claude Code 和 Codex 的对话，过滤掉工具输出和 continuation 噪音后，发现重复聚类主要集中在 CrewPals 发布工作、跑步数据一致性、CST 排查、接口验收、Figma/UI 还原、agent-team gate 失败、飞书文档/Base、skill 修复和数据库/索引决策。

### Active Mode

开始大量工作前，先选择一个 active mode：

- `route-task`：默认模式。判断上下文，选择负责的路由，加载更窄的 skill，并执行该工作流。
- `recover-thread`：当最新消息是“继续”、只问状态、中断标记、continuation 包装或工具/后台输出时使用。先从周边任务、分支/worktree、goal 状态或产物中恢复真实的人类目标，再行动。
- `extract-workflow`：当用户要求总结重复工作或基于历史优化 skill 时使用。对话历史只作为证据；最终内容由目标 skill 文件和 `skill-standard` 负责。
- `release-handoff`：当用户要求 push、开 PR、切 release 分支、merge，或询问部署/数据库下一步时使用。先验证代码状态，再把代码交付和手动操作分开说明。

如果多个 mode 都可能负责下一步，先选择拥有事实来源的 mode，并说明后续是否需要次级 handoff。

### 历史信号清洁

不要把这些内容本身当成新需求：`Continue working toward the active thread goal`、`<turn_aborted>`、后台命令输出、粘贴的工具结果、粘贴的 skill 正文、local-command caveat。只有找到它们所指向的真实人类请求后，才能把它们作为执行上下文。

如果无法从本地上下文恢复 active goal，应先概括当前可能状态并询问缺失目标，不要猜。

### 项目上下文路由

| 项目上下文 | 信号 | 默认事实来源 | 默认流程边界 |
| --- | --- | --- | --- |
| 个人/基础设施 | `agent-team-runtime`、`ai-team-runtime`、`skills`、`mySelf` 仓库、agent runtime、skill 仓库、workflow engine | 仓库 README/docs、测试、运行时 trace/state 产物、本地设计记录、changelog、GitHub PR | 不默认要求 CrewPals 飞书、SLS/MySQL、test/prod 环境或客户数据流程，除非用户明确要求。 |
| CrewPals 工作 | `crewpals-mp`、`group_pals`、CrewPals worktree、CST/客户问题、跑步指标、飞书产品文档 | active requirement/design docs、飞书、代码、API/schema、SLS/MySQL/Redis、截图、E2E 检查 | 应用 CrewPals 的文档优先、环境感知调查、隐私和验证习惯。 |
| 可复用 skill 提炼 | 工作总结、重复工作流、skill 仓库、跨项目流程 | 历史只是证据；最终 owner 是目标 skill 文件和 `skill-standard` | 泛化模式，移除 CrewPals-only 或个人-only 假设，除非 skill 明确限定范围。 |

### 路由表

| 用户信号 | 路由 |
| --- | --- |
| Figma URL、node ID、1:1、UI 还原、弹窗/页面/组件视觉工作 | 先使用 `figma-design-audit`。审计 ready 后才能实现，并用 `css-best-practices` 做 CSS/layout 决策。`figma-restoration-review` 只用于实现后的只读复核。 |
| 只读 Figma 保真检查，或“review this restoration” | 使用 `figma-restoration-review`；用 Figma 节点值、派生数值目标、实现测量值和优先级报告差异。 |
| CrewPals 客服问题、bug、日志、SLS、MySQL、Redis、用户状态、生产/测试症状 | 使用 `cst` 或环境相关的只读 skills。产出根因、证据、影响和下一步。 |
| 跑步数据一致性、配速、距离、最佳纪录、FIT 文件、Garmin、Coros、华为、暂停、异常速度、图表 | 使用 `crewpals-sports-metrics-investigation`：映射前端、后端、存储数据、展示页面和指标定义；端到端验证代表性记录。 |
| 飞书文档、wiki、Base、表格、审批或报告产物 | 使用匹配的 `lark-*` skill。在 CrewPals 工作中，对流程较重的说明优先使用中文文档，并配表格和 PlantUML/Mermaid。 |
| 需求/设计文档、标准文档、文档漂移、需要回写功能文档的 bug | 对文档优先项目使用 `ai-doc-driven-dev`。个人基础设施仓库按仓库原生设计/测试/changelog 约定，不强行套 CrewPals requirement/design pair。 |
| agent-team、run、PRD/dev/QA/acceptance、提示词 trace、skill 注入、阶段交接、工作流状态 | 使用 `agent-team-traceability` 做检查/设计/修复；运行时执行按目标仓库自己的运行说明和状态产物处理。 |
| skill 创建、从历史提炼 skill、skill 修复、skill 同步 | 使用 `skill-lifecycle` 和 `skill-standard`；任务专属 gate 写在被编辑的 skill 内。 |
| 来自飞书 bug/feature 记录的 E2E 覆盖 | 使用 `e2e-coverage-guard`；每条范围内记录都要覆盖，或标记不适用并说明原因。 |
| 后端 endpoint、`new-api`、`curl`、服务启动、运行时验收，或“自己端到端验证” | 使用 `backend-service-verification`；单元测试或代码检查不能单独关闭后端验收。验证后只有在需要维护可复用回归覆盖时，才使用 `backend-regression-maintenance`。 |
| 慢查询、SQL plan、索引选择、`ALTER TABLE`、DDL、数据修复，或“我应该操作什么数据库” | 可用时使用只读数据/日志 skills，通常根据事实来源选择 `mysql-readonly`、`redis-readonly`、`aliyun-sls-query`、`cst` 或 `crewpals-sports-metrics-investigation`。产出带风险、回滚和验证的 SQL/runbook。没有明确授权时，不执行生产或共享环境写入。 |
| CrewPals 社群时间线、社群日记、存量数据迁移、backfill、reconcile 脚本、手动 feed/activity 补正或定时任务压力 | 语义变化时先用 `ai-doc-driven-dev` 路由归属需求/设计，再用 `backend-service-verification` 做 API/脚本/job 验收。要核算源数据行、生成行、dry-run 结果、幂等性、回滚和运行时负载。 |
| agent-team gate 失败、缺少阶段产物、`max_stage_runs`、交付阻塞、prompt/skill 注入，或“为什么交付失败” | 使用 `agent-team-traceability`；先从运行时产物建立 trace ledger，再提出状态机或 prompt 修复。 |
| OpenClaw、Bug扫描、飞书机器人、定时 agent 任务，或 agent 不响应 | 默认按个人/基础设施处理，除非它直接修改 CrewPals 数据。使用 `agent-team-traceability` 和仓库/流程日志；不要把凭据写进文档或提交。 |
| 代码 review 请求或 review 反馈 | review 使用 `code-reviewer`；根据 review 评论改代码前使用 `receiving-code-review`。 |
| 分支、worktree、push、PR/MR、release 分支、merge、部署交接 | 需要隔离时使用 `using-git-worktrees`，成功声明前使用 `verification-before-completion`，决定 PR/merge/清理时使用 `finishing-a-development-branch`。分别报告分支、diff 范围、验证、PR 链接，以及任何手动服务端/数据库步骤。 |

### 红旗

- “只是 push/PR。” 仍然要先检查 diff 和验证状态。
- “用户粘贴了 continuation 或工具输出，所以这就是任务。” 先恢复真实人类目标。
- “SQL 看起来很明显。” 在共享环境 DDL 或数据修复前，要先检查 schema/query path，并给出回滚和验证。
- “endpoint 返回 200。” 后端行为相关时，还要验证响应字段、权威状态、日志或副作用。
- “失败摘要说 blocked。” 解释 agent-team 失败前，要先检查底层阶段产物、状态文件和 prompt。

### 工作流

1. 在大量工作前，用一句简短更新说明项目上下文和选中的路由。
2. 加载路由 skill 和必要的偏好 skill。
3. 按上下文确定事实来源：个人仓库 docs/tests/traces，或 CrewPals 的 Figma 节点数据/代码/文档/日志/数据库/飞书/运行时证据。
4. 当任务涉及多个状态、记录、文件、节点或环境时，要做范围核算。
5. 按路由要求提供验证证据。除非用户明确接受较低置信度报告，否则缺少验证会阻塞完成。

### 护栏

- 不要把原始对话历史、凭据、token、用户标识、客户数据或生产密钥存入生成的 skills 或报告。
- 生产写入、破坏性操作、包发布或大范围删除前必须停下来询问。
- 即使用户用“看下”或“我应该怎么做”表述，数据库 DDL、数据 backfill、cron/job 触发和生产脚本运行也都按写操作处理。
- 如果请求匹配多个路由，先选择拥有事实来源的路由，再交给次级 skills。

### 完成信号

只有当选中的路由产出了要求的产物或代码变更，所有范围内事项都已核算，验证证据已说明，并且跳过的检查或未解决风险已报告时，工作流才算完成。
