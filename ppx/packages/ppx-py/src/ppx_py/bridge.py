"""A small, stable Python/JavaScript RPC boundary."""

from __future__ import annotations

import asyncio
import inspect
import json
import logging
import threading
import uuid
from collections.abc import Callable, Mapping, Sequence
from typing import Any, Optional


LOGGER = logging.getLogger(__name__)


class BridgeError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def api_method(name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Explicitly expose a user method under a stable RPC name."""

    if not name or "." not in name:
        raise ValueError("PPX API 名称必须包含命名空间，例如 user.greet")

    def decorate(function: Callable[..., Any]) -> Callable[..., Any]:
        setattr(function, "__ppx_api_method__", name)
        return function

    return decorate


class Bridge:
    """The only object exposed to ``window.pywebview.api``."""

    def __init__(self) -> None:
        self._methods: dict[str, Callable[..., Any]] = {}
        self._window: Any = None

    def set_window(self, window: Any) -> None:
        self._window = window

    def register(self, name: str, handler: Callable[..., Any]) -> None:
        if name in self._methods:
            raise ValueError(f"PPX API 已注册: {name}")
        self._methods[name] = handler

    def register_api(self, api: object) -> None:
        found = 0
        for _, member in inspect.getmembers(api, predicate=callable):
            name = getattr(member, "__ppx_api_method__", None)
            if name:
                self.register(name, member)
                found += 1
        if not found:
            raise ValueError("业务 API 没有使用 @api_method 注册任何方法")

    def call(self, method: str, params: Any = None, request_id: Optional[str] = None) -> dict[str, Any]:
        request_id = request_id or uuid.uuid4().hex
        try:
            handler = self._methods.get(method)
            if handler is None:
                raise BridgeError("METHOD_NOT_FOUND", f"未注册的 API: {method}")
            if params is None:
                arguments, keywords = (), {}
            elif isinstance(params, Mapping):
                arguments, keywords = (), dict(params)
            elif isinstance(params, Sequence) and not isinstance(params, (str, bytes, bytearray)):
                arguments, keywords = tuple(params), {}
            else:
                raise BridgeError("INVALID_PARAMS", "params 必须是对象、数组或 null")
            try:
                inspect.signature(handler).bind(*arguments, **keywords)
            except TypeError as exc:
                raise BridgeError("INVALID_PARAMS", str(exc)) from exc
            data = _resolve_awaitable(handler(*arguments, **keywords))
            try:
                json.dumps(data, allow_nan=False)
            except (TypeError, ValueError) as exc:
                raise BridgeError(
                    "INVALID_RESULT", "Python API 返回值必须是可序列化的 JSON 数据"
                ) from exc
            return {"ok": True, "data": data, "error": None, "requestId": request_id}
        except BridgeError as exc:
            return self._failure(exc.code, str(exc), request_id)
        except Exception:
            LOGGER.exception("PPX Python API 执行失败: method=%s requestId=%s", method, request_id)
            return self._failure("INTERNAL_ERROR", "Python API 执行失败", request_id)

    def emit(self, event: str, data: Any) -> None:
        if self._window is None:
            return
        # ASCII escaping also protects JavaScript parsing from U+2028/U+2029 separators.
        event_json = json.dumps(event)
        data_json = json.dumps(data, allow_nan=False)
        self._window.evaluate_js(
            f"if (typeof window.__ppxDispatch === 'function') window.__ppxDispatch({event_json}, {data_json})"
        )

    @staticmethod
    def _failure(code: str, message: str, request_id: str) -> dict[str, Any]:
        return {
            "ok": False,
            "data": None,
            "error": {"code": code, "message": message},
            "requestId": request_id,
        }


def _resolve_awaitable(value: Any) -> Any:
    """Resolve async business methods behind pywebview's synchronous JS API."""
    if not inspect.isawaitable(value):
        return value
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(value)

    result: list[Any] = []
    failure: list[BaseException] = []

    def run() -> None:
        try:
            result.append(asyncio.run(value))
        except BaseException as exc:  # Re-raised on the calling thread below.
            failure.append(exc)

    worker = threading.Thread(target=run, name="ppx-async-api", daemon=True)
    worker.start()
    worker.join()
    if failure:
        raise failure[0]
    return result[0]


class JavascriptAPI:
    """Only expose RPC dispatch; registration and event emission stay in Python."""

    def __init__(self, bridge: Bridge) -> None:
        self._bridge = bridge

    def call(self, method: str, params: Any = None, request_id: Optional[str] = None) -> dict[str, Any]:
        return self._bridge.call(method, params, request_id)
