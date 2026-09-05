# 发布状态与后续维护

检查日期：2026-09-05。当前代码、教程和两个框架包均已公开，项目版本保持 `6.0.0`。

## 正式分发入口

| 内容 | 入口 |
| --- | --- |
| Python 框架包 | [ppx-py 6.0.0](https://pypi.org/project/ppx-py/6.0.0/) |
| JavaScript 框架包 | [ppx-js 6.0.0](https://www.npmjs.com/package/ppx-js/v/6.0.0) |
| 三端示例安装包与更新清单 | [V6.0.0 Release](https://github.com/pangao1990/PPX/releases/tag/V6.0.0) |
| 最新教程 | [PPX 文档](https://blog.pangao.vip/docs-ppx/) |
| V5 教程 | [V5 归档](https://blog.pangao.vip/docs-ppx/v5/) |
| V5 源码 | [V5.3.4 标签](https://github.com/pangao1990/PPX/tree/V5.3.4) |

原版 LOGO、品牌配色、V5 原文和归档入口均保留。当前框架只依赖 `ppx-py` 与 `ppx-js`，旧三包不再用于当前项目。

## 已完成的验证

最终代码 `66ed38d` 已通过 [build 工作流](https://github.com/pangao1990/PPX/actions/runs/33963464721)：六组 Python/Node 组合、依赖审计和三个安装包任务全部成功。公开包在独立环境安装后，通过 56 项 Python、11 项 JavaScript 测试、新建项目、初始化、环境诊断和前端构建。详细证据与范围见[验证记录](verification.md)。

Release 安装包延续旧版文件名，通过 asset label 标明架构。macOS 包仅适用于 Apple Silicon / arm64；Windows 和 Linux 包为 x64。Linux 使用 Ubuntu 24.04 构建基线，其他架构和更早发行版需另行构建验证。

## 仍需按目标系统完成的验收

- Windows/Linux 真机安装、逐项交互、覆盖升级和卸载；CI 成功生成安装包不能替代真机测试。
- 正式代码签名、macOS Developer ID 公证，以及对应系统的来源验证。
- 使用应用自己的数据和升级渠道验证权限、数据迁移与回滚。

当前公开安装包没有完成代码签名/公证，应在下载说明中如实标明，不能宣称所有系统已经完成验收或绝对没有 bug。

## 后续发版步骤

1. 分别检查应用仓库与 VitePress 文档仓库，完整提交代码、资源与锁文件；保留 `V5.3.4` 标签和 V5 原文。
2. 运行 `pnpm check`，检查依赖和许可证。推送 `main` 后等待 `build` 的六组质量检查和三个打包任务全部成功；也可在 **Actions → build → Run workflow** 在线打包。
3. 下载 `Setup_系统_架构` Artifacts 并核对 `SHA256SUMS`，按[客户端交互清单](desktop-qa.md)完成目标系统验收。
4. 按[两包发布说明](publishing.md)验收最终 wheel/sdist/tgz。Python 包可通过独立的 `publish-pypi` 工作流上传，必须填写同一提交成功的 build 运行 ID；JavaScript 包使用 npm 官方发布流程。
5. 从公开 PyPI/npm 重新安装并测试，随后创建对应 Release，上传三端安装包、架构标签、更新清单及校验值。客户端会校验 GitHub asset 的 SHA-256 digest。
6. 文档仓库执行 `pnpm check`，提交并推送，等待 GitHub Pages 的 Deploy 成功；逐页验证线上内容、资源、搜索及 V5 往返。
7. 同步 README、变更记录与实际测试结果。PyPI/npm 不允许覆盖已经发布的同版本，`6.0.0` 的文档修订不会重新上传这两个包。
8. 历史 Issue 回复仍由维护者审核草稿并亲自点击 Comment；是否关闭问题也由维护者决定。
