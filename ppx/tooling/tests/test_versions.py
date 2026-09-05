import json
import unittest
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


ROOT = Path(__file__).resolve().parents[3]


class VersionTests(unittest.TestCase):
    def test_v6_release_versions_are_aligned(self):
        with (ROOT / "ppx.toml").open("rb") as stream:
            config = tomllib.load(stream)
        with (ROOT / "ppx/packages/ppx-py/pyproject.toml").open("rb") as stream:
            python_version = tomllib.load(stream)["project"]["version"]
        versions = {
            config["project"]["version"],
            config["framework"]["python"],
            config["framework"]["javascript"],
            json.loads((ROOT / "package.json").read_text(encoding="utf-8"))["version"],
            json.loads((ROOT / "gui/package.json").read_text(encoding="utf-8"))["version"],
            json.loads((ROOT / "ppx/packages/ppx-js/package.json").read_text(encoding="utf-8"))["version"],
            python_version,
        }
        self.assertEqual(versions, {"6.0.0"})


if __name__ == "__main__":
    unittest.main()
