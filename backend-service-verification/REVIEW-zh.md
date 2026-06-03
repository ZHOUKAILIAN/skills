# Backend Service Verification 中文审阅版

> 这是 `SKILL.md` 的中文审阅译文，方便 PR review。正式 skill 入口仍然是英文 `SKILL.md`。

## 目标

证明一个后端改动是否真正完成：先从需求、技术方案、QA/前端/全链路测试用例中推导后端验证计划，再执行服务端检查，并输出可观察证据。

这个 skill 只做后端验证。它不验证前端布局、视觉样式、动画、浏览器渲染或 toast 位置；但会从这些用户可见断言中提取背后的后端事实。

## 原始测试用例只是输入，不是后端测试用例

用户给的 QA、前端或全链路测试用例只是输入材料，不能直接照抄成后端用例。

每条原始用例都要拆成：

1. 纯前端断言
2. 可由后端验证的事实
3. 全链路或人工断言
4. 推导出来的后端风险
5. 需要澄清的未知点

后端验证必须结合原始用例、需求、技术方案、API 契约、数据库模型、日志、队列、缓存和项目约定。

错误做法：

> 前端用例说点击保存后看到成功 toast，所以 API 返回 200 就算后端通过。

正确做法：

> 这个用例暗含一个创建操作。需要验证 response、权威数据库记录、审计/日志事件、重复提交行为，以及相关一致性不变量。

## 和 `five-layer-classifier` 的关系

这个 skill 必须能单独使用。`five-layer-classifier` 是可选的治理辅助，不是必需前置步骤。

单独使用时，继续做项目本地发现，产出验证计划/报告，并保守处理写回。对明显的目标位置使用项目已有约定；临时证据保留在本地；不确定的写回决策标记为 `needs classification` 或 `needs review`。

当资产责任、真源状态、仓库边界、写回位置会影响执行时，由 `five-layer-classifier` 决定这些问题。本 skill 消费这些决策来设计和执行后端验证，但不替代五层分类。

当以下问题不清楚，并且答案会影响写回位置、真源判断或是否进入共享历史时，应在本 skill 之前或执行中使用 `five-layer-classifier`：

1. 验证产物属于产品定义、实现现实、项目落地、共享治理、本地证据，还是研究材料
2. report、testcase、fixture、script、run log 应写入 product repo、control repo、本地 workspace，还是不写入
3. 临时验证结果是否允许成为正式 truth source
4. 混合职责产物是否应先拆分再写回
5. public/private history policy 是否影响目标位置

五层分类输出必须影响验证计划：

- Layer 1：定义目标产品语义和验收标准
- Layer 2：识别当前实现现实、可执行测试、schema、fixture 和 runtime behavior
- Layer 3：识别项目启动、打包、CI 和默认运行约定
- Layer 4：识别共享验证 gate、报告格式和发布规则
- Layer 5：识别只支持当前运行的本地证据，不能未经明确决策升级为正式资产

本 skill 是五层模型下的 Layer 4 验证治理 skill。不要把它当成某个项目的专用 runbook；它必须通过发现项目自己的验证约定来适配任意项目。

默认层级责任：

1. 需求和产品语义通常属于 Layer 1
2. 源码、测试、schema、fixture 和 runtime script 通常属于 Layer 2
3. 项目默认启动、打包和仓库结构通常属于 Layer 3
4. 共享验证政策、gate 和可复用验证报告属于 Layer 4
5. 临时运行日志、scratch query、本地 env note、一次性验证产物属于 Layer 5，除非被明确提升

写入验证计划、测试用例或报告前，要判断它是当前运行现实、共享验证治理，还是本地临时证据。如果边界可从项目约定明显判断，就继续并记录假设位置；如果边界模糊，不要阻塞验证，完成验证报告并把写回标记为 `needs classification`。

## 项目特定发现

每个项目都有自己的验证方式。设计或执行检查前要先发现。

查找项目本地来源，例如：

- README 或开发环境文档
- testing / verification 文档
- package scripts、Make targets、task runner 或 CI 配置
- 服务入口和配置样例
- 数据库 migration、schema、model 定义
- 现有测试和测试 fixture
- logging、tracing、queue、cache、worker 约定

使用发现到的项目约定。如果启动方式、测试数据、凭证或数据库访问不清楚，并且错误猜测会改变结果或触碰不安全数据，就停下来询问。

## 后端验证计划

执行前，先产出简洁计划，覆盖：

1. 后端范围和明确非范围
2. 原始测试用例拆解
3. 验证产物和临时证据的五层位置
4. 推导出来的后端验证用例
5. 服务启动和依赖就绪
6. 隔离测试数据和清理策略
7. 要执行的 API/RPC/CLI 调用
8. 数据库或持久化状态检查
9. 日志/trace 检查
10. 副作用：queue、outbox、cache、webhook、file、email、notification 或 worker 行为
11. 失败路径和边界场景
12. PASS/PARTIAL/FAIL 的完成标准

如果用户只要求计划，到计划为止，并标记尚未执行。

## 必须推导后端风险

即使原始测试用例没写，也要从需求和技术方案主动推导服务端风险。

检查变更是否涉及：

1. 幂等或重复执行
2. 数据一致性不变量
3. 并发或 race condition
4. 权限、角色、归属或租户隔离
5. 状态流转和终态
6. 事务、回滚或部分失败
7. 异步任务、队列、outbox、webhook、重试或 worker
8. cache 读写、失效或脏数据
9. 审计日志、业务日志、traceability 和敏感信息脱敏
10. migration、backfill、兼容或数据修复
11. quota、counter、balance、inventory、reward、coupon 等有限资源

每个适用风险都要添加验证项，或明确标记为 out of scope 并说明原因。

## 验证维度

### API 或服务行为

验证外部可观察的后端契约：状态码、response schema、error code、权限错误、校验错误，以及幂等 replay / 重复提交响应。

HTTP 200 或命令退出码本身不是正确性证据。

### 权威状态

不仅验证返回数据，还要验证权威持久化状态。

按项目不同，可能包括关系表、文档存储、cache key、文件、event/outbox 行、搜索索引记录或生成产物。

数据库检查只有在权威记录中观察到预期业务状态，并检查足够关联记录以证明行为时，才算完成。

### 一致性不变量

当计划或数据模型暗含总数、余额、计数、库存、奖励，或 `A = B + C` 这类公式时，要从权威数据验证不变量。

例子：

- 总额 = 明细之和 + 服务费 - 折扣
- 剩余库存 = 原库存 - 成功领取 + 退回
- 余额 = 初始余额 + 收入 - 支出
- 完成数不能大于总数
- 要求唯一时，一个业务实体只能有一个 active 状态

如果应检查的跨记录不变量没有验证，不要报告 PASS。

### 幂等性

如果操作可能重试、重复提交、收到重复回调，或使用 request id / idempotency key，要验证重复执行行为。

证据可包括：

1. 只有一条业务记录或一次预期状态流转
2. 没有重复副作用
3. 最终状态稳定
4. 符合预期的 duplicate/replay response
5. 设计中使用时有 idempotency key 或去重记录

### 并发

如果操作涉及有限资源、counter、balance、inventory、claim、lock、状态流转或唯一约束，要评估并发风险。

适用时，执行或设计并发验证，并检查最终权威状态，而不是只看单个请求响应。

证据应说明没有超卖、重复领取、重复扣款、负计数、非法状态、未处理死锁或 lost update。

### 权限和隔离

涉及用户、角色、组织或租户范围时，验证允许和拒绝访问。相关时包括跨租户或跨 owner 的读写。

### 状态机

如果功能有状态，要验证合法流转、非法流转、终态保护、重试行为，以及回滚或恢复预期。

### 异步和副作用

如果行为跨 queue、worker、outbox、webhook、email、notification、search index、cache 或 scheduled job，要验证触发记录以及最终效果或文档化的 pending 状态。

### 日志、Trace 和审计

当日志能证明预期业务事件、用 request/trace id 串联请求和下游工作、没有相关错误、敏感字段已脱敏时，日志才是验证证据。

不要打印原始 secret、cookie、Authorization header、password、token、私人 transcript 或带密码的完整生产连接串。

## 完成标准

只有满足所有适用条件时才报告 **PASS**：

1. 产物位置已记录为明确五层决策、项目约定假设，或 `needs classification`
2. 服务启动和依赖就绪已验证或不需要
3. 原始测试用例已拆成后端范围和非范围
4. 源用例中的后端事实已覆盖
5. 推导出来的后端风险已覆盖或明确排除
6. happy path 证据已观察到
7. 重要 negative path 已验证或明确排除
8. 权威状态已检查
9. 必要一致性不变量已检查
10. 适用时已检查幂等和并发
11. 适用时已检查副作用和异步行为
12. 适用时已检查 logs/traces/audit
13. 测试数据已清理或记录保留原因

证据不完整、环境不可用，或适用风险只设计未执行时，报告 **PARTIAL**。

观察到行为违反需求、计划、契约、状态、不变量或安全边界时，报告 **FAIL**。

## 报告格式

使用以下结构：

```text
Backend Service Verification Report

Result: PASS | PARTIAL | FAIL

1. Source Materials
   - Requirement:
   - Technical plan:
   - Source test cases:
   - Project verification docs/conventions:
   - Artifact placement decisions or assumptions:

2. Original Test Case Decomposition
   - Original case:
   - Frontend-only assertions:
   - Backend facts:
   - Full-stack/manual assertions:
   - Derived backend risks:

3. Backend Verification Plan
   - Scope / non-scope:
   - Artifact layer / writeback boundary:
   - Startup/dependencies:
   - Test data:
   - Calls to execute:
   - State checks:
   - Consistency invariants:
   - Idempotency:
   - Concurrency:
   - Permissions/state/async/logs:
   - Cleanup:

4. Execution Evidence
   - Commands or calls:
   - Responses:
   - Persisted-state evidence:
   - Log/trace evidence:
   - Side effects:

5. Gaps and Risks
   - Not verified:
   - Reason:
   - Impact:

6. Final Judgment
   - Result:
   - Why:

7. Proposed Regression Cases
   - P0 candidates:
   - P1 candidates:
   - P2 candidates:
   - Manual candidates:
```

`Proposed Regression Cases` 是交给 `backend-regression-maintenance` 的输入。
