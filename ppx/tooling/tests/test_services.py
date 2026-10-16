import sys
import os
import unittest
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from ppx_py import Application, BridgeError, Settings
from ppx_py.services import SystemService


ROOT = Path(__file__).resolve().parents[3]


class FakeEvent:
    def __init__(self):
        self.handlers = []

    def __iadd__(self, _handler):
        self.handlers.append(_handler)
        return self


class FakeWindow:
    x = 10
    y = 20
    width = 800
    height = 600
    on_top = False

    def __init__(self):
        self.actions = []
        self.dialog_options = None
        self.events = SimpleNamespace(shown=FakeEvent(), before_show=FakeEvent())

    def create_file_dialog(self, **options):
        self.dialog_options = options
        return "/tmp/report.pdf" if not options.get("allow_multiple", False) else ("/tmp/report.pdf",)

    def __getattr__(self, name):
        if name in {"minimize", "maximize", "restore", "toggle_fullscreen", "destroy"}:
            return lambda: self.actions.append(name)
        raise AttributeError(name)


class SystemServiceTests(unittest.TestCase):
    def setUp(self):
        self.window = FakeWindow()
        self.service = SystemService(SimpleNamespace(), lambda: self.window)

    def test_save_dialog_returns_selected_path(self):
        fake_webview = SimpleNamespace(SAVE_DIALOG=20)
        with patch.dict(sys.modules, {"webview": fake_webview}):
            result = self.service.save_file_dialog(
                filename="report.pdf",
                directory="/tmp",
                file_types=["PDF (*.pdf)"],
            )
        self.assertEqual(result, "/tmp/report.pdf")
        self.assertEqual(self.window.dialog_options, {
            "dialog_type": 20,
            "directory": "/tmp",
            "save_filename": "report.pdf",
            "file_types": ("PDF (*.pdf)",),
        })

    def test_open_dialog_can_select_one_or_multiple_files(self):
        fake_webview = SimpleNamespace(OPEN_DIALOG=10)
        with patch.dict(sys.modules, {"webview": fake_webview}):
            result = self.service.open_file_dialog(multiple=False)
        self.assertEqual(result[0]["filename"], "report.pdf")
        self.assertFalse(self.window.dialog_options["allow_multiple"])
        self.assertEqual(len(result), 1)
        with patch.dict(sys.modules, {"webview": fake_webview}):
            self.assertEqual(len(self.service.open_file_dialog(multiple=True)), 1)

        with self.assertRaisesRegex(BridgeError, "multiple 必须是布尔值"):
            self.service.open_file_dialog(multiple="false")

    def test_window_state_and_controls(self):
        self.assertEqual(self.service.get_window_state(), {
            "x": 10, "y": 20, "width": 800, "height": 600, "onTop": False,
        })
        for action in (
            self.service.minimize_window,
            self.service.maximize_window,
            self.service.restore_window,
            self.service.toggle_fullscreen,
            self.service.close_window,
        ):
            self.assertTrue(action())
        self.assertEqual(self.window.actions, [
            "minimize", "maximize", "restore", "toggle_fullscreen", "destroy",
        ])

    def test_cancelled_native_dialogs_return_empty_values(self):
        with patch.object(self.window, "create_file_dialog", return_value=None):
            self.assertEqual(self.service.open_file_dialog(), [])
            self.assertEqual(self.service.select_directory(), "")
            self.assertEqual(self.service.save_file_dialog(), "")

    def test_empty_path_does_not_open_current_working_directory(self):
        for value in ("", "  ", None, 42):
            with self.subTest(value=value), self.assertRaises(BridgeError):
                self.service.open_path(value)

    def test_application_registers_desktop_apis_and_applies_window_settings(self):
        settings = Settings.load(ROOT / "ppx.toml")
        application = Application(settings)
        expected = {
            "system.saveFileDialog", "window.getState", "window.minimize", "window.maximize",
            "window.restore", "window.toggleFullscreen", "window.close",
        }
        self.assertTrue(expected.issubset(application.bridge._methods))

        options = {}

        def create_window(**kwargs):
            options.update(kwargs)
            return self.window

        fake_webview = SimpleNamespace(
            screens=[SimpleNamespace(width=1200, height=800)],
            create_window=create_window,
            start=lambda **_kwargs: None,
        )
        with patch.dict(sys.modules, {"webview": fake_webview}):
            application.run(dev=True)
        exposed = [name for name in dir(options["js_api"]) if not name.startswith("_")]
        self.assertEqual(exposed, ["call"])
        self.assertTrue(options["js_api"].call("system.getAppInfo")["ok"])
        self.assertTrue(options["resizable"])
        self.assertFalse(options["fullscreen"])
        self.assertFalse(options["on_top"])
        self.assertFalse(options["confirm_close"])
        self.assertEqual(options["background_color"], "#FFFFFF")

    def test_linux_software_rendering_is_opt_in_and_preserves_environment(self):
        settings = Settings.load(ROOT / "ppx.toml")
        settings = replace(settings, application=replace(settings.application, single_instance=False))
        fake_webview = SimpleNamespace(
            screens=[SimpleNamespace(width=1200, height=800)],
            create_window=lambda **_kwargs: FakeWindow(), start=lambda **_kwargs: None,
        )
        for enabled in (False, True):
            configured = replace(settings, window=replace(settings.window, software_rendering=enabled))
            with patch.dict(sys.modules, {"webview": fake_webview}), patch(
                "ppx_py.application.platform.system", return_value="Linux"
            ), patch.dict(os.environ):
                os.environ.pop("WEBKIT_DISABLE_COMPOSITING_MODE", None)
                os.environ.pop("WEBKIT_DISABLE_DMABUF_RENDERER", None)
                Application(configured).run(dev=True)
                self.assertEqual(os.environ.get("WEBKIT_DISABLE_COMPOSITING_MODE"), "1" if enabled else None)
                self.assertEqual(os.environ.get("WEBKIT_DISABLE_DMABUF_RENDERER"), "1" if enabled else None)
        configured = replace(settings, window=replace(settings.window, software_rendering=True))
        with patch.dict(sys.modules, {"webview": fake_webview}), patch(
            "ppx_py.application.platform.system", return_value="Linux"
        ), patch.dict(os.environ, {"WEBKIT_DISABLE_DMABUF_RENDERER": "0"}):
            Application(configured).run(dev=True)
            self.assertEqual(os.environ["WEBKIT_DISABLE_DMABUF_RENDERER"], "0")

    def test_titlebar_workaround_only_runs_before_show_on_macos_26(self):
        settings = Settings.load(ROOT / "ppx.toml")
        settings = replace(settings, application=replace(settings.application, single_instance=False))
        for system, version, expected in (("Darwin", "26.5.2", 1), ("Darwin", "27.0.1", 0), ("Windows", "", 0)):
            window = FakeWindow()
            fake_webview = SimpleNamespace(
                screens=[SimpleNamespace(width=1200, height=800)],
                create_window=lambda **_kwargs: window, start=lambda **_kwargs: None,
            )
            with patch.dict(sys.modules, {"webview": fake_webview}), patch(
                "ppx_py.application.platform.system", return_value=system
            ), patch("ppx_py.application.platform.mac_ver", return_value=(version, (), "")):
                Application(settings).run(dev=True)
            self.assertEqual(len(window.events.before_show.handlers), expected)


if __name__ == "__main__":
    unittest.main()
