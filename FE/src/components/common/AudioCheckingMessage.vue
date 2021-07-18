<template>
  <div>
    <div v-if="valid">
      <div class="error-image" v-if="!valid.duration || !valid.noise || valid.count < 3">
        <img
          :src="`data:image/jpeg;base64, ${valid.img}`"
          alt="Checking audio image"
        />
      </div>
      <div class="text-danger" v-if="!valid.duration">
        - {{ $t('error_duration') }}
      </div>
      <div class="text-danger" v-if="valid.count < 3 && valid.duration">
        - {{ $t('error_count') }}{{ valid.count }}
      </div>
      <div
        class="text-danger"
        v-if="!valid.noise && valid.duration && valid.count >= 3"
      >
        - {{ $t('error_noise') }}
      </div>
    </div>
    <div v-if="loading">
      <b-spinner variant="primary" label="Spinning" />
      {{ $t('audio_checking') }}
    </div>
  </div>
</template>

<script>
export default {
  props: {
    valid: {
      type: Object,
      default: undefined,
    },
    loading: {
      type: Boolean,
      default: false,
    },
  },
};
</script>

<style scoped>
.error-image img {
  width: 65%;
}
@media screen and (max-width: 992px) {
  .error-image img {
    width: 70%;
  }
}
@media screen and (max-width: 600px) {
  .error-image img {
    width: 85%;
  }
}
</style>
