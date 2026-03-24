# {{date}} Figma Node `{{root_node}}` All Child Nodes

## Read Boundary

- Root node: `{{root_node}}`
- Boundary rule: {{boundary_rule}}
- Last included node or stopping rule: {{stop_rule}}

## Node Ledger

| Node ID | Parent | Name | Type | Relative x | Relative y | w | h | Depth | Status | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `{{node_1}}` | `{{parent_1}}` | `{{name_1}}` | `{{type_1}}` | `{{x_1}}` | `{{y_1}}` | `{{w_1}}` | `{{h_1}}` | `{{depth_1}}` | `{{status_1}}` | {{note_1}} |
| `{{node_2}}` | `{{parent_2}}` | `{{name_2}}` | `{{type_2}}` | `{{x_2}}` | `{{y_2}}` | `{{w_2}}` | `{{h_2}}` | `{{depth_2}}` | `{{status_2}}` | {{note_2}} |
| `{{node_3}}` | `{{parent_3}}` | `{{name_3}}` | `{{type_3}}` | `{{x_3}}` | `{{y_3}}` | `{{w_3}}` | `{{h_3}}` | `{{depth_3}}` | `{{status_3}}` | {{note_3}} |

## Status Legend

- `leaf`: 当前可见叶子层，已无更深子树
- `expanded`: 已继续展开并确认内部结构
- `shell`: metadata 或实例壳层，内部还有真实可见结构
- `skipped`: 明确不在当前边界内
- `unknown`: 还需进一步读取

## Notes

- 对实例节点，优先补内部真实结构，不要只记录 metadata 外框。
- 如果 metadata 与内部真实壳层不一致，备注里明确写清差异。
- 关键状态节点单独标注，方便后续写状态矩阵。
