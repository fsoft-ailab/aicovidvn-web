<template>
  <div>
    <image-detail-template>
      <template v-slot:image>
        <img src="static/imgs/nodata.jpg" alt="No data image" />
      </template>
      <template v-slot:detail-container>
        <h3>{{ $t('no_data') }}</h3>
        <p>{{ $t('no_data_detail') }}</p>
      </template>
    </image-detail-template>
  </div>
</template>
<script>
import ImageDetailTemplate from './ImageDetailTemplate';
export default {
  components: {
    'image-detail-template': ImageDetailTemplate,
  },
};
</script>

<style scoped></style>
