# {{date}} Figma Node `{{root_node}}` Verification

## Scope

- Figma file: `{{file_key}}`
- Root node: `{{root_node}}`
- Compared implementation: {{implementation_target}}
- States in scope: {{states_in_scope}}
- Manifest item: {{manifest_item}}

## Acceptance Thresholds

| Check | Threshold |
| --- | --- |
| Terminal coverage | `100%` |
| Vertical closure | `pass` |
| Horizontal closure | `pass` |
| Key geometry tolerance | `{{geometry_tolerance}}` |
| CSS handoff values | `geometry evidence captured; CSS primitives owned by css-best-practices` |
| State coverage | `100%` |
| Business logic source coverage | `100% of business-affecting content and branches mapped or explicitly blocked` |
| Shared-component impact review | `complete when shared components were edited` |
| Per-boundary review gate | `PASS or explicitly blocked/accepted` |
| Screenshot support | `not supported; node data and numeric measurements only` |

## Restoration Manifest Gate

| Boundary / state | Figma node | Implementation target | Review gate | Status |
| --- | --- | --- | --- | --- |
| {{manifest_item_1}} | `{{manifest_node_1}}` | {{manifest_target_1}} | {{manifest_review_gate_1}} | {{manifest_status_1}} |
| {{manifest_item_2}} | `{{manifest_node_2}}` | {{manifest_target_2}} | {{manifest_review_gate_2}} | {{manifest_status_2}} |

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

## Closure Check

| Container | Direction | Formula | Expected | Actual | Result |
| --- | --- | --- | --- | --- | --- |
| {{closure_container_1}} | vertical | `{{vertical_formula_1}}` | `{{vertical_expected_1}}` | `{{vertical_actual_1}}` | {{vertical_result_1}} |
| {{closure_container_2}} | horizontal | `{{horizontal_formula_1}}` | `{{horizontal_expected_1}}` | `{{horizontal_actual_1}}` | {{horizontal_result_1}} |

## CSS Best Practices Check

| Item | Expected | Actual | Result |
| --- | --- | --- | --- |
| Flow layout | {{expected_flow_layout}} | {{actual_flow_layout}} | {{flow_layout_result}} |
| Absolute/fixed positioning | {{expected_positioning_scope}} | {{actual_positioning_scope}} | {{positioning_result}} |
| Positioning rationale | {{expected_positioning_reason}} | {{actual_positioning_reason}} | {{positioning_reason_result}} |

## Content Check

| Item | Figma expectation | Business source | Actual | Result |
| --- | --- | --- | --- | --- |
| Title text | {{expected_title}} | {{title_business_source}} | {{actual_title}} | {{title_result}} |
| Typography | {{expected_typography}} | visual source: Figma | {{actual_typography}} | {{typography_result}} |
| Asset wiring | {{expected_assets}} | visual source: Figma or project asset map | {{actual_assets}} | {{asset_result}} |

## Business Logic Source Check

| Item | Figma sample or visual evidence | Required business source | Actual implementation source | Result |
| --- | --- | --- | --- | --- |
| Dynamic text / fields | {{figma_dynamic_text}} | {{expected_dynamic_source}} | {{actual_dynamic_source}} | {{dynamic_source_result}} |
| Lists / counts | {{figma_list_count_sample}} | {{expected_list_count_source}} | {{actual_list_count_source}} | {{list_count_result}} |
| Conditional branches | {{figma_branch_sample}} | {{expected_branch_source}} | {{actual_branch_source}} | {{branch_source_result}} |

## State Coverage Check

| State | Implemented | Verified | Notes |
| --- | --- | --- | --- |
| {{state_1}} | {{state_1_implemented}} | {{state_1_verified}} | {{state_1_notes}} |
| {{state_2}} | {{state_2_implemented}} | {{state_2_verified}} | {{state_2_notes}} |
| {{state_3}} | {{state_3_implemented}} | {{state_3_verified}} | {{state_3_notes}} |

## Integration and Regression Check

| Item | Expected | Actual | Result |
| --- | --- | --- | --- |
| API / PRD behavior | {{expected_api_behavior}} | {{actual_api_behavior}} | {{api_behavior_result}} |
| Existing analogous flow | {{expected_analogous_flow}} | {{actual_analogous_flow}} | {{analogous_flow_result}} |
| Shared component consumers | {{expected_consumer_scope}} | {{actual_consumer_scope}} | {{consumer_scope_result}} |
| Mock usage | {{expected_mock_usage}} | {{actual_mock_usage}} | {{mock_usage_result}} |

## Numeric Measurement Check

| State | Figma numeric source | Implementation measurement source | Measured property | Result | Notes |
| --- | --- | --- | --- | --- | --- |
| {{measure_state_1}} | {{figma_numeric_source_1}} | {{implementation_measurement_source_1}} | {{measured_property_1}} | {{measurement_result_1}} | {{measurement_notes_1}} |
| {{measure_state_2}} | {{figma_numeric_source_2}} | {{implementation_measurement_source_2}} | {{measured_property_2}} | {{measurement_result_2}} | {{measurement_notes_2}} |

## Commands Run

- {{command_1}}
- {{command_2}}
- {{command_3}}

## Final Outcome

- Exact restoration gate: {{final_gate_result}}
- Per-boundary status: {{per_boundary_status}}
- Blocking failures: {{blocking_failures}}
- Business logic source coverage: {{business_logic_source_coverage}}
- Shared-component impact review: {{shared_component_impact_status}}
- Blocking questions: {{blocking_questions_status}}
- Remaining risk: {{remaining_risk}}
