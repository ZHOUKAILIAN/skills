# figma-design-audit 中文翻译稿

原始文件：`figma-design-audit/SKILL.md`

说明：这是一份供审阅的中文翻译稿，不是可安装的 skill 文件。实际生效文件仍是英文 `SKILL.md`。

## 元数据

- `name`: `figma-design-audit`
- `description`: 当用户提供 Figma URL、fileKey 或 node-id，并且需要在实现前完整读取 Figma 节点、分类可见图层、推导设计几何、产出审计产物时使用。

## 目标

产出一个完整、只读的 Figma 审计包。这个 skill 只拥有 Figma 事实：可见节点覆盖、读到 terminal depth、节点分类、几何目标、视觉规格、状态样例、业务来源问题和未解决 blocker。

它不写 CSS，不改项目代码，不选择 flex/grid/absolute 等实现方式，也不做最终还原验收。

## 事实来源

Figma 是视觉事实来源：节点树、可见性、几何、字体、颜色、素材、视觉层级和视觉状态样例。

Figma 不自动拥有业务内容、数据字段、权限、条件分支、排序、过滤、数量、文案归属或记录渲染规则。这些必须从用户说明、产品需求、既有实现、API 合约、schema、运行时数据或其他明确业务来源解决。

## 必要输入

- Figma URL、`fileKey`、`node-id` 或明确的 Figma 边界。
- 审计边界：组件、frame、页面、弹窗、流程步骤、变体集或状态列表。
- 用户要求优先使用的业务来源，例如 PRD、既有组件、API 合约或 owner 文档。
- 如果需要持久产物，需要指定或采用项目内合适的产物位置；否则内联输出相同结构的审计内容。

如果边界不明确，先读可用 Figma metadata；只有多个候选边界仍然会改变范围时，才问用户。

## 适用场景

- 用户提供 Figma URL、`fileKey` 或 `node-id`。
- 用户要求编码前先读完子节点、状态、素材、变量或规格。
- Figma 还原任务需要先产出审计包，再进入 CSS 实现。
- 既有 Figma 审计可能不完整，需要补 terminal-depth 覆盖或 blocker 清理。

## 不适用场景

- 已经有完整审计，用户问 CSS 怎么实现：使用 `css-best-practices`。
- 用户要只读比较既有实现和 Figma：使用 `figma-restoration-review`。
- 任务不涉及 Figma 节点数据。

## 工作流

1. 根据用户请求和 Figma metadata 建立审计边界。
2. 把边界读到 terminal depth，并分类每个可见节点。
3. 从 Figma、代码、文档、schema、运行时数据或用户说明中解决几何、状态和业务来源问题。
4. 只有查过可用来源后仍无法解决的问题，才进入 Blocking Questions。
5. 写审计 README、节点 ledger，以及需要时的 manifest 或 verification artifact。
6. 对持久产物运行 `scripts/verify_figma_audit.py`。
7. 如果 gate 失败，修复具体失败项并重跑；如果无法自行解决，报告 `not ready`，不要交给 CSS 实现。

## 必须产出的审计内容

- 多屏、多边界、多状态或多流程步骤时，需要 restoration manifest。
- 边界 README：范围、来源优先级、读取依据、节点分类、几何推导、垂直/水平闭环、状态矩阵、业务来源映射、阻塞问题、验证摘要和 ready 状态。
- 完整节点 ledger：每个范围内可见节点的分类、几何、child count、展开状态、terminal proof、排除原因或 blocker 原因。
- 当实现相关不确定性查过来源仍未解决时，需要 Blocking Questions。

缺少这些产物或 verifier 不通过，审计不能交给实现。

## 关键 gate

### Exhaustive Node Read Gate

每个范围内可见节点都必须读到 terminal depth。不要抽样重复项，不要从兄弟节点推断结构，不要停在 frame、group、component、instance、icon wrapper、slot wrapper 或 design-system shell 外层。截图不能替代节点遍历。

每个可见节点都必须进入 ledger，包含 node id、parent id、name、type、visibility、depth、x、y、width、height、分类、child count、展开状态、展开依据、terminal proof、排除原因或 blocker 原因。

如果仍有 `unknown`、`unexpanded` 或 `blocked`，不能标记为 ready。

### Node Classification Gate

每个可见节点都要分类：

- `renderable-ui`：产品代码渲染。
- `platform-native`：宿主平台、运行时容器、浏览器、操作系统或小程序 shell 提供。
- `interaction-proxy`：设计中表达行为、过渡、手势、选中、展开或临时 overlay 的静态图层。
- `annotation-demo-only`：注释、箭头、预览 chrome、手机壳、演示壳层。

审计必须回答：这个节点是否在设计边界中可见；它应由产品代码渲染、交给平台、转成行为/状态，还是有理由排除。

### Geometry Audit Gate

Figma 坐标是设计测量证据，不是 CSS 实现指令。用 `x`、`y`、`width`、`height` 推导 parent inset、sibling gap、尺寸、垂直/水平闭环、字体、颜色、圆角、阴影、素材和状态目标值。

每个影响实现的间距或尺寸，都要记录容器、参考节点、公式和结果。

主要容器必须做闭环：

- 垂直：`top inset + internal gaps + content heights + bottom inset = container height`
- 水平：`left inset + internal gaps + content widths + right inset = container width`

闭环不通过时，继续读取或标 blocker；不要在这个 skill 里决定 CSS primitive。

### Resolve-Before-Asking Gate

不要一遇到 unknown 就问用户。先尝试从 Figma 节点、组件/实例展开、变量、样式、metadata、既有实现、props、store、hooks、API client、schema、fixtures、需求、技术设计、任务文本、相似 UI、运行时数据中解决。

只有同时满足这些条件才问用户：

1. unknown 影响实现或验收。
2. available sources 无法解决。
3. 继续做需要猜测。

问题要集中成一批问，不要一个一个打断。用户回答后更新审计，再重新跑 gate。

## 截图边界

截图只辅助定位、视觉状态匹配或后续 review。它不是必需证据，也不能替代节点遍历、shell 展开或几何推导。强制证据是 Figma 节点数据和派生目标值。

## 完成信号

审计完成必须满足：边界和来源优先级明确；所有范围内可见节点都进入 ledger；无 `unknown`、`unexpanded` 或未解决 `blocked`；shell-capable 节点有展开依据和 terminal proof；所有可见节点有分类和处理决策；几何推导有参考节点和公式；主要容器垂直/水平闭环通过；状态矩阵覆盖范围内状态；业务内容和分支有来源或已记录用户答案；Blocking Questions 为空或已回答；持久产物通过 `scripts/verify_figma_audit.py`。

## 证明包

报告完成或 `not ready` 时，需要说明：产物路径或内联章节、边界数、可见节点数、terminal/expanded/excluded/blocked 计数、读取过的 Figma 和业务来源、每个主要容器的几何闭环状态、Blocking Questions 状态、verifier 命令和结果。
