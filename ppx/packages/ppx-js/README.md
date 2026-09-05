# ppx-js

PPX 的轻量 JavaScript RPC 客户端。它只负责 Web 页面与 `ppx-py` 之间的稳定调用和事件边界，不依赖 Vue、Element Plus 或其他 UI 框架。

```bash
pnpm add ppx-js@6.0.0
```

```javascript
import { ppx } from 'ppx-js'

const owner = await ppx.call('system.getOwner')
const stop = ppx.on('changed', (data) => console.log(data))
stop()
```

RPC 默认使用 30 秒总超时，覆盖等待桥接和等待 Python 的完整过程，可用第三个参数调整：

```javascript
await ppx.call('report.create', { id: 1 }, { timeoutMs: 60_000 })
```

本包包含 TypeScript 声明，并可在 SSR/Node 环境中安全导入；实际调用只能发生在 PPX 的 pywebview 页面内。

每次调用在浏览器侧生成 requestId，并传给 Python。调用失败统一抛出 `PpxError`；超时和底层传输失败也会携带 requestId。可根据 `error.code` 处理 `BRIDGE_UNAVAILABLE`、`BRIDGE_ERROR`、`TIMEOUT`、`METHOD_NOT_FOUND`、`INVALID_PARAMS`、`INVALID_RESULT` 和业务侧返回的其他稳定错误码。

完整文档：[PPX JavaScript API](https://blog.pangao.vip/docs-ppx/v6/reference/javascript)
