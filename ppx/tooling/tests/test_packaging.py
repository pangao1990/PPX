import os
from types import SimpleNamespace

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ppx_py import Settings
from ppx_py.packaging import create_spec, installer_path, verify_installer
from ppx_py.packaging.installer import _linux, _macos, _windows
from ppx_py.scaffold import create_project


class PackagingTests(unittest.TestCase):
    def test_build_resolves_frontend_launcher_and_propagates_its_exit_code(self):
        from ppx_py.commands import build

        with tempfile.TemporaryDirectory() as directory:
            root = create_project("Build Demo", directory)
            launcher = root / ("pnpm.cmd" if os.name == "nt" else "pnpm")
            launcher.write_text("@exit /b 17\n" if os.name == "nt" else "#!/bin/sh\nexit 17\n", encoding="ascii")
            launcher.chmod(0o755)
            with patch.object(build, "find_project_root", return_value=root), patch.object(
                build.shutil, "which", return_value=str(launcher)
            ), patch.object(build, "create_spec") as spec:
                self.assertEqual(build.run(SimpleNamespace()), 17)
                spec.assert_not_called()

    def test_generates_private_entry_and_platform_specs(self):
        for system, marker in (("Darwin", "BUNDLE("), ("Windows", "COLLECT("), ("Linux", "a.binaries,")):
            with self.subTest(system=system), tempfile.TemporaryDirectory() as directory:
                root = create_project("Demo", directory)
                (root / "gui/dist").mkdir()
                (root / "gui/dist/index.html").write_text("<main></main>\n", encoding="utf-8")
                settings = Settings.load(root / "ppx.toml")
                with patch("ppx_py.packaging.spec.platform.system", return_value=system):
                    spec_path = create_spec(root, settings, console=True)
                spec = spec_path.read_text(encoding="utf-8")
                self.assertIn(marker, spec)
                self.assertIn("console=True", spec)
                self.assertNotIn("collect_submodules('ppx_py')", spec)
                self.assertIn("api.api", spec)
                self.assertIn("excludes=['pygments.formatters.img']", spec)
                self.assertNotIn("excludes=['PIL']", spec)
                self.assertTrue((root / "build/cache/ppx_entry.py").is_file())
                self.assertFalse((root / "main.py").exists())

    def test_expected_installer_names_and_headers(self):
        with tempfile.TemporaryDirectory() as directory:
            root = create_project("Demo", directory)
            settings = Settings.load(root / "ppx.toml")
            for system, ending in (("Darwin", "_macOS.dmg"), ("Windows", "_Windows.exe"), ("Linux", "_Linux.deb")):
                self.assertTrue(str(installer_path(root, settings, system)).endswith(ending))
            windows = root / "windows.exe"
            linux = root / "linux.deb"
            windows.write_bytes(b"MZ" + b"0" * 2048)
            linux.write_bytes(b"!<arch>\n" + b"0" * 2048)
            self.assertEqual(verify_installer(windows, "Windows"), [])
            self.assertEqual(verify_installer(linux, "Linux"), [])

    def test_platform_installer_metadata_is_generated_in_cache(self):
        with tempfile.TemporaryDirectory() as directory:
            root = create_project("Demo", directory)
            settings = Settings.load(root / "ppx.toml")
            (root / "build/Demo").mkdir(parents=True)
            (root / "build/Demo/Demo.exe").write_bytes(b"MZ")
            with patch("ppx_py.packaging.installer._find_iscc", return_value=Path("ISCC.exe")), patch(
                "ppx_py.packaging.installer._run"
            ):
                _windows(root, settings)
            iss = (root / "build/cache/installer.iss").read_text(encoding="utf-8-sig")
            self.assertIn("AppId={{", iss)
            self.assertIn("recursesubdirs", iss)

            (root / "build/Demo/Demo.exe").unlink()
            (root / "build/Demo").rmdir()
            (root / "build/Demo").write_bytes(b"binary")
            with patch("ppx_py.packaging.installer.shutil.which", return_value="/usr/bin/dpkg-deb"), patch(
                "ppx_py.packaging.installer._run"
            ):
                _linux(root, settings)
            control = (root / "build/cache/deb/demo/DEBIAN/control").read_text(encoding="utf-8")
            self.assertIn("Package: demo", control)
            self.assertIn("Version: 0.1.0", control)

            (root / "build/Demo").unlink()
            (root / "build/Demo.app").mkdir()
            with patch("ppx_py.packaging.installer._run"):
                _macos(root, settings)
            dmg = (root / "build/cache/dmg_settings.py").read_text(encoding="utf-8")
            self.assertIn("dmg-background.png", dmg)
            self.assertIn("Applications", dmg)


if __name__ == "__main__":
    unittest.main()
