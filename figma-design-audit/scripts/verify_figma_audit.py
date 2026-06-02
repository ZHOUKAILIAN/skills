#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


README_REQUIRED_HEADINGS = [
    "## Boundary and Scope",
    "## Restoration Manifest",
    "## Source Priority",
    "## Source Conflict Register",
    "## Blocking Questions",
    "## Node Classification and Handling",
    "## Derived Spacing",
    "## Vertical Closure Check",
    "## Horizontal Closure Check",
    "## CSS Handoff Values",
    "## State Matrix",
    "## State Discovery Ledger",
    "## Business Logic Source Map",
    "## Shared Component Impact",
    "## Shell vs Real Visible Bounds",
    "## Unexpanded Nodes",
    "## Verification Summary",
    "## Current Read Outcome",
]

README_REQUIRED_OUTCOME_KEYS = [
    "Boundary coverage:",
    "Terminal-node coverage:",
    "Derived spacing coverage:",
    "Vertical closure:",
    "Horizontal closure:",
    "State-matrix coverage:",
    "Business logic source coverage:",
    "Restoration manifest coverage:",
    "Source conflicts:",
    "Shared component impact review:",
    "Non-renderable review:",
    "Critical unknowns:",
    "CSS handoff values:",
    "Remaining uncertainty:",
    "Blocking questions:",
    "Ready for implementation:",
]

READY_VALUES = {"yes", "true", "ready"}
DECLARED_CLEAR_VALUES = {"none", "no", "0", "zero", "resolved", "all resolved", "cleared", "empty"}
CLEAR_OR_NON_BLOCKING_VALUES = DECLARED_CLEAR_VALUES | {"non-blocking", "non-blocking only", "documented non-blocking", "n/a", "na", "not applicable"}
UNRESOLVED_TOKENS = ("{{", "unknown", "unexpanded", "blocked", "tbd", "todo", "fixme")

LEDGER_REQUIRED_COLUMNS = [
    "Node ID",
    "Parent",
    "Name",
    "Type",
    "Relative x",
    "Relative y",
    "w",
    "h",
    "Depth",
    "Classification",
    "Handling decision",
    "Status",
    "Child count",
    "Terminal",
    "Expanded",
    "Expansion basis",
    "Reason if not expanded",
    "Completion proof",
    "Note",
]

READ_STATUSES = {"read"}
BLOCKED_READ_STATUSES = {"blocked", "unreadable", "unexpanded", "unknown"}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def read_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SystemExit(f"Could not read {path}: {exc}") from exc


def parse_outcome_value(readme_text: str, label: str) -> str | None:
    pattern = re.compile(rf"-\s+{re.escape(label)}\s*(.+)")
    match = pattern.search(readme_text)
    return match.group(1).strip() if match else None


def normalize_value(value: str | None) -> str | None:
    return value.lower().strip() if value is not None else None


def has_unresolved_token(text: str) -> bool:
    lowered = text.lower()
    return any(token in lowered for token in UNRESOLVED_TOKENS)


def validate_readme(readme_text: str) -> list[str]:
    errors: list[str] = []

    for heading in README_REQUIRED_HEADINGS:
        require(heading in readme_text, f"README is missing heading: {heading}", errors)

    for key in README_REQUIRED_OUTCOME_KEYS:
        require(key in readme_text, f"README is missing outcome key: {key}", errors)

    terminal_coverage = parse_outcome_value(readme_text, "Terminal-node coverage:")
    vertical_closure = parse_outcome_value(readme_text, "Vertical closure:")
    horizontal_closure = parse_outcome_value(readme_text, "Horizontal closure:")
    implementation_ready = parse_outcome_value(readme_text, "Ready for implementation:")
    blocking_questions = parse_outcome_value(readme_text, "Blocking questions:")
    state_coverage = parse_outcome_value(readme_text, "State-matrix coverage:")
    business_logic_source_coverage = parse_outcome_value(readme_text, "Business logic source coverage:")
    manifest_coverage = parse_outcome_value(readme_text, "Restoration manifest coverage:")
    source_conflicts = parse_outcome_value(readme_text, "Source conflicts:")
    shared_component_impact = parse_outcome_value(readme_text, "Shared component impact review:")
    non_renderable_review = parse_outcome_value(readme_text, "Non-renderable review:")
    critical_unknowns = parse_outcome_value(readme_text, "Critical unknowns:")
    css_handoff_values = parse_outcome_value(readme_text, "CSS handoff values:")
    remaining_uncertainty = parse_outcome_value(readme_text, "Remaining uncertainty:")

    require(terminal_coverage is not None, "README is missing terminal coverage value", errors)
    require(vertical_closure is not None, "README is missing vertical closure value", errors)
    require(horizontal_closure is not None, "README is missing horizontal closure value", errors)
    require(state_coverage is not None, "README is missing state-matrix coverage value", errors)
    require(business_logic_source_coverage is not None, "README is missing business logic source coverage value", errors)
    require(manifest_coverage is not None, "README is missing restoration manifest coverage value", errors)
    require(source_conflicts is not None, "README is missing source conflicts value", errors)
    require(shared_component_impact is not None, "README is missing shared component impact review value", errors)
    require(non_renderable_review is not None, "README is missing non-renderable review value", errors)
    require(critical_unknowns is not None, "README is missing critical unknowns value", errors)
    require(css_handoff_values is not None, "README is missing CSS handoff values value", errors)
    require(remaining_uncertainty is not None, "README is missing remaining uncertainty value", errors)
    require(blocking_questions is not None, "README is missing blocking questions value", errors)
    require(implementation_ready is not None, "README is missing implementation readiness value", errors)

    if implementation_ready and normalize_value(implementation_ready) in READY_VALUES:
        require(
            terminal_coverage is not None and terminal_coverage.lower() in {"100%", "yes", "complete", "all terminal"},
            "README cannot mark implementation ready unless terminal coverage is complete",
            errors,
        )
        require(
            vertical_closure is not None and vertical_closure.lower() in {"pass", "passed", "yes", "closed"},
            "README cannot mark implementation ready unless vertical closure passed",
            errors,
        )
        require(
            horizontal_closure is not None and horizontal_closure.lower() in {"pass", "passed", "yes", "closed"},
            "README cannot mark implementation ready unless horizontal closure passed",
            errors,
        )
        require(
            state_coverage is not None and state_coverage.lower() in {"100%", "yes", "complete", "all states covered"},
            "README cannot mark implementation ready unless state-matrix coverage is complete",
            errors,
        )
        require(
            business_logic_source_coverage is not None
            and business_logic_source_coverage.lower() in {"100%", "yes", "complete", "all mapped"},
            "README cannot mark implementation ready unless business logic source coverage is complete",
            errors,
        )
        require(
            manifest_coverage is not None and manifest_coverage.lower() in {"100%", "yes", "complete", "single boundary", "all mapped"},
            "README cannot mark implementation ready unless restoration manifest coverage is complete or single-boundary",
            errors,
        )
        require(
            source_conflicts is not None and normalize_value(source_conflicts) in CLEAR_OR_NON_BLOCKING_VALUES,
            "README cannot mark implementation ready unless Figma, PRD, code, and business-source conflicts are resolved or explicitly non-blocking",
            errors,
        )
        require(
            shared_component_impact is not None
            and shared_component_impact.lower() in {"100%", "yes", "complete", "not applicable", "n/a", "all reviewed"},
            "README cannot mark implementation ready unless shared component impact is reviewed or not applicable",
            errors,
        )
        require(
            non_renderable_review is not None and non_renderable_review.lower() in {"100%", "yes", "complete", "all reviewed"},
            "README cannot mark implementation ready unless non-renderable nodes are reviewed",
            errors,
        )
        require(
            critical_unknowns is not None and critical_unknowns.lower() in {"none", "no", "0", "zero"},
            "README cannot mark implementation ready unless critical unknowns are cleared",
            errors,
        )
        require(
            css_handoff_values is not None and css_handoff_values.lower() in {"100%", "yes", "complete", "all captured", "ready"},
            "README cannot mark implementation ready unless CSS handoff values are captured",
            errors,
        )
        require(
            remaining_uncertainty is not None and normalize_value(remaining_uncertainty) in CLEAR_OR_NON_BLOCKING_VALUES,
            "README cannot mark implementation ready unless remaining uncertainty is cleared or explicitly non-blocking",
            errors,
        )
        require(
            blocking_questions is not None and normalize_value(blocking_questions) in DECLARED_CLEAR_VALUES,
            "README cannot mark implementation ready unless blocking questions are cleared",
            errors,
        )

        # Ready artifacts should not carry unresolved placeholders or blocker tokens.
        for label, value in {
            "terminal coverage": terminal_coverage,
            "vertical closure": vertical_closure,
            "horizontal closure": horizontal_closure,
            "state coverage": state_coverage,
            "business logic source coverage": business_logic_source_coverage,
            "manifest coverage": manifest_coverage,
            "source conflicts": source_conflicts,
            "shared component impact": shared_component_impact,
            "non-renderable review": non_renderable_review,
            "critical unknowns": critical_unknowns,
            "CSS handoff values": css_handoff_values,
            "remaining uncertainty": remaining_uncertainty,
            "blocking questions": blocking_questions,
        }.items():
            require(
                value is not None and not has_unresolved_token(value),
                f"README cannot mark implementation ready unless {label} is resolved and free of placeholder tokens",
                errors,
            )

    return errors


def extract_ledger_header(ledger_text: str) -> str | None:
    for line in ledger_text.splitlines():
        if line.strip().startswith("| Node ID |"):
            return line
    return None


def extract_ledger_rows(ledger_text: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in ledger_text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("| `"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        rows.append(cells)
    return rows


def clean_cell(value: str) -> str:
    return value.strip().strip("`").strip()


def ledger_node_ids(ledger_text: str) -> set[str]:
    return {clean_cell(cells[0]) for cells in extract_ledger_rows(ledger_text) if cells and clean_cell(cells[0])}


def read_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise SystemExit(f"Could not read {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Could not parse JSON {path}: {exc}") from exc


def snapshot_nodes(snapshot: object) -> list[dict[str, object]]:
    if not isinstance(snapshot, dict):
        return []
    raw_nodes = snapshot.get("nodes", [])
    if not isinstance(raw_nodes, list):
        return []
    return [node for node in raw_nodes if isinstance(node, dict)]


def node_id(node: dict[str, object]) -> str:
    value = node.get("id", node.get("node_id", ""))
    return str(value).strip()


def node_visible(node: dict[str, object]) -> bool:
    if "visible" in node:
        return bool(node.get("visible"))
    if "visibility" in node:
        return str(node.get("visibility", "")).strip().lower() not in {"false", "hidden", "invisible"}
    return True


def node_read_status(node: dict[str, object]) -> str:
    return str(node.get("read_status", node.get("status", ""))).strip().lower()


def node_parent_id(node: dict[str, object]) -> str:
    return str(node.get("parent_id", "")).strip()


def node_child_ids(node: dict[str, object]) -> list[str] | None:
    value = node.get("child_ids")
    if not isinstance(value, list):
        return None
    return [str(item).strip() for item in value if str(item).strip()]


def node_child_count(node: dict[str, object]) -> int | None:
    value = node.get("child_count")
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    return None


def root_node_id(snapshot: object, nodes: list[dict[str, object]]) -> str:
    if isinstance(snapshot, dict):
        root = str(snapshot.get("root_node", "")).strip()
        if root:
            return root
    for node in nodes:
        if not node_parent_id(node):
            return node_id(node)
    return ""


def reachable_node_ids(*, root_id: str, by_id: dict[str, dict[str, object]]) -> set[str]:
    if root_id not in by_id:
        return set()
    visited: set[str] = set()
    stack = [root_id]
    while stack:
        current_id = stack.pop()
        if current_id in visited:
            continue
        visited.add(current_id)
        node = by_id.get(current_id)
        if node is None:
            continue
        child_ids = node_child_ids(node) or []
        stack.extend(child_id for child_id in child_ids if child_id in by_id and child_id not in visited)
    return visited


def validate_snapshot(snapshot_text: object, ledger_text: str) -> list[str]:
    errors: list[str] = []
    nodes = snapshot_nodes(snapshot_text)
    require(bool(nodes), "Figma snapshot must contain a non-empty nodes array", errors)

    by_id = {node_id(node): node for node in nodes if node_id(node)}
    expected_ids = {node_id(node) for node in nodes if node_id(node) and node_visible(node)}
    actual_ids = ledger_node_ids(ledger_text)
    missing_ids = sorted(expected_ids - actual_ids)
    require(not missing_ids, "Ledger is missing visible Figma snapshot nodes: " + ", ".join(missing_ids), errors)

    blocked_nodes = sorted(
        node_id(node)
        for node in nodes
        if node_id(node) and node_visible(node) and node_read_status(node) in BLOCKED_READ_STATUSES
    )
    require(not blocked_nodes, "Figma snapshot contains unreadable visible nodes: " + ", ".join(blocked_nodes), errors)

    non_read_nodes = sorted(
        node_id(node)
        for node in nodes
        if node_id(node) and node_visible(node) and node_read_status(node) not in READ_STATUSES
    )
    require(not non_read_nodes, "Figma snapshot visible nodes must have read_status=read: " + ", ".join(non_read_nodes), errors)

    duplicate_ids = sorted(
        node_id(node)
        for node in nodes
        if node_id(node) and sum(1 for other in nodes if node_id(other) == node_id(node)) > 1
    )
    require(not duplicate_ids, "Figma snapshot contains duplicate node ids: " + ", ".join(sorted(set(duplicate_ids))), errors)

    for node in nodes:
        current_id = node_id(node)
        if not current_id or not node_visible(node):
            continue
        child_ids = node_child_ids(node)
        child_count = node_child_count(node)
        require(child_ids is not None, f"Figma snapshot node {current_id} must include child_ids", errors)
        require(child_count is not None, f"Figma snapshot node {current_id} must include child_count", errors)
        if child_ids is None or child_count is None:
            continue
        require(
            child_count == len(child_ids),
            f"Figma snapshot node {current_id} child_count does not match child_ids length",
            errors,
        )
        missing_children = sorted(child_id for child_id in child_ids if child_id not in by_id)
        require(
            not missing_children,
            f"Figma snapshot node {current_id} child_ids missing from snapshot: " + ", ".join(missing_children),
            errors,
        )
        for child_id in child_ids:
            child = by_id.get(child_id)
            if child is None:
                continue
            require(
                node_parent_id(child) == current_id,
                f"Figma snapshot child {child_id} parent_id does not point back to {current_id}",
                errors,
            )

    root_id = root_node_id(snapshot_text, nodes)
    require(bool(root_id), "Figma snapshot must include root_node or one parentless root node", errors)
    require(root_id in by_id, f"Figma snapshot root_node is not present in nodes: {root_id}", errors)
    reachable_ids = reachable_node_ids(root_id=root_id, by_id=by_id)
    unreachable_visible = sorted(expected_ids - reachable_ids)
    require(
        not unreachable_visible,
        "Figma snapshot visible nodes are not reachable from root_node through child_ids: "
        + ", ".join(unreachable_visible),
        errors,
    )
    return errors


def validate_ledger(ledger_text: str, implementation_ready: bool) -> list[str]:
    errors: list[str] = []
    header = extract_ledger_header(ledger_text)
    require(header is not None, "Ledger is missing the node table header", errors)

    if header is not None:
        for column in LEDGER_REQUIRED_COLUMNS:
            require(f"| {column} " in header or header.endswith(f"| {column} |"), f"Ledger is missing column: {column}", errors)

    require("Child count" in ledger_text, "Ledger does not mention child count", errors)
    require("Classification" in ledger_text, "Ledger does not mention node classification", errors)
    require("Handling decision" in ledger_text, "Ledger does not mention handling decision", errors)
    require("Terminal" in ledger_text, "Ledger does not mention terminal status", errors)
    require("Expansion basis" in ledger_text, "Ledger does not mention expansion basis", errors)
    require("Completion proof" in ledger_text, "Ledger does not mention completion proof", errors)
    require("blocked" in ledger_text.lower(), "Ledger does not mention blocked status", errors)

    rows = extract_ledger_rows(ledger_text)
    require(bool(rows), "Ledger must contain at least one node row", errors)

    if implementation_ready:
        for row_number, cells in enumerate(rows, start=1):
            row_text = " | ".join(cells)
            require(
                "{{" not in row_text,
                f"Ledger row {row_number} cannot contain template placeholders when implementation is ready",
                errors,
            )
            require(
                not re.search(r"\b(unknown|unexpanded|blocked|tbd|todo|fixme)\b", row_text, re.IGNORECASE),
                f"Ledger row {row_number} cannot contain unresolved or blocked markers when implementation is ready",
                errors,
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Figma audit contract files.")
    parser.add_argument("--readme", required=True, type=Path, help="Path to README.md audit file")
    parser.add_argument("--ledger", required=True, type=Path, help="Path to ALL_CHILD_NODES.md audit file")
    parser.add_argument(
        "--figma-snapshot",
        required=True,
        type=Path,
        help="Path to figma-node-snapshot.json containing every in-scope visible Figma node read during traversal",
    )
    args = parser.parse_args()

    readme_text = read_file(args.readme)
    ledger_text = read_file(args.ledger)
    snapshot_text = read_json(args.figma_snapshot)
    implementation_ready = normalize_value(parse_outcome_value(readme_text, "Ready for implementation:")) in READY_VALUES

    errors = validate_readme(readme_text)
    errors.extend(validate_ledger(ledger_text, implementation_ready=implementation_ready))
    errors.extend(validate_snapshot(snapshot_text, ledger_text))

    if errors:
        for error in errors:
            fail(error)
        return 1

    print("PASS: audit contract verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
