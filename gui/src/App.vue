<script setup>
import { computed, onMounted, onUnmounted, ref, watch, nextTick } from 'vue'
import { ppx } from 'ppx-js'
import BtnUpdate from './components/BtnUpdate.vue'
import GettingStarted from './components/GettingStarted.vue'

const connected = ref(false)
const connecting = ref(true)
const appInfo = ref({ name: 'PPX', version: '6.0.0' })
const current = ref('overview')
const name = ref('开发者')
const greeting = ref('等待你的第一次 Python 调用。')
const owner = ref('点击获取当前设备的用户名')
const files = ref([])
const directory = ref('')
const note = ref('')
const savedNote = ref('')
const noteLoaded = ref(false)
const busy = ref(new Set())
const notice = ref(null)
const history = ref([])
const tabs = [
  { id: 'overview', label: '工作台', icon: '◈' },
  { id: 'files', label: '文件与目录', icon: '▤' },
  { id: 'storage', label: '本地存储', icon: '▣' }
]
const title = computed(() =>
  current.value === 'docs' ? '开发文档' : tabs.find((tab) => tab.id === current.value).label
)
watch(current, async () => {
  await nextTick()
  window.scrollTo({ top: 0 })
  document.getElementById('main-content')?.focus({ preventScroll: true })
})
watch(notice, async (value) => {
  if (!value) return
  await nextTick()
  document.querySelector('.notice')?.scrollIntoView({ block: 'nearest' })
})
const dirty = computed(() => note.value !== savedNote.value)
let disposed = false
let connectionAttempt = 0

async function run(key, method, params = null, options = {}) {
  if (busy.value.has(key)) return
  busy.value.add(key)
  notice.value = null
  const started = performance.now()
  try {
    const value = await ppx.call(method, params, options)
    history.value.unshift({ method, ok: true, duration: Math.round(performance.now() - started) })
    return { value }
  } catch (error) {
    notice.value = {
      error: true,
      text: error.message,
      detail: [error.code, error.requestId].filter(Boolean).join(' · ')
    }
    history.value.unshift({ method, ok: false, duration: Math.round(performance.now() - started) })
  } finally {
    history.value = history.value.slice(0, 5)
    busy.value.delete(key)
  }
}

async function connect() {
  const attempt = ++connectionAttempt
  connecting.value = true
  try {
    await ppx.ready({ timeoutMs: 1800 })
    if (disposed || attempt !== connectionAttempt) return
    connected.value = true
    const result = await run('info', 'system.getAppInfo')
    if (result) appInfo.value = result.value
    await loadNote()
  } catch {
    if (attempt === connectionAttempt) connected.value = false
  } finally {
    if (!disposed && attempt === connectionAttempt) connecting.value = false
  }
}
async function greet() {
  if (!name.value.trim()) return
  const result = await run('greet', 'user.greet', { name: name.value.trim() })
  if (result) greeting.value = result.value.message
}
async function getOwner() {
  const result = await run('owner', 'system.getOwner')
  if (result) owner.value = result.value
}
async function selectFiles() {
  const result = await run('files', 'system.openFileDialog', { multiple: true }, { timeoutMs: 0 })
  if (result && result.value.length) files.value = result.value
  else if (result) notice.value = { text: '已取消选择，保留当前文件列表。' }
}
async function selectDirectory() {
  const result = await run('directory', 'system.selectDirectory', null, { timeoutMs: 0 })
  if (result && result.value) directory.value = result.value
  else if (result) notice.value = { text: '已取消选择，保留当前目录。' }
}
async function loadNote() {
  const result = await run('note', 'storage.get', { key: 'demo.note', default: '' })
  if (result) {
    note.value = typeof result.value === 'string' ? result.value : ''
    savedNote.value = note.value
    noteLoaded.value = true
  }
}
async function saveNote() {
  const snapshot = note.value
  const result = await run('note', 'storage.set', { key: 'demo.note', value: snapshot })
  if (result) {
    savedNote.value = snapshot
    notice.value = { text: '已保存到本机，重启应用后仍可读取。' }
  }
}
async function deleteNote() {
  const result = await run('note', 'storage.delete', { key: 'demo.note' })
  if (result) {
    note.value = savedNote.value = ''
    notice.value = { text: '示例便签已清空。' }
  }
}
async function openExternal(event) {
  if (!connected.value) return
  event.preventDefault()
  const path = event.currentTarget.href
  const result = await run(`external:${path}`, 'system.openPath', { path })
  if (result && !result.value)
    notice.value = { error: true, text: '无法打开浏览器，请复制下方链接手动访问。', detail: path }
}
onMounted(() => {
  window.addEventListener('pywebviewready', connect)
  connect()
})
onUnmounted(() => {
  disposed = true
  window.removeEventListener('pywebviewready', connect)
})
</script>

<template>
  <div class="app-shell">
    <aside class="sidebar">
      <a class="brand" href="#" @click.prevent="current = 'overview'" aria-label="PPX 工作台"
        ><img class="brand-logo" src="/logo.png" alt="" width="48" height="48" />
        <span>PPX</span></a
      >
      <div class="sidebar-caption">开发，从这里开始</div>
      <nav aria-label="主要导航">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          :class="['nav-item', { active: current === tab.id }]"
          :aria-current="current === tab.id ? 'page' : undefined"
          @click="current = tab.id"
        >
          <span aria-hidden="true">{{ tab.icon }}</span
          >{{ tab.label }}
        </button>
      </nav>
      <div class="sidebar-bottom">
        <button :aria-current="current === 'docs' ? 'page' : undefined" @click="current = 'docs'">
          开发文档 <span>→</span>
        </button>
        <a
          href="https://github.com/pangao1990/PPX"
          target="_blank"
          rel="noopener noreferrer"
          @click="openExternal"
          >GitHub <span>↗</span></a
        >
        <div class="sidebar-footnote">Python 的能力<br />Web 的表达力</div>
      </div>
    </aside>
    <div class="main-shell">
      <header class="topbar">
        <div class="breadcrumb">
          示例应用 <span>/</span> <strong>{{ title }}</strong>
        </div>
        <span :class="['connection', { online: connected }]" role="status"
          ><i />{{ connected ? 'Python 已连接' : connecting ? '正在连接…' : '浏览器预览' }}</span
        >
      </header>
      <main id="main-content" tabindex="-1">
        <div v-if="!connected && !connecting" class="preview-banner" role="status">
          <div>
            <strong>当前为浏览器预览</strong
            ><span>桌面功能需要在 <code>ppx dev</code> 打开的窗口中使用。</span>
          </div>
          <button class="button small" @click="connect">重新连接</button>
        </div>
        <div
          v-if="notice"
          :class="['notice', { error: notice.error }]"
          :role="notice.error ? 'alert' : 'status'"
        >
          <div>
            {{ notice.text }}<small v-if="notice.detail">{{ notice.detail }}</small>
          </div>
          <button aria-label="关闭提示" @click="notice = null">×</button>
        </div>

        <template v-if="current === 'overview'">
          <section class="hero">
            <div>
              <div class="eyebrow">BUILD SOMETHING THAT MATTERS</div>
              <h1>让好想法，<br />成为桌面应用。</h1>
              <p>
                用 Python 处理业务，用 JavaScript 构建体验。<br />从一次简单调用开始，探索 PPX
                的桌面能力。
              </p>
              <button class="button primary" @click="current = 'docs'">
                开始构建 <span>→</span>
              </button>
            </div>
            <div class="hero-code" aria-label="Python 与 JavaScript 调用示例">
              <div class="code-title"><span /><span /><span /><b>一次调用，无限可能</b></div>
              <div class="code-body">
                <small>PYTHON / api.py</small>
                <pre><em>@api_method</em>("user.greet")
def greet(name):
  return {"message": f"你好，{name}！"}</pre>
                <div class="code-connector">↓ <span>PPX BRIDGE</span> ↓</div>
                <small>JAVASCRIPT / App.vue</small>
                <pre>
const result = await <em>ppx.call</em>(
  'user.greet', { name: '开发者' }
)</pre
                >
                <div class="code-result"><i /> 你好，开发者！</div>
              </div>
            </div>
          </section>
          <div class="section-heading">
            <div>
              <h2>试一试，桌面原生能力</h2>
              <p>这些操作会调用你本机的 Python。</p>
            </div>
            <span class="meta">{{ appInfo.name }}</span>
          </div>
          <div class="cards">
            <section class="card">
              <span class="card-icon">↔</span>
              <h3>向 Python 打个招呼</h3>
              <p>输入一个名字，获得后端返回的问候。</p>
              <form @submit.prevent="greet">
                <label for="name">你的名字</label>
                <div class="input-row">
                  <input
                    id="name"
                    v-model="name"
                    maxlength="80"
                    placeholder="例如：开发者"
                    :disabled="!connected"
                  /><button
                    class="button primary"
                    :disabled="!connected || !name.trim() || busy.has('greet')"
                  >
                    {{ busy.has('greet') ? '调用中…' : '调用 Python' }}
                  </button>
                </div>
              </form>
              <div class="result" role="status">{{ greeting }}</div>
              <code class="api-label">user.greet</code>
            </section>
            <section class="card">
              <span class="card-icon blue">⌘</span>
              <h3>认识你的设备</h3>
              <p>通过系统接口读取当前登录用户名。</p>
              <div class="owner-result" role="status">{{ owner }}</div>
              <button class="button" :disabled="!connected || busy.has('owner')" @click="getOwner">
                {{ busy.has('owner') ? '读取中…' : '获取本机用户名' }}</button
              ><code class="api-label">system.getOwner</code>
            </section>
          </div>
          <div class="quick-links">
            <button @click="current = 'files'">
              <span class="card-icon blue">▤</span>
              <div><strong>文件与目录</strong><span>打开系统选择器，连接本地资源</span></div>
              <b>→</b></button
            ><button @click="current = 'storage'">
              <span class="card-icon amber">▣</span>
              <div><strong>本地存储</strong><span>保存一段便签，重启后继续</span></div>
              <b>→</b>
            </button>
          </div>
        </template>

        <template v-else-if="current === 'files'">
          <div class="page-heading">
            <span class="eyebrow">LOCAL RESOURCES</span>
            <h1>文件与目录</h1>
            <p>使用系统原生对话框选择本地资源。此示例只读取路径，不上传或修改文件。</p>
          </div>
          <section class="card">
            <div class="section-heading">
              <div>
                <h2>选择文件</h2>
                <p>支持多选，取消选择会保留当前列表。</p>
              </div>
              <button
                class="button primary"
                :disabled="!connected || busy.has('files')"
                @click="selectFiles"
              >
                {{ busy.has('files') ? '等待选择…' : '选择文件' }}
              </button>
            </div>
            <div v-if="!files.length" class="empty-state">
              <span>▤</span><strong>还没有选择文件</strong>
              <p>点击“选择文件”，从本机添加一个或多个文件。</p>
            </div>
            <ul v-else class="file-list">
              <li v-for="file in files" :key="file.path">
                <span class="card-icon blue">▤</span>
                <div>
                  <strong>{{ file.filename }}</strong
                  ><code>{{ file.path }}</code>
                </div>
              </li>
            </ul>
          </section>
          <section class="card directory-card">
            <h2>选择工作目录</h2>
            <p>在自己的业务中，可将这个路径传给 Python 进行批量处理。</p>
            <button
              class="button"
              :disabled="!connected || busy.has('directory')"
              @click="selectDirectory"
            >
              选择目录
            </button>
            <div class="result" role="status">{{ directory || '尚未选择目录' }}</div>
          </section>
        </template>

        <template v-else-if="current === 'storage'">
          <div class="page-heading">
            <span class="eyebrow">KEEP IT LOCAL</span>
            <h1>本地存储</h1>
            <p>将少量偏好与状态保存在应用数据目录中，独立于安装目录。</p>
          </div>
          <section class="card">
            <div class="section-heading">
              <div>
                <h2>我的便签</h2>
                <p>在这里记下一个想法，点击保存后重启应用验证。</p>
              </div>
              <span class="save-state">{{
                !noteLoaded ? '尚未读取' : dirty ? '有未保存的修改' : '与本地一致'
              }}</span>
            </div>
            <label for="note">便签内容</label
            ><textarea
              id="note"
              v-model="note"
              rows="8"
              maxlength="10000"
              placeholder="下一个想做的桌面应用是…"
              :disabled="!connected || !noteLoaded || busy.has('note')"
            />
            <div class="editor-footer">
              <span>{{ note.length }} / 10000</span>
              <div>
                <button
                  v-if="!noteLoaded"
                  class="button"
                  :disabled="!connected || busy.has('note')"
                  @click="loadNote"
                >
                  重新读取</button
                ><button
                  class="button"
                  :disabled="!connected || !noteLoaded || busy.has('note') || (!note && !savedNote)"
                  @click="deleteNote"
                >
                  清空便签</button
                ><button
                  class="button primary"
                  :disabled="!connected || !noteLoaded || busy.has('note') || !dirty"
                  @click="saveNote"
                >
                  {{ busy.has('note') ? '处理中…' : '保存到本机' }}
                </button>
              </div>
            </div>
          </section>
          <div class="storage-explainer">
            <strong>这段数据保存在哪里？</strong>
            <p>
              Python 通过 <code>storage.set</code> 将内容写入当前用户的应用数据目录；下次启动通过
              <code>storage.get</code> 恢复。应用更新不会覆盖它。这个示例仅使用
              <code>demo.note</code> 一个键。
            </p>
          </div>
        </template>

        <GettingStarted v-else @open-external="openExternal" />

        <section class="activity">
          <div class="section-heading">
            <h2>最近调用</h2>
            <button v-if="history.length" class="text-button" @click="history = []">
              清空记录
            </button>
          </div>
          <p v-if="!history.length" class="muted">完成一次操作后，可在这里查看调用结果。</p>
          <ul v-else>
            <li v-for="(item, index) in history" :key="index">
              <span :class="['activity-dot', { failed: !item.ok }]" /><code>{{ item.method }}</code
              ><span>{{ item.ok ? '成功' : '失败' }}</span
              ><small>{{ item.duration }} ms</small>
            </li>
          </ul>
        </section>
        <footer class="app-footer">
          <span>PPX · 开源的跨平台桌面框架</span><BtnUpdate :disabled="!connected" />
        </footer>
      </main>
    </div>
  </div>
</template>
