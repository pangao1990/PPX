"""Built-in operating-system APIs."""

from __future__ import annotations

import getpass
import os
import platform
import subprocess
import webbrowser
from pathlib import Path
from typing import Any, Callable, Optional

from ..bridge import BridgeError
from ..settings import Settings


class SystemService:
    def __init__(self, settings: Settings, window: Callable[[], Any]) -> None:
        self.settings = settings
        self._window = window

    def get_app_info(self) -> dict[str, str]:
        return {
            "name": self.settings.project.name,
            "version": self.settings.project.version,
            "frameworkVersion": self.settings.framework.python,
        }

    @staticmethod
    def get_owner() -> str:
        return getpass.getuser()

    @staticmethod
    def open_path(path: str) -> bool:
        if not isinstance(path, str) or not path.strip():
            raise BridgeError("INVALID_PARAMS", "path 必须是非空路径或网址")
        if path.startswith(("http://", "https://")):
            return bool(webbrowser.open(path))
        target = str(Path(path).expanduser().resolve())
        system = platform.system()
        if system == "Darwin":
            return subprocess.call(["open", target]) == 0
        if system == "Windows":
            os.startfile(target)  # type: ignore[attr-defined]
            return True
        if system == "Linux":
            return subprocess.call(["xdg-open", target]) == 0
        return False

    def open_file_dialog(
        self,
        file_types: Optional[list[str]] = None,
        directory: str = "",
        multiple: bool = True,
    ) -> list[dict[str, str]]:
        import webview

        if not isinstance(multiple, bool):
            raise BridgeError("INVALID_PARAMS", "multiple 必须是布尔值")
        window = self._require_window()
        result = window.create_file_dialog(
            dialog_type=webview.OPEN_DIALOG,
            directory=directory,
            allow_multiple=multiple,
            file_types=tuple(file_types or ["全部文件 (*.*)"]),
        )
        return [
            {
                "filename": Path(item).name,
                "ext": Path(item).suffix,
                "dir": str(Path(item).parent),
                "path": str(item),
            }
            for item in (result or [])
        ]

    def save_file_dialog(
        self,
        filename: str = "",
        file_types: Optional[list[str]] = None,
        directory: str = "",
    ) -> str:
        import webview

        result = self._require_window().create_file_dialog(
            dialog_type=webview.SAVE_DIALOG,
            directory=directory,
            save_filename=filename,
            file_types=tuple(file_types or ["全部文件 (*.*)"]),
        )
        if isinstance(result, (tuple, list)):
            return str(result[0]) if result else ""
        return str(result or "")

    def select_directory(self, directory: str = "") -> str:
        import webview

        result = self._require_window().create_file_dialog(
            dialog_type=webview.FOLDER_DIALOG,
            directory=directory,
        )
        if isinstance(result, (tuple, list)):
            return str(result[0]) if result else ""
        return str(result or "")

    def get_window_state(self) -> dict[str, Any]:
        window = self._require_window()
        return {
            "x": int(window.x),
            "y": int(window.y),
            "width": int(window.width),
            "height": int(window.height),
            "onTop": bool(window.on_top),
        }

    def minimize_window(self) -> bool:
        self._require_window().minimize()
        return True

    def maximize_window(self) -> bool:
        self._require_window().maximize()
        return True

    def restore_window(self) -> bool:
        self._require_window().restore()
        return True

    def toggle_fullscreen(self) -> bool:
        self._require_window().toggle_fullscreen()
        return True

    def close_window(self) -> bool:
        self._require_window().destroy()
        return True

    def _require_window(self) -> Any:
        window = self._window()
        if window is None:
            raise BridgeError("WINDOW_NOT_READY", "窗口尚未创建")
        return window
