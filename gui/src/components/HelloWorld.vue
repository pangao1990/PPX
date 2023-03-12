<script setup>
import { ref, onMounted } from 'vue'

defineProps({
  msg: String
})

let creator = ref('pangao')

onMounted(() => {
  py2Js() // 挂载函数，供给python调用
})

const getOwner = () => {
  window.pywebview.api.getOwner().then((res) => {
    creator.value = res
  })
}

const py2Js = () => {
  // 挂载函数，供给python调用
  window['py2js'] = (resJson) => {
    const res = JSON.parse(resJson)
    console.log(res)
  }
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

    <p>本应用的业务层采用<b>本地Python</b>或调用<b>远程API</b>等方式</p>
    <p>视图层可使用任意一款你喜欢的前端框架，比如 <b>Vue</b>、<b>React</b>、<b>Angular</b>、<b>HTML</b> 等</p>

    <p>用户名：{{ creator }}</p>
    <button v-if="creator == 'pangao'" type="button" @click="getOwner">获取本机用户名</button>
  </div>
</template>

<style scoped>
a {
  color: #42b983;
}
</style>
