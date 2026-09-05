# PPX 两包发布说明

V6.0.0 最终只发布 `ppx-py` 和 `ppx-js`。旧的 `ppx-core`、`ppx-build`、`ppx-bridge` 已放弃，PyPI/npm 已发布版本不可覆盖，也不应再作为 V6 依赖。

## 发布闸门

发布前必须满足：Python 3.10/3.11/3.13 单测通过；Node 测试、GUI 构建和 audit 通过；wheel/tgz 可在全新环境安装；Windows、macOS、Linux 分别产出并验证安装包；三台真实系统完成安装、启动、RPC 与升级检查；README、开发文档和变更记录一致。

以下命令用于完成发布闸门后的人工发布；本地检查与打包不会自动执行上传。

## 构建候选产物

```bash
python -m pip install --upgrade build twine
mkdir -p dist/release
python -m build --outdir dist/release ppx/packages/ppx-py
pnpm --dir ppx/packages/ppx-js pack --pack-destination ../../../dist/release
python ppx/tooling/scripts/check_release.py --dist dist/release
python -m twine check dist/release/ppx_py-*
(cd ppx/packages/ppx-js && npm publish --dry-run --access public --registry=https://registry.npmjs.org)
```

## 全新环境验收

```bash
python -m venv /tmp/ppx-v6-candidate
/tmp/ppx-v6-candidate/bin/python -m pip install dist/release/ppx_py-6.0.0-py3-none-any.whl
/tmp/ppx-v6-candidate/bin/ppx --version
/tmp/ppx-v6-candidate/bin/ppx new Smoke --directory /tmp/ppx-smoke

mkdir -p /tmp/ppx-js-candidate
npm install --prefix /tmp/ppx-js-candidate --ignore-scripts "$PWD/dist/release/ppx-js-6.0.0.tgz"
(cd /tmp/ppx-js-candidate && node --input-type=module -e "import('ppx-js').then(m => console.log(typeof m.ppx.call))")
```

## 正式发布顺序

1. 发布 `ppx-py` 到 PyPI。
2. 从 PyPI 在全新环境安装并重复 CLI、脚手架、构建测试。
3. 发布 `ppx-js` 到 npm。
4. 从 npm 安装并重复 RPC 与 GUI 构建测试。
5. 三端安装包全部就绪后创建 GitHub Release，并附带 `ppx-update.json` 与所有文件的 SHA-256。
6. 只有前两包和 Release 资产都能公开下载时，才允许把更新通道指向这个 Release。

```bash
python -m twine upload dist/release/ppx_py-6.0.0*
(cd ppx/packages/ppx-js && npm publish --access public --registry=https://registry.npmjs.org)
```

PyPI 和 npm 同一版本均不能覆盖。正式上传前必须把 V6.0.0 当作一次不可撤销发布来检查；若上传后发现问题，只能发布更高版本，不能重新上传 6.0.0。
