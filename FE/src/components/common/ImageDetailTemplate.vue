<template>
  <b-row>
    <b-col cols="12" class="content-container">
      <b-row>
        <b-col lg="12">
          <div class="img-container">
            <slot name="image" />
          </div>
        </b-col>
      </b-row>
      <b-row>
        <b-col lg="12 mt-3">
          <div class="detail-container">
            <slot name="detail-container" />
          </div>
        </b-col>
      </b-row>
    </b-col>
  </b-row>
</template>

<script>
export default {};
</script>

<style scoped>
.content-container {
  position: absolute;
  left: 0%;
  top: 30%;
}
.img-container {
  text-align: center;
}
.img-container img {
  width: 240px;
  border-radius: 50%;
}
.detail-container {
  text-align: center;
}
.detail-container h3 {
  font-weight: 700;
  margin-top: 1rem;
  margin-bottom: 1rem;
}
</style>
