# backend-service-verification 中文审阅稿

## 目标

通过自己编写并执行服务端端到端自测，证明一个后端改动是否真正完成；判断必须同时验证 response、权威状态、日志和副作用。

这里的端到端，指跨过真实服务边界：API、RPC、CLI 命令、job trigger、webhook handler，或项目里等价的后端入口。不等于浏览器/UI 自动化；除非浏览器行为只是用来发现后端请求。

这个 skill 只负责后端验证。它不验证前端布局、视觉样式、动画、浏览器渲染或 toast 位置，除非这些用户可见断言背后隐含后端事实。

## 核心规则

没有已执行的 backend probe 和 evidence ledger，不允许报告 `PASS`。

每个后端事实、推导风险、必要负向路径和 proposed regression case，都必须能追溯到一个自己编写的 self-test case，以及一个可复现的 probe artifact，例如：

- `curl` 命令
- RPC 调用
- CLI 调用
- focused integration test
- SQL 查询
- log 查询
- cache/queue 检查
- 项目原生等价方式

错误：

```text
接口返回 200，所以后端验证通过。
```

正确：

```text
self-test 通过 API 创建了隔离测试记录；response 符合契约；权威表中存在预期字段；关联计数不变量成立；重复提交没有生成第二条业务记录；audit log 包含预期业务事件。
```

## 使用场景

当任务是验证后端需求、API/RPC/CLI 行为、服务端 bugfix、数据写入链路、异步 worker 行为，或需要后端证据的全链路/QA 用例时使用。

当 agent 应该主动创建后端 self-test cases、构造可执行 probe、调用服务，并检查日志、数据库、cache、queue、文件、audit records 或其他权威副作用时使用。

当原始测试用例是前端或 QA 视角，需要先拆解成后端事实，再做服务端端到端验证时使用。

## 不使用场景

不要用它验证纯前端视觉、文案布局、浏览器行为或 Figma 还原，除非这些检查隐含后端状态或服务行为。

当前需求验证完成后，如果要维护长期回归资产，把 `Proposed Regression Cases` 交给 `backend-regression-maintenance`。

## 必要输入

执行 probe 前，必须确定或标记 blocked：

- 要验证的需求、改动、bug、PR、endpoint、route、RPC method、CLI command、worker 或后端行为
- 目标环境：local、test、staging、production 或用户提供的 snapshot
- base URL、服务启动命令、RPC target、CLI entrypoint 或 job trigger method
- 认证方式、测试账号、tenant、fixture 或安全身份
- 是否允许写数据和触发外部副作用
- 被测试记录对应的权威状态存储和查询策略
- 每个 mutation 的 cleanup 策略

如果这些输入无法安全确定，只能继续 plan-only / evidence-review-only，或把受影响的可执行检查标为 `BLOCKED`。

## 事实来源

优先使用项目本地最强事实：

- 需求、验收标准、产品说明、issue、PR 或技术方案
- QA/前端/全链路原始测试用例
- API/RPC/CLI 契约、OpenAPI、protobuf、请求校验、路由定义或抓到的前端请求
- 实现代码、migration、schema、model、fixture、factory、已有测试
- runtime 配置、服务启动文档、依赖文档、CI 脚本、release 文档、sample request 或 local dev script
- 权威状态：数据库记录、持久化文件、cache key、outbox 行、queue message、搜索索引、生成产物或外部系统 test double
- 运行时证据：response、log、trace、audit、worker 输出、副作用、清理证据和命令输出

模型记忆、摘要、"看起来正确"、纯代码检查或 HTTP 200 本身，都不能作为已执行验证的事实来源。

## 可选治理上下文

这个 skill 必须能在没有 AI Coding 五层模型的情况下独立工作。

如果 five-layer classifier 或等价治理来源可用，并且资产 owner、truth-source 状态、写回位置、public/private history 会改变验证输出或仓库写入，就把该治理来源作为输入读取。不要在本 skill 里复制或重写五层模型，也不要要求用户必须安装五层。

如果治理来源不可用，继续做项目本地发现。目标位置明显时按项目约定处理；临时运行证据保守留在本地；写回边界不清时标记为 `needs boundary decision`，不要猜。

不要因为五层不可用就阻塞后端验证。只有写回目标或 owner 不安全时，才阻塞仓库写回。

## 模式和降级规则

执行前先选择一个 active mode：

- `plan-only`：用户只要求验证计划时使用。到 self-test cases 和 probe artifacts 草案为止，把所有 item 标为 `NOT_RUN`，不要声称后端行为通过。
- `execute-verification`：用户要求验证、测试、证明或检查完成时默认使用。发现服务边界，编写 self-test cases，创建可执行 probe，执行安全 probe，检查权威状态，并填写 evidence ledger。
- `evidence-review-only`：环境不能运行，但已有报告、日志、数据库快照、命令输出或历史 probe 输出时使用。只审查给定证据；除非证据完整满足完成标准，否则报告 `PARTIAL`。

降级规则：

- 启动、凭证、测试数据、依赖访问或写权限不安全/不可用时，把受影响的可执行检查标为 `BLOCKED` 或 `NOT_RUN`，不要编造证据。
- 机械检查不能运行时，只有在命名了被检查来源并报告 gap impact 后，才可以使用人工检查证据。
- 仓库写回 owner 不清楚时，继续验证，但把写回标记为 `needs boundary decision`。
- 如果项目原生 integration test 比原始 `curl` 更可靠，可以使用项目测试方式，但仍然必须记录具体请求、fixture、断言、权威状态检查和命令输出。

## 工作流

### 1. 事实来源盘点门禁

制定验证前，枚举事实来源，并标记 `read`、`missing`、`unavailable` 或 `not applicable`。

必须盘点：

1. 需求或验收来源
2. 技术方案或实现意图
3. 原始测试用例，如有
4. API/RPC/CLI 契约、抓到的请求、路由定义或 job trigger
5. 实现代码路径
6. schema、model、migration、fixture、factory 或权威状态定义
7. 项目启动、依赖、测试、local-dev 或 CI 约定
8. 认证、tenant、权限或测试身份约定
9. 相关时的 log、trace、queue、cache、worker、audit、外部副作用或 cleanup 约定

反偷懒门禁：不能只写“已阅读文档”或“已检查项目约定”。必须写出被检查的文件、命令、endpoint、route 或来源。缺少来源时，先记录影响再继续。

### 2. 环境和安全门禁

执行任何 probe 前，先判断环境和副作用。

必须记录：

```text
Environment:
Service startup or target base URL:
Auth or test identity source:
Allowed mutation scope:
External side effects possible:
Data isolation strategy:
Cleanup strategy:
Blocked operations:
Safety decision: safe_to_execute | plan_only | evidence_review_only | blocked
```

安全规则：

- 生产或共享环境写操作必须先得到用户明确批准。
- 不要发送真实 email、notification、payment、webhook 或外部 callback，除非用户明确批准该副作用。
- 报告中必须隐藏 secret、cookie、Authorization header、password、token、私有用户标识和完整生产连接串。
- 如果无法准备隔离数据，把 mutating probes 标为 `BLOCKED`，或降级为 plan-only。

反偷懒门禁：环境和 mutation scope 没记录前，不要执行 `curl`、RPC、CLI、SQL mutation、worker trigger 或 cleanup 命令。

### 3. 原始测试用例拆解门禁

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

反偷懒门禁：范围内原始用例必须零遗漏。如果一个原始用例隐含多个后端事实，要拆成多个 self-test case，不能只测最明显的 happy path。

### 4. 后端风险推导门禁

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

反偷懒门禁：不能批量写 `N/A`。每类风险都要引用需求、代码、schema 或项目约定作为理由。每个 `applies` 或 `unknown` 都必须对应 self-test case、blocker 或明确 out-of-scope 决策。

### 5. Self-Test Case Authoring Gate

执行前，为每个后端事实、适用风险、未知风险和重要负向路径编写一个后端端到端 self-test case。

每个 self-test case 必须包含：

```text
Self-test case ID:
Source case, requirement, code path, or risk:
Backend behavior under test:
Preconditions and isolated test data:
Entrypoint: API | RPC | CLI | worker trigger | webhook handler | other
Request method/path or command:
Headers/auth strategy, redacted:
Request body, params, or fixture:
Expected response status, schema, fields, or error code:
Expected authoritative state:
Expected logs, traces, audit rows, cache/queue/outbox effects, or worker effects:
Negative/idempotency/concurrency/permission/state checks:
Cleanup:
PASS criterion:
```

如果项目已有 integration 或 E2E 测试约定，在安全且成本合理时优先使用项目约定里的 focused test。如果不需要沉淀 durable test，或 durable test 成本过高，可以创建临时 probe，例如 `curl` + SQL/log/cache 检查。

反偷懒门禁：“测试这个 endpoint”不是 self-test case。用例必须具体到另一个 agent 可以不猜测地执行请求并检查预期状态。

### 6. Probe Artifact Gate

每个 self-test case 在声称执行前，都必须创建或记录可执行 probe artifact。

可接受的 probe artifact 包括：

- 带脱敏 secret 的精确 `curl` 命令
- RPC 调用、GraphQL operation、CLI 命令、worker trigger 或 webhook replay 命令
- focused project-native integration/E2E test command
- SQL 查询或 read-only 数据检查命令
- log、trace、audit、cache、queue、outbox、file、search-index 检查命令
- cleanup 命令或 cleanup verification query

每个 probe artifact 必须包含：

```text
Probe ID:
Self-test case ID:
Executable request or command:
Expected output:
Authoritative state query:
Runtime evidence query:
Cleanup or cleanup verification:
Safety notes:
```

反偷懒门禁：一个大命令可以支撑多行，但必须映射到每个 self-test case。没有映射到用例、预期结果和证据来源的命令，不能证明该用例。

### 7. 执行证据门禁

按项目发现到的约定执行 probe artifacts。执行不安全或不可行时，把受影响 case 标为 `BLOCKED` 或 `NOT_RUN`，并写原因。

每个 self-test case 都要维护 evidence ledger：

```text
Self-test case ID:
Probe ID:
Expected result:
Request or command executed:
Response evidence:
Authoritative state evidence:
Runtime evidence: log | trace | audit | cache | queue | worker | file | other
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

反偷懒门禁：代码检查、大测试套件通过或一个 happy-path `curl` 可以支撑证据，但不能替代 ledger。必须把运行时证据映射回每个 self-test case。没有映射到 case 的细节不算已验证。

## 完成标准

只有满足所有适用条件时才报告 **PASS**：

1. 事实来源盘点完整，或缺口已记录且不阻塞
2. 环境、认证、数据隔离、副作用和 cleanup 已被判定为可安全执行
3. 每个原始测试用例已拆解，或标记为不适用并说明原因
4. 每个后端事实都映射到 self-test case
5. 每类风险都已单独分类并有证据
6. 每个适用或未知风险都已验证、阻塞或明确排除
7. 每个必需 self-test case 都有 probe artifact
8. 每个必需 probe artifact 都在安全环境中执行过
9. 必需范围内的 evidence ledger 没有 `NOT_RUN` 或 `BLOCKED`
10. 每个必需 response、权威状态、运行时证据和 cleanup 检查通过
11. 每个必需不变量、幂等、并发、权限、状态、异步、副作用、log、trace 或 audit 检查通过
12. 重要负向路径已验证或明确排除

证据不完整、环境不可用、安全执行被阻塞、必需项为 `NOT_RUN`/`BLOCKED`，或适用风险只计划未执行时，报告 **PARTIAL**。

观察到行为违反需求、技术方案、API 契约、权威状态、不变量或安全边界时，报告 **FAIL**。

反偷懒门禁：不能把缺失执行证据降级成“风险较低”后仍报告 `PASS`。缺必需证据就是 `PARTIAL`；证据矛盾就是 `FAIL`。

## 门禁失败处理

当某个门禁不完整时，先补齐缺失的事实来源引用、self-test case 字段、probe artifact、ledger 行或执行证据。

如果缺失项无法安全补齐，不要继续报告 `PASS`。把受影响项标为 `NOT_RUN`、`BLOCKED` 或 `OUT_OF_SCOPE` 并说明原因；除非观察证据已经要求 `FAIL`，否则报告 `PARTIAL`。

不要把失败门禁改写成模糊剩余风险。失败项必须出现在报告的 evidence ledger 或 gaps section 中。

## Proposed Regression Cases

只从已执行的 self-test cases、已验证的后端事实、观察到的失败或已记录的 manual 检查中提出回归候选。

每个候选必须包含：

```text
Candidate ID:
Source self-test case:
Probe and evidence summary:
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

2. Environment and Safety
   - Environment:
   - Target base URL or service entrypoint:
   - Auth/test identity:
   - Mutation and side-effect scope:
   - Data isolation and cleanup:
   - Safety decision:

3. Original Test Case Decomposition
   - Original case ID:
   - Frontend-only assertions:
   - Backend facts:
   - Full-stack/manual assertions:
   - Derived backend risks:
   - Status and reason:

4. Risk Coverage Matrix
   - Risk category:
   - Applies / not applicable / unknown:
   - Evidence:
   - Self-test case or out-of-scope reason:

5. Self-Test Cases
   - Self-test case ID:
   - Backend behavior:
   - Request or command:
   - Expected response:
   - Expected authoritative state:
   - Expected runtime evidence:
   - Cleanup:
   - PASS criterion:

6. Probe Artifacts
   - Probe ID:
   - Self-test case ID:
   - Executable request or command:
   - State/log/cache/queue queries:
   - Cleanup check:

7. Execution Evidence Ledger
   - Self-test case ID:
   - Probe ID:
   - Request or command executed:
   - Response evidence:
   - Authoritative state evidence:
   - Runtime evidence:
   - Observed data:
   - Status:
   - Reason:
   - Cleanup evidence:

8. Gaps and Risks
   - Not verified:
   - Reason:
   - Impact:

9. Final Judgment
   - Result:
   - Why:

10. Proposed Regression Cases
   - Candidate ID:
   - Source self-test case:
   - Probe and evidence summary:
   - Suggested priority:
```

## Proof Package

最终回复必须包含：

- source inventory 数量，以及缺失或不可用的来源组
- environment and safety decision，包括是否执行了写操作或外部副作用
- 原始测试用例数量、已拆解数量、不适用于后端的数量
- risk matrix 中 `applies`、`not applicable`、`unknown` 的数量
- self-test case 数量和 probe artifact 数量
- evidence ledger 中 `PASS`、`FAIL`、`NOT_RUN`、`BLOCKED`、`OUT_OF_SCOPE` 的数量
- 作为证据使用的已脱敏命令、调用、查询、日志、trace、代码路径或文件
- 跳过或无法执行的检查、原因和影响
- cleanup 状态
- 最终 `PASS`、`PARTIAL` 或 `FAIL` 判断，以及支撑该判断的阻塞证据

## 安全边界

不要输出原始 secret、cookie、Authorization header、password、token、私人 transcript、私有用户标识或完整生产连接串。

没有明确用户要求时，不要写生产、修改共享数据、触发外部 callback 或发送 email/notification。

如果无法准备安全隔离数据，把受影响检查标为 `BLOCKED` 或 `Manual`；不要编造数据证据。
