<template>
  <b-row class="p-2 mb-2" v-if="exData.file">
    <b-col cols="12">
      <div class="sound-title"><slot name="sound-title" /></div>
    </b-col>
    <b-col cols="12">
      <b-row>
        <b-col cols="12" md="6" lg="6">
          <div>
            <audio controls class="mb-2">
              <source :src="exData.file" />
            </audio>
          </div>
        </b-col>
        <b-col cols="12" md="6" lg="6">
          <b-progress class="mt-2" :max="100" height="1.5rem" show-value>
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
    </b-col>
    <b-col cols="12">
      <template v-if="isProcess">
        <div class="float-right loading-spinner-text mb-3">
          <template v-if="!isBusy"> {{ $t('processing') }} </template>
          <template v-if="isBusy">
            {{ $t('server_busy') }}
          </template>
        </div>
        <div
          v-if="!isBusy"
          class="spinner-border text-primary loading-spinner"
          role="status"
        />
      </template>
      <template v-if="!isProcess">
        <span class="sound-explain-text" @click="explainMoreAction">{{
          $t('explain_more')
        }}</span>
      </template>
    </b-col>
  </b-row>
</template>

<script>
export default {
  props: {
    exData: {
      type: Object,
      default: undefined,
    },
  },
  data() {
    return {
      isProcess: false,
      isBusy: false,
    };
  },
  methods: {
    explainMoreAction() {
      this.$emit('explain', true);
    },
    process() {
      this.isBusy = false;
      this.isProcess = true;
    },
    busy() {
      this.isBusy = true;
      this.isProcess = true;
    },
    done() {
      this.isBusy = false;
      this.isProcess = false;
    },
  },
};
</script>

<style scoped>
audio {
  width: 100%;
}
.loading-spinner {
  float: right;
  position: relative;
  top: 10px;
  margin-right: 1rem;
}
.loading-spinner-text {
  position: relative;
  top: 1rem;
}
.sound-title {
  display: inline-block;
  position: relative;
  font-size: 1.2rem !important;
  top: -1.25rem;
  font-size: 1.5rem;
  width: 185px;
}

.sound-result-text {
  position: relative;
  top: 0.4rem;
  float: right;
}
.sound-explain-text {
  margin-top: 1rem;
  float: right;
  color: #4285f4;
  text-decoration: underline #4285f4;
}

.sound-explain-text:hover:hover {
  cursor: pointer;
}

.sound-info-icon {
  position: relative;
  top: -35px;
  font-size: 20px;
}
</style>
