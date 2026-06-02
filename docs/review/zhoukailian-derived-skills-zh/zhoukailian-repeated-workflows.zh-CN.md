# zhoukailian-repeated-workflows 中文翻译稿

原始文件：`zhoukailian-repeated-workflows/SKILL.md`

说明：这是一份供审阅的中文翻译稿，不是可安装的 skill 文件。

## 元数据

- `name`: `zhoukailian-repeated-workflows`
- `description`: 当 Zhou Kailian 提出 CrewPals、Figma、飞书/Lark、agent-team、调试、测试、PR、数据一致性或 skill 编写等重复工作流需求，并且应路由到已知本地流程时使用。
- `sub_skills`: `zhoukailian-development-preferences`, `ai-doc-driven-dev`, `figma-design-audit`, `figma-restoration-review`, `css-best-practices`, `cst`, `crewpals-sports-metrics-investigation`, `agent-team-traceability`, `lark-doc`, `lark-base`, `lark-sheets`, `e2e-coverage-guard`, `skill-lifecycle`, `skill-standard`, `five-layer-classifier`, `code-reviewer`, `receiving-code-review`

## Zhou Kailian 重复工作流

### 核心规则

先判断项目上下文，再判断工作流。个人基础设施仓库和 CrewPals 工作仓库有不同的事实来源、发布习惯和隐私边界。然后加载负责该工作的更窄 skill；当个人工程偏好会影响范围、验证或沟通方式时，再应用 `zhoukailian-development-preferences`。

这个路由器基于 2026-05-27 的本地 Codex 历史扫描：770 个 session 文件、6062 条真实用户消息，以及围绕 CrewPals 调试、Figma/UI 还原、飞书文档、agent-team 可追溯性、E2E 验证、PR 流程和跑步数据一致性的重复任务聚类。

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
| 代码 review 请求或 review 反馈 | review 使用 `code-reviewer`；根据 review 评论改代码前使用 `receiving-code-review`。 |
| 分支、worktree、push、PR/MR、发布交接 | 使用既有 git/worktree 实践；push/PR 前验证，并报告分支和检查结果。 |

### 工作流

1. 在大量工作前，用一句简短更新说明项目上下文和选中的路由。
2. 加载路由 skill 和必要的偏好 skill。
3. 按上下文确定事实来源：个人仓库 docs/tests/traces，或 CrewPals 的 Figma 节点数据/代码/文档/日志/数据库/飞书/运行时证据。
4. 当任务涉及多个状态、记录、文件、节点或环境时，要做范围核算。
5. 按路由要求提供验证证据。除非用户明确接受较低置信度报告，否则缺少验证会阻塞完成。

### 护栏

- 不要把原始对话历史、凭据、token、用户标识、客户数据或生产密钥存入生成的 skills 或报告。
- 生产写入、破坏性操作、包发布或大范围删除前必须停下来询问。
- 如果请求匹配多个路由，先选择拥有事实来源的路由，再交给次级 skills。

### 完成信号

只有当选中的路由产出了要求的产物或代码变更，所有范围内事项都已核算，验证证据已说明，并且跳过的检查或未解决风险已报告时，工作流才算完成。
