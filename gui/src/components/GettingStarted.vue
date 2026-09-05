<script setup>
defineEmits(['open-external'])
</script>

<template>
  <div class="page-heading">
    <span class="eyebrow">START BUILDING</span>
    <h1>开发文档</h1>
    <p>随客户端提供的入门说明，无需联网即可阅读。先跑通示例，再逐步替换成自己的业务。</p>
  </div>
  <div class="getting-started">
    <section class="card">
      <h2>1. 准备源码与开发环境</h2>
      <p>安装包用于体验应用；开发需要包含 <code>ppx.toml</code>、<code>api/</code>、<code>gui/</code> 和 <code>ppx/</code> 的本版本源码。</p>
      <p>准备 Python 3.10 或更高版本、Node.js 22.13 或更高版本，以及 pnpm 11。在项目根目录先创建虚拟环境。</p>
      <p>macOS / Linux：</p>
      <pre>python3 -m venv .venv</pre>
      <p>Windows：</p>
      <pre>py -m venv .venv</pre>
      <p>然后在同一目录执行以下命令，项目脚本会自动使用这个虚拟环境：</p>
      <pre>pnpm init
pnpm start</pre>
      <p><code>pnpm init</code> 安装依赖并检查环境，<code>pnpm start</code> 启动前端和桌面窗口。在桌面窗口中测试 Python 调用；普通浏览器只提供界面预览。</p>
    </section>
    <section class="card">
      <h2>2. 编写 Python 业务</h2>
      <p>在 <code>api/api.py</code> 中使用装饰器公开方法。返回可序列化为 JSON 的数据，例如字符串、数组或字典。</p>
      <pre>from ppx_py import api_method

@api_method("user.greet")
def greet(name: str):
    return {"message": f"你好，{name}！"}</pre>
      <p>生产代码应校验参数；示例源码已对空名字和长度做校验。耗时任务放在 Python 侧处理。</p>
    </section>
    <section class="card">
      <h2>3. 在 JavaScript 中调用</h2>
      <p>在 <code>gui/src/App.vue</code> 编写页面，通过 <code>ppx-js</code> 调用 Python 方法。参数名与 Python 方法的参数名一致。</p>
      <pre>import { ppx } from 'ppx-js'

try {
  const result = await ppx.call('user.greet', { name: '开发者' })
  console.log(result.message)
} catch (error) {
  console.error(error.code, error.message)
}</pre>
      <p>调用默认在 30 秒后超时。文件选择和更新下载需要等待用户操作或网络传输，可使用第三个参数 <code>{ timeoutMs: 0 }</code>；同时在页面提供等待状态。</p>
    </section>
    <section class="card">
      <h2>4. 体验内置能力</h2>
      <ul>
        <li><strong>工作台：</strong>输入名字调用 Python，或读取本机用户名。</li>
        <li><strong>文件与目录：</strong>选择一个或多个文件、选择目录。取消会保留之前的选择，示例不读取或上传文件内容。</li>
        <li><strong>本地存储：</strong>编辑便签、保存，再重启客户端验证。便签保存在当前用户的应用数据目录中。</li>
        <li><strong>检查应用更新：</strong>连接项目发布源；有可用更新时下载并校验安装包，由你决定是否打开安装。</li>
      </ul>
    </section>
    <section class="card">
      <h2>5. 测试与打包</h2>
      <p>在 <code>ppx.toml</code> 设置应用名称、版本、窗口和更新源。完成业务后，先检查，再构建：</p>
      <pre>pnpm check
pnpm build
pnpm verify:installer</pre>
      <p>产物位于 <code>build/</code>。macOS、Windows、Linux 安装包需要分别在对应系统构建和验收；Windows 需要 Inno Setup 6，Linux 需要 Debian 打包工具。</p>
    </section>
    <section class="card">
      <h2>项目资源与版本说明</h2>
      <p>在线介绍站默认介绍最新版，提供完整教程与 API 参考。旧项目可从 V5 归档入口查阅原文档；V5 与当前架构不兼容，请勿直接混用两代接口。</p>
      <div class="resource-links">
        <a class="button" href="https://github.com/pangao1990/PPX" target="_blank" rel="noopener noreferrer" @click="$emit('open-external', $event)">项目仓库 ↗</a>
        <a class="button" href="https://github.com/pangao1990/PPX/releases" target="_blank" rel="noopener noreferrer" @click="$emit('open-external', $event)">版本发布 ↗</a>
        <a class="button" href="https://github.com/pangao1990/PPX/issues" target="_blank" rel="noopener noreferrer" @click="$emit('open-external', $event)">问题反馈 ↗</a>
        <a class="button" href="https://blog.pangao.vip/docs-ppx/" target="_blank" rel="noopener noreferrer" @click="$emit('open-external', $event)">在线开发文档 ↗</a>
        <a class="button" href="https://blog.pangao.vip/docs-ppx/v5/" target="_blank" rel="noopener noreferrer" @click="$emit('open-external', $event)">V5 归档文档 ↗</a>
      </div>
    </section>
  </div>
</template>

<style scoped>
.getting-started { display: grid; gap: 18px; }
.card p { margin-top: 12px; }
pre { overflow-x: auto; background: #f5f7f8; border-radius: 8px; padding: 16px; font-size: 12px; line-height: 1.9; }
li { margin-top: 10px; color: #5f6c77; font-size: 13px; }
ul { padding-left: 20px; }
.resource-links { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 18px; }
</style>
