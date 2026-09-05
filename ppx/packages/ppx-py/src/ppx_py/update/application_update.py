"""Download application release assets without mutating framework sources."""

from __future__ import annotations

import hashlib
import os
import platform
import re
import threading
from pathlib import Path
from typing import Any, Callable, Optional

import httpx
from packaging.version import InvalidVersion, Version

from ..settings import Settings

class _DownloadCancelled(Exception):
    pass


ProgressCallback = Callable[[dict[str, Any]], None]


class ApplicationUpdater:
    def __init__(self, settings: Settings, progress: Optional[ProgressCallback] = None) -> None:
        self.settings = settings
        self.progress = progress or (lambda _value: None)
        self._cancelled = threading.Event()
        self._download_lock = threading.Lock()

    def check(self) -> dict[str, Any]:
        if not self.settings.application_update.enabled:
            return {"code": 1, "msg": "应用更新已关闭"}
        if not self.settings.application_update.release_url:
            return {"code": -1, "msg": "未配置 applicationUpdate.releaseUrl"}
        release = self._get_release()
        if not release["status"]:
            return {"code": -1, "msg": f"连接更新服务器失败: {release['msg']}"}
        try:
            has_update = self.compare_versions(self.settings.project.version, release["version"])
        except InvalidVersion:
            return {"code": -1, "msg": f"服务端版本号格式不正确: {release['version']}"}
        if not has_update:
            return {"code": 1, "msg": f"{self.settings.project.version} 已是最新版本"}
        return {
            "code": 0,
            "msg": f"有新版 {release['version']}，当前版本为 {self.settings.project.version}",
            "htmlUrl": release["htmlUrl"],
            "assets": release["assets"],
            "body": release["body"],
        }

    def download(self) -> dict[str, Any]:
        if not self._download_lock.acquire(blocking=False):
            return {"code": -2, "msg": "已有下载任务正在进行"}
        try:
            self._cancelled.clear()
            return self._download_release()
        finally:
            self._download_lock.release()

    def _download_release(self) -> dict[str, Any]:
        checked = self.check()
        if checked["code"] != 0:
            return checked
        asset = self.select_asset(checked["assets"])
        if asset is None:
            return {"code": -2, "msg": f"没有适用于 {platform.system()} 的安装包"}
        name = str(asset.get("name") or "")
        if not self.safe_asset_name(name):
            return {"code": -2, "msg": "安装包文件名不安全，已拒绝下载"}
        digest = str(asset.get("digest") or "")
        if self.sha256_from_digest(digest) is None:
            return {"code": -2, "msg": "安装包缺少有效的 SHA-256，已拒绝下载"}
        path = self.settings.download_dir / name
        for _ in range(3):
            if self._cancelled.is_set():
                return {"code": -2, "msg": "取消更新"}
            result = self._download(
                asset["browser_download_url"], path, int(asset.get("size", 0)), digest
            )
            if result["msg"] != "连接超时":
                if result["status"]:
                    return {"code": 0, "msg": "下载程序包成功", "downloadPath": str(path)}
                return {"code": -2, "msg": "下载程序包失败: " + result["msg"]}
        return {"code": -2, "msg": "下载程序包失败: 连接超时"}

    def cancel(self) -> bool:
        self._cancelled.set()
        return True

    def _get_release(self) -> dict[str, Any]:
        try:
            response = httpx.get(
                self.settings.application_update.release_url,
                follow_redirects=True,
                headers={"Accept": "application/vnd.github+json", "User-Agent": self.settings.project.slug},
                timeout=httpx.Timeout(5.0, connect=3.0),
            )
            response.raise_for_status()
            payload = response.json()
            return {
                "status": True,
                "version": payload.get("tag_name") or payload["name"],
                "htmlUrl": payload["html_url"],
                "assets": payload.get("assets", []),
                "body": payload.get("body") or "",
            }
        except Exception as exc:
            return {"status": False, "msg": str(exc)}

    @staticmethod
    def compare_versions(current: str, available: str) -> bool:
        return Version(available.lstrip("Vv")) > Version(current.lstrip("Vv"))

    @staticmethod
    def select_asset(assets: list[dict[str, Any]]) -> Optional[dict[str, Any]]:
        platform_info = {
            "Windows": (".exe", ("windows", "win")),
            "Darwin": (".dmg", ("macos", "darwin", "mac")),
            "Linux": (".deb", ("linux",)),
        }
        extension, system_names = platform_info.get(platform.system(), ("", ()))
        candidates = [
            asset for asset in assets
            if str(asset.get("name", "")).lower().endswith(extension)
            and any(name in str(asset.get("name", "")).lower() for name in system_names)
        ]
        groups = {
            "arm64": ("arm64", "aarch64"),
            "x64": ("x64", "x86_64", "amd64"),
            "x86": ("x86", "i386", "i686", "ia32"),
            "arm": ("arm", "armv7l", "armhf"),
        }
        machine = platform.machine().lower()
        current = next((key for key, aliases in groups.items() if machine in aliases), None)
        matching, generic = [], []
        for asset in candidates:
            name = asset["name"].lower()
            # Boundaries avoid treating x86_64 as x86 or darwin as win.
            recognized = {
                key for key, aliases in groups.items()
                if any(re.search(r"(?:^|[_.-])" + re.escape(alias) + r"(?:[_.-]|$)", name)
                       for alias in aliases)
            }
            if "x64" in recognized:
                recognized.discard("x86")
            if current in recognized:
                matching.append(asset)
            elif not recognized or re.search(r"(?:^|[_.-])universal(?:2)?(?:[_.-]|$)", name):
                generic.append(asset)
        return next(iter(matching or generic), None)

    @staticmethod
    def safe_asset_name(name: str) -> bool:
        return bool(
            name
            and name not in (".", "..")
            and "/" not in name
            and "\\" not in name
            and not any(ord(char) < 32 or char in ':<>"|?*' for char in name)
            and not name.endswith((" ", "."))
            and Path(name).name == name
        )

    @staticmethod
    def sha256_from_digest(digest: str) -> Optional[str]:
        parts = digest.split(":", 1)
        if len(parts) != 2 or parts[0].lower() != "sha256":
            return None
        value = parts[1].lower()
        if len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
            return None
        return value

    def _download(self, url: str, path: Path, size: int, digest: str = "") -> dict[str, Any]:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(path.suffix + ".part")
        expected_hash = self.sha256_from_digest(digest)
        if expected_hash is None:
            return {"status": False, "msg": "缺少有效的 SHA-256"}
        sha256 = hashlib.sha256()
        try:
            with temporary.open("wb") as stream:
                with httpx.Client(follow_redirects=True) as client:
                    with client.stream("GET", url, timeout=httpx.Timeout(15.0, connect=5.0)) as response:
                        response.raise_for_status()
                        total_size = size or int(response.headers.get("Content-Length", 0))
                        downloaded = 0
                        for chunk in response.iter_bytes(chunk_size=64 * 1024):
                            if self._cancelled.is_set():
                                raise _DownloadCancelled()
                            if chunk:
                                stream.write(chunk)
                                sha256.update(chunk)
                                downloaded += len(chunk)
                                self.progress({
                                    "sizeShow": f"{self.bytes_to_size(downloaded)} / {self.bytes_to_size(total_size)}",
                                    "percentage": min(100, int(downloaded / total_size * 100)) if total_size else 0,
                                })
                stream.flush()
                os.fsync(stream.fileno())
            if self._cancelled.is_set():
                raise _DownloadCancelled()
            if expected_hash and sha256.hexdigest().lower() != expected_hash:
                self._remove(temporary)
                return {"status": False, "msg": "安装包完整性校验失败"}
            os.replace(temporary, path)
            return {"status": True, "msg": "下载成功", "downloadPath": str(path)}
        except _DownloadCancelled:
            self._remove(temporary)
            return {"status": False, "msg": "取消更新"}
        except httpx.TimeoutException:
            self._remove(temporary)
            return {"status": False, "msg": "连接超时"}
        except httpx.NetworkError:
            self._remove(temporary)
            return {"status": False, "msg": "联网失败"}
        except Exception as exc:
            self._remove(temporary)
            return {"status": False, "msg": str(exc)}

    @staticmethod
    def _remove(path: Path) -> None:
        try:
            path.unlink()
        except OSError:
            pass

    @staticmethod
    def bytes_to_size(byte_count: int) -> str:
        value = float(byte_count)
        for index, unit in enumerate(("B", "KB", "MB", "GB", "TB", "PB", "EB")):
            if value < 1024 or unit == "EB":
                decimals = 0 if index < 2 else 1 if index == 2 else 2
                return f"{round(value, decimals)} {unit}"
            value /= 1024
        return f"{byte_count} B"  # pragma: no cover
