# Backend Regression Maintenance 中文审阅版

> 这是 `SKILL.md` 的中文审阅译文，方便 PR review。正式 skill 入口仍然是英文 `SKILL.md`。

## 目标

把已验证过的后端场景转成可复用的回归资产，用来保护未来发布，且适用于任意项目。

这是 AI Coding 五层模型下的 Layer 4 回归治理 skill。它不重新执行后端验证，也不从头重新分类原始前端用例。它消费后端验证报告、proposed regression cases、已有回归文件和项目约定，用来维护长期后端回归套件。

## 和 `five-layer-classifier` 的关系

这个 skill 必须能单独使用。`five-layer-classifier` 是可选的治理辅助，不是必需前置步骤。

单独使用时，按照项目现有 testcase、test、release 和 CI 约定维护回归资产。如果目标位置明显，就继续并记录假设边界；如果目标位置不明显，仍然产出 case decisions 和 pre-release run list，但把文件写回标记为 `NEEDS_REVIEW`，不要写错地方。

当资产责任、正式真源状态、承载边界、public/private 建议、split/downgrade/local-retention 动作会影响结果时，由 `five-layer-classifier` 判断。本 skill 消费这些判断来维护回归资产，但不替代五层分类，也不能自己发明层级边界。

当以下问题不清楚，并且答案会影响写回、public/private history、正式 truth-source 状态或 split/merge 决策时，编辑回归文件前应使用 `five-layer-classifier`：

1. 后端回归用例在这个项目里应该放在哪里
2. 某项内容是 executable implementation test、project release convention、shared governance rule、temporary local evidence，还是 research
3. proposed case 是否混合了 implementation reality 和 governance policy，是否应该拆分
4. run log、scratch SQL query 或一次性验证 note 是否只是 Layer 5 本地证据
5. public/private policy 是否允许产物进入 public history

分类结果控制写回：

1. executable tests、fixtures、mocks、schemas 这类表达当前实现现实的内容，通常属于 Layer 2
2. 项目特定默认测试布局、release checklist 位置、CI wiring，通常属于 Layer 3
3. shared regression policy、priority rules、release-gate governance，属于 Layer 4
4. one-off run logs、scratch SQL、temporary evidence、本地 notes，属于 Layer 5，除非被明确提升

如果 proposed regression case 混合了实现事实和共享治理，建议拆分，而不是强行放进一个文件。

如果没有分类结果，但写回边界从项目约定看很明显，就继续并记录假设 layer 或 boundary。如果边界不明显，不要丢掉回归维护工作：输出 case decisions 和 run list，然后把文件写回标记为 `NEEDS_REVIEW`，不要写错地方。

## 输入

使用可用材料，例如：

1. 后端验证报告
2. proposed regression cases
3. 需要 traceability 时的原始需求和技术方案
4. 已有 backend regression index 或 testcase 文件
5. 已有自动化测试文件和命名约定
6. release 或 CI 文档
7. 可用时的五层分类或项目写回政策

如果缺少 proposed cases，只能从验证报告推导。如果报告缺少后端证据，把 case 标记为 `NEEDS_REVIEW`，不要编造稳定回归用例。

## 回归用例准入条件

后端回归用例必须至少有一个后端可观察断言：

- API/RPC/CLI response contract
- 数据库或持久化状态检查
- cache、queue、outbox、search index、file、webhook、email、notification 或 worker effect
- log、trace、audit 或 event 证据
- 幂等、一致性、并发、权限、隔离、状态机或 migration 断言

如果 case 只涉及前端布局、动画、视觉样式、浏览器渲染或 toast 位置，而且没有后端事实，就拒绝或标记为 `Manual`。

## 维护流程

1. 阅读 verification report 和 proposed regression cases
2. 编辑前发现项目已有 regression/testcase 组织方式
3. 将 proposed cases 与现有 cases 对比，避免重复
4. add、update、merge、reject 或标记需要审阅
5. 分配优先级：P0、P1、P2 或 Manual
6. 保留到需求、源测试用例、PR、issue 或 verification report 的 traceability
7. 更新项目使用的 regression index 或模块文件
8. 产出 pre-release run list

如果项目已有测试用例目录结构，不要引入新的 testcase 目录结构。除非用户要求新结构，否则跟随项目已有组织方式。

不要把 Layer 5 临时证据放进正式 regression suite。只有具备清晰后端可观察断言和可追溯来源的稳定 case 才能提升。

## 优先级规则

### P0 — 每次发布都跑

P0 用于每次发布前都必须跑的后端用例：

- login、auth、permission、tenant isolation 或 ownership boundary
- 核心 money、coupon、reward、order、inventory、balance 或数据写入链路
- duplicate submit/callback/retry 可能造成损失或数据损坏的幂等路径
- 失败会破坏核心数据的数据一致性不变量
- 历史上脆弱的关键路径

P0 失败会阻断 pre-release PASS 判断。

### P1 — 相关模块变更时跑

P1 用于重要的模块级行为。当相关模块、数据模型、API、worker、queue、cache 或依赖变化时要跑。

### P2 — 周期性或大版本回归

P2 用于低频、边缘、兼容、migration、export、backfill 或成本较高的 case。大版本或周期性回归时跑。

### Manual — 已文档化但未自动化

Manual 用于需要人工确认、不可用第三方系统、真实外部回调、不稳定测试数据，或无法安全复现环境的 case。

Manual case 仍然要出现在 release checklist 中，不能静默丢掉。

## Case 记录字段

保持项目已有格式。如果没有格式，使用简洁记录：

```text
ID:
Title:
Module:
Priority: P0 | P1 | P2 | Manual
Source:
Backend assertions:
Inputs / fixtures:
Expected response:
Expected state:
Consistency / idempotency / concurrency checks:
Logs / side effects:
Automation status: automated | manual-command | manual | pending
Cleanup:
```

## 发布前运行清单

生成实用 run list，而不是简单说“全部跑”：

1. 所有 P0 cases
2. 变更模块相关的 P1 cases
3. schema、backfill 或 persistence 变更时的 migration/data-integrity cases
4. 相关基础设施变更时的 async/queue/outbox/cache cases
5. 大版本或高风险变更相关的 P2 cases
6. 仍需人工验证的 Manual cases

只有所需 P0 cases 通过且所需证据可用时，才报告 **PASS**。

如果仍有 manual cases、不可用环境或未执行的 required cases，报告 **PARTIAL**。

如果任何 required P0 case 失败，或回归 case 暴露错误行为，报告 **FAIL**。

## 报告格式

使用以下结构：

```text
Backend Regression Maintenance Report

Result: UPDATED | NO_CHANGE | NEEDS_REVIEW

1. Inputs
   - Verification report:
   - Existing regression files:
   - Project conventions:
   - Five-layer/writeback policy:

2. Case Decisions
   - Proposed case:
   - Decision: add | update | merge | duplicate | reject | manual | needs_review
   - Priority:
   - Reason:
   - Target file:
   - Layer / boundary:

3. Files Updated
   - ...

4. Regression Index Summary
   - P0:
   - P1:
   - P2:
   - Manual:

5. Pre-Release Run List
   - P0 all-release cases:
   - P1 changed-module cases:
   - Required migration/data/async cases:
   - Manual checks:

6. Skipped or Rejected
   - Reason:

7. Follow-ups
   - Cases needing automation:
   - Missing environment/docs:
```
