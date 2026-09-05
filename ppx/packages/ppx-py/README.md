# ppx-py

PPX 的 Python 运行时、命令行与三端打包器。开发者通过 `ppx new/init/icon/dev/doctor/update/build` 使用它，不需要接触框架内部实现。

## 安装与创建项目

需要 Python 3.9+。前端工具链需要 Node.js 22.13+ 与 pnpm 11.x。

```bash
python -m pip install ppx-py==6.0.0
ppx new my-app --frontend vue
cd my-app
ppx init
ppx dev
```

新项目只暴露 Python 业务目录 `api/`、Web 前端目录 `gui/`、可替换图片目录 `ppx/assets/`，以及 `ppx.toml`、`ppx.lock` 等配置文件。框架入口、窗口协调、PyInstaller spec 和三端安装器脚本均在包内实现并按需生成。

## Python 业务 API

```python
from ppx_py import api_method


@api_method("user.greet")
def greet(name: str):
    return {"message": f"你好，{name}！"}
```

也可以直接注册 `async def`。在 `ppx.toml` 的 `[python].modules` 中声明业务模块后，PPX 会自动导入并注册带 `@api_method` 的函数。普通业务项目不需要创建 `Application`、`Bridge` 或 `main.py`。

使用 `resource_path()` 读取打包前后位置一致的业务资源，使用 `app_data_path()` 获取当前操作系统规范的可写用户数据路径。内置 RPC 还提供打开/保存文件对话框、目录选择、窗口状态与最小化/最大化/全屏/关闭控制。

## 命令

```text
ppx new NAME --frontend TEMPLATE 创建 vanilla、vue 或 react 项目
ppx init                         安装业务依赖并诊断
ppx doctor                       检查配置、版本、资源和平台工具
ppx doctor --json                输出机器可读诊断结果
ppx icon SOURCE                  从方形主图生成三端图标
ppx dev                          启动前端并打开桌面窗口
ppx update                       兼容校验后更新 ppx-py 与 ppx-js
ppx build                        生成当前平台应用和安装包
```

`ppx update --check` 和 `ppx update --dry-run` 不修改环境。兼容更新不会覆盖 `api/`、`gui/src/`、`ppx/assets/` 或应用数据；不兼容更新会在安装前停止。

`ppx icon` 接受至少 512×512 的方形 PNG、JPEG 或 WebP 图片，在 `ppx/assets/` 原子生成 `logo.png`、`logo.ico` 与 `logo.icns`。DMG 背景图仍由开发者单独维护。

完整文档：[PPX 文档](https://blog.pangao.vip/docs-ppx/v6/guide/introduction)
