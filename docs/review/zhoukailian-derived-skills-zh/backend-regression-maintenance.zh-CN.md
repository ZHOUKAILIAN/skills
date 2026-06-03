# backend-regression-maintenance 中文审阅稿

## 目标

把已验证的后端场景沉淀成可复用回归覆盖，保护后续发布。

这个 skill 消费后端验证报告、evidence ledger、proposed regression cases、已有回归文件和项目约定。它不重新执行后端验证，也不从头重新分类原始前端用例。

## 核心规则

没有后端证据，不允许沉淀回归用例。

每个 proposed case 都必须有 decision ledger 行，追溯到验证证据，写明后端可观察断言、去重结果、优先级理由、写回目标或写回阻塞原因。

错误：

```text
这个前端用例很重要，所以加入后端回归。
```

正确：

```text
验证证据证明重复领取优惠券只生成一条 claim 和一张 user coupon。将其作为 P0 幂等回归用例加入已有 coupon service 测试文件。
```

## 使用场景

当后端验证已经产出报告、evidence ledger、proposed regression cases，或发现可能需要长期保护的后端失败时使用。

用于按项目已有约定更新回归索引、测试用例文件、自动化测试、release checklist 或 pre-release run list。

## 不使用场景

不要用它证明当前后端改动正确；应先使用 `backend-service-verification`。

不要把前端布局、动画、toast 位置、浏览器渲染用例复制进后端回归，除非存在后端可观察断言。

## 事实来源

优先使用项目本地最强事实：

- 后端验证报告和 evidence ledger
- proposed regression cases
- 需要追溯时的原始需求、技术方案、PR、issue 或 source test case
- 已有 backend regression index、testcase 文件、自动化测试、fixture、mock、命名约定
- release、CI、preflight 或 pre-release checklist 文档
- 可用时的项目 owner 或写回政策

如果缺少 proposed cases，只能从验证报告推导候选。如果报告缺少后端证据，把候选标为 `NEEDS_REVIEW`，不要编造稳定回归用例。

## 可选治理上下文

这个 skill 必须能在没有 AI Coding 五层模型的情况下独立工作。

如果 five-layer classifier 或等价治理来源可用，并且 owner、truth-source 状态、写回位置、split/merge 决策、public/private history 会改变回归资产写入位置，就把该治理来源作为输入读取。不要在本 skill 里复制或重写五层模型，也不要要求用户必须安装五层。

如果治理来源不可用，遵循项目已有 testcase、test、release 和 CI 约定。目标位置明显时继续并记录假设；目标位置不明显时，输出 case decisions 和 run list，把文件写回标记为 `NEEDS_REVIEW`。

不要因为治理分类不可用就丢掉回归决策。只阻塞不安全的写回。

## 模式和降级规则

执行前先选择一个 active mode：

- `maintain-assets`：项目已有明显 regression/test/checklist 位置，或用户已选择写回目标时使用。更新目标资产并验证维护结果。
- `decision-only`：写回 owner、目标位置或格式不清楚时使用。产出候选决策和 pre-release run list，但文件写回标记为 `NEEDS_REVIEW`。
- `review-only`：用户只要求审查 proposed regression coverage 时使用。不编辑文件，只报告决策、缺口和建议写回目标。

降级规则：

- evidence ledger 不可用时，只能从验证报告中有名称的后端证据推导候选；弱证据候选标记为 `NEEDS_REVIEW`。
- 项目没有现有 regression 格式时，使用本 skill 的简洁 case record，除非用户要求其他格式。
- 机械验证不能运行时，报告人工检查证据和跳过检查的影响。

## 回归用例资格

后端回归用例至少要有一个后端可观察断言：

- API/RPC/CLI response contract
- 数据库或持久化状态检查
- cache、queue、outbox、搜索索引、文件、webhook、email、notification 或 worker effect
- log、trace、audit 或 event 证据
- 幂等、一致性、并发、权限、隔离、状态机、migration 或兼容性断言

只有前端布局、动画、视觉样式、浏览器渲染或 toast 位置，且没有后端事实时，拒绝或标记为 `Manual`。

临时运行日志、scratch SQL、本地证据可以支撑候选判断，但它们本身不是稳定回归用例。

## 工作流

### 1. 输入证据门禁

修改回归资产前，必须读取并核算：

1. 后端验证报告
2. execution evidence ledger
3. proposed regression cases
4. 已有 regression/testcase 文件
5. 已有自动化测试、fixture、mock、命名约定
6. release、CI 或 pre-release run 文档
7. 可用时的 owner 或写回政策

反偷懒门禁：验证报告或 evidence ledger 可用时，不能只根据摘要继续。如果没有 evidence ledger，从报告推导出的每个候选都先标为 `NEEDS_REVIEW`，直到找到后端证据。

### 2. 候选核算门禁

每个 proposed case 和每个值得考虑沉淀的后端失败，都要创建 decision ledger 行。

必填字段：

```text
Candidate ID:
Source verification item or failure:
Evidence summary:
Backend-observable assertion:
Eligibility: eligible | manual | reject | needs_review
Decision: add | update | merge | duplicate | reject | manual | needs_review
Reason:
```

反偷懒门禁：候选必须零遗漏。不能把多个 proposed cases 合并成一句“已有回归覆盖”，除非每个候选都有自己的 decision row。

### 3. 去重门禁

把每个 eligible candidate 和已有回归用例、自动化测试比较。

按行为和权威断言去重，不只按标题。检查：

1. API/RPC/CLI 契约
2. 状态或持久化数据断言
3. 不变量、幂等、并发、权限、状态、异步或 migration 断言
4. fixture/setup 重叠
5. 既有测试失败模式或历史 bug 链接

反偷懒门禁：每个 `duplicate` 或 `merge` 决策必须写出现有文件、测试、case ID 或 checklist item。如果无法命名目标，决策就是 `needs_review`，不是 `duplicate`。

### 4. 优先级门禁

每个非 rejected candidate 都要分配 `P0`、`P1`、`P2` 或 `Manual`。

`P0` 用于每次发布前都必须跑的场景：

- login、auth、permission、tenant isolation 或 ownership boundary
- 核心 money、coupon、reward、order、inventory、balance 或数据写入链路
- duplicate submit/callback/retry 可能造成损失或数据损坏的幂等路径
- 失败会破坏核心数据的数据一致性不变量
- 历史上脆弱的关键路径

`P1` 用于相关模块、数据模型、API、worker、queue、cache 或依赖变化时应运行的重要模块行为。

`P2` 用于低频、边界、兼容、migration、export、backfill 或昂贵场景，通常在大版本或计划回归中运行。

`Manual` 用于需要人工确认、不可用第三方系统、真实外部 callback、不稳定测试数据，或无法安全复现的环境。

反偷懒门禁：不能批量分配优先级。每个优先级都要有业务风险、数据风险、发布风险、历史脆弱性或执行成本理由。

### 5. 写回门禁

保持项目已有格式和位置。项目已有 testcase 目录结构时，不要新建另一套结构。

每个 accepted candidate 都要记录：

```text
Target file or asset:
Change type: add | update | merge | checklist-only | manual-only
Writeback boundary: existing convention | user decision | needs_review
Automation status: automated | manual-command | manual | pending
```

如果项目没有格式，使用简洁记录：

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

反偷懒门禁：不要把临时证据写进正式 regression suite。只提升有稳定后端断言和可追溯来源的场景。

### 6. 上线前运行清单门禁

生成可执行 run list，不要只说“run everything”：

1. 所有 P0 cases
2. 变更模块相关 P1 cases
3. schema、backfill、persistence 变化时的 migration/data-integrity cases
4. 相关基础设施变化时的 async/queue/outbox/cache cases
5. 大版本或高风险变更相关 P2 cases
6. 仍需人工验证的 Manual cases

反偷懒门禁：每个 `P0` 和每个 `Manual` 都必须出现在 run list，或说明当前发布为什么不可运行。P1/P2 纳入时必须写明变更模块或发布条件。

### 7. 维护验证门禁

编辑文件或产出 run list 后，验证维护结果。

检查：

1. 每个 candidate 都有一个 decision row
2. 每个非 rejected case 都有优先级和可追溯证据
3. 新增或修改的 ID 在目标范围内唯一
4. accepted P0 和 Manual cases 已进入 pre-release run list
5. 目标文件符合项目已有格式和命名约定
6. 可用的 formatter、linter、test、validator 或 index check 已运行

反偷懒门禁：写入成功不等于维护完成。index、生成清单或目标测试文件无法机械验证时，报告人工检查证据和剩余风险。

## 完成标准

只有当目标文件或 run list 已按预期更新、所有候选决策已核算、维护验证通过或跳过检查已说明时，报告 **UPDATED**。

只有当所有候选都是 duplicate、rejected、manual-only 或 already covered，并且每个决策都命名已有覆盖或拒绝原因时，报告 **NO_CHANGE**。

当写回目标、证据、去重、优先级或 owner 不足以安全更新时，报告 **NEEDS_REVIEW**。

对于 pre-release 判断：

- 只有所需 P0 cases 通过且证据可用时，报告 **PASS**。
- 如果仍有 manual cases、不可用环境或未执行的 required cases，报告 **PARTIAL**。
- 如果任何 required P0 case 失败，或回归 case 暴露错误行为，报告 **FAIL**。

## 门禁失败处理

当某个门禁不完整时，先补齐缺失的 decision row、去重证据、优先级理由、run-list 条目或维护检查。

如果缺失项无法安全解决，不要把 `UPDATED` 或 `NO_CHANGE` 当作维护完成来报告。把受影响候选或写回目标标记为 `NEEDS_REVIEW`，并在报告中写出 blocker。

不要把缺失证据或未命名的 duplicate coverage 降级成小 follow-up。没有证据、优先级理由或命名 duplicate target 的候选仍然未解决。

## 报告格式

```text
Backend Regression Maintenance Report

Result: UPDATED | NO_CHANGE | NEEDS_REVIEW

1. Inputs
   - Verification report:
   - Evidence ledger:
   - Existing regression files:
   - Project conventions:
   - Writeback policy:

2. Candidate Decision Ledger
   - Candidate ID:
   - Evidence summary:
   - Backend assertion:
   - Eligibility:
   - Decision:
   - Priority:
   - Reason:
   - Target file:

3. Deduplication Results
   - Candidate ID:
   - Existing coverage:
   - Decision:

4. Files Updated
   - File:
   - Change:
   - Verification:

5. Regression Index Summary
   - P0:
   - P1:
   - P2:
   - Manual:

6. Pre-Release Run List
   - P0 all-release cases:
   - P1 changed-module cases:
   - Required migration/data/async cases:
   - Relevant P2 cases:
   - Manual checks:

7. Skipped, Rejected, or Needs Review
   - Candidate:
   - Reason:
   - Required next decision:

8. Maintenance Verification
   - Checks run:
   - Result:
   - Skipped checks and reason:
```

## Proof Package

最终回复必须包含：

- 已检查的输入证据，包括 evidence ledger 是否可用
- candidate 数量和 decision 数量，包括 `add`、`update`、`merge`、`duplicate`、`reject`、`manual`、`needs_review`
- 每个 duplicate 或 merge 决策的去重证据
- P0、P1、P2、Manual 优先级汇总
- 已修改的文件或 run-list 产物，或写回阻塞原因
- 已运行的维护验证检查及结果
- 跳过或无法执行的检查、原因和影响
- 最终 `UPDATED`、`NO_CHANGE` 或 `NEEDS_REVIEW` 结果

## 安全边界

不要把 secret、私有用户标识、生产连接串、原始 token 或客户数据写进 regression cases、报告、提交或 run list。

不要新增会修改生产或共享环境的测试。只有不安全数据可用时，把 case 标为 `Manual` 或 `NEEDS_REVIEW`。
