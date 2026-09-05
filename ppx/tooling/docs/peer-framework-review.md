# 同类开源框架功能评估

评估日期：2026-09-04。仅记录与 PPX“业务与框架分离”目标直接相关的能力。

## 本次采用

| 来源 | 同类能力 | PPX 实现 |
| --- | --- | --- |
| Tauri create-tauri-app、Wails templates | 创建时选择前端模板 | `ppx new --frontend vanilla|vue|react` |
| Tauri `icon`、Wails `generate icons` | 用一张主图生成平台图标 | `ppx icon SOURCE` 生成 PNG/ICO/ICNS |
| Wails `doctor`、buildinfo | 环境信息用于自动化诊断 | `ppx doctor --json` |

官方参考：

- https://github.com/tauri-apps/create-tauri-app
- https://v2.tauri.app/develop/icons/
- https://wails.io/docs/reference/cli/
- https://briefcase.readthedocs.io/en/latest/reference/commands/
- https://www.electronforge.io/cli

## 暂缓

- 权限/Capability：Tauri 的最小权限模型值得借鉴，但 PPX 需要先定义多窗口、远程页面和插件边界；V6.0.0 不仓促增加一套难以验证的权限语言。
- 托盘、全局快捷键、自动启动、系统通知：需要逐平台行为与签名测试，适合作为后续独立模块。
- 跨平台交叉编译：pywebview 与系统 WebView 依赖决定了应在目标系统构建，继续使用三端 CI，不宣称本机交叉打包。
- 自动改写业务代码：与 PPX 的业务保护原则冲突，框架更新只更新两个包和受管锁文件。
