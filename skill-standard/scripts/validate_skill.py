#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["PyYAML>=6,<7"]
# ///
"""Read-only structural checks; not a semantic or behavioral skill evaluator."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML 6.x is required; use a compatible environment or uv run this script.", file=sys.stderr)
    raise SystemExit(2) from None


# Skill dependencies are names, not filesystem paths. Do not impose a lowercase
# naming convention on existing external skills.
NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*\Z")


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        try:
            if key in result:
                raise ValueError(f"duplicate metadata key: {key!r}")
            result[key] = value
        except TypeError:
            raise ValueError("metadata mapping keys must be hashable scalars") from None
    return result


class UniqueKeyLoader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        # Reject explicit duplicates before SafeLoader expands YAML merges.
        # A local value overriding a merged default remains valid YAML.
        keys = []
        for key_node, _ in node.value:
            key = (
                "<<" if key_node.tag == "tag:yaml.org,2002:merge"
                else self.construct_object(key_node, deep=deep)
            )
            keys.append((key, None))
        unique_pairs(keys)
        return super().construct_mapping(node, deep=deep)


def reject_constant(value):
    raise ValueError(f"invalid JSON constant: {value}")


def json_metadata(text: str) -> dict:
    return json.loads(text, object_pairs_hook=unique_pairs, parse_constant=reject_constant)


def frontmatter(text: str) -> dict:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("SKILL.md must start with a YAML frontmatter delimiter")
    try:
        end = lines.index("---", 1)
    except ValueError:
        raise ValueError("SKILL.md has no closing frontmatter delimiter") from None
    result = yaml.load("\n".join(lines[1:end]), Loader=UniqueKeyLoader)
    if not isinstance(result, dict):
        raise ValueError("SKILL.md frontmatter must be a mapping")
    return result


def validate(skill_dir: Path, assets: list[str]) -> list[str]:
    errors: list[str] = []
    try:
        root = skill_dir.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        return [f"Cannot resolve skill directory: {exc}"]
    if not root.is_dir():
        return [f"Not a skill directory: {skill_dir}"]

    documents = {}
    for filename, parser in (("SKILL.md", frontmatter), ("skill.json", json_metadata)):
        try:
            data = parser((root / filename).read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise ValueError("metadata must be an object/mapping")
            documents[filename] = data
        except (OSError, UnicodeError, ValueError, yaml.YAMLError) as exc:
            errors.append(f"{filename}: {exc}")

    for filename, data in documents.items():
        for key in ("name", "description"):
            value = data.get(key)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{filename}: {key} must be a non-empty string")
        name = data.get("name")
        if isinstance(name, str):
            if not NAME.fullmatch(name):
                errors.append(f"{filename}: name must be a plain skill name")
            if name != root.name:
                errors.append(f"{filename}: name does not match directory {root.name!r}")

    if len(documents) == 2:
        for key in ("name", "description"):
            left, right = (data.get(key) for data in documents.values())
            if isinstance(left, str) and isinstance(right, str) and left.strip() != right.strip():
                errors.append(f"{key}: SKILL.md and skill.json differ")

    dependencies = documents.get("skill.json", {}).get("sub_skills", [])
    if not isinstance(dependencies, list):
        errors.append("skill.json: sub_skills must be a list of skill names")
    else:
        seen = set()
        for dependency in dependencies:
            if not isinstance(dependency, str) or not NAME.fullmatch(dependency):
                errors.append("skill.json: each sub_skills entry must be a plain skill name")
                continue
            if dependency in seen:
                errors.append(f"skill.json: duplicate dependency {dependency!r}")
            if dependency == documents.get("skill.json", {}).get("name"):
                errors.append("skill.json: a skill cannot depend on itself")
            seen.add(dependency)

    for asset in assets:
        relative = Path(asset)
        if not asset or relative.is_absolute() or ".." in relative.parts:
            errors.append(f"Asset must be skill-local without parent traversal: {asset!r}")
            continue
        try:
            target = (root / relative).resolve(strict=True)
            if target == root or root not in target.parents:
                errors.append(f"Asset must stay inside the skill directory: {asset!r}")
        except (OSError, RuntimeError) as exc:
            errors.append(f"Asset {asset!r}: {exc}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_dir", type=Path, help="Target skill directory")
    parser.add_argument(
        "--asset", action="append", default=[], metavar="RELATIVE_PATH",
        help="Actual declared asset to check; repeat for multiple assets",
    )
    args = parser.parse_args()
    errors = validate(args.skill_dir, args.asset)
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"PASS (structural only): {args.skill_dir}; {len(args.asset)} selected asset(s)")
    print("Not checked: unselected assets, dependency availability, semantics, agent behavior.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
