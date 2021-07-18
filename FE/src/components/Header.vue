<template>
  <header class="site-header">
    <div class="container">
      <div class="site-header-inner">
        <a class="brand header-brand" href="/">
          <img src="static/imgs/logofpt.png" alt="logo" />
        </a>
      </div>
    </div>
    <div class="container-fluid">
      <a class="nav-toggle" @click="setLanguage('en')" v-if="!isEng">ENG</a>
      <a class="nav-toggle" @click="setLanguage('vi')" v-if="isEng">VI</a>
    </div>
  </header>
</template>

<script>
import { mapActions } from 'vuex';
export default {
  data() {
    return {
      isEng: false,
    };
  },
  methods: {
    ...mapActions({ setLang: 'setLang' }),
    setLanguage(langText) {
      this.isEng = langText === 'en';
      this.setLang({ context: this, lang: langText });
    },
  },
};
</script>

<style scoped>
a:hover {
  color: #6c7afa;
  text-decoration: none;
}
.site-header {
  position: relative;
  padding: 24px 0;
}
.site-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 16%;
  width: 84%;
  height: 500px;
  background-image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTQ4MCIgaGVpZ2h0PSI2NTAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+ICAgIDxwYXRoIGQ9Ik03MzEuMjA3IDY0OS44MDJDOTM1LjQ4NCA2NDIuMTQgMTQ4MCAzMzcuMzI1IDE0ODAgMTgwLjg4OGMwLTE1Ni40MzgtMzA5Ljc0NC0zNi4wNTUtNzIwLTM2LjA1NVMwLTE3NC40ODMgMCAxMzUuMTQ0YzAgMzA5LjYyNyA1MjYuOTMgNTIyLjMyIDczMS4yMDcgNTE0LjY1OHoiIGZpbGw9IiNGNkY4RkEiIGZpbGwtcnVsZT0iZXZlbm9kZCIvPjwvc3ZnPg==);
  background-size: 1140px 500px;
  background-repeat: no-repeat;
}
.site-header-inner {
  display: inline-flex;
  height: 40%;
  width: 18%;
  z-index: 40;
  position: absolute;
}
.nav-toggle {
  position: absolute;
  right: 15px;
  top: 15px;
  font-family: 'Krub', sans-serif;
  font-weight: 500;
  font-size: 16px;
  z-index: 10;
  border: 0;
  background: rgba(34, 34, 34, 0.5);
  transition: all 0.4s;
  outline: none !important;
  line-height: 1;
  cursor: pointer;
  text-align: right;
  padding: 10px 12px;
  border-radius: 2px;
  color: #fff;
  width: 60px;
  text-align: center;
}
</style>
