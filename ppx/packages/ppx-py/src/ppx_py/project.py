"""Project discovery and lockfile primitives."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10
    import tomli as tomllib

from .settings import Settings


def find_project_root(start: Optional[Path] = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / "ppx.toml").is_file():
            return candidate
    raise FileNotFoundError("当前目录及其父目录中没有 ppx.toml")


def load_settings(root: Optional[Path] = None) -> Settings:
    project_root = root or find_project_root()
    return Settings.load(project_root / "ppx.toml")


def read_lock(root: Path) -> Dict[str, Any]:
    path = root / "ppx.lock"
    if not path.is_file():
        raise FileNotFoundError("缺少 ppx.lock，请从完整的 V6 项目模板重新创建项目")
    with path.open("rb") as stream:
        return tomllib.load(stream)


def write_lock(root: Path, values: Dict[str, str]) -> None:
    path = root / "ppx.lock"
    content = (
        "# 此文件由 ppx update 管理，请勿手动修改。\n"
        f"lockVersion = {int(values['lockVersion'])}\n"
        f"projectFormat = {int(values['projectFormat'])}\n\n"
        "[framework]\n"
        f"python = \"{values['python']}\"\n"
        f"javascript = \"{values['javascript']}\"\n\n"
        "[compatibility]\n"
        f"pythonApi = \"{values['pythonApi']}\"\n"
        f"javascriptApi = \"{values['javascriptApi']}\"\n"
        f"dataSchema = \"{values['dataSchema']}\"\n"
    )
    descriptor, temporary_name = tempfile.mkstemp(prefix=".ppx.lock.", dir=root, text=True)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()
