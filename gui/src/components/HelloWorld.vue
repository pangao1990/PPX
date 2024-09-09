<template>
  <div class="center-col">
    <h1>{{ msg }}</h1>

    <p>
      基于
      <a href="https://pywebview.flowrl.com" target="_blank">Pywebview</a>
      |
      <a href="https://pyinstaller.readthedocs.io" target="_blank">PyInstaller</a>
      |
      <a href="https://v3.cn.vuejs.org" target="_blank">Vue3</a>
      框架，构建macOS、Windows和Linux平台的客户端。
    </p>

    <p>本应用的业务层采用<b>本地Python</b>或调用<b>远程API</b>等方式</p>
    <p>视图层可使用任意一款你喜欢的前端框架，比如 <b>Vue</b>、<b>React</b>、<b>Angular</b>、<b>HTML</b> 等</p>

    <p>用户名：{{ creator }}</p>
    <button v-if="creator == 'pangao'" type="button" @click="getOwner">获取本机用户名</button>

    <!-- 检测更新 -->
    <BtnUpdate class="mt10" />
  </div>
</template>

<script setup>
import BtnUpdate from './BtnUpdate.vue'
import { ref } from 'vue'

defineProps({
  msg: String
})

let creator = ref('pangao')

const getOwner = () => {
  // 获取本机用户名
  window.pywebview.api.system_getOwner().then((res) => {
    creator.value = res
  })
}

</script>

<style scoped>
a {
  color: #42b983;
}
</style>
