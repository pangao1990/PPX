import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from ppx_py import Application, BridgeError, Settings
from ppx_py.services import SystemService


ROOT = Path(__file__).resolve().parents[3]


class FakeEvent:
    def __iadd__(self, _handler):
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
        self.events = SimpleNamespace(shown=FakeEvent())

    def create_file_dialog(self, **options):
        self.dialog_options = options
        return ("/tmp/report.pdf",)

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


if __name__ == "__main__":
    unittest.main()
