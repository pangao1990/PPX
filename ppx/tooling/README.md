# Tooling

`ppx/tooling/` 只放 PPX 开源仓库维护工具，`ppx new` 生成的普通应用不包含这里：

- `docs/`：框架更新策略与包发布说明。
- `scripts/`：跨平台命令转发、清理、安装包和发布产物检查。
- `tests/`：Python 自动化测试，包括配置、RPC、更新、目录边界和三端打包结构。

应用业务代码只放在根目录的 `api/`、`gui/src/` 和 `api/resources/`，可修改打包资源位于 `ppx/assets/`。两个待发布包位于 `ppx/packages/`。
