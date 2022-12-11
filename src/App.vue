<script setup>
import HelloWorld from './components/HelloWorld.vue'
</script>


<template>
  <div>
    <div class="logo-box">
      <img alt="Vue logo" src="./assets/vue.png" />
      <span />
      <img alt="pywebview logo" src="./assets/pywebview.png" />
      <span />
      <img alt="pyinstaller logo" src="./assets/pyinstaller.png" />
    </div>
    <HelloWorld msg="Hello Vue3 + pywebview + PyInstaller" />
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.logo-box {
  display: flex;
  width: 100%;
  justify-content: center;
}

.logo-box span {
  width: 74px;
}
</style>
