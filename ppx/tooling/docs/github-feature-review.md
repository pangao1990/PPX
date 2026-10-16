# 同类开源项目功能调研（2026-09-26）

本次调研通过 GitHub Releases API 查看了 `r0x0r/pywebview` 6.2.1、`beeware/briefcase` 0.4.5 和 `tauri-apps/tauri` v3 alpha 的近期发布内容，并结合 PPX 的 pywebview + PyInstaller 架构筛选可移植功能。

## 可借鉴功能

- Briefcase 0.4.5 强调隔离环境、下载哈希校验和安装器选项。PPX 已有应用更新包的 SHA-256 校验、框架更新清单校验和三端安装包验证，因此无需重复引入一套依赖管理器。
- pywebview 6.2.1 的近期修复集中在 Windows 屏幕缩放报告；PPX 的窗口尺寸目前基于 `webview.screens[0]`，已保留在依赖版本中，后续 Windows 验收应继续覆盖高 DPI 场景。
- Tauri 的 single-instance 能力适合 PPX 桌面应用：同一应用被用户从快捷方式重复打开时，第二个进程不应再创建第二个窗口或重复占用资源。

## 本次移植

PPX 新增 `[application].singleInstance`（默认 `true`）。运行时在用户数据目录持有系统文件锁（Windows 使用 msvcrt，macOS/Linux 使用 flock）：

- 已有存活进程持有锁时，第二次启动会立即失败并给出明确提示；
- 进程退出或崩溃时由系统自动释放锁，不依赖 PID 检查和删除锁文件；
- 窗口正常关闭或启动中途失败都会在 `finally` 中释放锁；
- 设为 `false` 可兼容需要多实例的开发或特殊应用。

同时修复了 pywebview 单文件选择在部分平台返回字符串时被逐字符遍历的问题。
