#!/usr/bin/env python3
"""Fail fast when two-package PPX release inputs or artifacts disagree."""

from __future__ import annotations

import argparse
import json
import sys
import tarfile
import zipfile
from pathlib import Path
from typing import List

from packaging.version import InvalidVersion, Version

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib


ROOT = Path(__file__).resolve().parents[3]


def read_toml(path: Path) -> dict:
    with path.open("rb") as stream:
        return tomllib.load(stream)


def check_sources() -> List[str]:
    errors: List[str] = []
    settings = read_toml(ROOT / "ppx.toml")
    lock = read_toml(ROOT / "ppx.lock")
    manifest = json.loads((ROOT / "ppx-update.json").read_text(encoding="utf-8"))
    root_package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    gui_package = json.loads((ROOT / "gui/package.json").read_text(encoding="utf-8"))
    js = json.loads((ROOT / "ppx/packages/ppx-js/package.json").read_text(encoding="utf-8"))
    py = read_toml(ROOT / "ppx/packages/ppx-py/pyproject.toml")["project"]
    version = str(settings["project"]["version"])
    try:
        if Version(version).major != 6:
            errors.append(f"项目版本不是 V6: {version}")
    except InvalidVersion:
        errors.append(f"项目版本无效: {version}")

    for source, candidate in {
        "package.json": root_package["version"],
        "gui/package.json": gui_package["version"],
        "ppx-py": py["version"],
        "ppx-js": js["version"],
        "ppx-update.json": manifest["releaseVersion"],
    }.items():
        if candidate != version:
            errors.append(f"{source} 版本 {candidate} 与项目版本 {version} 不一致")
    for package, key, candidate in (
        ("ppx-py", "python", py["version"]),
        ("ppx-js", "javascript", js["version"]),
    ):
        if settings["framework"].get(key) != candidate:
            errors.append(f"ppx.toml 中的 {package} 版本不一致")
        if lock["framework"].get(key) != candidate:
            errors.append(f"ppx.lock 中的 {package} 版本不一致")
        if manifest.get("packages", {}).get(package) != candidate:
            errors.append(f"ppx-update.json 中的 {package} 版本不一致")
    dependencies = set(py.get("dependencies", []))
    for prefix in ("pillow==", "pyinstaller==", "pywebview=="):
        if not any(item.startswith(prefix) for item in dependencies):
            errors.append(f"ppx-py 缺少固定依赖 {prefix}")
    if py.get("name") != "ppx-py" or js.get("name") != "ppx-js":
        errors.append("发布包名称不是 ppx-py / ppx-js")
    if py.get("license") != "AGPL-3.0-only" or js.get("license") != "AGPL-3.0-only":
        errors.append("发布包许可证必须是 AGPL-3.0-only")
    if js.get("types") != "./src/index.d.ts":
        errors.append("ppx-js 没有发布 TypeScript 声明入口")
    for package in ("ppx-py", "ppx-js"):
        if not (ROOT / "ppx/packages" / package / "LICENSE").is_file():
            errors.append(f"{package} 缺少 LICENSE")
    for relative in ("src/index.js", "src/index.d.ts"):
        if not (ROOT / "ppx/packages/ppx-js" / relative).is_file():
            errors.append(f"ppx-js 缺少 {relative}")
    if f"## {version}" not in (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"):
        errors.append(f"CHANGELOG.md 缺少 {version} 条目")
    return errors


def check_artifacts(directory: Path, version: str) -> List[str]:
    errors: List[str] = []
    expected = {
        "python": directory / f"ppx_py-{version}-py3-none-any.whl",
        "javascript": directory / f"ppx-js-{version}.tgz",
    }
    for name, path in expected.items():
        if not path.is_file():
            errors.append(f"缺少 {name} 发布产物: {path.name}")
    if errors:
        return errors
    with zipfile.ZipFile(expected["python"]) as archive:
        names = set(archive.namelist())
        for required in (
            "ppx_py/__init__.py",
            "ppx_py/cli.py",
            "ppx_py/paths.py",
            "ppx_py/commands/icon.py",
            "ppx_py/packaging/installer.py",
            "ppx_py/template/assets/logo.png",
        ):
            if required not in names:
                errors.append(f"ppx-py wheel 缺少 {required}")
        if "ppx_py/template/assets/logo.svg" in names:
            errors.append("ppx-py wheel 包含未使用的 logo.svg")
        metadata_name = next((name for name in names if name.endswith(".dist-info/METADATA")), "")
        metadata = archive.read(metadata_name).decode("utf-8") if metadata_name else ""
        if "Requires-Dist: pyinstaller==" not in metadata:
            errors.append("ppx-py wheel 缺少 PyInstaller 依赖")
        if "Requires-Dist: pillow==" not in metadata:
            errors.append("ppx-py wheel 缺少 Pillow 图标生成依赖")
    with tarfile.open(expected["javascript"], "r:gz") as archive:
        names = set(archive.getnames())
        for required in ("package/src/index.js", "package/src/index.d.ts", "package/package.json"):
            if required not in names:
                errors.append(f"ppx-js tgz 缺少 {required}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="检查 PPX 发布版本和构建产物")
    parser.add_argument("--dist", type=Path, help="同时检查 wheel 和 npm tgz 所在目录")
    args = parser.parse_args()
    errors = check_sources()
    version = str(read_toml(ROOT / "ppx.toml")["project"]["version"])
    if args.dist:
        errors.extend(check_artifacts(args.dist.resolve(), version))
    if errors:
        for error in errors:
            print(f"[失败] {error}")
        return 1
    print(f"[通过] PPX {version} {'源码与产物' if args.dist else '发布源码'}一致性检查")
    return 0


if __name__ == "__main__":
    sys.exit(main())
