<template>
  <div>
    <image-detail-template>
      <template v-slot:image>
        <img src="static/imgs/employee-cv.jpg" />
      </template>
      <template v-slot:detail-container>
        <!-- <h3>{{ $t('need_candidate') }}</h3>
        <p>{{ $t('need_candidate_detail') }}</p> -->
      </template>
    </image-detail-template>
  </div>
</template>
<script>
import ImageDetailTemplate from './ImageDetailTemplate'
export default {
  components: {
    'image-detail-template': ImageDetailTemplate
  }
}
</script>

<style scoped></style>
