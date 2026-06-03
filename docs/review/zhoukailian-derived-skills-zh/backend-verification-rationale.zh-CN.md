# backend verification skills 建立说明

## 1. 为什么要建立这组 skill

这组 skill 的目标不是“多写一份测试说明”，而是补 AI Coding 流程里最容易失真的一环：**验证和回归沉淀**。

现在很多 coding agent 已经能根据需求和技术方案完成实现，但经常卡在这些问题上：

1. 只跑单测或只看接口返回 200，就认为需求完成。
2. 用户给的测试用例通常是前端/全链路视角，agent 会直接照抄，无法转成服务端可验证事实。
3. 数据库、日志、队列、缓存、异步任务、幂等、一致性、并发等服务端风险没有被系统性检查。
4. 当前需求验证完之后，验证经验没有沉淀成长期回归资产。
5. 下一次上线仍然只验证当前需求，历史核心功能缺少稳定回归保护。

因此需要一组 skill，把流程固定成：

```text
需求 + 技术方案 + 原始测试用例
  ↓
推导服务端验证计划
  ↓
执行后端证据验证
  ↓
输出验证报告和 Proposed Regression Cases
  ↓
维护长期回归用例库
  ↓
形成上线前回归清单
```

这让 agent 不只是“实现了”，而是能回答：

```text
这个需求为什么算真的做完？
哪些证据证明它做对了？
哪些历史能力需要被继续保护？
上线前要跑哪些回归？
```

## 2. 为什么拆成两个 skill

这组能力拆成两个 skill：

```text
backend-service-verification
backend-regression-maintenance
```

原因是它们解决的问题不同。

### 2.1 `backend-service-verification`

它负责当前需求的验证闭环。

它要做的事情包括：

1. 读取需求、技术方案、原始测试用例。
2. 将前端/QA/全链路测试用例拆解成服务端可验证事实。
3. 从技术方案中主动推导服务端风险。
4. 发现项目自己的启动、测试、数据库、日志和依赖方式。
5. 设计后端验证计划。
6. 执行 API/RPC/CLI、数据库、日志、副作用、幂等、一致性、并发、权限、状态机、异步等验证。
7. 输出 `PASS` / `PARTIAL` / `FAIL`。
8. 输出 `Proposed Regression Cases`，供后续沉淀。

一句话：

> 证明这次服务端改动是否真的做对了。

### 2.2 `backend-regression-maintenance`

它负责长期回归资产维护。

它要做的事情包括：

1. 读取 verification report 和 proposed regression cases。
2. 读取项目已有回归用例、测试目录、release/CI 约定。
3. 去重、合并、更新、拒绝或标记需要审阅。
4. 将用例分成 `P0` / `P1` / `P2` / `Manual`。
5. 更新回归索引或项目已有用例文件。
6. 生成上线前 run list。

一句话：

> 把这次验证中值得长期保留的服务端场景沉淀成回归保护。

### 2.3 为什么不是三个 skill

看起来可以拆成：

```text
测试用例分类
服务端验证
回归归档
```

但不建议这样拆。

原因是“测试用例分类”和“服务端验证计划”强耦合。判断一个原始测试用例中哪些是服务端事实，必须结合：

1. 需求语义；
2. 技术方案；
3. API 设计；
4. 数据库模型；
5. 状态机；
6. 幂等、并发、一致性风险；
7. 项目实际验证方式。

如果先做一个独立分类 skill，很容易只按文字表面分类，例如把“按钮连续点击只提交一次”当成纯前端防抖，而漏掉服务端幂等验证。

所以当前设计是：

```text
backend-service-verification
  = 测试用例拆解 + 服务端风险推导 + 验证执行 + Proposed Regression Cases

backend-regression-maintenance
  = 消费 Proposed Regression Cases，维护长期回归库
```

这样是单向流：

```text
A → B
```

避免不可靠的：

```text
A → B → A
```

## 3. 原始测试用例为什么不能直接用

用户提供的测试用例通常不是服务端测试用例，而是前端/产品/QA 视角。

例如：

```text
用户点击领取优惠券，页面提示领取成功，优惠券出现在券包里。
```

这个用例不能只转换成：

```text
POST /claim 返回 200。
```

它背后的服务端验证应包括：

1. 用户是否满足领取条件。
2. 优惠券库存是否正确扣减。
3. `coupon_claims` 是否只新增一条记录。
4. `user_coupons` 是否新增可用券。
5. 重复领取是否幂等。
6. 并发领取是否不会超卖。
7. 库存扣减和领取记录数量是否一致。
8. 审计日志或业务日志是否有对应事件。
9. 失败路径是否返回正确错误码。

也就是说，原始测试用例只是输入材料。skill 要把它“解编译”为：

```text
Frontend-only assertions
Backend-verifiable facts
Full-stack/manual assertions
Derived backend risks
Unknowns
```

然后再生成真正适合服务端验证的计划。

## 4. 需要覆盖哪些服务端风险

`backend-service-verification` 不只验证需求 happy path，还要主动推导服务端风险。

重点包括：

1. **幂等**
   - 重复提交、重复回调、重试是否只产生一次业务效果。

2. **一致性不变量**
   - 例如 `A = B + C`、总额 = 明细 + 服务费 - 优惠、库存 = 原库存 - 成功领取 + 退回。

3. **并发**
   - 多请求同时执行时是否会超卖、重复领取、重复扣款、负库存、非法状态或 lost update。

4. **权限和隔离**
   - 普通用户、管理员、跨租户、跨 owner 的允许/拒绝行为是否正确。

5. **状态机**
   - 合法流转、非法流转、终态保护、重试和回滚是否正确。

6. **异步和副作用**
   - queue、outbox、worker、webhook、email、notification、cache、search index 是否按预期触发并最终一致。

7. **日志、Trace 和审计**
   - 是否能通过 requestId/traceId 证明链路，是否有业务事件，是否没有敏感字段泄露。

这些点很多不会出现在原始前端测试用例中，但它们是服务端上线质量的关键。

## 5. 和五层模型的关系

这组 skill 和 `five-layer-classifier` 的关系是：

```text
five-layer-classifier
  ↓ 决定资产责任、真源状态、仓库边界、写回位置

backend-service-verification
  ↓ 在这些边界内设计并执行验证

backend-regression-maintenance
  ↓ 在这些边界内维护长期回归资产
```

### 5.1 五层 skill 负责什么

`five-layer-classifier` 负责判断：

1. 一个文件或产物属于哪一层；
2. 它是不是正式 truth source；
3. 它应该放在 product repo、control repo、本地 workspace，还是不应该写入；
4. 它能不能进入 public history；
5. 它是否混合职责、需要拆分；
6. 它是应该正式沉淀，还是只保留为本地临时证据。

### 5.2 验证 skill 负责什么

`backend-service-verification` 不负责发明层级边界。

它负责在已知或可合理假设的项目边界内：

1. 推导验证计划；
2. 启动服务或发现启动方式；
3. 调接口/命令；
4. 查数据库/状态；
5. 查日志/trace；
6. 验证副作用；
7. 输出验证报告。

如果边界复杂或不清楚，它应调用或提示使用 `five-layer-classifier`。

### 5.3 回归维护 skill 负责什么

`backend-regression-maintenance` 不负责重新验证需求，也不负责重新分类全部原始测试用例。

它负责：

1. 消费验证报告中的 `Proposed Regression Cases`；
2. 根据项目已有结构和五层边界决定是否写回；
3. 维护 P0/P1/P2/Manual 回归库；
4. 生成上线前 run list。

## 6. 五层模型如何影响验证和归档

五层模型不是额外流程，而是防止验证资产写错位置。

默认关系如下：

| 层级 | 对验证体系的意义 |
| --- | --- |
| Layer 1 产品定义 | 提供产品语义、验收标准、业务契约 |
| Layer 2 当前实现 | 源码、测试、schema、fixture、runtime script、可执行验证资产 |
| Layer 3 项目落地 | 项目启动方式、CI、release checklist、默认测试目录 |
| Layer 4 共享治理 | 验证政策、回归分级规则、release gate、报告格式 |
| Layer 5 本地现场 | 临时日志、scratch SQL、一次性验证证据、本地 env note |

例如：

1. 一条自动化测试文件通常是 Layer 2。
2. 项目默认“上线前跑哪些测试”的 release checklist 可能是 Layer 3。
3. P0/P1/P2 的通用分级规则是 Layer 4。
4. 本次运行时的一段临时 SQL 查询结果是 Layer 5。
5. 如果一个文件同时写了业务 truth、测试代码和治理规则，应考虑拆分。

## 7. 为什么这组 skill 不能强依赖五层

这组 skill 必须能被别人单独使用。

不是所有用户都有五层模型，也不是每个项目都已经做过五层分类。因此 skill 需要有 fallback：

1. 没有五层上下文时，仍然可以按项目本地文档和已有约定完成验证。
2. 写回位置明显时，按项目已有结构写入，并记录假设边界。
3. 写回位置不明显时，不阻塞验证，但将写回标记为 `needs classification` 或 `NEEDS_REVIEW`。
4. 临时证据保守处理，不自动升级为正式 truth source。

也就是说：

```text
单独使用：可以完成验证和报告。
结合五层：可以更准确地决定哪些东西能正式沉淀、沉淀到哪里。
```

## 8. 为什么这组 skill 要适用于所有项目

虽然名字里有 backend，但它不能是 `group_pals` 或某个具体项目的专用手册。

不同项目可能有完全不同的验证方式：

1. Go/Kratos 项目可能通过 `go test`、Biz Mock、MockLog、Makefile 和多依赖服务验证。
2. Node 项目可能通过 package scripts、API tests、数据库 migration 和 Playwright/API runner 验证。
3. Python 项目可能通过 pytest、fixtures、CLI、Celery/Redis 或本地服务验证。
4. CLI 项目可能通过命令输出、本地文件、cache/outbox 和 fake server 验证。
5. agent runtime 项目可能通过 trace、checkpoint、session state、handoff 和 replay 验证。

因此 skill 只能规定：

1. 需要发现项目自己的验证方式；
2. 需要从需求和测试用例推导服务端事实；
3. 需要验证权威状态和服务端风险；
4. 需要保留证据和完成标准；
5. 需要把长期有价值的用例沉淀成回归资产。

它不能硬编码某个项目的命令、目录或数据库表。

## 9. 最终形成的能力

这组 skill 最终让 AI Coding 流程从：

```text
需求 → 实现 → 跑测试 → 总结
```

升级为：

```text
需求 → 技术方案 → 原始测试用例
  → 服务端验证计划
  → API/DB/log/side-effect/idempotency/consistency/concurrency 验证
  → PASS/PARTIAL/FAIL 报告
  → Proposed Regression Cases
  → P0/P1/P2/Manual 回归沉淀
  → 上线前 run list
```

这就是建立这两个 skill 的原因。

它们解决的是：

1. 当前需求如何证明做对；
2. 服务端风险如何系统性验证；
3. 原始前端/QA 测试用例如何转成服务端事实；
4. 每次需求完成后如何沉淀回归资产；
5. 上线前如何保护历史核心功能；
6. 在五层模型下如何避免验证产物写错层级或边界。
