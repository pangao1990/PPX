"""PPX command line entry point."""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from . import __version__
from .commands import build, dev, doctor, icon, update
from .scaffold import create_project, initialize_project


def _new(args: object) -> int:
    try:
        target = create_project(
            str(getattr(args, "name")),
            getattr(args, "directory", None),
            str(getattr(args, "frontend", "vanilla")),
        )
        print(f"PPX 项目已创建: {target}")
        print(f"下一步: cd {target.name} && ppx init && ppx dev")
        return 0
    except Exception as exc:
        print(f"[失败] {exc}")
        return 1


def _init(_args: object) -> int:
    return initialize_project()


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ppx", description="PPX developer tools")
    parser.add_argument("--version", action="version", version=f"PPX {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)

    new_parser = commands.add_parser("new", help="创建只有业务代码与可配置资源的新项目")
    new_parser.add_argument("name", help="项目名称")
    new_parser.add_argument("--directory", help="目标目录，默认使用项目名生成目录")
    new_parser.add_argument(
        "--frontend",
        choices=("vanilla", "vue", "react"),
        default="vanilla",
        help="前端模板，默认 vanilla",
    )
    new_parser.set_defaults(handler=_new)

    init_parser = commands.add_parser("init", help="安装业务依赖并检查项目")
    init_parser.set_defaults(handler=_init)

    doctor_parser = commands.add_parser("doctor", help="检查项目和开发环境")
    doctor_parser.add_argument("--json", action="store_true", dest="json_output", help="输出机器可读 JSON")
    doctor_parser.set_defaults(handler=doctor.run)

    icon_parser = commands.add_parser("icon", help="从一张方形主图生成三端应用图标")
    icon_parser.add_argument("source", help="至少 512×512 的方形 PNG/JPEG/WebP 图片")
    icon_parser.add_argument("--output", help="输出目录，默认使用 ppx.toml 的 paths.assets")
    icon_parser.set_defaults(handler=icon.run)

    update_parser = commands.add_parser("update", help="安全更新 PPX 框架依赖")
    mode = update_parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="只检查可用更新")
    mode.add_argument("--dry-run", action="store_true", help="显示更新计划，不修改文件或环境")
    update_parser.add_argument("--to", metavar="VERSION", help="更新到指定 V6 版本")
    update_parser.set_defaults(handler=update.run)

    dev_parser = commands.add_parser("dev", help="同时启动前端与桌面窗口")
    dev_parser.add_argument("--cef", action="store_true", help="使用 CEF（仅 Windows）")
    dev_parser.add_argument("--skip-frontend", action="store_true", help="前端服务已启动时不重复启动")
    dev_parser.set_defaults(handler=dev.run)

    build_parser = commands.add_parser("build", help="构建前端并用 PyInstaller 打包")
    build_parser.add_argument("--console", action="store_true", help="保留控制台窗口")
    build_parser.add_argument("--skip-frontend", action="store_true", help="不重复构建前端")
    build_parser.set_defaults(handler=build.run)
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    # Windows redirects stdout/stderr using the legacy system code page.
    # CLI output is UTF-8 so Chinese diagnostics also work in pipes and logs.
    for stream in (sys.stdout, sys.stderr):
        if stream is not None and hasattr(stream, "reconfigure") and not stream.isatty():
            stream.reconfigure(encoding="utf-8", errors="backslashreplace")
    args = make_parser().parse_args(argv)
    return int(args.handler(args))


if __name__ == "__main__":
    raise SystemExit(main())
