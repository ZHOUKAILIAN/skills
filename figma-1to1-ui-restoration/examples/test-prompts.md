# Test Prompts

这些样例要覆盖“已有粗版本收紧”“从零实现组件”“整页还原 + 多状态”三类典型任务。

## Prompt 0: 先处理 Figma MCP 未就绪

这是 Figma 链接：https://www.figma.com/design/abc123/demo?node-id=150-27773  
如果你发现 Figma MCP 还没连上，先告诉我怎么配置，不要假装已经读过节点，也不要先开始改代码。

### 期望

- 先检测 Figma MCP 是否可用
- MCP 不可用时停止审计和开发
- 给出 `codex mcp add figma --url https://mcp.figma.com/mcp`
- 提醒启用 `rmcp_client`
- 提醒执行 `codex mcp login figma`
- 说明需要重启 Codex 后再继续原任务

## Prompt 1: 读全节点再收紧粗版本

读取这个 Figma 节点 `150-27773`，并把下面所有子节点都读到最底层。  
我不要只看截图，要把字体大小、行高、间距、按钮尺寸、状态差异都列出来。  
确认读完整之后，再直接修改原来的粗版本代码。

### 期望

- 自动先定义读取边界
- 建立完整节点台账
- 明确哪些节点已经达到 terminal no-children 状态
- 明确哪些节点只是 shell，需要继续展开
- 如果落了审计文档，开发前应先通过 audit verifier
- 在开发前完成完整读取
- 直接修改原实现，不新建平行版本

## Prompt 2: 从零实现单个组件

这是一个新的 Figma 组件，帮我 1 比 1 实现到 Vue 里。  
先把这个节点和它的所有状态、资产、变量读完整，再开始开发。

### 期望

- 不假设只需要读根节点
- 能覆盖组件状态和资产盘点
- 能把 spacing 表达为基于几何关系推导的值
- 在没有现有实现时创建新实现
- 开发前先完成节点边界盘点

## Prompt 3: 还原整页模块

这个页面不用整站都做，先把 Figma 里的报名模块、弹层和底部 CTA 这一段完整还原。  
现有页面已经有一个粗版本，按 Figma 精修，所有节点信息读完再开始改。

### 期望

- 先界定模块边界
- 继续深读被点名的状态节点和实例内部结构
- 区分 metadata 外框和真实壳层
- 给出 top inset、bottom inset 和 sibling gap 的推导
- 给出至少一个垂直闭环检查
- 如果生成了 README.md 和 ALL_CHILD_NODES.md，应先验证通过再开始实现
- 用 TDD 收紧到 1:1
- 给出验证结果

## Prompt 4: 不允许跳过上下边距推导

这个弹层不要只看左右边距。  
Figma 里没有直接的 margin 字段，你根据节点坐标把 top inset、bottom inset 和中间 gap 都算出来。  
如果没有完成垂直方向闭环，就不要开始写代码。

### 期望

- 明确说明 spacing 来自几何推导，不是 Figma 原生字段
- 至少写出一个 top inset 的推导式
- 至少写出一个 bottom inset 的推导式
- 至少写出一个 sibling gap 的推导式
- 未完成闭环前不开始实现

## Prompt 5: 想要接近 99% 的还原

这个模块我不是只要功能对，我要接近 99% 的还原。  
除了读 Figma 和写测试，还要给我一套验证方式，证明结构、几何、状态和视觉都对上了。  
如果只是说“看起来差不多”，不算完成。

### 期望

- 输出应包含验证合同，而不是只说“已测试”
- 应区分 structure check、geometry check、content check、visual diff check、state coverage check
- 应给出可度量阈值，而不是模糊表述
- 只有在这些关卡都通过时，才可以说接近 99% 还原
