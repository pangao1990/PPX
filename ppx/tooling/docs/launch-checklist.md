# 上线步骤与当前状态

检查日期：2026-09-05。本地通过不等于远端 CI 或三端发布验收已经完成。

## 当前已完成

- 客户端恢复原版 LOGO，图像与旧版文件 SHA-256 一致；保留原版安装图标。
- 客户端与介绍站风格统一，品牌和普通页面不再刻意附加版本标记；实际版本号、兼容说明和旧 URL 保留。
- Python / JavaScript 回归、GUI 构建、依赖一致性、安全审计、发布包元数据检查。
- `build` 与文档部署工作流通过 actionlint 检查；引用的 Action 版本存在。
- macOS 客户端交互与安装包验证；详细范围见 [验证记录](verification.md)。
- V5 原文档和归档入口保留；源码使用已经公开的 `V5.3.4` 标签。

## 还不能省略的验收

- 修改后的 Actions 尚未在远端运行，Windows/Linux 安装包及真机体验尚未验收。
- 正式分发前完成 macOS Developer ID 签名/公证及 Windows 签名方案。
- 公网更新下载、安装、覆盖升级及卸载需要在三套目标系统实际验证。
- 截至本次检查，PyPI 的 `ppx-py==6.0.0`、npm 的 `ppx-js@6.0.0` 尚无公开版本。发布前仍须确认账号拥有包名权限，且版本未被占用。
- 本机 Python 使用 LibreSSL，`twine check` 虽通过但有 urllib3 兼容性提示；正式联网上传应使用带受支持 OpenSSL 的 Python 环境。
- 新版介绍站已部署，教程仓库提交为 `71dc5b4`，[Deploy 运行成功](https://github.com/pangao1990/docs-ppx/actions/runs/33960956269)。客户端已同步最新版文档和 V5 归档入口。

## 建议的执行顺序

1. **核对两个仓库的改动。** 应用与 VitePress 文档是独立仓库，应分别提交。特别检查本次结构迁移涉及的删除和新增文件，勿只提交已跟踪文件而漏掉 `ppx/`、锁文件、新组件或文档。
2. **保留旧版。** 公开的 `V5.3.4` 标签已可访问，不要删除或移动它。本地 `v5` 维护分支若需公开，可在核对指向后单独推送；目前 README 不依赖该分支才能访问旧源码。
3. **提交候选代码并运行 Actions。** 推送到 `main` 自动触发，或者在工作流已进入默认分支后通过 **Actions → build → Run workflow** 手动触发。查看质量矩阵和三个打包任务，必须全部通过。
4. **下载三个 Artifact。** 从运行记录下载 `Setup_系统_架构`，解压并核对 `SHA256SUMS`。候选保留 14 天；它们还不是公开 Release。
5. **完成三端安装验收。** 按 [交互验收清单](desktop-qa.md)逐项点击，验证实际业务依赖、权限、文件选择、存储、退出与更新。Linux 候选以 Ubuntu 24.04 为构建基线；不能直接宣称兼容更旧发行版。发现问题先修复再重新生成候选。
6. **发布两个框架包。** 按 [两包发布说明](publishing.md)从最终提交重新生成 wheel/sdist/tgz，校验并在全新环境安装。先发布 `ppx-py`，从 PyPI 安装验证；再发布 `ppx-js`，从 npm 安装验证。同版本不可覆盖。
7. **上线介绍站。** 在文档仓库确认 GitHub Pages 使用 GitHub Actions，推送文档并检查 Deploy 工作流。线上逐个验证新文档、搜索、资源和 V5 归档入口。注意应用仓库与文档仓库的部署是两个操作。
8. **同步状态并生成最终客户端。** 客户端的在线文档入口已随介绍站部署完成同步；后续发布仍须重新构建、复测。README 的“准备发布”提示应在框架包真实可安装后修改。确保最后的提交、测试记录和安装包来自同一份代码。
9. **创建 GitHub Release。** 两个包都可公开安装、最终客户端通过验收后，为对应提交创建匹配 `ppx-update.json` 的版本标签，上传三端签名安装包、更新清单和校验值。当前更新器会检查 GitHub asset 的 SHA-256 digest，不能只上传一个校验文本就认为客户端验证已满足。
10. **发送 Issue 回复。** 三条历史问题分别处理；不要因为新版本完成就把未复现问题标记为已修复。草稿供维护者核对后亲自点击 Comment，是否关闭 Issue 也由维护者决定。

若采用分阶段上线，每个阶段都应保留准确的状态说明。

## 仅供本地预检的命令

```bash
pnpm check
node ppx/tooling/scripts/python.mjs -m pip check
pnpm audit --audit-level high --registry=https://registry.npmjs.org
pnpm build
pnpm verify:installer
node ppx/tooling/scripts/python.mjs ppx/tooling/scripts/installer_checksum.py
git diff --check
```

在文档仓库另行执行 `pnpm check`。以上命令不发布包、不推送 Git、不创建 Release。
