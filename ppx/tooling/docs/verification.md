# 本地与远端验证记录

日期：2026-09-05。此记录说明本次修改的实际验证范围；通过本地测试不代表已经通过所有平台的发布验收。

最终源码提交 `2fe6d91` 的 [GitHub Actions](https://github.com/pangao1990/PPX/actions/runs/33962115357) 已全部通过：六组 Python/Node 质量检查，以及 Windows x64、macOS arm64、Linux x64 三个安装包任务。教程仓库提交 `617d673` 的 [Deploy](https://github.com/pangao1990/docs-ppx/actions/runs/33961884835) 已成功上线。以下结果仅对应本次验证的代码、依赖与环境。


## 自动化检查

本机为 macOS arm64。最初使用 Python 3.9，安全审计后已将项目 `.venv` 升级到 Python 3.13.5，使用 Pillow 12.3.0 和 Node.js 24.14。最终支持 Python 3.10+。执行：

```bash
pnpm check
node ppx/tooling/scripts/python.mjs -m pip check
pnpm pre
pnpm build
pnpm verify:installer
git diff --check
```

结果：

- doctor：17 项通过，0 项失败。
- Python：55 项测试通过。
- JavaScript：11 项测试通过。
- Vue 生产构建、发布源码一致性检查通过。
- Python 依赖一致性检查通过。
- macOS 调试 `.app`、正式 `.app` 和 `PPX-V6.0.0_macOS.dmg` 生成成功，DMG 校验通过。
- Vanilla、Vue、React 三种 `ppx new` 模板在临时目录中分别安装依赖并完成构建；该轮 `ppx-js` 使用本地包引用。
- 候选 wheel/sdist/tgz 通过发布产物检查，wheel/sdist 通过 `twine check`。在不继承系统包的独立虚拟环境安装候选 wheel，并在仓库外的临时目录创建新项目，使用候选 tgz 完成 `ppx init`、17 项 doctor 检查和 GUI 构建；实际注册业务模块后的 `user.greet` 返回正确结果。
- `pnpm audit` 未发现已知漏洞；应用和文档站工作流通过 actionlint。远端运行状态在下方单独记录；工作流静态检查不等于三端打包已通过。

新增回归覆盖：关闭超时、就绪监听清理、事件订阅异常隔离、重复取消订阅、错误 CPU 架构、并发下载、检查阶段取消、最后一块数据到达时取消、窗口显示前存储写入、端口占用及启动失败后的清理。

另通过实际启动 Vite 的集成检查确认：配置端口确实被使用，流程结束后端口释放。该检查调用真实 pnpm/Vite，不依赖 Popen 模拟。

## 真实桌面验证

开发运行时使用真实 pywebview 窗口：

- 页面显示“Python 已连接”。
- JavaScript → Python 问候结果正确，requestId 保留。
- 本地存储写入和读取一致；测试使用临时数据目录。
- 空名字返回 `INVALID_PARAMS`。
- `window.pywebview.api` 仅包含 `call`。

随后启动打包产物 `build/PPX.app/Contents/MacOS/PPX`，通过实际界面输入“打包验收”，点击调用，页面显示“你好，打包验收！”。原生文件对话框可打开；取消后恢复按钮并显示正常取消提示，没有把取消误报成失败。

本轮进一步按[客户端交互验收清单](desktop-qa.md)逐个点击打包客户端入口：中文与空格文件名多选、取消后保留列表、目录选择、便签保存后重启恢复及清空、内置文档和全部外链均完成检查。原来的 `/v6/guide/quick-start` 线上路径返回 404；客户端入门改为随包提供的离线说明，在线 V5 入口明确区分。项目仓库、发布、问题反馈和在线介绍站四个不同 URL 均返回 HTTP 200。

恢复品牌后再次构建最终 macOS `.app` 和 DMG，并生成 `build/SHA256SUMS`。重新打开最终应用，确认原版多色 P 图标、无多余版本标签、Python 已连接；输入“最终验收”后返回“你好，最终验收！”，开发文档按钮正常打开离线内容。此次复查未修改用户已有便签。

## 浏览器界面检查

使用 Playwright 检查 1280px 桌面、390px 窄屏、600px 中等窗口与 960×360 低高度窗口。普通浏览器场景显示预览状态并禁用桌面操作。

本轮浏览器回归完成 29 个常规检查点、9 个异常与恢复检查点，以及低高度侧栏滚动点击检查，均通过。

交互检查使用仅注入测试浏览器的 RPC 模拟器，不包含在应用代码或安装包中。覆盖问候、文件/目录路径展示、便签保存后刷新恢复，以及更新的检查、进度和取消/完成状态。模拟网络与文件对话框只能验证页面状态，不能代替真实下载或其他操作系统的原生对话框验收。

截图保存在本地忽略目录 `output/playwright/`，包括工作台、便签窄屏、文档首页、V5 原首页和文档深色窄屏。

## 文档站

在独立的 VitePress 仓库执行 `pnpm check`：

- 48 个页面构建成功。
- 1,605 个站内页面、资源及锚点链接检查通过。
- V5 原文档和资源共 25 个文件与原提交逐字节一致。
- 原 V5 首页完整保存至 `src/v5/home.md`，与原首页逐字节一致。
- 浏览器验证最新版首页 → V5 入口 → V5 原首页，归档提示和返回最新版链接正常。
- 本地搜索能找到“示例工作台”；390px 深色页面无横向溢出。

## 尚未覆盖的发布条件

本轮没有运行 Windows/Linux 真机安装、覆盖升级、卸载；远端 CI 已完成完整的 Python/Node 版本矩阵和三端安装包生成。macOS 构建产物未做 Developer ID 签名和公证；本地构建通过不等于可以绕过 Gatekeeper 公开分发。

2026-09-05 上线复查后，教程仓库提交 `617d673` 已推送，[GitHub Pages 部署成功](https://github.com/pangao1990/docs-ppx/actions/runs/33961884835)。客户端已同步在线文档入口。框架包与 Release 的公开发布验收见本文末尾记录。真实公网 Release 下载、系统安装权限、签名与应用数据迁移仍需使用应用自己的发布渠道完成验收。不要将该记录表述为“所有系统没有任何 bug”。

## 推送前全访问复查

- 再次通过 55 项 Python、11 项 JavaScript 测试、依赖一致性与前端安全审计。
- 浏览器逐页访问 47 个内容页面（另有 404 页面），检查 112 个资源地址；首页、搜索结果跳转、V5 往返、深色主题和窄屏菜单可用。
- 修正首页遗漏的旧源码链接，统一指向公开的 `V5.3.4` 标签；移除 Git 中的 VitePress 缓存，并加入忽略规则。
- 原生客户端再次验证中文与空格文件名多选，结果路径正确。
- 部署后线上 47 个内容页面逐页访问通过，70 个实际加载的资源地址未见 HTTP 错误或未捕获脚本异常。客户端更新文档入口后，29 个常规交互检查点通过，macOS 安装包重新构建及校验通过。
- 两仓库待提交文件未发现私钥或常见访问令牌特征，未包含构建产物、虚拟环境或浏览器测试数据。

## 远端检查与修复

首次运行六组 Python/Node 矩阵、macOS 与 Linux 安装包均通过。Windows 测试发现英文系统使用 cp1252 输出中文诊断时抛出 `UnicodeEncodeError`。本机用同编码重现后，已将 CLI 重定向输出设为 UTF-8，并让构建脚本默认使用 UTF-8；新增回归测试覆盖帮助与创建项目，55 项 Python 测试通过。修复后的三端工作流结果以 GitHub Actions 对应提交为准。

安全复查中 GitHub 识别出 Pillow 11.3.0 的已知漏洞，已升级到修复版本 12.3.0，并同步将最低 Python 版本提高到 3.10。新增 Python 依赖审计作为远端质量闸门；旧 Python 3.9 的通过记录不再代表当前支持范围。

Windows 后续打包发现 `subprocess` 无法直接定位 `pnpm.cmd`。已让构建、初始化和更新统一使用解析后的 pnpm 路径，新增实际执行临时前端启动器并传播失败退出码的回归测试。最终本地 Python 55 项、JavaScript 11 项通过。Python 审计未发现已知第三方依赖漏洞；该轮本地 `ppx-py` 由源码检查和回归测试验证，发布后的注册表安装另行复测。

最终本地环境使用 OpenSSL 3.0.16，Pillow 12.3.0、setuptools 84.0.0 与 pip 26.2.1。GitHub Dependabot 未关闭告警为 0，远端 Python 与前端审计均通过。安全依赖升级后的 macOS 应用已实际启动，显示 Python 已连接，返回“你好，上线复查 ✅！”，最新版在线文档和 V5 归档入口均能打开系统浏览器。最终 wheel/sdist 通过元数据检查，wheel/tgz 在新的隔离环境中完成新建项目、初始化、GUI 构建和真实业务 API 调用。

V5 归档的一处 pywebview 官方外链已随上游迁移；通过 VitePress 渲染规则修正地址，历史 Markdown 原文保持不变。修复后检查的 24 个外部目标均可访问。

三个 GitHub Artifact 已实际下载，ZIP 的 SHA-256 与 GitHub 提供的 digest 一致；包内安装文件也分别与 `SHA256SUMS` 一致。名称为 `Setup_Windows_X64`、`Setup_macOS_ARM64`、`Setup_Linux_X64`，本地留存在忽略目录 `output/playwright/ci-artifacts/`。这些是该轮 CI 的安装包；公开 Release 使用包含最终架构修复的新构建，见下方记录。

## 注册表发布前复查

新增安装包架构标签回归测试：保留旧文件名时，更新器同时读取 GitHub asset label，拒绝下载架构不匹配或标记矛盾的安装包。本地 56 项 Python、11 项 JavaScript 测试以及生产构建通过；本节新增修复的远端结果另行记录，不沿用此前 CI 的结果。


## 公开包发布验收

2026-09-05，最终代码提交 `66ed38d` 的 [build 工作流](https://github.com/pangao1990/PPX/actions/runs/33963464721) 全部成功：Python 3.10 / 3.11 / 3.13 × Node 22 / 24 六组质量检查、依赖审计，以及 Windows x64、macOS arm64、Linux x64 安装包构建与校验均通过。该提交包含 56 项 Python 和 11 项 JavaScript 测试。

- [ppx-py 6.0.0](https://pypi.org/project/ppx-py/6.0.0/) 已通过 [PyPI 可信发布工作流](https://github.com/pangao1990/PPX/actions/runs/33963776890) 上传 wheel/sdist。独立环境从官方 PyPI 安装后，56 项 Python 测试和 `pip check` 通过；24 个 Python 源文件与最终提交逐字节一致。
- [ppx-js 6.0.0](https://www.npmjs.com/package/ppx-js/v/6.0.0) 已发布。公开 tgz 的完整性摘要与本地验收包一致；安装后的 JavaScript 文件与最终提交一致，11 项 JavaScript 测试通过。
- 使用公开包新建 Vue 项目、初始化依赖、17 项 doctor 检查和 GUI 生产构建全部通过，不再依赖本地 wheel/tgz 引用。
- [V6.0.0 Release](https://github.com/pangao1990/PPX/releases/tag/V6.0.0) 已公开。保留旧安装包文件名，asset label 分别声明 Windows x64、macOS arm64、Linux x64；附带 `ppx-update.json` 与 `SHA256SUMS`。五个 GitHub asset 的摘要均与本地文件一致。

注册表里的 `6.0.0` 不再覆盖；后续文档同步仍保持项目版本为 `6.0.0`。Windows/Linux 真机交互、覆盖安装与卸载，以及正式代码签名和 macOS 公证仍属于未覆盖范围，不能表述为所有平台绝对没有 bug。

旧的 PyPI 项目 `ppx-core`、`ppx-build` 和 npm 包 `ppx-bridge` 已删除；公开版本查询均返回 404。PyPI 项目管理列表已确认仅保留新的 `ppx-py` 与原有无关项目。

发布后已从 GitHub 公网重新下载全部五个 Release 文件，大小与 SHA-256 均与 GitHub digest 和本地最终文件一致。公开清单包含两个 `6.0.0` 包；应用更新检查返回“6.0.0 已是最新版本”。使用公开资产验证 Windows x64、macOS arm64、Linux x64 的安装包选择正确，Intel Mac 与 Linux arm64 不会误选其他架构。

文档提交 `8232e00` 已通过 [GitHub Pages Deploy](https://github.com/pangao1990/docs-ppx/actions/runs/33965082085)。本地构建检查 48 页、1605 个内链通过，线上浏览器逐页访问 47 个内容页面未发现 HTTP 或脚本错误。客户端发布后再通过 29 个常规交互和 9 个异常恢复检查点。一次外链断言因测试脚本写死旧开发端口而失败，修正脚本为检查当前页面地址后完整复跑通过；该改动未进入生产包。

包介绍页复查：npm 实际加载了原版 LOGO、微信支付、支付宝与公众号四张图片。PyPI 已正确渲染介绍内容和图片引用，但本次网络访问其 `pypi-camo.freetls.fastly.net` 图片代理连接超时，导致图片及维护者头像未显示；原始图片地址返回 HTTP 200。这是当前检查网络下的外部图片加载限制，不影响 wheel/sdist 安装，不能写成 PyPI 图片展示已全部通过。
