# CST 智能客服使用指南

## 1. CST 是什么

CST（Customer Service Troubleshooting）是一个**智能客服问题排查助手**。

当你遇到用户反馈问题，但不确定是哪里出了问题时，CST 可以帮你：

- 快速定位问题出在哪个环节（前端的错、后端的错、还是数据问题）
- 给出清晰的排查结论，产品、客服、研发都能看懂
- 在排查结束后，把结论自动沉淀到飞书文档
- 提供下一步建议动作

**一句话定位：CST 不是修复工具，而是一个帮你找到"问题出在哪"的调查工具。**

---

## 2. 适用场景

当你听到以下类型的问题反馈时，适合用 CST：

| 反馈来源 | 典型场景 |
|---------|---------|
| 客服 | 用户说操作失败了，但不知道是前端、后端还是数据的问题 |
| 产品 | 某个功能表现异常，需要确认影响范围和根因 |
| 用户反馈 | 页面报错、数据不对、状态异常 |

**CST 的目标**：不是只回答"报错了没有"，而是形成一份所有人都能看懂的排查结论。

---

## 3. 安装 CST

### 前提条件

- 已安装 Claude Code（Codex）
- 如果希望自动写飞书文档：已安装 `lark-cli`

### 安装步骤

**Step 1.** 在 Codex 中加载 CST skill

```
/sc:load cst
```

**Step 2.** 配置文件

CST 使用前需要配置你的业务信息，让它知道查哪个代码仓库、日志和数据库。

复制配置文件模板：

```bash
cd cst
cp config.env.example config.env
```

然后编辑 `config.env`，填写你的业务信息：

```env
# 前端仓库
CST_FRONTEND_GIT_REPO="git@your-gitlab.com/your-org/your-frontend-repo.git"
CST_FRONTEND_CODE_PATH="apps/web"

# 后端仓库
CST_BACKEND_GIT_REPO="git@your-gitlab.com/your-org/your-backend-repo.git"
CST_BACKEND_CODE_PATH="services/api"

# 日志查询方式（联系研发获取）
CST_LOG_ACCESS_METHOD="aliyun-cli"

# MySQL 只读账号（联系研发获取）
CST_MYSQL_HOST="your-mysql-host.rwlb.rds.aliyuncs.com"
CST_MYSQL_PORT="3306"
CST_MYSQL_USER="readonly_user"
CST_MYSQL_PASSWORD="YOUR_PASSWORD_HERE"

# 可选：飞书文档记录
CST_FEISHU_DOC_URL="https://your-domain.feishu.cn/docx/your-doc-token"
CST_FEISHU_LOG_TITLE_PREFIX="[CST]"
```

> **谁来配置？** 配置文件一般由研发同学初始化，产品同学可以直接使用。如果环境变量已经配好，跳过这一步。

如果你希望 CST 每次排查结束都自动写入飞书文档，再额外做一次初始化：

```bash
npm install -g @larksuite/cli
lark-cli config init
lark-cli auth login --recommend
```

完成后，CST 会优先使用 `lark-cli` 的本地登录状态，不需要把 token 贴到聊天里。

---

## 4. 使用 CST

### 标准排查流程

当你拿到一个用户问题，按以下步骤告诉 CST：

---

**Step 1. 先把问题现象说清楚**

不要一上来就让 CST 查代码。先把基本信息对齐：

- 具体是哪个用户/账号
- 大概发生在什么时间
- 哪个页面、功能、或操作
- 期望结果是什么
- 实际结果是什么
- 是偶发还是稳定复现
- 现在是否仍在发生

---

**Step 2. 让 CST 开始排查**

把上面的信息整理好后，直接告诉 CST你要排查的问题，比如：

```
帮我排查：用户小王在结算页面点击支付后，提示"系统繁忙"，但客服后台没有看到订单记录。
```

CST 会自动完成以下工作：

1. **查日志** - 确认问题是否真的发生，找出错误信息和时间窗口
2. **读代码** - 串起从前端到后端的完整链路
3. **查数据库** - 验证数据状态是否符合预期
4. **出结论** - 告诉你问题出在哪一层，以及建议的下一步动作
5. **写飞书文档** - 如果 `CST_FEISHU_DOC_URL` 已配置，就把排查结论追加到目标文档里

---

**Step 3. 拿到排查结论**

CST 会输出一份标准格式的结论，包含：

- **Symptoms**：用户实际观察到的现象
- **Action**：建议立即执行的动作
- **Code Problem**：具体的代码或配置问题（如果涉及）
- **Why it happened**：为什么会由这个问题触发
- **Impact**：对产品、客服、研发各自的影响
- **Evidence**：关键日志、SQL、代码路径

如果配置了飞书文档，CST 会把这份结论按同样结构追加进去，方便后续复盘、交接和统计。

---

## 5. 输出示例

一份完整的 CST 排查结论大概长这样：

```md
## Symptoms
- 用户小王在 3 月 28 日 14:32 提交订单，页面提示"系统繁忙"
- 订单未出现在客服后台，支付渠道也未收到请求

## Action
- [ ] 确认该用户在 14:32 前是否有其他异常操作
- [ ] 检查订单服务在此时段的错误日志
- [ ] 通知研发查看支付回调服务状态

## Code Problem
- 支付回调服务在高峰期触发限流，导致回调失败但前端未正确展示错误

## Why it happened
- 用户点击支付 -> 后端创建订单 -> 调用支付渠道 -> 支付超时/限流 -> 订单状态卡住 -> 前端显示"系统繁忙"

## Impact
- **产品侧**：约 2% 的高峰期支付请求受影响
- **客服侧**：收到类似反馈可直接告知用户"支付通道繁忙，稍后重试"
- **研发侧**：需要优化限流策略或增加重试机制

## Evidence
- 日志：pay-callback 错误码 429，14:30-14:35 时段共 47 次
- 数据库：订单表 order_id=xxx 状态为 pending，支付表无记录
```

---

## 6. 常见问题

**Q：CST 能直接修复问题吗？**

A：不能。CST 是一个排查工具，目标是帮你找到问题出在哪里。如果需要修复，CST 会告诉你应该找哪个研发同学处理。

**Q：CST 能回答所有问题吗？**

A：不能。CST 主要擅长排查"用户感知到异常但根因不清楚"的问题。对于功能性咨询（比如"这个按钮是做什么的"）或者需要修改数据的场景，不适合用 CST。

**Q：CST 查不到结论怎么办？**

A：如果 CST 排查后仍无法确定根因，它会告诉你需要补充哪些信息，或者建议直接联系对应研发的同学。

**Q：谁来维护 config.env？**

A：一般由研发同学初始化和维护。如果你们团队的配置文件已经配好，产品同学直接使用即可，不需要关心具体配置内容。

**Q：飞书 token 要发给 CST 吗？**

A：不建议。更推荐在本机执行一次 `lark-cli config init` 和 `lark-cli auth login --recommend`，让 CLI 保存登录态；CST 只需要知道目标文档链接，不需要你把 token 明文贴到聊天里。

---

## 7. 联系研发

CST 排查过程中可能需要研发同学协助配置或提供：

| 需要的内容 | 联系谁 |
|-----------|--------|
| 前端/后端仓库地址 | 研发 |
| 日志访问方式 | 研发 |
| MySQL 只读账号 | 研发/DBA |
| 阿里云 AccessKey | 研发 |
