"""Typed, instance-scoped PPX project settings."""

from __future__ import annotations

import os
import platform
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Union

from packaging.version import InvalidVersion, Version

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10
    import tomli as tomllib


class SettingsError(ValueError):
    """Raised when ppx.toml is absent or invalid."""


_WINDOWS_RESERVED_NAMES = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{number}" for number in range(1, 10)),
    *(f"LPT{number}" for number in range(1, 10)),
}


@dataclass(frozen=True)
class ProjectSettings:
    name: str
    slug: str
    version: str
    identifier: str
    developer: str
    description: str
    website: str
    windows_app_id: str
    project_format: int


@dataclass(frozen=True)
class WindowSettings:
    width_ratio: float = 2 / 3
    height_ratio: float = 4 / 5
    min_width_ratio: float = 0.5
    min_height_ratio: float = 0.5
    resizable: bool = True
    fullscreen: bool = False
    always_on_top: bool = False
    confirm_close: bool = False
    background_color: str = "#FFFFFF"


@dataclass(frozen=True)
class DevelopmentSettings:
    port: int = 5173


@dataclass(frozen=True)
class StorageSettings:
    filename: str = "storage.json"


@dataclass(frozen=True)
class ApplicationUpdateSettings:
    enabled: bool = True
    release_url: str = ""


@dataclass(frozen=True)
class CompatibilitySettings:
    python_api: str = "6.0"
    javascript_api: str = "6.0"
    data_schema: str = "1"


@dataclass(frozen=True)
class FrameworkSettings:
    python: str = "6.0.0"
    javascript: str = "6.0.0"
    channel: str = "stable"
    release_url: str = ""


@dataclass(frozen=True)
class PythonSettings:
    modules: tuple[str, ...] = ("api.api",)


@dataclass(frozen=True)
class PathSettings:
    frontend: str = "gui"
    resources: str = "api/resources"
    assets: str = "ppx/assets"


@dataclass(frozen=True)
class Settings:
    config_path: Path
    project_root: Path
    runtime_root: Path
    project: ProjectSettings
    window: WindowSettings
    development: DevelopmentSettings
    storage: StorageSettings
    application_update: ApplicationUpdateSettings
    compatibility: CompatibilitySettings
    framework: FrameworkSettings
    python: PythonSettings
    paths: PathSettings

    @classmethod
    def load(cls, path: Union[str, os.PathLike[str]] = "ppx.toml") -> "Settings":
        config_path = Path(path)
        if not config_path.is_absolute():
            base = Path(getattr(sys, "_MEIPASS", Path.cwd()))
            config_path = base / config_path
        config_path = config_path.resolve()
        if not config_path.is_file():
            raise SettingsError(f"找不到 PPX 配置文件: {config_path}")

        try:
            with config_path.open("rb") as stream:
                raw = tomllib.load(stream)
        except Exception as exc:
            raise SettingsError(f"无法读取 {config_path.name}: {exc}") from exc

        project = _table(raw, "project")
        required = ("name", "slug", "version", "identifier", "developer", "format")
        missing = [key for key in required if key not in project]
        if missing:
            raise SettingsError("[project] 缺少配置: " + ", ".join(missing))
        project_format = _integer(project["format"], "project.format")
        if project_format != 6:
            raise SettingsError(
                f"V6 只支持 project.format = 6，当前为 {project_format}；"
                "请新建 V6 项目，不要覆盖或原地迁移 V5 项目。"
            )

        window = _table(raw, "window")
        development = _table(raw, "development")
        storage = _table(raw, "storage")
        updates = _table(raw, "applicationUpdate")
        compatibility = _table(raw, "compatibility")
        framework = _table(raw, "framework")
        python = _table(raw, "python")
        paths = _table(raw, "paths")
        runtime_root = Path(getattr(sys, "_MEIPASS", config_path.parent)).resolve()

        name = _required_text(project, "name", "[project]")
        slug = _required_text(project, "slug", "[project]")
        version = _valid_version(project["version"], "project.version")
        identifier = _required_text(project, "identifier", "[project]")
        developer = _single_line(_required_text(project, "developer", "[project]"), "project.developer")
        if (
            name in (".", "..")
            or name.endswith((" ", "."))
            or any(ord(character) < 32 or character in '<>:"/\\|?*' for character in name)
            or name.split(".", 1)[0].upper() in _WINDOWS_RESERVED_NAMES
        ):
            raise SettingsError("project.name 不是有效的跨平台文件名")
        if not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", slug):
            raise SettingsError("project.slug 只能包含小写字母、数字和中划线，且不能以中划线开头或结尾")
        identifier_part = r"[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?"
        if not re.fullmatch(rf"{identifier_part}(?:\.{identifier_part})+", identifier):
            raise SettingsError("project.identifier 必须是至少两段的反向域名，例如 com.example")
        windows_app_id = str(project.get("windowsAppId", "")).strip()
        if not re.fullmatch(
            r"[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}",
            windows_app_id,
        ):
            raise SettingsError("project.windowsAppId 必须是非空的标准 GUID（不含花括号）")
        description = _single_line(str(project.get("description", "")), "project.description")
        website = _single_line(str(project.get("website", "")), "project.website")

        width_ratio = _ratio(window.get("widthRatio", 2 / 3), "window.widthRatio")
        height_ratio = _ratio(window.get("heightRatio", 4 / 5), "window.heightRatio")
        min_width_ratio = _ratio(window.get("minWidthRatio", 0.5), "window.minWidthRatio")
        min_height_ratio = _ratio(window.get("minHeightRatio", 0.5), "window.minHeightRatio")
        if min_width_ratio > width_ratio or min_height_ratio > height_ratio:
            raise SettingsError("window.minWidthRatio/minHeightRatio 不能大于初始窗口比例")
        resizable = _boolean(window.get("resizable", True), "window.resizable")
        fullscreen = _boolean(window.get("fullscreen", False), "window.fullscreen")
        always_on_top = _boolean(window.get("alwaysOnTop", False), "window.alwaysOnTop")
        confirm_close = _boolean(window.get("confirmClose", False), "window.confirmClose")
        background_color = str(window.get("backgroundColor", "#FFFFFF")).strip()
        if not re.fullmatch(r"#[0-9A-Fa-f]{6}", background_color):
            raise SettingsError("window.backgroundColor 必须是 #RRGGBB 十六进制颜色")

        port = _integer(development.get("port", 5173), "development.port")
        if not 1 <= port <= 65535:
            raise SettingsError("development.port 必须在 1 到 65535 之间")
        storage_filename = str(storage.get("filename", "storage.json")).strip()
        if (
            not storage_filename
            or storage_filename in (".", "..")
            or ".." in storage_filename
            or "/" in storage_filename
            or "\\" in storage_filename
            or Path(storage_filename).name != storage_filename
        ):
            raise SettingsError("storage.filename 必须是文件名，不能包含目录或 ..")

        python_api = _required_text(compatibility, "pythonApi", "[compatibility]")
        javascript_api = _required_text(compatibility, "javascriptApi", "[compatibility]")
        data_schema = _required_text(compatibility, "dataSchema", "[compatibility]")
        python_version = _valid_version(framework.get("python", "6.0.0"), "framework.python")
        javascript_version = _valid_version(
            framework.get("javascript", "6.0.0"), "framework.javascript"
        )
        modules_value = python.get("modules", ["api.api"])
        if not isinstance(modules_value, list) or not modules_value or not all(
            isinstance(value, str) and value.strip() for value in modules_value
        ):
            raise SettingsError("python.modules 必须是非空模块名数组")
        frontend_path = _safe_relative_path(paths.get("frontend", "gui"), "paths.frontend")
        resources_path = _safe_relative_path(
            paths.get("resources", "api/resources"), "paths.resources"
        )
        assets_path = _safe_relative_path(paths.get("assets", "ppx/assets"), "paths.assets")
        channel = str(framework.get("channel", "stable")).strip().lower()
        if channel not in {"stable", "beta", "nightly"}:
            raise SettingsError("framework.channel 只能是 stable、beta 或 nightly")

        return cls(
            config_path=config_path,
            project_root=config_path.parent,
            runtime_root=runtime_root,
            project=ProjectSettings(
                name=name,
                slug=slug,
                version=version,
                identifier=identifier,
                developer=developer,
                description=description,
                website=website,
                windows_app_id=windows_app_id,
                project_format=project_format,
            ),
            window=WindowSettings(
                width_ratio=width_ratio,
                height_ratio=height_ratio,
                min_width_ratio=min_width_ratio,
                min_height_ratio=min_height_ratio,
                resizable=resizable,
                fullscreen=fullscreen,
                always_on_top=always_on_top,
                confirm_close=confirm_close,
                background_color=background_color.upper(),
            ),
            development=DevelopmentSettings(port=port),
            storage=StorageSettings(filename=storage_filename),
            application_update=ApplicationUpdateSettings(
                enabled=_boolean(updates.get("enabled", True), "applicationUpdate.enabled"),
                release_url=str(updates.get("releaseUrl", "")),
            ),
            compatibility=CompatibilitySettings(
                python_api=python_api,
                javascript_api=javascript_api,
                data_schema=data_schema,
            ),
            framework=FrameworkSettings(
                python=python_version,
                javascript=javascript_version,
                channel=channel,
                release_url=str(framework.get("releaseUrl", "")),
            ),
            python=PythonSettings(modules=tuple(value.strip() for value in modules_value)),
            paths=PathSettings(
                frontend=frontend_path,
                resources=resources_path,
                assets=assets_path,
            ),
        )

    @property
    def app_id(self) -> str:
        return f"{self.project.identifier}.{self.project.slug}"

    @property
    def app_data_dir(self) -> Path:
        system = platform.system()
        if system == "Darwin":
            root = Path.home() / "Library" / "Application Support"
        elif system == "Windows":
            root = Path(os.environ.get("APPDATA") or Path.home() / "AppData" / "Roaming")
        else:
            root = Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local" / "share")
        return root / self.app_id

    @property
    def download_dir(self) -> Path:
        return Path.home() / "Downloads"

    @property
    def frontend_dir(self) -> Path:
        bundled = self.runtime_root / "web"
        return bundled if hasattr(sys, "_MEIPASS") else self.frontend_source_dir / "dist"

    @property
    def frontend_source_dir(self) -> Path:
        return self.project_root / self.paths.frontend

    @property
    def resource_source_dir(self) -> Path:
        return self.project_root / self.paths.resources

    @property
    def asset_dir(self) -> Path:
        return self.project_root / self.paths.assets

    @property
    def resource_dir(self) -> Path:
        return self.runtime_root / "resources" if hasattr(sys, "_MEIPASS") else self.resource_source_dir


def _table(raw: Mapping[str, Any], name: str) -> Mapping[str, Any]:
    value = raw.get(name, {})
    if not isinstance(value, Mapping):
        raise SettingsError(f"[{name}] 必须是 TOML 表")
    return value


def _required_text(table: Mapping[str, Any], key: str, section: str) -> str:
    value = str(table.get(key, "")).strip()
    if not value:
        raise SettingsError(f"{section} 的 {key} 不能为空")
    return value


def _single_line(value: str, field: str) -> str:
    if "\n" in value or "\r" in value or "\0" in value:
        raise SettingsError(f"{field} 必须是单行文本")
    return value


def _valid_version(value: Any, field: str) -> str:
    text = str(value).strip()
    try:
        Version(text)
    except InvalidVersion as exc:
        raise SettingsError(f"{field} 不是有效版本号: {text}") from exc
    return text


def _ratio(value: Any, field: str) -> float:
    if isinstance(value, bool):
        raise SettingsError(f"{field} 必须是数字")
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise SettingsError(f"{field} 必须是数字") from exc
    if not 0 < result <= 1:
        raise SettingsError(f"{field} 必须大于 0 且不大于 1")
    return result


def _integer(value: Any, field: str) -> int:
    if isinstance(value, bool):
        raise SettingsError(f"{field} 必须是整数")
    try:
        result = int(value)
    except (TypeError, ValueError) as exc:
        raise SettingsError(f"{field} 必须是整数") from exc
    if isinstance(value, float) and not value.is_integer():
        raise SettingsError(f"{field} 必须是整数")
    return result


def _boolean(value: Any, field: str) -> bool:
    if not isinstance(value, bool):
        raise SettingsError(f"{field} 必须是 true 或 false")
    return value


def _safe_relative_path(value: Any, field: str) -> str:
    text = str(value).strip().replace("\\", "/")
    path = Path(text)
    if not text or path.is_absolute() or ".." in path.parts:
        raise SettingsError(f"{field} 必须是项目内的相对路径")
    return path.as_posix()
