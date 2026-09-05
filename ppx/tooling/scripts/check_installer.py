#!/usr/bin/env python3
"""Verify the installer produced for the current operating system."""

from __future__ import annotations

import argparse
import platform
import sys
from pathlib import Path
from typing import List, Optional

from ppx_py import Settings
from ppx_py.packaging import installer_path, verify_installer


ROOT = Path(__file__).resolve().parents[3]


def expected_installer(root: Path, system: str, settings: Settings) -> Path:
    return installer_path(root, settings, system)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="检查 PPX 当前平台安装包")
    parser.add_argument("--system", choices=("Darwin", "Windows", "Linux"), default=platform.system())
    parser.add_argument("--path", type=Path, help="覆盖默认安装包路径")
    args = parser.parse_args(argv)
    settings = Settings.load(ROOT / "ppx.toml")
    path = args.path.resolve() if args.path else expected_installer(ROOT, args.system, settings)
    errors = verify_installer(path, args.system)
    if errors:
        for error in errors:
            print(f"[失败] {error}")
        return 1
    print(f"[通过] {args.system} 安装包校验成功: {path} ({path.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
