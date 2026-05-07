# Classification Report Template

Use this template for final artifacts. Keep rows concise; put uncertainty in `理由 / 风险` instead of hiding it.

## Scope

- Mode:
- Root:
- Paths:
- Purpose:
- Public/private policy:
- Source inputs inspected:
- Exclusions:

## File-Level Classification Table

| 路径 | 主层级 | 所属域 | 是否正式真理源 | 默认承载边界 | public 历史 | 动作建议 | 理由 / 风险 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `path/to/file` | 第一层 / 第二层 / 第三层 / 第四层 / 第五层 / 五层之外 / 待拆分 | 产品域 / 项目桥接域 / 工程复用域 / 研究材料 / 待定 | 是 / 否 / needs policy | 产品仓 / 控制仓正式区 / 本地控制区 / 研究归档 / 待拆分 / needs policy | 可 / 否 / 脱敏后 / needs policy | 保留 / 迁移 / 拆分 / 降级 / 本地保留 / 不正式化 / needs human decision | one-sentence reason |

Use `待拆分` when one file carries multiple primary responsibilities. Use `needs human decision` when policy, ownership, or canonical status cannot be determined from available sources.

## High-Risk Misclassification List

| 对象 | 风险 | 建议 |
| --- | --- | --- |
| `path` | e.g. Layer 5 live handoff looks like a governance doc | keep local; do not promote without explicit adoption |

## Stable Formal Entries

- Product definition entries:
- Current implementation reality entries:
- Project landing entries:
- Shared governance entries:

## Migration, Split, And Retention Recommendations

- Migrate:
- Split:
- Downgrade:
- Keep local:
- Archive as research:
- Do not formalize yet:

## Agent Guide

- Read first:
- Trust as product definition:
- Trust as current runtime reality:
- Trust as shared governance:
- Use only for current local continuity:
- Write back to:
- Do not write back to:

## Proof Package

- In-scope files or groups:
- Classified:
- Excluded:
- Blocked / needs human decision:
- Verification checks:
- Red-line findings:
- Policy gaps:
