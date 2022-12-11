<script setup>
import { ref } from 'vue'

defineProps({
  msg: String
})

let creator = ref('pangao')

const getOwner = () => {
  window.pywebview.api.getOwner().then((res) => {
    creator.value = res
  })
}

</script>

<template>
  <div>
    <h1>{{ msg }}</h1>

    <p>
      基于
      <a href="https://v3.cn.vuejs.org" target="_blank">Vue3</a>
      |
      <a href="https://pywebview.flowrl.com" target="_blank">pywebview</a>
      |
      <a href="https://pyinstaller.readthedocs.io" target="_blank">PyInstaller</a>
      框架，构建macOS和windows平台的客户端。
    </p>

    <p>本应用的视图层采用HTML+JS+CSS，业务层采用本地Python+调用远程API，支持HMR。</p>

    <p>用户名：{{ creator }}</p>
    <button v-if="creator == 'pangao'" type="button" @click="getOwner">获取本机用户名</button>
  </div>
</template>

<style scoped>
a {
  color: #42b983;
}
</style>
