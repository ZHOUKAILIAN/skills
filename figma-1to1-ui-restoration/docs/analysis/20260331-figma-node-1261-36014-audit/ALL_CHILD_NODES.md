# 20260331 Figma Node `1261:36014` All Child Nodes

## Read Boundary

- Root node: `1261:36014`
- Boundary rule: only popup subtree `活动报名`
- Last included node or stopping rule: stop only when metadata traversal is exhausted and shell-capable nodes have completion proof from design-context expansion

## Node Ledger

| Node ID | Parent | Name | Type | Relative x | Relative y | w | h | Depth | Status | Child count | Terminal | Expanded | Expansion basis | Reason if not expanded | Completion proof | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `1261:36015` | `1261:36014` | `Rectangle 2` | `VECTOR` | `0` | `0` | `375` | `478` | `1` | `terminal` | `0` | `yes` | `n/a` | `metadata` | none | metadata shows no children and no inner shell logic | popup background shell |
| `1261:36016` | `1261:36014` | `时间` | `FRAME` | `19` | `64` | `336` | `28` | `1` | `expanded` | `2` | `yes` | `yes` | `metadata + child reads` | none | metadata children fully enumerated; nested icon instance expanded through root design context | time row |
| `1261:36017` | `1261:36016` | `签到时间：3月15日 17:00-21:00` | `TEXT` | `26` | `4` | `239` | `20` | `2` | `terminal` | `0` | `yes` | `n/a` | `metadata` | none | text leaf | copy node |
| `1261:36018` | `1261:36016` | `时间` | `INSTANCE` | `4` | `5` | `18` | `18` | `2` | `terminal` | `0` | `yes` | `yes` | `design_context via root` | none | internal vector + ellipse exposed in design context | shell-capable icon instance |
| `1261:36019` | `1261:36014` | `地点` | `FRAME` | `19` | `96` | `336` | `28` | `1` | `expanded` | `3` | `yes` | `yes` | `metadata + child reads` | none | metadata children fully enumerated; icon instances expanded through root design context | location row |
| `1261:36020` | `1261:36019` | `签到地点：招商局广场` | `TEXT` | `26` | `4` | `157` | `20` | `2` | `terminal` | `0` | `yes` | `n/a` | `metadata` | none | text leaf | copy node |
| `1261:36021` | `1261:36019` | `箭头` | `INSTANCE` | `185` | `21` | `14` | `14` | `2` | `terminal` | `0` | `yes` | `yes` | `design_context via root` | none | nested arrow structure exposed in design context | shell-capable arrow instance |
| `1261:36022` | `1261:36019` | `位置` | `INSTANCE` | `4` | `5` | `18` | `18` | `2` | `terminal` | `0` | `yes` | `yes` | `design_context via root` | none | internal vector + ellipse exposed in design context | shell-capable icon instance |
| `1261:36023` | `1261:36014` | `Rectangle 3` | `ROUNDED_RECTANGLE` | `19` | `99` | `336` | `222` | `1` | `terminal` | `0` | `yes` | `n/a` | `metadata` | none | no child nodes; visual group background shell | background behind rows |
| `1261:36024` | `1261:36014` | `组_未选中` | `INSTANCE` | `19` | `140` | `336` | `68` | `1` | `shell` | `0` | `yes` | `yes` | `metadata + dedicated design_context` | none | metadata has no children, but design context revealed row shell, label, and count | unselected option row |
| `1261:36025` | `1261:36014` | `组_未选中` | `INSTANCE` | `19` | `284` | `336` | `68` | `1` | `terminal` | `0` | `yes` | `yes` | `metadata + root design_context` | none | same shell structure as `1261:36024`, confirmed through root design context | repeated unselected row |
| `1261:36026` | `1261:36014` | `组_选中` | `INSTANCE` | `19` | `212` | `336` | `68` | `1` | `shell` | `0` | `yes` | `yes` | `metadata + dedicated design_context` | none | metadata has no children, but design context revealed highlighted row background, label, and count | selected option row |
| `1261:36027` | `1261:36014` | `弹窗_标题` | `INSTANCE` | `19` | `16` | `336` | `32` | `1` | `shell` | `0` | `yes` | `yes` | `metadata + dedicated design_context` | none | metadata has no children, but design context revealed title text and close button | popup title row |

## Status Legend

- `terminal`: metadata and required shell expansion checks show no remaining implementation-relevant internal structure
- `expanded`: node had internal structure and was fully inspected
- `shell`: metadata or instance shell required design-context expansion before terminal proof
- `skipped`: explicitly out of the current boundary
- `unknown`: still requires further reads

## Notes

- 对实例节点，优先补内部真实结构，不要只记录 metadata 外框。
- 如果 metadata 与内部真实壳层不一致，备注里明确写清差异。
- 关键状态节点单独标注，方便后续写状态矩阵。
- `Child count` 取自当前 metadata 读取结果，用来判断是否还能继续递归。
- `Terminal` 只有在 child count 为 `0` 时才能标记为 `yes`。
- 对 `instance` 等 shell-capable 节点，`Terminal = yes` 还必须有 `Expansion basis` 和 `Completion proof`，不能只靠 metadata 无子节点。
- `Expanded` 不是是否存在子节点，而是是否已经继续读到实现所需的真实可见层级。
- 如果某个关键节点没有展开，必须在 `Reason if not expanded` 里说明为什么当前仍然可以继续。
