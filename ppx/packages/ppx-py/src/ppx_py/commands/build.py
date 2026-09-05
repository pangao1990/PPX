"""Build the frontend and package the desktop application."""

from __future__ import annotations

import subprocess
import sys

from ..packaging import create_installer, create_spec
from ..project import find_project_root, load_settings


def run(args: object) -> int:
    root = find_project_root()
    settings = load_settings(root)
    if not getattr(args, "skip_frontend", False):
        result = subprocess.run(
            ["pnpm", "-C", settings.paths.frontend, "run", "build"], cwd=root, check=False
        )
        if result.returncode:
            return result.returncode
    spec = create_spec(root, settings, bool(getattr(args, "console", False)))
    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--clean",
        "--noconfirm",
        "--distpath",
        str(root / "build"),
        "--workpath",
        str(root / "build" / "cache" / "work"),
        str(spec),
    ]
    result = subprocess.call(command, cwd=root)
    if result:
        return result
    if getattr(args, "console", False):
        print(f"调试应用已生成: {root / 'build'}")
        return 0
    try:
        installer = create_installer(root, settings)
        print(f"安装包已生成并验证: {installer}")
        return 0
    except Exception as exc:
        print(f"[失败] {exc}")
        return 1
