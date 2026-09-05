"""PPX V6 application lifecycle."""

from __future__ import annotations

import mimetypes
from pathlib import Path
from typing import Any, Union

from .bridge import Bridge, JavascriptAPI
from .services import SystemService
from .settings import Settings
from .storage import JsonStorage
from .update import ApplicationUpdater


class Application:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.bridge = Bridge()
        self.window: Any = None
        self.storage = JsonStorage(settings.app_data_dir / settings.storage.filename)
        self.system = SystemService(settings, lambda: self.window)
        self.application_updater = ApplicationUpdater(
            settings, lambda progress: self.bridge.emit("applicationUpdate.progress", progress)
        )
        self._register_core_api()

    @classmethod
    def from_config(cls, path: Union[str, Path] = "ppx.toml") -> "Application":
        return cls(Settings.load(path))

    def register_api(self, api: object) -> "Application":
        self.bridge.register_api(api)
        return self

    def _register_core_api(self) -> None:
        methods = {
            "system.getAppInfo": self.system.get_app_info,
            "system.getOwner": self.system.get_owner,
            "system.openPath": self.system.open_path,
            "system.openFileDialog": self.system.open_file_dialog,
            "system.saveFileDialog": self.system.save_file_dialog,
            "system.selectDirectory": self.system.select_directory,
            "window.getState": self.system.get_window_state,
            "window.minimize": self.system.minimize_window,
            "window.maximize": self.system.maximize_window,
            "window.restore": self.system.restore_window,
            "window.toggleFullscreen": self.system.toggle_fullscreen,
            "window.close": self.system.close_window,
            "storage.get": self.storage.get,
            "storage.set": self.storage.set,
            "storage.delete": self.storage.delete,
            "applicationUpdate.check": self.application_updater.check,
            "applicationUpdate.download": self.application_updater.download,
            "applicationUpdate.cancel": self.application_updater.cancel,
        }
        for name, handler in methods.items():
            self.bridge.register(name, handler)

    def run(self, *, dev: bool = False, cef: bool = False) -> None:
        import webview

        if dev:
            url = f"http://127.0.0.1:{self.settings.development.port}/"
        else:
            url = str(self.settings.frontend_dir / "index.html")
            if not Path(url).is_file():
                raise FileNotFoundError(f"前端产物不存在，请先执行 ppx build: {url}")
            mimetypes.add_type("application/javascript", ".js")

        screen = webview.screens[0]
        width = int(screen.width * self.settings.window.width_ratio)
        height = int(screen.height * self.settings.window.height_ratio)
        self.window = webview.create_window(
            title=self.settings.project.name,
            url=url,
            js_api=JavascriptAPI(self.bridge),
            width=width,
            height=height,
            min_size=(
                int(width * self.settings.window.min_width_ratio),
                int(height * self.settings.window.min_height_ratio),
            ),
            resizable=self.settings.window.resizable,
            fullscreen=self.settings.window.fullscreen,
            on_top=self.settings.window.always_on_top,
            confirm_close=self.settings.window.confirm_close,
            background_color=self.settings.window.background_color,
        )
        self.bridge.set_window(self.window)
        self.window.events.shown += self._on_shown
        webview.start(debug=dev, http_server=True, gui="cef" if cef else None)

    def _on_shown(self, *_args: Any) -> None:
        self.storage.initialize()
