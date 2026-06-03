# backend verification skills 建立说明

## 1. 为什么要建立这组 skill

这组 skill 的目标不是“多写一份测试说明”，而是补 AI Coding 流程里最容易失真的一环：**用数据证据证明后端改动，并把值得长期保护的场景沉淀成回归资产**。

常见失败模式是：

1. 只跑一个大测试命令，就认为所有细节都验证过。
2. 只看接口返回 200，就认为业务正确。
3. 直接照抄前端/QA 测试用例，无法拆成服务端可验证事实。
4. 数据库、日志、队列、缓存、异步任务、幂等、一致性、并发、权限、状态机等风险没有逐项检查。
5. 当前需求验证完之后，没有把关键场景沉淀成长期回归保护。

因此这组 skill 固定的是一条证据链：

```text
需求 + 技术方案 + 原始测试用例
  ↓
事实来源盘点
  ↓
原始用例拆解
  ↓
服务端风险矩阵
  ↓
逐项验证计划
  ↓
执行证据台账
  ↓
PASS / PARTIAL / FAIL
  ↓
Proposed Regression Cases
  ↓
回归候选决策台账
  ↓
上线前 run list
```

这让 agent 不能只说“我跑了测试”，而必须回答：

```text
哪些后端事实被验证了？
证据来自哪里？
观察到的数据是什么？
哪些风险没有验证？
为什么最终是 PASS、PARTIAL 或 FAIL？
哪些场景值得加入长期回归？
```

## 2. 为什么拆成两个 skill

这组能力拆成两个 skill：

```text
backend-service-verification
backend-regression-maintenance
```

原因是它们的职责边界不同。

### 2.1 backend-service-verification

它负责当前需求的验证闭环。

它要做的事情包括：

1. 读取需求、技术方案、原始测试用例、API 契约、代码、schema、项目运行约定。
2. 将前端/QA/全链路测试用例拆解成服务端可验证事实。
3. 从需求、技术方案、代码和 schema 主动推导服务端风险。
4. 为每个事实和风险建立验证项。
5. 执行 API/RPC/CLI、数据库、日志、副作用、幂等、一致性、并发、权限、状态机、异步等验证。
6. 维护 execution evidence ledger。
7. 输出 `PASS` / `PARTIAL` / `FAIL`。
8. 输出 `Proposed Regression Cases`，供后续沉淀。

一句话：

```text
证明这次服务端改动是否真的做对。
```

### 2.2 backend-regression-maintenance

它负责长期回归资产维护。

它要做的事情包括：

1. 读取 backend verification report、evidence ledger 和 proposed regression cases。
2. 读取项目已有回归用例、测试目录、release/CI 约定。
3. 为每个候选建立 decision ledger。
4. 去重、合并、更新、拒绝或标记需要审阅。
5. 将用例分成 `P0` / `P1` / `P2` / `Manual`。
6. 更新回归索引、项目已有用例文件或 run list。
7. 验证维护结果：候选是否零遗漏、ID 是否唯一、P0/Manual 是否进入 run list、格式/索引/测试是否可验证。

一句话：

```text
把这次验证中有证据支撑、值得长期保护的服务端场景沉淀成回归覆盖。
```

### 2.3 为什么不是三个 skill

看起来可以拆成：

```text
测试用例分类
服务端验证
回归归档
```

但不建议这样拆。

“测试用例分类”和“服务端验证计划”强耦合。判断一个前端用例里哪些是服务端事实，必须结合需求语义、技术方案、API、代码、数据库模型、状态机、幂等、并发、一致性风险，以及项目实际验证方式。

如果先做独立分类，很容易按文字表面分类，例如把“按钮连续点击只提交一次”当成纯前端防抖，而漏掉服务端幂等验证。

所以当前设计是：

```text
backend-service-verification
  = 用例拆解 + 风险推导 + 逐项执行 + evidence ledger + proposed regression cases

backend-regression-maintenance
  = 消费有证据的 proposed cases，维护长期回归资产
```

这是一条单向流：

```text
A → B
```

避免不可靠的：

```text
A → B → A
```

## 3. 为什么必须强调数据证据

后端验证不能停在“命令运行了”或“接口返回了”。

例如原始用例是：

```text
用户点击领取优惠券，页面提示领取成功，优惠券出现在券包里。
```

不能只验证：

```text
POST /claim 返回 200。
```

它背后的服务端证据应包括：

1. 用户是否满足领取条件。
2. 优惠券库存是否正确扣减。
3. `coupon_claims` 是否只新增一条记录。
4. `user_coupons` 是否新增可用券。
5. 重复领取是否只产生一次业务效果。
6. 并发领取是否不会超卖。
7. 库存扣减和领取记录数量是否一致。
8. 审计日志或业务日志是否有对应事件。
9. 失败路径是否返回正确错误码。

因此 `backend-service-verification` 要求每个验证项都有 evidence ledger：

```text
Item ID:
Expected result:
Action performed:
Evidence source:
Observed data:
Status:
Reason:
Cleanup evidence:
```

这解决的是“AI 跑了一个大的，但很多细节没有执行到”的问题。大命令可以作为证据来源，但必须映射回每个 item；没有映射的细节不算验证过。

## 4. 反偷懒门禁如何下沉到每个阶段

这组 skill 不只在最后说“要验证”，而是在关键阶段都设置本地门禁。

### 4.1 Source Inventory Gate

必须列出需求、技术方案、原始测试用例、API 契约、代码、schema、项目运行约定、日志/队列/cache/worker 约定等来源，并标记 `read`、`missing`、`unavailable` 或 `not applicable`。

不能只写“已阅读文档”。

### 4.2 Source Test Case Decomposition Gate

每个原始用例都必须拆解：

```text
Frontend-only assertions
Backend-verifiable facts
Full-stack/manual assertions
Derived backend risks
Unknowns
```

范围内原始用例必须零遗漏。

### 4.3 Risk Coverage Matrix

幂等、一致性、并发、权限、状态机、事务、异步、cache、日志、migration、有限资源等风险必须逐项标记 `applies`、`not applicable` 或 `unknown`。

不能批量写 `N/A`。每类风险都要有理由。

### 4.4 Verification Plan Gate

每个后端事实或适用风险都必须成为一个验证项，并写明预期行为、数据准备、执行动作、证据来源、权威状态检查、清理和 PASS 标准。

“查 DB”“跑测试”“看日志”都不够，必须具体到权威表/存储、记录标识、查询策略或日志事件。

### 4.5 Execution Evidence Gate

每个验证项都必须有执行证据行。

如果环境不可用、数据不可准备、执行不安全，必须标为 `NOT_RUN` 或 `BLOCKED`，而不是口头判断通过。

### 4.6 Regression Decision Ledger

每个 proposed regression case 和值得沉淀的后端失败，都必须有决策行。

不能把多个候选合并成一句“已有回归覆盖”。每个候选都要有：

```text
Evidence summary
Backend assertion
Eligibility
Decision
Priority
Target file or blocker
```

### 4.7 Maintenance Verification Gate

回归维护完成后，还要验证维护结果：

1. 每个候选是否有决策。
2. 每个非 rejected case 是否有优先级和证据。
3. 新增或修改 ID 是否唯一。
4. P0 和 Manual 是否进入 run list。
5. 目标文件是否符合项目格式。
6. 可用的 formatter、linter、test、validator 或 index check 是否运行。

## 5. 和五层模型的关系

这组 skill 不能强依赖五层模型。

原因是：

1. 很多用户只安装这两个 backend skill，没有安装五层模型。
2. 后端验证的核心事实来自项目本身：需求、方案、API、代码、schema、数据库、日志、队列、cache、测试和运行时证据。
3. 五层模型解决的是资产 owner、truth-source、写回位置、public/private history、split/merge 等治理问题，不是后端验证本身。

因此当前设计是：

```text
没有五层：
  继续按项目本地事实和约定完成验证/回归维护。
  写回位置明显时按项目约定写。
  写回边界不清时标记 needs boundary decision 或 NEEDS_REVIEW。

有五层或等价治理来源：
  当 owner、truth-source、写回位置、public/private history 会影响结果时，读取该治理来源作为输入。
  使用其决策约束写回。
  不在 backend skill 里复制或重写五层模型。
```

这意味着：

```text
backend skill 可以单独使用；
有五层时可以自己读到五层输出；
但不会把五层变成安装依赖或主流程前置条件。
```

因此 `skill.json` 不声明 `five-layer-classifier` 为 `sub_skills`。这是为了避免没有五层上下文的用户被强行绑定到一个额外模型。

## 6. 为什么回归维护必须消费验证证据

`backend-regression-maintenance` 不能直接从前端用例幻想后端回归。

它只能消费：

1. backend verification report
2. evidence ledger
3. proposed regression cases
4. observed backend failures
5. 已有项目回归资产和约定

如果 report 缺少证据，候选必须标为 `NEEDS_REVIEW`。不能为了填回归库而编造稳定用例。

回归用例必须有后端可观察断言，例如：

1. API/RPC/CLI 契约
2. 数据库或持久化状态
3. cache、queue、outbox、search index、file、worker 副作用
4. log、trace、audit、event
5. 幂等、一致性、并发、权限、隔离、状态机、migration、兼容性

只有前端布局、动画、toast 位置这类内容，不能作为后端回归用例。

## 7. 最终形成的能力

这组 skill 把 AI Coding 后端验证从：

```text
需求 → 实现 → 跑一个测试 → 总结
```

升级为：

```text
需求 → 技术方案 → 原始测试用例
  → 事实来源盘点
  → 原始用例拆解
  → 风险覆盖矩阵
  → 逐项验证计划
  → API/DB/log/side-effect/idempotency/consistency/concurrency 验证
  → evidence ledger
  → PASS/PARTIAL/FAIL
  → Proposed Regression Cases
  → candidate decision ledger
  → P0/P1/P2/Manual 回归沉淀
  → 上线前 run list
```

它解决的是：

1. 当前需求如何证明做对。
2. 服务端风险如何系统性验证。
3. 原始前端/QA 测试用例如何转成服务端事实。
4. 如何防止 AI 跑一个大命令后漏掉细节。
5. 每次需求完成后如何沉淀长期回归资产。
6. 没有五层模型时也能独立运行；有治理上下文时能读取并使用其边界决策。
