<template>
  <div>
    <b-modal
      ref="thank-you-modal"
      size="md"
      centered
      hide-footer
      title="Thank you"
    >
      <b-row>
        <b-col cols="12">
          <div class="text-center">
            <div>
              <img
                class="model-image"
                src="static/imgs/thank-you.png"
                alt="thank you image"
              />
            </div>
            <h3>{{ $t('thankyou_feedback') }}</h3>
            <p>{{ $t('thankyou_helpus') }}</p>
          </div>
        </b-col>
      </b-row>
    </b-modal>
  </div>
</template>

<script>
export default {
  methods: {
    showModal() {
      this.$refs['thank-you-modal'].show();
    },
    hideModal() {
      this.$refs['thank-you-modal'].hide();
    },
  },
};
</script>

<style scoped>
.model-image {
  width: 50%;
}
</style>
