"""Atomic JSON key/value storage kept outside the application bundle."""

from __future__ import annotations

import json
import os
import threading
from pathlib import Path
from typing import Any

from ..bridge import BridgeError


class JsonStorage:
    def __init__(self, path: Path) -> None:
        self.path = path
        self._lock = threading.RLock()

    def initialize(self) -> None:
        with self._lock:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            if not self.path.exists():
                self._write({})

    def get(self, key: str, default: Any = None) -> Any:
        self._validate_key(key)
        return self._read().get(key, default)

    def set(self, key: str, value: Any) -> bool:
        self._validate_key(key)
        self._validate_value(value)
        with self._lock:
            data = self._read()
            data[key] = value
            self._write(data)
        return True

    def delete(self, key: str) -> bool:
        self._validate_key(key)
        with self._lock:
            data = self._read()
            existed = key in data
            data.pop(key, None)
            self._write(data)
        return existed

    def _read(self) -> dict[str, Any]:
        with self._lock:
            if not self.path.exists():
                return {}
            with self.path.open("r", encoding="utf-8") as stream:
                value = json.load(stream)
            if not isinstance(value, dict):
                raise ValueError(f"存储文件根节点必须是对象: {self.path}")
            return value

    def _write(self, value: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + ".part")
        with temporary.open("w", encoding="utf-8") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, self.path)

    @staticmethod
    def _validate_key(key: Any) -> None:
        if not isinstance(key, str):
            raise BridgeError("INVALID_PARAMS", "存储键必须是字符串")

    @staticmethod
    def _validate_value(value: Any) -> None:
        try:
            json.dumps(value, ensure_ascii=False, allow_nan=False)
        except (TypeError, ValueError) as exc:
            raise BridgeError("INVALID_PARAMS", "存储值必须是可序列化的标准 JSON 数据") from exc
