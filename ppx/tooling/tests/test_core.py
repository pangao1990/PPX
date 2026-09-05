import asyncio
import json
import io
import math
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from ppx_py import Bridge, BridgeError, Settings, SettingsError, api_method, app_data_path, resource_path
from ppx_py.commands import doctor
from ppx_py.commands.doctor import Check
from ppx_py.storage import JsonStorage


ROOT = Path(__file__).resolve().parents[3]


class ExampleAPI:
    @api_method("example.add")
    def add(self, left, right):
        return left + right

    @api_method("example.bug")
    def bug(self):
        raise TypeError("internal implementation detail")

    @api_method("example.asyncAdd")
    async def async_add(self, left, right):
        await asyncio.sleep(0)
        return left + right

    @api_method("example.invalidResult")
    def invalid_result(self):
        return {1, 2, 3}


class BridgeTests(unittest.TestCase):
    def test_dispatches_registered_api_and_wraps_result(self):
        bridge = Bridge()
        bridge.register_api(ExampleAPI())
        result = bridge.call("example.add", {"left": 2, "right": 3}, "request-1")
        self.assertEqual(result, {"ok": True, "data": 5, "error": None, "requestId": "request-1"})

    def test_unknown_method_has_stable_error_shape(self):
        result = Bridge().call("missing.method", request_id="request-2")
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "METHOD_NOT_FOUND")
        self.assertEqual(result["requestId"], "request-2")

    def test_invalid_parameters_are_reported(self):
        bridge = Bridge()
        bridge.register_api(ExampleAPI())
        result = bridge.call("example.add", "bad")
        self.assertEqual(result["error"]["code"], "INVALID_PARAMS")

    def test_type_error_inside_business_method_is_not_misreported_or_exposed(self):
        bridge = Bridge()
        bridge.register_api(ExampleAPI())
        with self.assertLogs("ppx_py.bridge", level="ERROR"):
            result = bridge.call("example.bug")
        self.assertEqual(result["error"]["code"], "INTERNAL_ERROR")
        self.assertEqual(result["error"]["message"], "Python API 执行失败")

    def test_async_business_method_works_with_or_without_a_running_loop(self):
        bridge = Bridge()
        bridge.register_api(ExampleAPI())
        self.assertEqual(bridge.call("example.asyncAdd", [2, 3])["data"], 5)

        async def invoke_from_loop():
            return bridge.call("example.asyncAdd", {"left": 4, "right": 5})

        self.assertEqual(asyncio.run(invoke_from_loop())["data"], 9)

    def test_non_json_business_result_has_stable_error(self):
        bridge = Bridge()
        bridge.register_api(ExampleAPI())
        result = bridge.call("example.invalidResult", request_id="invalid-result")
        self.assertEqual(result["error"], {
            "code": "INVALID_RESULT",
            "message": "Python API 返回值必须是可序列化的 JSON 数据",
        })
        self.assertEqual(result["requestId"], "invalid-result")


class SettingsAndStorageTests(unittest.TestCase):
    def test_loads_v6_project(self):
        settings = Settings.load(ROOT / "ppx.toml")
        self.assertEqual(settings.project.version, "6.0.0")
        self.assertEqual(settings.project.project_format, 6)
        self.assertTrue(settings.window.resizable)
        self.assertEqual(settings.window.background_color, "#FFFFFF")

    def test_rejects_v5_project(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ppx.toml"
            path.write_text(
                "[project]\nname='x'\nslug='x'\nversion='5.0.0'\nidentifier='test'\ndeveloper='x'\nformat=5\n",
                encoding="utf-8",
            )
            with self.assertRaises(SettingsError):
                Settings.load(path)

    def test_rejects_invalid_release_critical_settings(self):
        original = (ROOT / "ppx.toml").read_text(encoding="utf-8")
        invalid_values = (
            ('name = "PPX"', 'name = "CON"'),
            ('slug = "ppx"', 'slug = "Bad/Slug"'),
            ('identifier = "vip.pangao"', 'identifier = "../escape"'),
            ('developer = "PanGao"', 'developer = "bad\\nvalue"'),
            ('windowsAppId = "F35003AB-441A-C0A6-4527-937E6A02F789"', 'windowsAppId = ""'),
            ('version = "6.0.0"', 'version = "not a version"'),
            ('widthRatio = 0.6667', 'widthRatio = 1.1'),
            ('widthRatio = 0.6667', 'widthRatio = true'),
            ('port = 5173', 'port = 70000'),
            ('filename = "storage-v6.json"', 'filename = "../storage.json"'),
            ('format = 6', 'format = "six"'),
            ('python = "6.0.0"', 'python = "broken"'),
            ('channel = "stable"', 'channel = "unknown"'),
            ('pythonApi = "6.0"', 'pythonApi = ""'),
            ('enabled = true', 'enabled = "false"'),
            ('backgroundColor = "#FFFFFF"', 'backgroundColor = "white"'),
        )
        for old, new in invalid_values:
            with self.subTest(value=new), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "ppx.toml"
                path.write_text(original.replace(old, new, 1), encoding="utf-8")
                with self.assertRaises(SettingsError):
                    Settings.load(path)

    def test_business_paths_are_stable_and_reject_traversal(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            resources = root / "resources"
            resources.mkdir()
            sample = resources / "model.dat"
            sample.write_bytes(b"model")
            settings = SimpleNamespace(resource_dir=resources, app_data_dir=root / "data")
            with patch("ppx_py.paths.Settings.load", return_value=settings):
                self.assertEqual(resource_path("model.dat"), sample.resolve())
                self.assertEqual(app_data_path("cache/result.json"), (root / "data/cache/result.json").resolve())
                self.assertTrue((root / "data").is_dir())
                with self.assertRaises(ValueError):
                    resource_path("../secret")
                with self.assertRaises(FileNotFoundError):
                    resource_path("missing.dat")

    def test_empty_platform_data_environment_uses_home_fallback(self):
        settings = Settings.load(ROOT / "ppx.toml")
        with patch("ppx_py.settings.platform.system", return_value="Linux"), patch.dict(
            os.environ, {"XDG_DATA_HOME": ""}
        ), patch("ppx_py.settings.Path.home", return_value=Path("/home/tester")):
            self.assertEqual(
                settings.app_data_dir,
                Path("/home/tester/.local/share/vip.pangao.ppx"),
            )
        with patch("ppx_py.settings.platform.system", return_value="Windows"), patch.dict(
            os.environ, {"APPDATA": ""}
        ), patch("ppx_py.settings.Path.home", return_value=Path("C:/Users/tester")):
            self.assertEqual(
                settings.app_data_dir,
                Path("C:/Users/tester/AppData/Roaming/vip.pangao.ppx"),
            )

    def test_storage_can_save_before_window_shown(self):
        with tempfile.TemporaryDirectory() as directory:
            storage = JsonStorage(Path(directory) / "nested" / "storage.json")
            storage.set("note", "saved before shown")
            storage.initialize()
            self.assertEqual(storage.get("note"), "saved before shown")

    def test_json_storage_persists_values_atomically(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "storage.json"
            storage = JsonStorage(path)
            storage.initialize()
            self.assertTrue(storage.set("theme", {"dark": True}))
            self.assertEqual(storage.get("theme"), {"dark": True})
            self.assertFalse(Path(str(path) + ".part").exists())
            self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["theme"], {"dark": True})

            for invalid in ({1, 2}, math.nan):
                with self.subTest(invalid=invalid), self.assertRaisesRegex(
                    BridgeError, "标准 JSON"
                ):
                    storage.set("invalid", invalid)
            with self.assertRaisesRegex(BridgeError, "存储键必须是字符串"):
                storage.set(1, "value")
            self.assertNotIn("invalid", json.loads(path.read_text(encoding="utf-8")))


class DoctorTests(unittest.TestCase):
    def test_pnpm_version_range_rejects_next_major(self):
        self.assertTrue(doctor._in_range("11.25.0", "11.0.0", "12.0.0"))
        self.assertFalse(doctor._in_range("10.9.0", "11.0.0", "12.0.0"))
        self.assertFalse(doctor._in_range("12.0.0", "11.0.0", "12.0.0"))
        self.assertFalse(doctor._in_range("unknown", "11.0.0", "12.0.0"))

    def test_json_output_is_machine_readable(self):
        output = io.StringIO()
        checks = [Check(True, "Python", "3.11"), Check(False, "ppx-js", "未安装")]
        with patch.object(doctor, "find_project_root", return_value=ROOT), patch.object(
            doctor, "collect_checks", return_value=checks
        ), redirect_stdout(output):
            result = doctor.run(SimpleNamespace(json_output=True))
        payload = json.loads(output.getvalue())
        self.assertEqual(result, 1)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["summary"], {"passed": 1, "failed": 1, "total": 2})
        self.assertEqual(payload["checks"][1]["name"], "ppx-js")

    def test_json_output_remains_valid_when_project_loading_fails(self):
        output = io.StringIO()
        with patch.object(doctor, "find_project_root", side_effect=FileNotFoundError("missing")), redirect_stdout(output):
            result = doctor.run(SimpleNamespace(json_output=True))
        payload = json.loads(output.getvalue())
        self.assertEqual(result, 1)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["checks"][0]["name"], "项目")


if __name__ == "__main__":
    unittest.main()
