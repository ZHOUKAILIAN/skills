"""Temporary-fixture tests; these do not evaluate agent behavior."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from validate_skill import validate


SCRIPT = Path(__file__).with_name("validate_skill.py")


class ValidateSkillTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "example-skill"
        self.root.mkdir()
        self.metadata = {"name": "example-skill", "description": "Use when testing skills."}
        self.write_json()
        self.write_frontmatter('description: "Use when testing skills."')

    def write_json(self):
        (self.root / "skill.json").write_text(json.dumps(self.metadata), encoding="utf-8")

    def write_frontmatter(self, description):
        (self.root / "SKILL.md").write_text(
            f"---\nname: example-skill\n{description}\n---\n\n# Example\n",
            encoding="utf-8",
        )

    def assert_issue(self, text, assets=None):
        self.assertTrue(any(text in error for error in validate(self.root, assets or [])))

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), *map(str, args)],
            capture_output=True, text=True, check=False,
        )

    def test_supported_yaml_scalars_and_surrounding_whitespace(self):
        for description in (
            "description: Use when testing skills.",
            'description: "Use when testing skills."',
            "description: 'Use when testing skills.'",
            "description: |\n  Use when testing skills.",
            "description: >\n  Use when\n  testing skills.",
        ):
            with self.subTest(description=description):
                self.write_frontmatter(description)
                self.assertEqual(validate(self.root, []), [])

    def test_invalid_json_and_yaml(self):
        (self.root / "skill.json").write_text("{", encoding="utf-8")
        self.write_frontmatter("description: [")
        self.assert_issue("skill.json:")
        self.assert_issue("SKILL.md:")

    def test_duplicate_yaml_keys(self):
        for field in (
            'name: other-skill\nname: example-skill',
            'description: Other\ndescription: Use when testing skills.',
            'sub_skills: [other]\nsub_skills: []',
        ):
            with self.subTest(field=field):
                (self.root / "SKILL.md").write_text(
                    f"---\n{field}\n---\n", encoding="utf-8",
                )
                self.assert_issue("duplicate metadata key")

    def test_duplicate_json_keys(self):
        for field in ("name", "description", "sub_skills"):
            with self.subTest(field=field):
                (self.root / "skill.json").write_text(
                    f'{{"{field}": "first", "{field}": "last"}}', encoding="utf-8",
                )
                self.assert_issue("duplicate metadata key")

    def test_yaml_merge_override_is_not_an_explicit_duplicate(self):
        (self.root / "SKILL.md").write_text(
            "---\ndefaults: &defaults\n  description: Default description\n"
            "<<: *defaults\nname: example-skill\ndescription: Use when testing skills.\n---\n",
            encoding="utf-8",
        )
        self.assertEqual(validate(self.root, []), [])

    def test_json_nonfinite_constants(self):
        for value in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(value=value):
                (self.root / "skill.json").write_text(
                    f'{{"extra": {value}}}', encoding="utf-8",
                )
                self.assert_issue("invalid JSON constant")

    def test_unsafe_yaml_tags_are_rejected(self):
        self.write_frontmatter("description: !!python/object:builtins.str {}")
        self.assert_issue("SKILL.md")

    def test_missing_delimiters_or_mapping(self):
        for text in ("name: example-skill", "---\nname: example-skill", "---\n[]\n---"):
            with self.subTest(text=text):
                (self.root / "SKILL.md").write_text(text, encoding="utf-8")
                self.assert_issue("SKILL.md")

    def test_non_object_json(self):
        (self.root / "skill.json").write_text("[]", encoding="utf-8")
        self.assert_issue("metadata must be an object")

    def test_missing_files_and_directory(self):
        (self.root / "SKILL.md").unlink()
        self.assert_issue("SKILL.md")
        self.assertTrue(validate(self.root / "absent", []))
        self.assertTrue(validate(self.root / "skill.json", []))

    def test_invalid_utf8(self):
        (self.root / "SKILL.md").write_bytes(b"\xff")
        self.assert_issue("SKILL.md")

    def test_metadata_mismatch(self):
        self.metadata["description"] = "Use when something else happens."
        self.metadata["name"] = "other-skill"
        self.write_json()
        self.assert_issue("description: SKILL.md and skill.json differ")
        self.assert_issue("name does not match directory")

    def test_empty_and_non_string_fields(self):
        for value in (None, "", "   ", 12, []):
            with self.subTest(value=value):
                self.metadata["description"] = value
                self.write_json()
                self.assert_issue("description must be a non-empty string")

    def test_dependency_shape(self):
        for value in (None, "other-skill", {}, [12], ["../other"], ["/absolute"], [""]):
            with self.subTest(value=value):
                self.metadata["sub_skills"] = value
                self.write_json()
                self.assert_issue("sub_skills")

    def test_duplicate_and_self_dependencies(self):
        self.metadata["sub_skills"] = ["external-skill", "external-skill", "example-skill"]
        self.write_json()
        self.assert_issue("duplicate dependency")
        self.assert_issue("cannot depend on itself")

    def test_external_dependency_is_not_an_availability_failure(self):
        self.metadata["sub_skills"] = ["not-installed-here"]
        self.write_json()
        self.assertEqual(validate(self.root, []), [])

    def test_selected_assets_only(self):
        assets = self.root / "assets"
        assets.mkdir()
        (assets / "template.md").write_text("Template", encoding="utf-8")
        with (self.root / "SKILL.md").open("a", encoding="utf-8") as stream:
            stream.write("Example, not bundled: `scripts/example-only.py`\n")
        self.assertEqual(validate(self.root, ["assets", "assets/template.md"]), [])
        self.assert_issue("Asset", ["missing.md"])
        self.assertEqual(validate(self.root, []), [])

    def test_asset_traversal_absolute_root_and_symlink_escape(self):
        outside = Path(self.temp.name) / "outside.md"
        outside.write_text("Outside", encoding="utf-8")
        (self.root / "escape.md").symlink_to(outside)
        for value in ("", ".", "../outside.md", str(outside), "escape.md"):
            with self.subTest(value=value):
                self.assert_issue("Asset", [value])

    def test_cli_exit_codes_and_limits(self):
        result = self.run_cli(self.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("structural only", result.stdout)
        self.assertIn("dependency availability", result.stdout)
        result = self.run_cli(self.root, "--asset", "missing.md")
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL:", result.stderr)
        self.assertEqual(self.run_cli().returncode, 2)

    def test_missing_yaml_dependency_is_a_tooling_error(self):
        result = subprocess.run(
            [sys.executable, "-S", str(SCRIPT), str(self.root)],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("PyYAML", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_validation_does_not_change_target(self):
        before = {p.name: p.read_bytes() for p in self.root.iterdir()}
        self.assertEqual(self.run_cli(self.root).returncode, 0)
        after = {p.name: p.read_bytes() for p in self.root.iterdir()}
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
