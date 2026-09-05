"""Run Vite and the PPX desktop runtime as one developer command."""

from __future__ import annotations

import subprocess
import socket
import time
import os
import signal
import shutil

from ..project import find_project_root, load_settings
from ..runtime import run_project


def _wait_for_port(port: int, process: subprocess.Popen[bytes], timeout: float = 30.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"前端开发服务提前退出，退出码 {process.returncode}")
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.2):
                return
        except OSError:
            time.sleep(0.1)
    raise TimeoutError(f"等待前端开发服务端口 {port} 超时")


def _stop(process: subprocess.Popen[bytes]) -> None:
    if os.name == "nt":
        if process.poll() is None:
            subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], capture_output=True, check=False)
        return
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait()


def run(args: object) -> int:
    root = find_project_root()
    settings = load_settings(root)
    process = None
    try:
        if not getattr(args, "skip_frontend", False):
            try:
                with socket.create_connection(("127.0.0.1", settings.development.port), timeout=0.2):
                    raise RuntimeError(
                        f"端口 {settings.development.port} 已被占用。请修改 development.port；"
                        "如果该端口是你已启动的当前项目前端，请使用 --skip-frontend。"
                    )
            except OSError:
                pass
            process = subprocess.Popen(
                [shutil.which("pnpm") or "pnpm", "-C", settings.paths.frontend, "run", "dev",
                 "--host", "127.0.0.1", "--port", str(settings.development.port), "--strictPort"],
                cwd=root,
                start_new_session=os.name != "nt",
            )
            _wait_for_port(settings.development.port, process)
        run_project(root / "ppx.toml", dev=True, cef=bool(getattr(args, "cef", False)))
        return 0
    except KeyboardInterrupt:
        return 130
    except Exception as exc:
        print(f"[失败] {exc}")
        return 1
    finally:
        if process is not None:
            _stop(process)
