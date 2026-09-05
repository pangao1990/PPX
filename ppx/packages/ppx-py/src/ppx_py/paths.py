"""Stable business paths in development and packaged applications."""

from __future__ import annotations

from pathlib import Path
from typing import Union

from .settings import Settings


PathValue = Union[str, Path]


def resource_path(relative: PathValue = "", config: PathValue = "ppx.toml") -> Path:
    """Return a read-only bundled resource path and reject directory traversal."""
    root = Settings.load(config).resource_dir
    target = _safe_child(root, relative)
    if not target.exists():
        raise FileNotFoundError(f"业务资源不存在: {target}")
    return target


def app_data_path(relative: PathValue = "", config: PathValue = "ppx.toml") -> Path:
    """Return a writable per-user application-data path."""
    root = Settings.load(config).app_data_dir
    root.mkdir(parents=True, exist_ok=True)
    return _safe_child(root, relative)


def _safe_child(root: Path, relative: PathValue) -> Path:
    root = root.resolve()
    value = Path(relative)
    if value.is_absolute():
        raise ValueError("路径必须是相对于 PPX 目录的路径")
    target = (root / value).resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise ValueError("路径不能离开 PPX 管理目录") from exc
    return target
