<template>
  <div class="is-boxed">
    <div class="body-wrap boxed-container">
      <slot name="header" />
      <slot name="main" />
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style scoped>
.is-boxed {
  background: #f6f8fa;
}
.boxed-container {
  max-width: 1440px;
  margin: 0 auto;
  box-shadow: 0 16px 48px #e3e7eb;
}
.body-wrap {
  background: #fff;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
</style>
