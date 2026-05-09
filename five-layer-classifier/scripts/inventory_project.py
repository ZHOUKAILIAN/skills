#!/usr/bin/env python3
"""Build a file ledger for five-layer project classification.

The script does not classify files. It creates a deterministic inventory so the
agent can account for scope before applying the five-layer model.
"""

from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path
from typing import Iterable


DEFAULT_EXCLUDE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    ".DS_Store",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "dist",
    "build",
    "coverage",
    ".next",
    ".nuxt",
    ".turbo",
    ".cache",
    ".parcel-cache",
}

TEXT_EXTS = {
    ".md",
    ".mdx",
    ".txt",
    ".rst",
    ".json",
    ".jsonc",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".vue",
    ".py",
    ".sh",
    ".css",
    ".scss",
    ".html",
    ".xml",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a file inventory for five-layer classification."
    )
    parser.add_argument("paths", nargs="*", default=["."], help="Files or directories to scan.")
    parser.add_argument("--root", default=".", help="Root used for relative paths.")
    parser.add_argument("--format", choices=("markdown", "csv"), default="markdown")
    parser.add_argument("--out", help="Write output to this file instead of stdout.")
    parser.add_argument(
        "--include-hidden",
        action="store_true",
        help="Include hidden files and directories except explicit excludes.",
    )
    parser.add_argument(
        "--exclude-dir",
        action="append",
        default=[],
        help="Additional directory name to exclude. Repeat as needed.",
    )
    parser.add_argument(
        "--max-heading-bytes",
        type=int,
        default=32768,
        help="Bytes to inspect when finding the first Markdown heading.",
    )
    return parser.parse_args()


def is_hidden(path: Path) -> bool:
    return any(part.startswith(".") and part not in (".", "..") for part in path.parts)


def iter_files(paths: Iterable[Path], root: Path, excludes: set[str], include_hidden: bool) -> list[Path]:
    files: list[Path] = []
    for raw_path in paths:
        path = raw_path if raw_path.is_absolute() else root / raw_path
        if not path.exists():
            continue
        if path.is_file():
            if include_hidden or not is_hidden(path.relative_to(root) if path.is_relative_to(root) else path):
                files.append(path.resolve())
            continue
        for dirpath, dirnames, filenames in os.walk(path):
            current = Path(dirpath)
            dirnames[:] = [
                name
                for name in sorted(dirnames)
                if name not in excludes and (include_hidden or not name.startswith("."))
            ]
            for filename in sorted(filenames):
                file_path = current / filename
                if not include_hidden and filename.startswith("."):
                    continue
                files.append(file_path.resolve())
    return sorted(set(files), key=lambda p: str(p))


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def first_heading(path: Path, max_bytes: int) -> str:
    if path.suffix.lower() not in TEXT_EXTS:
        return ""
    try:
        data = path.read_bytes()[:max_bytes]
    except OSError:
        return ""
    if b"\x00" in data:
        return ""
    try:
        text = data.decode("utf-8", errors="replace")
    except UnicodeDecodeError:
        return ""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped[:120]
    return ""


def path_signals(relative_path: str) -> str:
    parts = set(Path(relative_path).parts)
    signals: list[str] = []
    if {"src", "app", "pages", "components", "api"} & parts:
        signals.append("implementation")
    if {"test", "tests", "__tests__", "e2e", "spec"} & parts:
        signals.append("tests")
    if {"docs", "documentation"} & parts:
        signals.append("docs")
    if {"tasks", "tickets", "issues"} & parts:
        signals.append("task-state")
    if {"tmp", "temp", "scratch", "logs"} & parts:
        signals.append("local-or-research")
    if {"coordination", "governance", "rules", "workflow"} & parts:
        signals.append("governance")
    if {"archive", "research", "discussion"} & parts:
        signals.append("research")
    return ",".join(signals)


def rows(files: list[Path], root: Path, max_heading_bytes: int) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    for file_path in files:
        relative = rel(file_path, root)
        try:
            size = str(file_path.stat().st_size)
        except OSError:
            size = "?"
        result.append(
            {
                "path": relative,
                "bytes": size,
                "ext": file_path.suffix.lower(),
                "signals": path_signals(relative),
                "first_heading": first_heading(file_path, max_heading_bytes),
            }
        )
    return result


def to_markdown(data: list[dict[str, str]]) -> str:
    lines = [
        "| path | bytes | ext | signals | first_heading |",
        "| --- | ---: | --- | --- | --- |",
    ]
    for row in data:
        values = [
            row["path"],
            row["bytes"],
            row["ext"],
            row["signals"],
            row["first_heading"],
        ]
        escaped = [value.replace("|", "\\|").replace("\n", " ") for value in values]
        lines.append("| " + " | ".join(escaped) + " |")
    return "\n".join(lines) + "\n"


def to_csv(data: list[dict[str, str]]) -> str:
    from io import StringIO

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=["path", "bytes", "ext", "signals", "first_heading"])
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    excludes = DEFAULT_EXCLUDE_DIRS | set(args.exclude_dir)
    paths = [Path(p) for p in args.paths]
    files = iter_files(paths, root, excludes, args.include_hidden)
    data = rows(files, root, args.max_heading_bytes)
    text = to_markdown(data) if args.format == "markdown" else to_csv(data)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
