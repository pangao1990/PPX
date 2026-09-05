"""Create and verify the native installer for the current platform."""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

from ..settings import Settings


class PackagingError(RuntimeError):
    pass


def installer_path(root: Path, settings: Settings, system: Optional[str] = None) -> Path:
    current = system or platform.system()
    suffix = {"Darwin": "macOS.dmg", "Windows": "Windows.exe", "Linux": "Linux.deb"}.get(current)
    if suffix is None:
        raise PackagingError(f"不支持的平台: {current}")
    return root / "build" / f"{settings.project.name}-V{settings.project.version}_{suffix}"


def create_installer(root: Path, settings: Settings) -> Path:
    system = platform.system()
    if system == "Darwin":
        result = _macos(root, settings)
    elif system == "Windows":
        result = _windows(root, settings)
    elif system == "Linux":
        result = _linux(root, settings)
    else:
        raise PackagingError(f"不支持的平台: {system}")
    errors = verify_installer(result, system)
    if errors:
        raise PackagingError("安装包验证失败: " + "; ".join(errors))
    return result


def verify_installer(path: Path, system: Optional[str] = None) -> List[str]:
    current = system or platform.system()
    errors: List[str] = []
    if not path.is_file():
        return [f"文件不存在: {path}"]
    if path.stat().st_size < 1024:
        errors.append("文件异常小")
    header = path.read_bytes()[:8]
    if current == "Windows" and not header.startswith(b"MZ"):
        errors.append("Windows 安装包缺少 MZ 文件头")
    if current == "Linux" and not header.startswith(b"!<arch>\n"):
        errors.append("Debian 安装包文件头无效")
    if current == "Darwin":
        hdiutil = shutil.which("hdiutil")
        if not hdiutil:
            errors.append("找不到 hdiutil")
        elif subprocess.run([hdiutil, "verify", str(path)], capture_output=True, check=False).returncode:
            errors.append("hdiutil verify 未通过")
    return errors


def _macos(root: Path, settings: Settings) -> Path:
    app = root / "build" / f"{settings.project.name}.app"
    if not app.is_dir():
        raise PackagingError(f"找不到 macOS 应用: {app}")
    background = settings.asset_dir / "dmg-background.png"
    icon = settings.asset_dir / "logo.icns"
    for path in (background, icon):
        if not path.is_file():
            raise PackagingError(f"缺少 DMG 资源: {path}")
    output = installer_path(root, settings, "Darwin")
    output.unlink(missing_ok=True)
    config = root / "build" / "cache" / "dmg_settings.py"
    config.parent.mkdir(parents=True, exist_ok=True)
    config.write_text(
        "files = [%r]\n" % str(app)
        + "symlinks = {'Applications': '/Applications'}\n"
        + "icon_locations = {%r: (160, 140), 'Applications': (430, 140)}\n" % app.name
        + "window_rect = ((200, 200), (590, 416))\n"
        + "icon_size = 72\ntext_size = 12\n"
        + "badge_icon = %r\nbackground = %r\n" % (str(icon), str(background)),
        encoding="utf-8",
    )
    _run([sys.executable, "-m", "dmgbuild", "-s", str(config), f"{settings.project.name} V{settings.project.version}", str(output)], root)
    return output


def _windows(root: Path, settings: Settings) -> Path:
    app_dir = root / "build" / settings.project.name
    executable = app_dir / f"{settings.project.name}.exe"
    if not executable.is_file():
        raise PackagingError(f"找不到 Windows 应用: {executable}")
    iscc = _find_iscc()
    if iscc is None:
        raise PackagingError("找不到 Inno Setup 6（ISCC.exe），请先安装后再执行 ppx build")
    output = installer_path(root, settings, "Windows")
    iss = root / "build" / "cache" / "installer.iss"
    iss.parent.mkdir(parents=True, exist_ok=True)

    def q(value: object) -> str:
        return str(value).replace('"', '""')

    iss.write_text(f'''#define MyAppName "{q(settings.project.name)}"
#define MyAppVersion "{q(settings.project.version)}"
#define MyAppPublisher "{q(settings.project.developer)}"
#define MyAppURL "{q(settings.project.website)}"
#define MyAppExeName "{q(settings.project.name)}.exe"
[Setup]
AppId={{{{{q(settings.project.windows_app_id)}}}
AppName={{#MyAppName}}
AppVersion={{#MyAppVersion}}
AppPublisher={{#MyAppPublisher}}
AppPublisherURL={{#MyAppURL}}
DefaultDirName={{autopf}}\\{{#MyAppName}}
PrivilegesRequired=lowest
OutputDir={q(root / "build")}
OutputBaseFilename={q(output.stem)}
SetupIconFile={q(settings.asset_dir / "logo.ico")}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
[Languages]
Name: "chinesesimp"; MessagesFile: "compiler:Default.isl"
[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; Flags: unchecked
[Files]
Source: "{q(app_dir)}\\*"; DestDir: "{{app}}"; Flags: recursesubdirs createallsubdirs ignoreversion
[Icons]
Name: "{{autoprograms}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"
Name: "{{autodesktop}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"; Tasks: desktopicon
[Run]
Filename: "{{app}}\\{{#MyAppExeName}}"; Flags: nowait postinstall skipifsilent
''', encoding="utf-8-sig")
    _run([str(iscc), "/Qp", str(iss)], root)
    return output


def _find_iscc() -> Optional[Path]:
    direct = shutil.which("ISCC.exe") or shutil.which("iscc")
    if direct:
        return Path(direct)
    for variable in ("ProgramFiles(x86)", "ProgramFiles", "LOCALAPPDATA"):
        base = os.environ.get(variable)
        if base:
            candidate = Path(base) / "Inno Setup 6" / "ISCC.exe"
            if candidate.is_file():
                return candidate
    return None


def _linux(root: Path, settings: Settings) -> Path:
    executable = root / "build" / settings.project.name
    if not executable.is_file():
        raise PackagingError(f"找不到 Linux 应用: {executable}")
    dpkg = shutil.which("dpkg-deb")
    if not dpkg:
        raise PackagingError("找不到 dpkg-deb，请先安装 dpkg-dev")
    stage = root / "build" / "cache" / "deb" / settings.project.slug
    if stage.exists():
        shutil.rmtree(stage)
    binary_dir = stage / "opt" / settings.project.slug / "bin"
    desktop_dir = stage / "usr/share/applications"
    icon_dir = stage / "usr/share/icons/hicolor/128x128/apps"
    control_dir = stage / "DEBIAN"
    for path in (binary_dir, desktop_dir, icon_dir, control_dir):
        path.mkdir(parents=True, exist_ok=True)
    shutil.copy2(executable, binary_dir / settings.project.slug)
    shutil.copy2(settings.asset_dir / "logo.png", icon_dir / f"{settings.project.slug}.png")
    architecture = "arm64" if platform.machine().lower() in {"arm64", "aarch64"} else "amd64"
    (control_dir / "control").write_text(
        f"Package: {settings.project.slug}\nVersion: {settings.project.version}\nSection: utils\nPriority: optional\nArchitecture: {architecture}\nMaintainer: {settings.project.developer}\nDescription: {settings.project.description or settings.project.name}\n",
        encoding="utf-8",
    )
    (desktop_dir / f"{settings.project.slug}.desktop").write_text(
        f"[Desktop Entry]\nName={settings.project.name}\nComment={settings.project.description}\nExec=/opt/{settings.project.slug}/bin/{settings.project.slug}\nIcon={settings.project.slug}\nTerminal=false\nType=Application\nCategories=Utility;\n",
        encoding="utf-8",
    )
    output = installer_path(root, settings, "Linux")
    output.unlink(missing_ok=True)
    _run([dpkg, "--build", "--root-owner-group", str(stage), str(output)], root)
    return output


def _run(command: List[str], root: Path) -> None:
    result = subprocess.run(command, cwd=root, check=False)
    if result.returncode:
        raise PackagingError(f"命令执行失败 ({result.returncode}): {' '.join(command)}")
