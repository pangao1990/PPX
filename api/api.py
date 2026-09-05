"""User-owned API methods. PPX never overwrites this file during updates."""

from ppx_py import BridgeError, api_method


@api_method("user.greet")
def greet(name: str) -> dict[str, str]:
    if not isinstance(name, str) or not name.strip() or len(name.strip()) > 80:
        raise BridgeError("INVALID_PARAMS", "请输入 1 至 80 个字符的名字")
    return {"message": f"你好，{name.strip()}！"}
