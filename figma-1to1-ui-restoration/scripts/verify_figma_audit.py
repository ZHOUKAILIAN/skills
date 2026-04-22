#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


README_REQUIRED_HEADINGS = [
    "## Boundary and Scope",
    "## Node Classification and Handling",
    "## Derived Spacing",
    "## Vertical Closure Check",
    "## State Matrix",
    "## Existing Interaction Component Inventory",
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
    "State-matrix coverage:",
    "Existing interaction component reuse:",
    "Non-renderable review:",
    "Critical unknowns:",
    "Ready for implementation:",
]

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
    "Status",
    "Child count",
    "Terminal",
    "Expanded",
    "Expansion basis",
    "Reason if not expanded",
    "Completion proof",
    "Note",
]


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


def validate_readme(readme_text: str) -> list[str]:
    errors: list[str] = []

    for heading in README_REQUIRED_HEADINGS:
        require(heading in readme_text, f"README is missing heading: {heading}", errors)

    for key in README_REQUIRED_OUTCOME_KEYS:
        require(key in readme_text, f"README is missing outcome key: {key}", errors)

    terminal_coverage = parse_outcome_value(readme_text, "Terminal-node coverage:")
    vertical_closure = parse_outcome_value(readme_text, "Vertical closure:")
    implementation_ready = parse_outcome_value(readme_text, "Ready for implementation:")
    state_coverage = parse_outcome_value(readme_text, "State-matrix coverage:")
    component_reuse = parse_outcome_value(readme_text, "Existing interaction component reuse:")
    non_renderable_review = parse_outcome_value(readme_text, "Non-renderable review:")
    critical_unknowns = parse_outcome_value(readme_text, "Critical unknowns:")

    require(terminal_coverage is not None, "README is missing terminal coverage value", errors)
    require(vertical_closure is not None, "README is missing vertical closure value", errors)
    require(state_coverage is not None, "README is missing state-matrix coverage value", errors)
    require(component_reuse is not None, "README is missing interaction component reuse value", errors)
    require(non_renderable_review is not None, "README is missing non-renderable review value", errors)
    require(critical_unknowns is not None, "README is missing critical unknowns value", errors)
    require(implementation_ready is not None, "README is missing implementation readiness value", errors)

    if implementation_ready and implementation_ready.lower() in {"yes", "true", "ready"}:
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
            state_coverage is not None and state_coverage.lower() in {"100%", "yes", "complete", "all states covered"},
            "README cannot mark implementation ready unless state-matrix coverage is complete",
            errors,
        )
        require(
            component_reuse is not None
            and component_reuse.lower() not in {"missing", "unknown", "unreviewed", "tbd"},
            "README cannot mark implementation ready unless interaction component reuse is reviewed or marked not applicable",
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

    return errors


def extract_ledger_header(ledger_text: str) -> str | None:
    for line in ledger_text.splitlines():
        if line.strip().startswith("| Node ID |"):
            return line
    return None


def validate_ledger(ledger_text: str) -> list[str]:
    errors: list[str] = []
    header = extract_ledger_header(ledger_text)
    require(header is not None, "Ledger is missing the node table header", errors)

    if header is not None:
        for column in LEDGER_REQUIRED_COLUMNS:
            require(f"| {column} " in header or header.endswith(f"| {column} |"), f"Ledger is missing column: {column}", errors)

    require("Child count" in ledger_text, "Ledger does not mention child count", errors)
    require("Terminal" in ledger_text, "Ledger does not mention terminal status", errors)
    require("Expansion basis" in ledger_text, "Ledger does not mention expansion basis", errors)
    require("Completion proof" in ledger_text, "Ledger does not mention completion proof", errors)

    row_pattern = re.compile(r"^\| `.+` \|", re.MULTILINE)
    rows = row_pattern.findall(ledger_text)
    require(bool(rows), "Ledger must contain at least one node row", errors)

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Figma audit contract files.")
    parser.add_argument("--readme", required=True, type=Path, help="Path to README.md audit file")
    parser.add_argument("--ledger", required=True, type=Path, help="Path to ALL_CHILD_NODES.md audit file")
    args = parser.parse_args()

    readme_text = read_file(args.readme)
    ledger_text = read_file(args.ledger)

    errors = validate_readme(readme_text)
    errors.extend(validate_ledger(ledger_text))

    if errors:
        for error in errors:
            fail(error)
        return 1

    print("PASS: audit contract verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
