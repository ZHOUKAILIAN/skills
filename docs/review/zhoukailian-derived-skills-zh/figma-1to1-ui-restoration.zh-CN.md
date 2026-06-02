# figma-1to1-ui-restoration 中文翻译稿

原始文件：`figma-1to1-ui-restoration/SKILL.md`

说明：这是一份供审阅的中文翻译稿，不是可安装的 skill 文件。实际生效文件仍是英文 `SKILL.md`。

## 元数据

- `name`: `figma-1to1-ui-restoration`
- `description`: 当用户提供 Figma URL、fileKey 或 node-id，并希望对组件、弹窗、页面或局部模块做精确 1:1 UI 实现或还原时使用。
- `sub_skills`: `figma-design-audit`, `css-best-practices`, `figma-restoration-review`

## 核心规则

这个 skill 是没有外部 runtime 控制 workflow 时，单个 assistant session 内精确 Figma-to-code 还原的协调入口。它不拥有详细的 Figma 审计规则、CSS 实现规则或最终只读复核规则。它负责把任务路由给正确 owner，并且在上一阶段没有产出可验证证据时阻止进入下一阶段。

用户意图决定顶层目标，但阶段 owner 固定：`figma-design-audit` 拥有 Figma 事实，`css-best-practices` 拥有实现策略，`figma-restoration-review` 拥有只读验收复核。本 skill 只在当前 assistant session 内排序这些阶段，并在缺少必需证据时阻止 handoff。

## 活动模式

只有当用户要做实现或还原时使用本 skill，而不是只读 review。

如果用户只是要求编码前检查 Figma，使用 `figma-design-audit`。如果用户只是要求对比既有实现和 Figma，使用 `figma-restoration-review`。

如果已有外部 workflow runtime 控制 stage 和 gate，不要让这个 skill 覆盖 runtime。应按 runtime 的 stage contract 执行，并在对应阶段注入 owner skills。

## 工作流

1. 先用 `figma-design-audit` 执行 Figma 事实收集阶段。
2. 在 Figma 审计标记 `Ready for implementation: yes` 且没有未解决 Blocking Questions 之前，不写应用代码。
3. 实现阶段使用 `css-best-practices`，把已审计 Figma 值当作测量证据，把项目代码库当作实现上下文。
4. 除非 PRD、API/schema、既有事实来源或用户明确回答改变业务规则，否则保留产品已有业务逻辑。
5. 实现存在后，当用户要求 review、任务需要保真签收或视觉风险较高时，用 `figma-restoration-review` 做只读数值验收复核。

## Handoff Gate

### 审计到实现

从 `figma-design-audit` 交给 `css-best-practices` 之前，必须满足：

- 每个范围内可见节点都有 terminal-depth 覆盖或有理由排除。
- 每个可见节点已分类为 `renderable-ui`、`platform-native`、`interaction-proxy` 或 `annotation-demo-only`。
- 几何值由 Figma 节点数据推导，并包含命名参考节点和闭环检查。
- 影响业务的 Figma 样例已映射到来源或用户答案。
- Blocking Questions 为空或已明确回答。
- 有持久审计产物时，audit verifier 已通过。

如果审计是 `not ready`，继续停留在审计阶段，或询问 `figma-design-audit` 产出的成组 blocking questions。

### 实现到复核

只有相关源码已经修改且可运行或可检查时，才从实现阶段交给 `figma-restoration-review`。review skill 是只读的，只报告 deviation，不改代码。

## Owner 边界

| 范围 | Owner skill |
| --- | --- |
| Figma 节点遍历、可见节点分类、测量证据、状态样例、阻塞问题 | `figma-design-audit` |
| CSS/layout/styling 实现策略、单位转换、flow vs absolute、可维护性 | `css-best-practices` |
| 实现后的保真复核和 deviation checklist | `figma-restoration-review` |
| 本 skill | 阶段顺序、handoff gate、最终证明包 |

## Red Flags

- “可以靠截图还原 UI” -> 回到 `figma-design-audit`；当前流程要求 Figma node values 和数值几何对齐。
- “Figma 审计还有 blocker，但答案大概率很明显” -> 先从来源解决，或实现前询问成组问题。
- “Figma x/y 意味着每个节点都应该 absolute” -> 使用 `css-best-practices`；Figma 坐标是测量证据，不是 CSS 策略。
- “review 发现 deviation，所以在 review skill 里修” -> 切回实现模式；`figma-restoration-review` 是只读。

## 完成信号

只有满足这些条件，协调式还原才算完成：

- Figma 审计阶段完成，或 blocker 状态已明确报告。
- 如要求实现，代码变更遵循 `css-best-practices` 并保留业务来源决策。
- 用户要求或高风险保真任务已运行 `figma-restoration-review`，或说明跳过原因。
- 最终回复报告审计产物、实现变更文件、验证命令/结果、未解决 blocker，以及已运行的 review 结果。
