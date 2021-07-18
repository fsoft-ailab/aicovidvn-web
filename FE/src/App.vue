<template>
  <div id="app">
    <notifications group="noti" />
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
#app {
  font-family: sans-serif;
  color: #444444;
  font-weight: 400;
  overflow: hidden;
}
@media (max-width: 641px) {
  h3 {
    font-size: 20px;
  }
  h4 {
    font-size: 18px;
  }
}
</style>
