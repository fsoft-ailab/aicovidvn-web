<template>
  <section class="result-container">
    <!-- <b-row>
      <b-col cols="12">
        <h4 class="result-title">Result</h4>
      </b-col>
    </b-row> -->
    <b-row>
      <b-col cols="12">
        <div class="px-3">
          <template v-if="data">
            <h5>
              {{ $t('summary_result') }}:
              <span v-if="data.isGoodCondition" class="text-success">{{
                $t('negative')
              }}</span>
              <span v-if="!data.isGoodCondition" class="text-danger"
                >{{ $t('positive') }}*</span
              >
            </h5>
            <template v-if="!data.isGoodCondition">
              <p class="mb-0 mt-3">
                {{ $t('note') }}: <br />
                <i>
                  *<span class="text-danger">{{ $t('positive') }}</span
                  >: {{ $t('summary_warn') }}</i
                >
              </p>
            </template>
          </template>
        </div>
      </b-col>
    </b-row>
  </section>
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
      result: 0,
    };
  },
};
</script>

<style scoped>
.result-title {
  margin-top: 20px;
}
</style>
