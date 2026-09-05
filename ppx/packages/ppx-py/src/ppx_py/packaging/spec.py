"""Generate all PyInstaller internals inside build/cache."""

from __future__ import annotations

import platform
from pathlib import Path

from ..settings import Settings


def create_entry(root: Path) -> Path:
    cache = root / "build" / "cache"
    cache.mkdir(parents=True, exist_ok=True)
    entry = cache / "ppx_entry.py"
    entry.write_text(
        "from ppx_py.runtime import run_project\n\n"
        "if __name__ == '__main__':\n"
        "    run_project()\n",
        encoding="utf-8",
    )
    return entry


def create_spec(root: Path, settings: Settings, console: bool) -> Path:
    cache = root / "build" / "cache"
    cache.mkdir(parents=True, exist_ok=True)
    spec_path = cache / "ppx.spec"
    entry = create_entry(root)
    system = platform.system()
    icon_suffix = {"Darwin": "icns", "Windows": "ico"}.get(system, "png")
    icon = settings.asset_dir / f"logo.{icon_suffix}"
    if not icon.is_file():
        raise FileNotFoundError(f"缺少打包图标: {icon}")
    if not settings.frontend_dir.is_dir():
        raise FileNotFoundError(f"缺少前端产物: {settings.frontend_dir}")
    datas = [(str(settings.frontend_dir), "web"), (str(settings.config_path), ".")]
    if settings.resource_source_dir.is_dir():
        datas.append((str(settings.resource_source_dir), "resources"))
    hidden = list(settings.python.modules)

    if system == "Linux":
        executable = f"""exe = EXE(
    pyz, a.scripts, a.binaries, a.datas, [],
    name={settings.project.name!r}, debug=False, bootloader_ignore_signals=False,
    strip=False, upx=True, console={console!r}, icon={str(icon)!r},
)
"""
        bundle = ""
    else:
        executable = f"""exe = EXE(
    pyz, a.scripts, [], exclude_binaries=True,
    name={settings.project.name!r}, debug=False, bootloader_ignore_signals=False,
    strip=False, upx=True, console={console!r}, icon={str(icon)!r},
)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=True, name={settings.project.name!r})
"""
        bundle = ""
        if system == "Darwin":
            bundle = f"""app = BUNDLE(
    coll, name={str(settings.project.name + '.app')!r}, icon={str(icon)!r},
    bundle_identifier={settings.app_id!r}, version={settings.project.version!r},
)
"""

    spec_path.write_text(
        f"""# -*- mode: python ; coding: utf-8 -*-
a = Analysis(
    [{str(entry)!r}], pathex=[{str(root)!r}], binaries=[], datas={datas!r},
    hiddenimports={hidden!r}, hookspath=[],
    # Pygments' optional image formatter imports Pillow and causes PyInstaller
    # to collect every PIL image plugin.  PPX does not use that formatter, but
    # excluding it (instead of PIL itself) still lets business code use Pillow.
    hooksconfig={{}}, runtime_hooks=[], excludes=['pygments.formatters.img'], noarchive=False,
)
pyz = PYZ(a.pure)
{executable}
{bundle}
""",
        encoding="utf-8",
    )
    return spec_path
