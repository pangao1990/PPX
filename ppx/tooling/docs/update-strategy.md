# PPX 一键更新策略

## 边界

更新器只管理两个包和两个元数据文件：Python 环境中的 `ppx-py`、`gui/package.json` 中的 `ppx-js`、`ppx.toml` 的 `[framework]`、`ppx.lock`。开发者拥有并永久保护：

- `api/`
- `gui/src/`
- `ppx/assets/`
- 应用数据目录

PPX 不向现有项目复制新版模板，不做三方合并，不覆盖业务文件。

## 兼容判断

Release 的 `ppx-update.json` 必须包含 `projectFormat`、`pythonApi`、`javascriptApi`、`dataSchema`。四项与当前项目完全一致才允许自动更新。目标版本必须属于 V6、通道一致、不得降级，清单本身必须通过 GitHub 提供的 SHA-256 校验。

兼容时，更新顺序为：记录保护目录摘要与受管文件备份；安装精确版本 `ppx-py`；安装精确版本 `ppx-js`；原子写入配置和锁；再次验证保护目录摘要。失败时恢复受管文件和原依赖。

不兼容时，命令在任何安装与写操作前退出并逐项报告冲突。V6 不自动修改函数调用和数据格式；应按目标版本文档人工处理，重大结构变化则新建项目。

## 更新清单示例

```json
{
  "schemaVersion": 1,
  "releaseVersion": "6.1.0",
  "channel": "stable",
  "requires": {
    "projectFormat": 6,
    "pythonApi": "6.0",
    "javascriptApi": "6.0",
    "dataSchema": "1"
  },
  "provides": {
    "pythonApi": "6.0",
    "javascriptApi": "6.0",
    "dataSchema": "1"
  },
  "packages": {
    "ppx-py": "6.1.0",
    "ppx-js": "6.1.0"
  }
}
```

## 日常使用

```bash
ppx update --check
ppx update --dry-run
ppx update
ppx doctor
```

同一 PPX Release 也能修复两包版本漂移。每次更新后必须执行业务测试和当前平台调试构建；正式发布应用前再完成三端构建。
