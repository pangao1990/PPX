import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from ppx_py.scaffold import create_project, initialize_project


ROOT = Path(__file__).resolve().parents[3]


class ProjectStructureTests(unittest.TestCase):
    def test_repository_has_three_clear_source_directories(self):
        for relative in ("api", "gui", "ppx"):
            self.assertTrue((ROOT / relative).is_dir(), relative)
        for legacy in ("app", "packages", "pyapp", "resources", "tooling", "main.py"):
            self.assertFalse((ROOT / legacy).exists(), legacy)
        for relative in ("assets", "packages/ppx-py", "packages/ppx-js", "tooling/tests"):
            self.assertTrue((ROOT / "ppx" / relative).exists(), relative)

    def test_new_project_exposes_no_framework_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = create_project("Clear Demo", directory)
            directories = sorted(path.name for path in root.iterdir() if path.is_dir() and not path.name.startswith("."))
            self.assertEqual(directories, ["api", "gui", "ppx"])
            self.assertEqual(sorted(path.name for path in (root / "ppx").iterdir()), ["assets"])
            self.assertEqual(
                sorted(path.name for path in (root / "ppx/assets").iterdir()),
                ["dmg-background.png", "logo.icns", "logo.ico", "logo.png"],
            )
            self.assertFalse((root / "main.py").exists())
            self.assertFalse((root / "packages").exists())
            self.assertFalse((root / "tooling").exists())

    def test_new_project_supports_vanilla_vue_and_react_templates(self):
        cases = {
            "vanilla": ("src/main.js", set()),
            "vue": ("src/App.vue", {"vue"}),
            "react": ("src/App.jsx", {"react", "react-dom"}),
        }
        for frontend, (source, framework_dependencies) in cases.items():
            with self.subTest(frontend=frontend), tempfile.TemporaryDirectory() as directory:
                root = create_project("Template Demo", directory, frontend)
                package = json.loads((root / "gui/package.json").read_text(encoding="utf-8"))
                self.assertTrue((root / "gui" / source).is_file())
                self.assertEqual(set(package["dependencies"]) - {"ppx-js"}, framework_dependencies)
                self.assertEqual(package["dependencies"]["ppx-js"], "6.0.0")

    def test_init_installs_only_business_dependencies_then_frontend(self):
        with tempfile.TemporaryDirectory() as directory:
            root = create_project("Init Demo", directory)
            (root / "api/requirements.txt").write_text("numpy==2.0.0\n", encoding="utf-8")
            with patch("ppx_py.scaffold.subprocess.run", return_value=SimpleNamespace(returncode=0)) as run, patch(
                "ppx_py.commands.doctor.run", return_value=0
            ) as doctor:
                self.assertEqual(initialize_project(root), 0)
            self.assertEqual(run.call_count, 2)
            self.assertEqual(run.call_args_list[0].args[0][1:4], ["-m", "pip", "install"])
            self.assertEqual(run.call_args_list[1].args[0], ["pnpm", "install"])
            doctor.assert_called_once()


if __name__ == "__main__":
    unittest.main()
