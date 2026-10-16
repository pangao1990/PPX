"""Cross-platform single-instance lock for desktop applications."""

from __future__ import annotations

import errno
import os
from pathlib import Path
from typing import BinaryIO, Optional


class InstanceAlreadyRunning(RuntimeError):
    """Raised when another process owns the application's instance lock."""


class InstanceLock:
    """Hold an OS lock; process exit releases it even after a crash."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._stream: Optional[BinaryIO] = None

    def acquire(self) -> None:
        if self._stream is not None:
            raise InstanceAlreadyRunning("应用已经在运行")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        descriptor = os.open(self.path, os.O_CREAT | os.O_RDWR, 0o600)
        stream = os.fdopen(descriptor, "r+b")
        try:
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            stream.close()
            if exc.errno in (errno.EACCES, errno.EAGAIN, errno.EDEADLK):
                raise InstanceAlreadyRunning("应用已经在运行") from exc
            raise
        try:
            stream.write(f"{os.getpid()}\n".encode("ascii"))
            stream.truncate()
            stream.flush()
        except BaseException:
            stream.close()
            raise
        self._stream = stream

    def release(self) -> None:
        if self._stream is None:
            return
        stream, self._stream = self._stream, None
        # Keep the file: unlinking it lets racing processes lock different inodes.
        stream.close()

    def __enter__(self) -> "InstanceLock":
        self.acquire()
        return self

    def __exit__(self, *_args: object) -> None:
        self.release()
