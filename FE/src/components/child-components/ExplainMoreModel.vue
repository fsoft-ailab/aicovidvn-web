<template>
  <div>
    <b-modal
      ref="explain-more-modal"
      size="xl"
      centered
      hide-footer
      :title="$t('explain_more')"
    >
      <div class="d-block" v-if="exData">
        <b-row class="mb-3">
          <b-col cols="4" lg="3">
            <span class="model-label">{{ $t('status') }}: </span>
          </b-col>
          <b-col cols="8" lg="9">
            <span :class="exData.status ? 'text-success' : 'text-danger'">
              {{ exData.status ? $t('negative') : $t('positive') }}
            </span>
          </b-col>
        </b-row>
        <b-row class="mb-3">
          <b-col cols="4" lg="3">
            <span class="model-label">{{ $t('result') }}: </span>
          </b-col>
          <b-col cols="8" lg="9">
            <b-progress
              class="sound-progress-result"
              :max="100"
              height="1.5rem"
              show-value
            >
              <b-progress-bar
                :value="(exData.detect[1] * 100).toFixed(2)"
                :label="`${(exData.detect[1] * 100).toFixed(2)}%`"
                variant="danger"
              ></b-progress-bar>
              <b-progress-bar
                :value="(exData.detect[0] * 100).toFixed(2)"
                :label="`${(exData.detect[0] * 100).toFixed(2)}%`"
                variant="success"
              ></b-progress-bar>
            </b-progress>
          </b-col>
        </b-row>
        <div class="model-item-container">
          <span class="model-label">{{ $t('abnormal_feature') }}: </span>
          <img
            class="feature-img w-100"
            :src="`${exData.featureImage}`"
            alt="Feature image"
          />
        </div>
      </div>
    </b-modal>
  </div>
</template>

<script>
export default {
  props: {
    data: {
      type: Object,
      default: undefined,
    },
  },
  data() {
    return {
      exData: undefined,
    };
  },
  methods: {
    initData(data) {
      this.exData = data;
    },
    showModel() {
      this.$refs['explain-more-modal'].show();
    },
    hideModel() {
      this.$refs['explain-more-modal'].hide();
    },
  },
};
</script>

<style scoped>
.feature-img {
  max-height: 600px;
}
.model-label {
  float: left;
}
.sound-progress-result {
  float: left;
  width: 86%;
}
.model-item-container {
  margin-bottom: 1rem;
}
</style>
