<script setup>
import { onMounted, onUnmounted, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import 'element-plus/es/components/message/style/css'
import { ppx } from 'ppx-js'

const props = defineProps({ disabled: Boolean })
const state = reactive({
  checking: false,
  canDownload: false,
  downloading: false,
  cancelling: false,
  visible: false,
  code: 1,
  message: '',
  body: '',
  url: '',
  path: '',
  percentage: 0,
  size: ''
})
let unsubscribe = () => {}
onMounted(() => {
  unsubscribe = ppx.on('applicationUpdate.progress', (progress) => {
    if (!state.downloading) return
    state.percentage = Math.max(0, Math.min(100, Number(progress.percentage) || 0))
    state.size = progress.sizeShow || ''
  })
})
onUnmounted(() => unsubscribe())

async function check() {
  if (props.disabled || state.checking) return
  if (state.downloading || state.path) {
    state.visible = true
    return
  }
  state.checking = true
  try {
    const result = await ppx.call('applicationUpdate.check')
    state.code = result.code
    state.canDownload = result.code === 0
    state.message = result.msg
    state.body = result.body || ''
    state.url = result.htmlUrl || ''
    state.visible = true
  } catch (error) {
    ElMessage.error(error.message)
  } finally {
    state.checking = false
  }
}
async function download() {
  if (state.downloading) return
  state.downloading = true
  state.percentage = 0
  state.size = '正在连接更新服务器…'
  state.path = ''
  try {
    // Downloads can exceed the normal 30-second RPC budget; cancellation is a separate RPC.
    const result = await ppx.call('applicationUpdate.download', null, { timeoutMs: 0 })
    state.message = result.msg
    state.code = result.code
    if (result.code === 1) state.canDownload = false
    if (result.code === 0) {
      state.path = result.downloadPath
      state.percentage = 100
      state.message = '下载完成，SHA-256 校验已通过。点击“打开安装包”继续安装。'
    }
  } catch (error) {
    state.code = -2
    state.message = error.message
  } finally {
    state.downloading = false
    state.cancelling = false
    state.visible = true
  }
}
async function cancel() {
  if (state.cancelling) return
  state.cancelling = true
  try {
    await ppx.call('applicationUpdate.cancel')
    state.size = '正在取消，等待当前网络读取结束…'
  } catch (error) {
    state.cancelling = false
    ElMessage.error(error.message)
  }
}
async function open(path) {
  try {
    const opened = await ppx.call('system.openPath', { path })
    if (!opened) ElMessage.error('系统未能打开该位置，请手动打开。')
  } catch (error) {
    ElMessage.error(error.message)
  }
}
function closeResult() {
  state.visible = false
}
</script>

<template>
  <button class="text-button update-button" :disabled="disabled || state.checking" @click="check">
    {{
      state.checking
        ? '检查中…'
        : state.downloading
          ? '查看下载进度'
          : state.path
            ? '更新已下载'
            : '检查应用更新 ↗'
    }}
  </button>
  <el-dialog
    v-model="state.visible"
    :title="state.downloading ? '下载应用更新' : '应用更新'"
    align-center
    :close-on-click-modal="false"
    :show-close="!state.downloading"
    :close-on-press-escape="!state.downloading"
  >
    <template v-if="state.downloading">
      <p class="update-description" role="status">{{ state.size }}</p>
      <el-progress :percentage="state.percentage" :stroke-width="10" />
      <p class="update-caption">下载完成后会校验安装包，随后由你选择是否打开安装。</p>
    </template>
    <template v-else>
      <p class="update-description" role="status">{{ state.message }}</p>
      <pre v-if="state.body && !state.path" class="release-notes">{{ state.body }}</pre>
      <code v-if="state.path" class="download-path">{{ state.path }}</code>
    </template>
    <template #footer>
      <div class="update-actions">
        <button v-if="state.url && !state.downloading" class="text-button" @click="open(state.url)">
          查看发布页面 ↗
        </button>
        <template v-if="state.downloading"
          ><button class="button" :disabled="state.cancelling" @click="cancel">
            {{ state.cancelling ? '取消中…' : '取消下载' }}</button
          ><button class="button primary" @click="state.visible = false">后台下载</button></template
        >
        <template v-else
          ><button class="button" @click="closeResult">
            {{ state.canDownload && !state.path ? '稍后再说' : '关闭' }}</button
          ><button v-if="state.path" class="button primary" @click="open(state.path)">
            打开安装包</button
          ><button v-else-if="state.canDownload" class="button primary" @click="download">
            {{ state.code === 0 ? '下载更新' : '重新下载' }}
          </button></template
        >
      </div>
    </template>
  </el-dialog>
</template>

<style scoped>
.update-button {
  white-space: nowrap;
}
.update-description {
  font-size: 14px;
  color: #515e6a;
  margin-bottom: 18px;
}
.update-caption {
  font-size: 12px;
  margin-top: 16px;
}
.release-notes {
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  max-height: 35vh;
  overflow: auto;
  background: #f5f7f8;
  padding: 15px;
  border-radius: 8px;
  font: 12px/1.9 inherit;
  color: #6f7982;
}
.download-path {
  display: block;
  overflow-wrap: anywhere;
  font-size: 11px;
  padding: 12px;
  background: #f5f7f8;
  border-radius: 6px;
}
.update-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  flex-wrap: wrap;
}
.update-actions > .text-button {
  margin-right: auto;
}
</style>
