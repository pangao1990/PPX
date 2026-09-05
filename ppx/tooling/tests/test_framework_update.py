import json
import hashlib
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from ppx_py.commands import update
from ppx_py.commands.update import IncompatibleUpdate, UpdateError, UpdatePlan, apply_plan, make_plan
from ppx_py.project import read_lock
from ppx_py import Settings


ROOT = Path(__file__).resolve().parents[3]
MANIFEST = json.loads((ROOT / "ppx-update.json").read_text(encoding="utf-8"))


class FrameworkUpdateTests(unittest.TestCase):
    def test_compatible_manifest_creates_plan(self):
        settings = Settings.load(ROOT / "ppx.toml")
        plan = make_plan(settings, read_lock(ROOT), MANIFEST)
        self.assertEqual(plan.target, "6.0.0")
        self.assertFalse(plan.needed)

    def test_same_release_repairs_package_version_drift(self):
        settings = Settings.load(ROOT / "ppx.toml")
        lock = json.loads(json.dumps(read_lock(ROOT)))
        lock["framework"]["javascript"] = "5.9.0"
        plan = make_plan(settings, lock, MANIFEST)
        self.assertTrue(plan.needed)

    def test_downgrade_is_rejected(self):
        settings = Settings.load(ROOT / "ppx.toml")
        manifest = json.loads(json.dumps(MANIFEST))
        manifest["releaseVersion"] = "5.9.0"
        manifest["packages"] = {key: "5.9.0" for key in manifest["packages"]}
        with self.assertRaises(IncompatibleUpdate):
            make_plan(settings, read_lock(ROOT), manifest)

    def test_update_channel_must_match(self):
        settings = Settings.load(ROOT / "ppx.toml")
        manifest = dict(MANIFEST, channel="beta")
        with self.assertRaises(IncompatibleUpdate):
            make_plan(settings, read_lock(ROOT), manifest)

    def test_manifest_asset_requires_and_verifies_sha256(self):
        content = json.dumps(MANIFEST).encode("utf-8")
        digest = "sha256:" + hashlib.sha256(content).hexdigest()
        release = SimpleNamespace(
            raise_for_status=lambda: None,
            json=lambda: {
                "tag_name": "v6.0.0",
                "assets": [{
                    "name": "ppx-update.json",
                    "browser_download_url": "https://example.test/manifest",
                    "digest": digest,
                }],
            },
        )
        manifest = SimpleNamespace(raise_for_status=lambda: None, content=content)
        with patch.object(update.httpx, "get", side_effect=[release, manifest]):
            self.assertEqual(update.fetch_manifest("https://example.test/latest"), MANIFEST)

        release_without_digest = SimpleNamespace(
            raise_for_status=lambda: None,
            json=lambda: {
                "tag_name": "v6.0.0",
                "assets": [{
                    "name": "ppx-update.json",
                    "browser_download_url": "https://example.test/manifest",
                }],
            },
        )
        with patch.object(update.httpx, "get", return_value=release_without_digest):
            with self.assertRaises(update.UpdateError):
                update.fetch_manifest("https://example.test/latest")

    def test_incompatible_manifest_is_rejected(self):
        settings = Settings.load(ROOT / "ppx.toml")
        manifest = dict(MANIFEST)
        manifest["requires"] = dict(MANIFEST["requires"], pythonApi="7.0")
        with self.assertRaises(IncompatibleUpdate):
            make_plan(settings, read_lock(ROOT), manifest)

    def test_check_and_dry_run_never_apply_plan(self):
        manifest = json.loads(json.dumps(MANIFEST))
        manifest["releaseVersion"] = "6.1.0"
        manifest["packages"] = {key: "6.1.0" for key in manifest["packages"]}
        for mode in ("check", "dry_run"):
            args = SimpleNamespace(check=mode == "check", dry_run=mode == "dry_run", to=None)
            with patch.object(update, "find_project_root", return_value=ROOT), patch.object(
                update, "fetch_manifest", return_value=manifest
            ), patch.object(update, "apply_plan") as apply:
                self.assertEqual(update.run(args), 0)
                apply.assert_not_called()

    def test_apply_only_changes_framework_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "api").mkdir()
            (root / "gui" / "src").mkdir(parents=True)
            (root / "ppx" / "assets").mkdir(parents=True)
            (root / "api" / "api.py").write_text("business = True\n", encoding="utf-8")
            (root / "gui" / "src" / "main.js").write_text("// user code\n", encoding="utf-8")
            (root / "gui" / "package.json").write_text('{"dependencies": {}}\n', encoding="utf-8")
            (root / "ppx.toml").write_text((ROOT / "ppx.toml").read_text(encoding="utf-8"), encoding="utf-8")
            (root / "ppx.lock").write_text((ROOT / "ppx.lock").read_text(encoding="utf-8"), encoding="utf-8")
            (root / "ppx" / "assets" / "logo.png").write_bytes(b"user")
            plan = UpdatePlan("6.0.0", "6.1.0", "6.1.0", "6.1.0", "6.0", "6.0", "1")
            with patch("ppx_py.commands.update._run"):
                apply_plan(root, plan)
            self.assertEqual((root / "api" / "api.py").read_text(encoding="utf-8"), "business = True\n")
            self.assertEqual((root / "gui" / "src" / "main.js").read_text(encoding="utf-8"), "// user code\n")
            self.assertEqual((root / "ppx" / "assets" / "logo.png").read_bytes(), b"user")
            self.assertEqual(read_lock(root)["framework"]["python"], "6.1.0")
            self.assertIn('python = "6.1.0"', (root / "ppx.toml").read_text(encoding="utf-8"))

    def test_failed_update_restores_configured_frontend_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "api").mkdir()
            (root / "webui" / "src").mkdir(parents=True)
            (root / "ppx" / "assets").mkdir(parents=True)
            config = (ROOT / "ppx.toml").read_text(encoding="utf-8").replace(
                'frontend = "gui"', 'frontend = "webui"'
            )
            (root / "ppx.toml").write_text(config, encoding="utf-8")
            (root / "ppx.lock").write_text((ROOT / "ppx.lock").read_text(encoding="utf-8"), encoding="utf-8")
            frontend_manifest = root / "webui" / "package.json"
            frontend_manifest.write_text('{"dependencies": {}}\n', encoding="utf-8")
            original = frontend_manifest.read_bytes()
            plan = UpdatePlan("6.0.0", "6.1.0", "6.1.0", "6.1.0", "6.0", "6.0", "1")
            calls = 0

            def fail_during_javascript_update(_command, _root):
                nonlocal calls
                calls += 1
                if calls == 2:
                    frontend_manifest.write_text('{"dependencies":{"ppx-js":"6.1.0"}}\n', encoding="utf-8")
                    raise UpdateError("simulated failure")

            with patch("ppx_py.commands.update._run", side_effect=fail_during_javascript_update), patch(
                "ppx_py.commands.update.subprocess.run", return_value=SimpleNamespace(returncode=0)
            ):
                with self.assertRaises(UpdateError):
                    apply_plan(root, plan)
            self.assertEqual(frontend_manifest.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
