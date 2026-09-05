"""Framework-owned application bootstrap."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Union

from .application import Application
from .settings import Settings


def create_application(settings: Settings) -> Application:
    """Create an application and register every configured business module."""
    root = str(settings.project_root)
    if root not in sys.path:
        sys.path.insert(0, root)
    application = Application(settings)
    for module_name in settings.python.modules:
        try:
            module = importlib.import_module(module_name)
        except Exception as exc:
            raise RuntimeError(f"无法导入业务 API 模块 {module_name}: {exc}") from exc
        application.register_api(module)
    return application


def run_project(config: Union[str, Path] = "ppx.toml", *, dev: bool = False, cef: bool = False) -> None:
    settings = Settings.load(config)
    create_application(settings).run(dev=dev, cef=cef)
