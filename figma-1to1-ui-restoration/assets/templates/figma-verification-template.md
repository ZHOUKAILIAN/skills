# {{date}} Figma Node `{{root_node}}` Verification

## Scope

- Figma file: `{{file_key}}`
- Root node: `{{root_node}}`
- Compared implementation: {{implementation_target}}
- States in scope: {{states_in_scope}}

## Acceptance Thresholds

| Check | Threshold |
| --- | --- |
| Terminal coverage | `100%` |
| Vertical closure | `pass` |
| Key geometry tolerance | `{{geometry_tolerance}}` |
| CSS best practices | `css-best-practices satisfied; positioning exceptions justified` |
| Component reuse | `existing interaction component owners recorded; new behavior-heavy UI justified` |
| State coverage | `100%` |
| Visual diff status | `pass` |

## Structure Check

| Item | Result | Evidence |
| --- | --- | --- |
| Boundary coverage | {{boundary_result}} | {{boundary_evidence}} |
| Terminal coverage | {{terminal_result}} | {{terminal_evidence}} |
| Shell handling | {{shell_result}} | {{shell_evidence}} |

## Geometry Check

| Assertion | Expected | Actual | Tolerance | Result |
| --- | --- | --- | --- | --- |
| Top inset | `{{expected_top_inset}}` | `{{actual_top_inset}}` | `{{top_inset_tolerance}}` | {{top_inset_result}} |
| Bottom inset | `{{expected_bottom_inset}}` | `{{actual_bottom_inset}}` | `{{bottom_inset_tolerance}}` | {{bottom_inset_result}} |
| Main gap | `{{expected_main_gap}}` | `{{actual_main_gap}}` | `{{main_gap_tolerance}}` | {{main_gap_result}} |
| CTA size | `{{expected_cta_size}}` | `{{actual_cta_size}}` | `{{cta_tolerance}}` | {{cta_result}} |

## CSS Best Practices Check

| Item | Expected | Actual | Result |
| --- | --- | --- | --- |
| Flow layout | {{expected_flow_layout}} | {{actual_flow_layout}} | {{flow_layout_result}} |
| Absolute/fixed positioning | {{expected_positioning_scope}} | {{actual_positioning_scope}} | {{positioning_result}} |
| Positioning rationale | {{expected_positioning_reason}} | {{actual_positioning_reason}} | {{positioning_reason_result}} |

## Content Check

| Item | Expected | Actual | Result |
| --- | --- | --- | --- |
| Title text | {{expected_title}} | {{actual_title}} | {{title_result}} |
| Typography | {{expected_typography}} | {{actual_typography}} | {{typography_result}} |
| Asset wiring | {{expected_assets}} | {{actual_assets}} | {{asset_result}} |

## Interaction Component Reuse Check

| Candidate | Expected owner or extension path | Actual implementation decision | Result | Notes |
| --- | --- | --- | --- | --- |
| `{{reuse_candidate_1}}` | {{reuse_expected_1}} | {{reuse_actual_1}} | {{reuse_result_1}} | {{reuse_notes_1}} |
| `{{reuse_candidate_2}}` | {{reuse_expected_2}} | {{reuse_actual_2}} | {{reuse_result_2}} | {{reuse_notes_2}} |

## State Coverage Check

| State | Implemented | Verified | Notes |
| --- | --- | --- | --- |
| {{state_1}} | {{state_1_implemented}} | {{state_1_verified}} | {{state_1_notes}} |
| {{state_2}} | {{state_2_implemented}} | {{state_2_verified}} | {{state_2_notes}} |
| {{state_3}} | {{state_3_implemented}} | {{state_3_verified}} | {{state_3_notes}} |

## Visual Diff Check

| State | Figma source | Implementation source | Viewport / crop | Diff result | Notes |
| --- | --- | --- | --- | --- | --- |
| {{diff_state_1}} | {{figma_image_1}} | {{impl_image_1}} | {{viewport_rule_1}} | {{diff_result_1}} | {{diff_notes_1}} |
| {{diff_state_2}} | {{figma_image_2}} | {{impl_image_2}} | {{viewport_rule_2}} | {{diff_result_2}} | {{diff_notes_2}} |

## Commands Run

- {{command_1}}
- {{command_2}}
- {{command_3}}

## Final Outcome

- Meets `99% restored` threshold: {{final_threshold_result}}
- Blocking failures: {{blocking_failures}}
- Remaining risk: {{remaining_risk}}
