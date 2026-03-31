# 20260331 Figma Node `1261:36014` Verification

## Scope

- Figma file: `gmjTw5th1TFPxAd1uzodY2`
- Root node: `1261:36014`
- Compared implementation: audit-only pressure test, no target codebase attached
- States in scope: current popup state with one selected row and two unselected rows

## Acceptance Thresholds

| Check | Threshold |
| --- | --- |
| Terminal coverage | `100%` |
| Vertical closure | `pass` |
| Key geometry tolerance | `<= 1px` |
| State coverage | `100%` |
| Visual diff status | `pass` |

## Structure Check

| Item | Result | Evidence |
| --- | --- | --- |
| Boundary coverage | pass | popup subtree fully enumerated in `ALL_CHILD_NODES.md` |
| Terminal coverage | pass | all in-bound nodes have terminal proof; shell-capable instances expanded with design context |
| Shell handling | pass | `1261:36024`, `1261:36026`, `1261:36027` explicitly recorded as metadata-insufficient shells |

## Geometry Check

| Assertion | Expected | Actual | Tolerance | Result |
| --- | --- | --- | --- | --- |
| Top inset | `16` | `16` | `0` | pass |
| Bottom inset | `126` | `126` | `0` | pass |
| Main gap | `4` | `4` | `0` | pass |
| Row size | `336x68` | `336x68` | `0` | pass |

## Content Check

| Item | Expected | Actual | Result |
| --- | --- | --- | --- |
| Title text | `活动报名` | `活动报名` | pass |
| Typography | title `17/28`, body `15/20` | matches Figma reads | pass |
| Asset wiring | popup shell and row backgrounds present | assets exposed via design context | pass |

## State Coverage Check

| State | Implemented | Verified | Notes |
| --- | --- | --- | --- |
| unselected row | yes in Figma source | yes | `1261:36024` and `1261:36025` |
| selected row | yes in Figma source | yes | `1261:36026` |
| popup title row | yes in Figma source | yes | `1261:36027` |

## Visual Diff Check

| State | Figma source | Implementation source | Viewport / crop | Diff result | Notes |
| --- | --- | --- | --- | --- | --- |
| popup default | Figma screenshot of `1261:36014` | not available | popup subtree crop | pending | no external implementation was attached for screenshot diff |
| row selected | Figma screenshot of selected row inside `1261:36014` | not available | row crop | pending | requires target implementation screenshot |

## Commands Run

- `get_metadata(1261:36014)`
- `get_design_context(1261:36014)`
- `get_design_context(1261:36024)`
- `get_design_context(1261:36026)`
- `get_design_context(1261:36027)`
- `get_screenshot(1261:36014)`

## Final Outcome

- Meets `99% restored` threshold: no
- Blocking failures: no target implementation screenshot or rendered output was attached, so visual diff and implementation-side geometry checks cannot complete
- Remaining risk: audit chain is strong for this popup subtree, but end-to-end fidelity is still unproven without implementation-side verification
