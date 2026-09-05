"""Plan and apply framework-only PPX updates."""

from __future__ import annotations

import json
import hashlib
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import httpx
from packaging.version import InvalidVersion, Version

from ..project import find_project_root, load_settings, read_lock, write_lock


class UpdateError(RuntimeError):
    pass


class IncompatibleUpdate(UpdateError):
    pass


class LegacyRelease(IncompatibleUpdate):
    def __init__(self, version: str):
        super().__init__(f"公开更新通道当前仍是 {version}，该版本没有 V6 安全更新清单")
        self.version = version


@dataclass(frozen=True)
class UpdatePlan:
    current: str
    target: str
    python: str
    javascript: str
    python_api: str
    javascript_api: str
    data_schema: str
    current_python: Optional[str] = None
    current_javascript: Optional[str] = None

    @property
    def needed(self) -> bool:
        current_packages = (self.current_python or self.current, self.current_javascript or self.current)
        return Version(self.target) > Version(self.current) or (
            Version(self.target) == Version(self.current)
            and current_packages != (self.python, self.javascript)
        )


def _sha256_from_digest(digest: str) -> Optional[str]:
    parts = digest.split(":", 1)
    if len(parts) != 2 or parts[0].lower() != "sha256":
        return None
    value = parts[1].lower()
    if len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
        return None
    return value


def fetch_manifest(release_url: str, target: Optional[str] = None) -> Dict[str, Any]:
    if not release_url:
        raise UpdateError("未配置 framework.releaseUrl")
    url = release_url
    if target and url.endswith("/latest"):
        url = url[:-len("/latest")] + f"/tags/v{target.lstrip('Vv')}"
    try:
        release_response = httpx.get(
            url,
            follow_redirects=True,
            headers={"Accept": "application/vnd.github+json", "User-Agent": "ppx-py"},
            timeout=httpx.Timeout(10.0, connect=5.0),
        )
        release_response.raise_for_status()
        release = release_response.json()
        release_version = str(release.get("tag_name") or release.get("name") or "")
        asset = next(
            (item for item in release.get("assets", []) if item.get("name") == "ppx-update.json"),
            None,
        )
        if asset is None:
            try:
                if release_version and Version(release_version.lstrip("Vv")).major < 6:
                    raise LegacyRelease(release_version)
            except InvalidVersion:
                pass
            raise UpdateError("目标版本没有 ppx-update.json，不能执行安全更新")
        expected_hash = _sha256_from_digest(str(asset.get("digest") or ""))
        if expected_hash is None:
            raise UpdateError("ppx-update.json 缺少有效的 SHA-256，不能执行安全更新")
        manifest_response = httpx.get(asset["browser_download_url"], follow_redirects=True, timeout=10.0)
        manifest_response.raise_for_status()
        content = manifest_response.content
        if hashlib.sha256(content).hexdigest().lower() != expected_hash:
            raise UpdateError("ppx-update.json 完整性校验失败")
        manifest = dict(json.loads(content))
        try:
            if release_version and Version(release_version.lstrip("Vv")) != Version(
                str(manifest.get("releaseVersion", "")).lstrip("Vv")
            ):
                raise UpdateError("GitHub Release 版本与 ppx-update.json 不一致")
        except InvalidVersion as exc:
            raise UpdateError(f"Release 或更新清单版本无效: {exc}") from exc
        return manifest
    except UpdateError:
        raise
    except Exception as exc:
        raise UpdateError(f"无法读取 PPX 更新清单: {exc}") from exc


def make_plan(settings: Any, lock: Dict[str, Any], manifest: Dict[str, Any]) -> UpdatePlan:
    if manifest.get("schemaVersion") != 1:
        raise UpdateError("不支持的更新清单格式")
    manifest_channel = str(manifest.get("channel") or "")
    if manifest_channel != settings.framework.channel:
        raise IncompatibleUpdate(
            f"更新通道不匹配：项目为 {settings.framework.channel}，清单为 {manifest_channel or '未声明'}"
        )
    required = manifest.get("requires", {})
    if not isinstance(required, dict):
        raise UpdateError("更新清单的 requires 必须是对象")
    required_keys = {"projectFormat", "pythonApi", "javascriptApi", "dataSchema"}
    missing_required = sorted(required_keys - set(required))
    if missing_required:
        raise UpdateError("更新清单缺少兼容要求: " + ", ".join(missing_required))
    actual = {
        "projectFormat": settings.project.project_format,
        "pythonApi": settings.compatibility.python_api,
        "javascriptApi": settings.compatibility.javascript_api,
        "dataSchema": settings.compatibility.data_schema,
    }
    conflicts = [
        f"{key}: 项目为 {actual[key]}，新版本要求 {value}"
        for key, value in required.items()
        if key in actual and str(actual[key]) != str(value)
    ]
    if conflicts:
        raise IncompatibleUpdate(
            "该版本与当前项目不兼容，已停止且没有修改任何业务文件：\n- " + "\n- ".join(conflicts)
        )
    packages = manifest.get("packages", {})
    if not isinstance(packages, dict):
        raise UpdateError("更新清单的 packages 必须是对象")
    try:
        target = str(manifest["releaseVersion"]).lstrip("Vv")
        target_version = Version(target)
        if target_version.major != 6:
            raise IncompatibleUpdate("V6 更新器只接受 V6 版本；V5 与 V6 之间不执行迁移")
        python = str(packages["ppx-py"])
        javascript = str(packages["ppx-js"])
        for version in (python, javascript):
            Version(version)
    except (KeyError, InvalidVersion, TypeError) as exc:
        raise UpdateError(f"更新清单缺少有效版本: {exc}") from exc

    compatibility = manifest.get("provides", required)
    if not isinstance(compatibility, dict):
        raise UpdateError("更新清单的 provides 必须是对象")
    missing_provided = sorted({"pythonApi", "javascriptApi", "dataSchema"} - set(compatibility))
    if missing_provided:
        raise UpdateError("更新清单缺少兼容能力: " + ", ".join(missing_provided))
    current_framework = lock.get("framework", {})
    current_versions = [
        str(current_framework.get("python", settings.framework.python)),
        str(current_framework.get("javascript", settings.framework.javascript)),
    ]
    try:
        parsed_current = [Version(version) for version in current_versions]
    except InvalidVersion as exc:
        raise UpdateError(f"ppx.lock 包含无效的框架版本: {exc}") from exc
    current = current_versions[parsed_current.index(max(parsed_current))]
    if target_version < Version(current):
        raise IncompatibleUpdate(f"不支持降级：当前为 {current}，目标为 {target}")
    for package, installed, wanted in zip(
        ("ppx-py", "ppx-js"), current_versions, (python, javascript)
    ):
        if Version(wanted) < Version(installed):
            raise IncompatibleUpdate(f"不支持降级 {package}: {installed} -> {wanted}")
    return UpdatePlan(
        current=current,
        target=target,
        python=python,
        javascript=javascript,
        python_api=str(compatibility.get("pythonApi", settings.compatibility.python_api)),
        javascript_api=str(compatibility.get("javascriptApi", settings.compatibility.javascript_api)),
        data_schema=str(compatibility.get("dataSchema", settings.compatibility.data_schema)),
        current_python=current_versions[0],
        current_javascript=current_versions[1],
    )


def _replace_framework_versions(path: Path, plan: UpdatePlan) -> None:
    original = path.read_text(encoding="utf-8")
    section = re.search(r"(?ms)^\[framework\]\s*$.*?(?=^\[|\Z)", original)
    if section is None:
        raise UpdateError("ppx.toml 缺少 [framework]")
    updated_section = section.group(0)
    for key, value in (("python", plan.python), ("javascript", plan.javascript)):
        pattern = rf'(?m)^(\s*{key}\s*=\s*)["\'][^"\']*["\']'
        updated_section, count = re.subn(pattern, rf'\g<1>"{value}"', updated_section, count=1)
        if count != 1:
            raise UpdateError(f"ppx.toml 的 [framework] 缺少 {key}")
    _atomic_text(path, original[:section.start()] + updated_section + original[section.end():])


def _atomic_text(path: Path, content: str) -> None:
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent, text=True)
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


def _run(command: list[str], root: Path) -> None:
    result = subprocess.run(command, cwd=root, check=False)
    if result.returncode:
        raise UpdateError(f"命令执行失败 ({result.returncode}): {' '.join(command)}")


def apply_plan(root: Path, plan: UpdatePlan) -> None:
    settings = load_settings(root)
    protected = [root / "api", settings.frontend_source_dir / "src", settings.asset_dir]
    before = {str(path): _tree_signature(path) for path in protected}
    current_lock = read_lock(root)
    current_framework = current_lock.get("framework", {})
    managed_paths = (
        root / "ppx.toml",
        root / "ppx.lock",
        root / "package.json",
        root / "pnpm-lock.yaml",
        settings.frontend_source_dir / "package.json",
        settings.frontend_source_dir / "pnpm-lock.yaml",
    )
    backups = {
        path: path.read_bytes()
        for path in managed_paths
        if path.exists()
    }
    python_updated = False
    try:
        _run([
            sys.executable, "-m", "pip", "install", "--upgrade", "--disable-pip-version-check",
            "--only-binary", "ppx-py",
            f"ppx-py=={plan.python}",
        ], root)
        python_updated = True
        _run([
            "pnpm", "--dir", settings.paths.frontend, "add", "--save-exact", "--ignore-scripts",
            f"ppx-js@{plan.javascript}",
        ], root)
        _replace_framework_versions(root / "ppx.toml", plan)
        write_lock(root, {
            "lockVersion": "1",
            "projectFormat": "6",
            "python": plan.python,
            "javascript": plan.javascript,
            "pythonApi": plan.python_api,
            "javascriptApi": plan.javascript_api,
            "dataSchema": plan.data_schema,
        })
        after = {str(path): _tree_signature(path) for path in protected}
        if before != after:
            raise UpdateError("安全检查失败：更新命令改动了 api/、gui/src/ 或 ppx/assets/")
    except Exception:
        for path, content in backups.items():
            path.write_bytes(content)
        for path in managed_paths:
            if path not in backups and path.is_file():
                path.unlink()
        if python_updated and current_framework.get("python"):
            subprocess.run([
                sys.executable, "-m", "pip", "install", "--disable-pip-version-check",
                "--only-binary", "ppx-py",
                f"ppx-py=={current_framework['python']}",
            ], cwd=root, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if (root / "pnpm-lock.yaml").is_file():
            subprocess.run(
                ["pnpm", "install", "--frozen-lockfile", "--ignore-scripts"],
                cwd=root,
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        raise


def _tree_signature(path: Path) -> Dict[str, str]:
    if not path.exists():
        return {}
    return {
        str(item.relative_to(path)): hashlib.sha256(item.read_bytes()).hexdigest()
        for item in sorted(path.rglob("*"))
        if item.is_file()
    }


def describe(plan: UpdatePlan) -> None:
    if not plan.needed:
        print(f"PPX {plan.current} 已是最新版本")
        return
    if Version(plan.target) == Version(plan.current):
        print(f"检测到 PPX {plan.target} 依赖漂移，将恢复锁定版本")
    else:
        print(f"可更新：PPX {plan.current} -> {plan.target}")
    print(f"  ppx-py: {plan.python}")
    print(f"  ppx-js: {plan.javascript}")
    print("  保护范围: api/、gui/src/、ppx/assets/ 与用户数据不会被修改")


def run(args: object) -> int:
    try:
        root = find_project_root()
        settings = load_settings(root)
        lock = read_lock(root)
        requested = getattr(args, "to", None)
        if requested:
            try:
                requested_version = Version(requested.lstrip("Vv"))
            except InvalidVersion as exc:
                raise UpdateError(f"--to 不是有效版本号: {requested}") from exc
            if requested_version.major != 6:
                raise IncompatibleUpdate("V6 更新器只接受 V6 版本；V5 与 V6 之间不执行迁移")
        manifest = fetch_manifest(settings.framework.release_url, requested)
        plan = make_plan(settings, lock, manifest)
        if requested and Version(requested.lstrip("Vv")) != Version(plan.target):
            raise UpdateError(f"服务器返回版本 {plan.target}，与 --to {requested} 不一致")
        describe(plan)
        if getattr(args, "check", False) or getattr(args, "dry_run", False) or not plan.needed:
            return 0
        apply_plan(root, plan)
        print(f"PPX 已更新到 {plan.target}。建议立即执行 ppx doctor 和项目测试。")
        return 0
    except LegacyRelease as exc:
        if getattr(args, "to", None):
            print(f"[不兼容] {exc}")
            print("V6 不支持更新到 V5，也不执行 V5/V6 迁移。")
            return 2
        print(f"PPX {settings.framework.python} 已是当前 V6 项目版本；{exc}")
        return 0
    except IncompatibleUpdate as exc:
        print(f"[不兼容] {exc}")
        print("V6 不执行源码迁移；请按目标版本模板创建新项目并手动移入业务代码。")
        return 2
    except Exception as exc:
        print(f"[失败] {exc}")
        return 1
