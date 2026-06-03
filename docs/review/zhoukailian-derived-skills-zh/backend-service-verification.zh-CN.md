# backend-service-verification 中文审阅稿

## 目标

证明一个后端改动是否真正完成：从需求、技术方案、QA/前端/全链路测试用例中拆出后端可验证事实，执行服务端检查，并报告判断背后的数据证据。

这个 skill 只负责后端验证。它不验证前端布局、视觉样式、动画、浏览器渲染或 toast 位置，除非这些用户可见断言背后隐含后端事实。

## 核心规则

没有 evidence ledger，不允许报告 `PASS`。

每个后端事实、推导风险、必要负向路径都必须有一行证据台账，包含：

- 预期结果
- 证据来源
- 已执行动作或已检查来源
- 观察到的数据
- 状态
- 每个非 `PASS` 状态的原因

错误：

```text
接口返回 200，所以后端验证通过。
```

正确：

```text
创建请求返回了预期 schema；权威表中存在预期记录；关联计数不变量成立；重复提交没有生成第二条业务记录；审计日志包含预期业务事件。
```

## 使用场景

当任务是验证后端需求、API/RPC/CLI 行为、服务端 bugfix、数据写入链路、异步 worker 行为，或需要后端证据的全链路/QA 用例时使用。

当原始测试用例是前端或 QA 视角，需要拆解成后端事实时使用。

## 不使用场景

不要用它验证纯前端视觉、文案布局、浏览器行为或 Figma 还原，除非这些检查隐含后端状态或服务行为。

当前需求验证完成后，如果要维护长期回归资产，把 `Proposed Regression Cases` 交给 `backend-regression-maintenance`。

## 事实来源

优先使用项目本地最强事实：

- 需求、验收标准、产品说明、issue、PR 或技术方案
- QA/前端/全链路原始测试用例
- API/RPC/CLI 契约、OpenAPI、protobuf、请求校验、路由定义
- 实现代码、migration、schema、model、fixture、已有测试
- runtime 配置、服务启动文档、依赖文档、CI 脚本、release 文档
- 权威状态：数据库记录、持久化文件、cache key、outbox 行、queue message、搜索索引、生成产物
- 运行时证据：response、log、trace、audit、worker 输出、副作用、清理证据

模型记忆、摘要、"看起来正确"、HTTP 200 本身都不能当作事实来源。

## 可选治理上下文

这个 skill 必须能在没有 AI Coding 五层模型的情况下独立工作。

如果 five-layer classifier 或等价治理来源可用，并且资产 owner、truth-source 状态、写回位置、public/private history 会改变验证输出或仓库写入，就把该治理来源作为输入读取。不要在本 skill 里复制或重写五层模型，也不要要求用户必须安装五层。

如果治理来源不可用，继续做项目本地发现。目标位置明显时按项目约定处理；临时运行证据保守留在本地；写回边界不清时标记为 `needs boundary decision`，不要猜。

不要因为五层不可用就阻塞后端验证。只有写回目标或 owner 不安全时，才阻塞仓库写回。

## 模式和降级规则

执行前先选择一个 active mode：

- `plan-only`：用户只要求验证计划时使用。到计划为止，把所有 item 标为 `NOT_RUN`，不要声称后端行为通过。
- `execute-verification`：用户要求验证、测试、证明或检查完成时默认使用。先产出计划，再执行安全检查，并填写 evidence ledger。
- `evidence-review-only`：环境不能运行，但已有报告、日志、数据库快照或历史输出时使用。只审查给定证据；除非证据完整满足完成标准，否则报告 `PARTIAL`。

降级规则：

- 启动、凭证、测试数据或依赖访问不安全/不可用时，把受影响项标为 `BLOCKED` 或 `NOT_RUN`，不要编造证据。
- 机械检查不能运行时，只有在命名了被检查来源并报告 gap impact 后，才可以使用人工检查证据。
- 仓库写回 owner 不清楚时，继续验证，但把写回标记为 `needs boundary decision`。

## 工作流

### 1. 事实来源盘点门禁

制定验证计划前，枚举事实来源，并标记 `read`、`missing`、`unavailable` 或 `not applicable`。

必须盘点：

1. 需求或验收来源
2. 技术方案或实现意图
3. 原始测试用例，如有
4. API/RPC/CLI 契约或路由定义
5. 实现代码路径
6. schema、model、migration、fixture 或权威状态定义
7. 项目启动、依赖、测试或 CI 约定
8. 相关时的 log、trace、queue、cache、worker 或副作用约定

反偷懒门禁：不能只写“已阅读文档”或“已检查项目约定”。必须写出被检查的文件、命令或来源。缺少来源时，先记录影响再继续。

### 2. 原始测试用例拆解门禁

用户给的 QA、前端或全链路用例是输入材料，不是可以直接复制的后端用例。

每个原始用例都要有拆解行：

```text
Original case ID:
Original assertion:
Frontend-only assertions:
Backend-verifiable facts:
Full-stack/manual assertions:
Derived backend risks:
Unknowns:
Status: covered | not backend-applicable | blocked
Reason:
```

反偷懒门禁：范围内原始用例必须零遗漏。如果一个原始用例隐含多个后端事实，要拆成多个验证项，不能只测最明显的 happy path。

### 3. 后端风险推导门禁

必须从需求、技术方案、代码、schema、原始测试用例主动推导服务端风险，即使原始用例没有写。

每类风险都要标记 `applies`、`not applicable` 或 `unknown`，并写明证据和下一步：

1. 幂等或重复执行
2. 数据一致性不变量
3. 并发或竞态
4. 权限、角色、归属或租户隔离
5. 状态流转和终态
6. 事务、回滚或部分失败
7. 异步任务、queue、outbox、webhook、重试或 worker
8. cache 读写、失效或脏数据
9. 审计日志、业务日志、可追溯性和敏感信息脱敏
10. migration、backfill、兼容或数据修复
11. quota、counter、balance、inventory、reward、coupon 等有限资源

反偷懒门禁：不能批量写 `N/A`。每类风险都要引用需求、代码、schema 或项目约定作为理由。每个 `applies` 或 `unknown` 都必须对应验证项、blocker 或明确 out-of-scope 决策。

### 4. 验证计划门禁

执行前，为每个后端事实或适用风险创建一个验证项。

每项必须包含：

```text
Verification item ID:
Source case or risk:
Expected backend behavior:
Data setup and isolation:
Action to execute or source to inspect:
Evidence sources:
Authoritative state checks:
Invariant, idempotency, concurrency, permission, state, async, log, or side-effect checks:
Cleanup:
PASS criterion:
```

如果用户只要求计划，到这里停止，并把每个 item 标为 `NOT_RUN`。

反偷懒门禁：计划必须写出具体证据来源。“执行后端验证”不是计划。“查 DB”也不够，除非写出权威表/存储、记录标识或查询策略。

### 5. 执行证据门禁

按项目发现到的约定执行计划。执行不安全或不可行时，把受影响项标为 `BLOCKED` 或 `NOT_RUN`，并写原因。

每项都要维护 evidence ledger：

```text
Item ID:
Expected result:
Action performed:
Evidence source: response | database | cache | queue | log | trace | audit | file | code | test output | other
Observed data:
Status: PASS | FAIL | NOT_RUN | BLOCKED | OUT_OF_SCOPE
Reason:
Cleanup evidence:
```

证据规则：

- API/RPC/CLI 检查必须包含契约相关的 status、schema、error code 或返回字段。
- 权威状态检查必须查看事实来源，不能只看返回值。
- 一致性检查必须从权威数据验证实际不变量。
- 幂等检查必须证明重复执行不会产生重复业务效果。
- 并发检查必须检查最终权威状态，不能只看单个 response。
- 权限检查在相关时必须包括允许和拒绝访问。
- 状态机检查在相关时必须包括合法流转、非法流转和终态保护。
- 异步和副作用检查必须验证触发记录以及最终效果或文档化的 pending 状态。
- log、trace、audit 只有在证明业务事件、串联请求和下游工作、且不泄露敏感信息时才算证据。

反偷懒门禁：一个大命令或一个大测试套件可以支撑多行证据，但不能替代 ledger。必须把命令输出或运行时证据映射回每个 item。没有映射到 item 的细节不算已验证。

## 完成标准

只有满足所有适用条件时才报告 **PASS**：

1. 事实来源盘点完整，或缺口已记录且不阻塞
2. 每个原始测试用例已拆解，或标记为不适用并说明原因
3. 每个后端事实都映射到验证项
4. 每类风险都已单独分类并有证据
5. 每个适用或未知风险都已验证、阻塞或明确排除
6. 必需范围内的 evidence ledger 没有 `NOT_RUN` 或 `BLOCKED`
7. 每个必需权威状态检查通过
8. 每个必需不变量、幂等、并发、权限、状态、异步、副作用、log、trace 或 audit 检查通过
9. 重要负向路径已验证或明确排除
10. 测试数据清理已完成或已记录

证据不完整、环境不可用、必需项为 `NOT_RUN`/`BLOCKED`，或适用风险只计划未执行时，报告 **PARTIAL**。

观察到行为违反需求、技术方案、API 契约、权威状态、不变量或安全边界时，报告 **FAIL**。

反偷懒门禁：不能把缺失证据降级成“风险较低”后仍报告 `PASS`。缺必需证据就是 `PARTIAL`；证据矛盾就是 `FAIL`。

## 门禁失败处理

当某个门禁不完整时，先补齐缺失的 ledger 行、事实来源引用或执行证据。

如果缺失项无法安全补齐，不要继续报告 `PASS`。把受影响项标为 `NOT_RUN`、`BLOCKED` 或 `OUT_OF_SCOPE` 并说明原因；除非观察证据已经要求 `FAIL`，否则报告 `PARTIAL`。

不要把失败门禁改写成模糊剩余风险。失败项必须出现在报告的 evidence ledger 或 gaps section 中。

## Proposed Regression Cases

只从已验证的后端事实、观察到的失败或已记录的 manual 检查中提出回归候选。

每个候选必须包含：

```text
Candidate ID:
Source verification item:
Evidence summary:
Backend assertion:
Suggested priority: P0 | P1 | P2 | Manual
Why it should or should not become long-term regression coverage:
```

`Proposed Regression Cases` 是交给 `backend-regression-maintenance` 的输入。

## 报告格式

```text
Backend Service Verification Report

Result: PASS | PARTIAL | FAIL

1. Source Inventory
   - Source:
   - Status:
   - Evidence or location:
   - Gap impact:

2. Original Test Case Decomposition
   - Original case ID:
   - Frontend-only assertions:
   - Backend facts:
   - Full-stack/manual assertions:
   - Derived backend risks:
   - Status and reason:

3. Risk Coverage Matrix
   - Risk category:
   - Applies / not applicable / unknown:
   - Evidence:
   - Verification item or out-of-scope reason:

4. Verification Plan
   - Item ID:
   - Expected backend behavior:
   - Evidence sources:
   - Data setup and cleanup:
   - PASS criterion:

5. Execution Evidence Ledger
   - Item ID:
   - Action performed:
   - Observed data:
   - Status:
   - Reason:
   - Cleanup evidence:

6. Gaps and Risks
   - Not verified:
   - Reason:
   - Impact:

7. Final Judgment
   - Result:
   - Why:

8. Proposed Regression Cases
   - Candidate ID:
   - Source verification item:
   - Evidence summary:
   - Suggested priority:
```

## Proof Package

最终回复必须包含：

- source inventory 数量，以及缺失或不可用的来源组
- 原始测试用例数量、已拆解数量、不适用于后端的数量
- risk matrix 中 `applies`、`not applicable`、`unknown` 的数量
- evidence ledger 中 `PASS`、`FAIL`、`NOT_RUN`、`BLOCKED`、`OUT_OF_SCOPE` 的数量
- 作为证据使用的命令、调用、查询、日志、trace、代码路径或文件
- 跳过或无法执行的检查、原因和影响
- cleanup 状态
- 最终 `PASS`、`PARTIAL` 或 `FAIL` 判断，以及支撑该判断的阻塞证据

## 安全边界

不要输出原始 secret、cookie、Authorization header、password、token、私人 transcript、私有用户标识或完整生产连接串。

没有明确用户要求时，不要写生产、修改共享数据、触发外部 callback 或发送 email/notification。

如果无法准备安全隔离数据，把受影响检查标为 `BLOCKED` 或 `Manual`；不要编造数据证据。
