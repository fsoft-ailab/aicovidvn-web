<template>
  <div>
    <b-row>
      <b-col cols="6" md="6" lg="5">
        <span class="float-right">{{ name }} :</span>
      </b-col>
      <b-col cols="6" md="6" lg="7" class="rate-img-container">
        <!-- <div class="circle-status" :class="computedColor"></div> -->
        <rate :length="5" :value="value.toFixed(2) * 5" :disabled="true" />
        <span v-if="name.toLowerCase() == 'rate'" :class="computedColor">{{
          value.toFixed(2)
        }}</span>
      </b-col>
    </b-row>
  </div>
</template>

<script>
export default {
  props: {
    name: {
      type: String,
      default: '',
    },
    value: {
      type: Number,
      default: 0,
    },
    min: {
      type: Number,
      default: 0,
    },
    max: {
      type: Number,
      default: 0,
    },
    rateLength: {
      type: Number,
      default: 10,
    },
  },
  computed: {
    computedColor() {
      const evg = (this.min + this.max) / 2;
      if (this.value >= this.min + evg * 0.2 && this.value <= evg) {
        return 'text-warning';
      }
      if (this.value > evg) {
        return 'text-success';
      }
      return 'text-danger';
    },
  },
};
</script>
<style>
.Rate {
  float: left;
}
.Rate .Rate__view {
  display: none;
}
.Rate button {
  padding: 0;
}
</style>
<style scoped>
.rate-img-container span {
  float: left;
}
.rate-img-container .circle-status {
  float: left;
  width: 15px;
  height: 15px;
  border-radius: 50%;
  position: relative;
  top: 2px;
}
</style>
