import json
from pathlib import Path
import tempfile
import unittest

import catalog
import lesson
import start


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "user/Projects/repo"
        self.registry = catalog.read(catalog.ROOT / "shared/resources.json")
        self.modules = catalog.read(catalog.ROOT / "modules/catalog.json")
        for r in self.registry["resources"]:
            r["scope"] = "repo"
            if r["required"]:
                r["path"] = "fixtures/" + r["id"] + ("" if r["id"] == "learnability-patterns" else "/SKILL.md")
                target = self.repo / r["path"]
                if r["id"] == "learnability-patterns":
                    target.mkdir(parents=True)
                else:
                    target.parent.mkdir(parents=True)
                    target.write_text("Test skill fixture", encoding="utf-8")
        for m in self.modules["modules"]:
            for path in [m["brief"], m["reference"], *[s.get("evidence") for s in m["standards"]]]:
                if path:
                    target = self.repo / path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text("Test reference fixture", encoding="utf-8")
        self.save()

    def save(self):
        lesson.save_json(self.repo / "shared/resources.json", self.registry)
        lesson.save_json(self.repo / "modules/catalog.json", self.modules)

    def test_subject_standard_and_level_filters(self):
        self.assertEqual(len(catalog.select(self.repo, subject="SCIENCE")), 5)
        self.assertEqual([m["id"] for m in catalog.select(self.repo, standard="4-ls1-1")], ["lily-dissection"])
        doctoral = catalog.select(self.repo, subject="statistics", level="doctoral")
        self.assertEqual([m["id"] for m in doctoral], ["psychometrics-statistics"])
        self.assertEqual(doctoral[0]["standards"], [])
        self.assertEqual(catalog.select(self.repo, subject="science", level="doctoral"), [])

    def test_preferences_and_shared_engine_across_levels(self):
        self.modules["modules"][-1]["preferences"]["language"] = "zh"
        self.save()
        advanced = catalog.context("psychometrics-statistics", self.repo)
        lily = catalog.context("lily-dissection", self.repo)
        self.assertEqual(advanced["shared_resources"], lily["shared_resources"])
        self.assertEqual(advanced["preferences"]["language"], "zh")
        self.assertEqual(lily["preferences"]["language"], "en")
        self.assertTrue(advanced["preferences"]["offline"])
        self.assertTrue(advanced["preferences"]["preserve_mathematical_depth"])
        self.assertIsNone(advanced["reference"])
        self.assertEqual(len(advanced["source_sha256"]), 3)

    def test_missing_optional_is_reported_and_required_is_rejected(self):
        self.assertIn("blender", catalog.check(self.repo)["optional_unavailable"])
        self.registry["resources"][0]["path"] = "missing"
        self.save()
        with self.assertRaisesRegex(ValueError, "Required knowledge"):
            catalog.knowledge(self.repo)
        with self.assertRaisesRegex(ValueError, "Required knowledge"):
            catalog.check(self.repo)

    def test_unknown_module_and_resource_fail(self):
        with self.assertRaisesRegex(ValueError, "Unknown module"):
            catalog.context("unknown", self.repo)
        self.modules["modules"][0]["resources"].append("unknown")
        self.save()
        with self.assertRaisesRegex(ValueError, "Unknown resource"):
            catalog.load(self.repo)

    def test_existing_wrong_resource_type_is_unavailable(self):
        skill = next(r for r in self.registry["resources"] if r["id"] == "frontend-design")
        original = skill["path"]
        skill["path"] = str(Path(original).parent)
        self.save()
        with self.assertRaisesRegex(ValueError, "frontend-design"):
            catalog.check(self.repo)
        skill["path"] = original
        self.registry["resources"][0]["path"] = original
        self.save()
        with self.assertRaisesRegex(ValueError, "learnability-patterns"):
            catalog.knowledge(self.repo)

    def test_duplicate_ids_and_missing_evidence_fail(self):
        self.modules["modules"].append(self.modules["modules"][0])
        self.save()
        with self.assertRaisesRegex(ValueError, "duplicate"):
            catalog.load(self.repo)
        self.modules["modules"].pop()
        self.modules["modules"][0]["standards"][0]["evidence"] = "missing.md"
        self.save()
        with self.assertRaisesRegex(ValueError, "Missing standard evidence"):
            catalog.load(self.repo)

    def test_paths_cannot_escape_declared_root(self):
        with self.assertRaisesRegex(ValueError, "escapes"):
            catalog.resolve(self.repo, "repo", "../outside")

    def test_launcher_seeds_doctoral_context_without_lily_and_preserves_reopen(self):
        root = Path(self.temp.name) / "doctoral-workspace"
        start.prepare_workspace(root, self.repo, "psychometrics-statistics")
        packet = lesson.read_json(root / "materials/module-context.json")
        self.assertEqual(packet["module"]["level"], "doctoral")
        self.assertFalse((root / "materials/lily-2d.html").exists())
        self.assertNotIn("grade 4", (root / "preview/index.html").read_text())
        knowledge = lesson.read_json(root / "knowledge.json")
        self.assertEqual(knowledge, catalog.knowledge(self.repo))
        self.assertIn(knowledge["frontend_skill"], knowledge["tool_skills"])
        before = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
        self.registry["defaults"]["language"] = "changed"
        self.save()
        start.prepare_workspace(root, self.repo, "psychometrics-statistics")
        self.assertEqual(before, {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()})
        with self.assertRaisesRegex(ValueError, "Workspace module differs"):
            start.prepare_workspace(root, self.repo, "lily-dissection")
        self.assertEqual(before, {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()})

    def test_existing_unbound_workspace_is_not_silently_migrated(self):
        root = Path(self.temp.name) / "existing"
        lesson.initialize(root)
        with self.assertRaisesRegex(ValueError, "unset"):
            start.prepare_workspace(root, self.repo, "psychometrics-statistics")
        self.assertFalse((root / "materials/module-context.json").exists())
        start.prepare_workspace(root, self.repo)

    def test_lily_keeps_reference_and_does_not_modify_original(self):
        root = Path(self.temp.name) / "lily"
        reference = self.repo / "modules/lily-dissection/index-2d.html"
        before = reference.read_bytes()
        start.prepare_workspace(root, self.repo, "lily-dissection")
        self.assertEqual((root / "materials/lily-2d.html").read_bytes(), before)
        self.assertEqual(reference.read_bytes(), before)

    def test_other_module_reference_preserves_format_without_lily_name(self):
        source = self.repo / "modules/psychometrics-statistics/input.txt"
        source.write_text("Teacher curriculum input", encoding="utf-8")
        self.modules["modules"][-1]["reference"] = str(source.relative_to(self.repo))
        self.save()
        root = Path(self.temp.name) / "advanced-with-input"
        start.prepare_workspace(root, self.repo, "psychometrics-statistics")
        self.assertEqual((root / "materials/module-reference.txt").read_bytes(), source.read_bytes())
        self.assertFalse((root / "materials/lily-2d.html").exists())


if __name__ == "__main__":
    unittest.main()
