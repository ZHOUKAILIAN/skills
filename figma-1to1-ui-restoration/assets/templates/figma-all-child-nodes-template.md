# {{date}} Figma Node `{{root_node}}` All Child Nodes

## Read Boundary

- Root node: `{{root_node}}`
- Boundary rule: {{boundary_rule}}
- Last included node or stopping rule: {{stop_rule}}

## Node Ledger

| Node ID | Parent | Name | Type | Relative x | Relative y | w | h | Depth | Status | Child count | Terminal | Expanded | Expansion basis | Reason if not expanded | Completion proof | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `{{node_1}}` | `{{parent_1}}` | `{{name_1}}` | `{{type_1}}` | `{{x_1}}` | `{{y_1}}` | `{{w_1}}` | `{{h_1}}` | `{{depth_1}}` | `{{status_1}}` | `{{child_count_1}}` | `{{terminal_1}}` | `{{expanded_1}}` | `{{expansion_basis_1}}` | {{not_expanded_reason_1}} | {{completion_proof_1}} | {{note_1}} |
| `{{node_2}}` | `{{parent_2}}` | `{{name_2}}` | `{{type_2}}` | `{{x_2}}` | `{{y_2}}` | `{{w_2}}` | `{{h_2}}` | `{{depth_2}}` | `{{status_2}}` | `{{child_count_2}}` | `{{terminal_2}}` | `{{expanded_2}}` | `{{expansion_basis_2}}` | {{not_expanded_reason_2}} | {{completion_proof_2}} | {{note_2}} |
| `{{node_3}}` | `{{parent_3}}` | `{{name_3}}` | `{{type_3}}` | `{{x_3}}` | `{{y_3}}` | `{{w_3}}` | `{{h_3}}` | `{{depth_3}}` | `{{status_3}}` | `{{child_count_3}}` | `{{terminal_3}}` | `{{expanded_3}}` | `{{expansion_basis_3}}` | {{not_expanded_reason_3}} | {{completion_proof_3}} | {{note_3}} |

## Status Legend

- `terminal`: metadata 中已无子节点，可停止递归
- `expanded`: 已继续展开并确认内部结构
- `shell`: metadata 或实例壳层，内部还有真实可见结构
- `skipped`: 明确不在当前边界内
- `unknown`: 还需进一步读取

## Notes

- 对实例节点，优先补内部真实结构，不要只记录 metadata 外框。
- 如果 metadata 与内部真实壳层不一致，备注里明确写清差异。
- 关键状态节点单独标注，方便后续写状态矩阵。
- `Child count` 取自当前 metadata 读取结果，用来判断是否还能继续递归。
- `Terminal` 只有在 child count 为 `0` 时才能标记为 `yes`。
- 对 `instance` 等 shell-capable 节点，`Terminal = yes` 还必须有 `Expansion basis` 和 `Completion proof`，不能只靠 metadata 无子节点。
- `Expanded` 不是是否存在子节点，而是是否已经继续读到实现所需的真实可见层级。
- 如果某个关键节点没有展开，必须在 `Reason if not expanded` 里说明为什么当前仍然可以继续。
