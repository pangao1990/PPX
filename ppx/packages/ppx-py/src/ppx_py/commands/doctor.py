"""Validate a PPX V6 project and its current-platform toolchain."""

from __future__ import annotations

import importlib.metadata
import json
import platform
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List, Optional

from packaging.version import InvalidVersion, Version

from ..project import find_project_root, load_settings, read_lock


@dataclass
class Check:
    ok: bool
    name: str
    detail: str


def _command_version(command: str, args: List[str]) -> Optional[str]:
    executable = shutil.which(command)
    if not executable:
        return None
    result = subprocess.run([executable, *args], capture_output=True, text=True, check=False)
    value = (result.stdout or result.stderr).strip()
    return value.splitlines()[0] if value else "unknown"


def _at_least(value: Optional[str], required: str) -> bool:
    if value is None:
        return False
    try:
        return Version(value.lstrip("vV")) >= Version(required)
    except InvalidVersion:
        return False


def _in_range(value: Optional[str], minimum: str, maximum_exclusive: str) -> bool:
    if value is None:
        return False
    try:
        parsed = Version(value.lstrip("vV"))
        return Version(minimum) <= parsed < Version(maximum_exclusive)
    except InvalidVersion:
        return False


def collect_checks(root: Path) -> List[Check]:
    settings = load_settings(root)
    checks = [
        Check(settings.project.project_format == 6, "项目格式", f"V{settings.project.project_format}"),
        Check(sys.version_info >= (3, 9), "Python", sys.version.split()[0]),
    ]
    node = _command_version("node", ["--version"])
    pnpm = _command_version("pnpm", ["--version"])
    checks.extend([
        Check(_at_least(node, "22.13.0"), "Node.js", node or "未安装"),
        Check(_in_range(pnpm, "11.0.0", "12.0.0"), "pnpm", pnpm or "未安装"),
    ])
    try:
        installed = importlib.metadata.version("ppx-py")
        checks.append(Check(installed == settings.framework.python, "ppx-py", f"已安装 {installed}，配置 {settings.framework.python}"))
    except importlib.metadata.PackageNotFoundError:
        checks.append(Check(False, "ppx-py", "未安装"))

    js_manifest = settings.frontend_source_dir / "node_modules" / "ppx-js" / "package.json"
    if js_manifest.is_file():
        installed_js = str(json.loads(js_manifest.read_text(encoding="utf-8")).get("version", "未知"))
        checks.append(Check(installed_js == settings.framework.javascript, "ppx-js", f"已安装 {installed_js}，配置 {settings.framework.javascript}"))
    else:
        checks.append(Check(False, "ppx-js", "未安装，请执行 ppx init"))

    for name, target in (
        ("api", root / "api"),
        ("gui", settings.frontend_source_dir),
        ("ppx/assets", settings.asset_dir),
        ("api/requirements.txt", root / "api/requirements.txt"),
    ):
        checks.append(Check(target.exists(), name, "存在" if target.exists() else "缺失"))
    for filename in ("logo.png", "logo.ico", "logo.icns", "dmg-background.png"):
        target = settings.asset_dir / filename
        checks.append(Check(target.is_file(), f"资源 {filename}", "存在" if target.is_file() else "缺失"))

    try:
        lock = read_lock(root)
        framework = lock.get("framework", {})
        compatibility = lock.get("compatibility", {})
        lock_ok = (
            lock.get("projectFormat") == 6
            and framework.get("python") == settings.framework.python
            and framework.get("javascript") == settings.framework.javascript
            and compatibility.get("pythonApi") == settings.compatibility.python_api
            and compatibility.get("javascriptApi") == settings.compatibility.javascript_api
            and compatibility.get("dataSchema") == settings.compatibility.data_schema
        )
        checks.append(Check(lock_ok, "ppx.lock", "与 ppx.toml 一致" if lock_ok else "与 ppx.toml 不一致"))
    except Exception as exc:
        checks.append(Check(False, "ppx.lock", str(exc)))

    system = platform.system()
    if system == "Darwin":
        checks.extend([
            Check(shutil.which("hdiutil") is not None, "hdiutil", shutil.which("hdiutil") or "未安装"),
            Check(_module_available("dmgbuild"), "dmgbuild", "已安装" if _module_available("dmgbuild") else "未安装"),
        ])
    elif system == "Windows":
        from ..packaging.installer import _find_iscc
        iscc = _find_iscc()
        checks.append(Check(iscc is not None, "Inno Setup 6", str(iscc) if iscc else "未安装"))
    elif system == "Linux":
        checks.append(Check(shutil.which("dpkg-deb") is not None, "dpkg-deb", shutil.which("dpkg-deb") or "未安装"))
    return checks


def _module_available(name: str) -> bool:
    try:
        importlib.metadata.version(name)
        return True
    except importlib.metadata.PackageNotFoundError:
        return False


def run(args: object) -> int:
    json_output = bool(getattr(args, "json_output", False))
    try:
        root = find_project_root()
        checks = collect_checks(root)
    except Exception as exc:
        if json_output:
            print(json.dumps({
                "ok": False,
                "project": str(locals().get("root", "")),
                "summary": {"passed": 0, "failed": 1, "total": 1},
                "checks": [asdict(Check(False, "项目", str(exc)))],
            }, ensure_ascii=False, indent=2))
            return 1
        print(f"[失败] 项目: {exc}")
        return 1
    failed = sum(not item.ok for item in checks)
    if json_output:
        print(json.dumps({
            "ok": failed == 0,
            "project": str(root),
            "summary": {"passed": len(checks) - failed, "failed": failed, "total": len(checks)},
            "checks": [asdict(check) for check in checks],
        }, ensure_ascii=False, indent=2))
        return 1 if failed else 0
    print(f"PPX Doctor: {root}")
    for check in checks:
        print(f"[{'通过' if check.ok else '失败'}] {check.name}: {check.detail}")
    print(f"检查完成：{len(checks) - failed} 项通过，{failed} 项失败")
    return 1 if failed else 0
