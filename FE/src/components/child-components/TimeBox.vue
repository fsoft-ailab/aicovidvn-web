<template>
  <span v-if="isShow">
    {{ displayTime }}
  </span>
</template>

<script>
export default {
  data() {
    return {
      isShow: false,
      displayTime: '0:00',
      curTime: 0,
      intervalFunc: undefined,
    };
  },
  methods: {
    millisToMinutesAndSeconds(millis) {
      const minutes = Math.floor(millis / 60000);
      const seconds = ((millis % 60000) / 1000).toFixed(0);
      return minutes + ':' + (seconds < 10 ? '0' : '') + seconds;
    },
    start() {
      this.isShow = true;
      this.intervalFunc = setInterval(() => {
        this.curTime += 1000;
        this.displayTime = this.millisToMinutesAndSeconds(this.curTime);
      }, 1000);
    },
    stop() {
      this.isShow = false;
      clearInterval(this.intervalFunc);
      this.intervalFunc = undefined;
      this.curTime = 0;
      this.displayTime = '0:00';
    },
  },
};
</script>

<style scoped></style>
