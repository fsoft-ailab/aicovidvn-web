<template>
  <div>
    <!-- Header -->
    <header id="header">
      <b-container fluid>
        <a class="nav-toggle" @click="setLanguage('en')" v-if="!isEng">ENG</a>
        <a class="nav-toggle" @click="setLanguage('vi')" v-if="isEng">VI</a>
      </b-container>
    </header>
    <!-- Hero section -->
    <section id="hero" class="d-flex align-items-center">
      <div
        class="container d-flex flex-column align-items-center justify-content-center"
        data-aos="fade-up"
      >
        <h1 id="media_nondisplay">{{ $t('apptitle') }}</h1>
        <h2 data-language="appsubtitle1" id="media_nondisplay2">
          {{ $t('appsubtitle1') }}
        </h2>
        <h2>{{ $t('appsubtitle2') }}</h2>
        <b-button class="btn-get-started" @click="redirectToPredictPage">{{
          $t('btnstart')
        }}</b-button>
      </div>
    </section>
    <!-- End hero section -->
    <main id="main">
      <!-- About section -->
      <section id="about" class="about">
        <b-container>
          <b-row class="no-gutters">
            <b-col
              xl="5"
              class="content align-items-stretch"
              data-aos="fade-right"
            >
              <div class="content">
                <h3>{{ $t('abth3') }}</h3>
                <p>{{ $t('abtp') }}</p>
              </div>
            </b-col>
            <b-col xl="7" class="align-items-stretch" data-aos="fade-left">
              <div class="content justify-content-center">
                <b-row>
                  <b-col
                    md="4"
                    class="icon-box"
                    data-aos="fade-up"
                    data-aos-delay="100"
                  >
                    <i class="bx bxs-book"></i>
                    <h4>{{ $t('reason1h4') }}</h4>
                    <p>{{ $t('reason1p') }}</p>
                  </b-col>
                  <b-col
                    md="4"
                    class="icon-box"
                    data-aos="fade-up"
                    data-aos-delay="200"
                  >
                    <i class="bx bx-phone"></i>
                    <h4>{{ $t('reason2h4') }}</h4>
                    <p>{{ $t('reason2p') }}</p>
                  </b-col>
                  <b-col
                    md="4"
                    class="icon-box"
                    data-aos="fade-up"
                    data-aos-delay="300"
                  >
                    <i class="bx bxs-heart"></i>
                    <h4>{{ $t('reason3h4') }}</h4>
                    <p>{{ $t('reason3p') }}</p>
                  </b-col>
                </b-row>
              </div>
            </b-col>
          </b-row>
        </b-container>
      </section>
      <!-- End about section -->
      <!-- Team section -->
      <section id="team" class="team">
        <b-container data-aos="fade-up">
          <div class="section-title">
            <h2>{{ $t('teamh2') }}</h2>
          </div>
          <!-- <div class="owl-carousel team-carousel"> -->
          <carousel
            :nav="false"
            :autoplay="true"
            :dots="true"
            :responsive="{
              0: {
                items: 1,
              },
              600: {
                items: 2,
              },
              1000: {
                items: 3,
              },
            }"
          >
            <div class="member">
              <img
                src="static/imgs/team/Phong.jpeg"
                class="member-img"
                alt="member-logo"
              />
              <h3>Nguyễn Xuân Phong</h3>
              <h4>Chief AI Officer</h4>
            </div>

            <div class="member">
              <img
                src="static/imgs/team/Linh.jpeg"
                class="member-img"
                alt="member-logo"
              />
              <h3>Trần Thùy Linh</h3>
              <h4>Program Lead - AI Lab</h4>
            </div>

            <div class="member">
              <img
                src="static/imgs/team/Viet.jpg"
                class="member-img"
                alt="member-logo"
              />
              <h3>Trần Quốc Việt</h3>
              <h4>Developer</h4>
            </div>

            <div class="member">
              <img
                src="static/imgs/team/Giang.jpg"
                class="member-img"
                alt="member-logo"
              />
              <h3>Nguyễn Hoàng Giang</h3>
              <h4>Developer</h4>
            </div>

            <div class="member">
              <img
                src="static/imgs/team/Ly.png"
                class="member-img"
                alt="member-logo"
              />
              <h3>Lê Thị Vân Ly</h3>
              <h4>Developer</h4>
            </div>
            <!-- </div> -->
          </carousel>
        </b-container>
      </section>
      <!-- End Team section -->
      <!-- Footer -->
      <footer id="footer">
        <b-container class="py-4">
          <div class="mr-md-auto text-center text-md-left">
            <img src="static/imgs/logofpt.png" alt="logo" />
          </div>
        </b-container>
      </footer>
      <!-- End footer -->
      <button
        class="back-to-top"
        aria-label="Back to top"
        :style="{ opacity: isShowScrollBtn ? 1 : 0 }"
        @click="scrollToTop"
      >
        <i class="icofont-simple-up" />
      </button>
    </main>
  </div>
</template>

<script>
import carousel from 'vue-owl-carousel';
import { mapActions } from 'vuex';
import Header from './Header.vue';
import UrlConstant from '../common/constant/url-constant';
export default {
  components: { Header, carousel },
  mounted() {
    window.addEventListener('scroll', this.scrollListener);
  },
  data() {
    return {
      isEng: false,
      isShowScrollBtn: false,
    };
  },
  methods: {
    ...mapActions({ setLang: 'setLang' }),
    setLanguage(langText) {
      this.isEng = langText === 'en';
      this.setLang({ context: this, lang: langText });
    },
    scrollListener(event) {
      if (document.scrollingElement.scrollTop > 100) {
        this.isShowScrollBtn = true;
      } else {
        this.isShowScrollBtn = false;
      }
    },
    redirectToPredictPage() {
      const url = new URL(window.location.href);
      const data = url.searchParams.get('data');
      let redirectUrl = `${UrlConstant.BASE_URL}/predicts`;
      if (data !== undefined && data) {
        redirectUrl = `${redirectUrl}?data=${data}`;
      }
      window.location.href = redirectUrl;
    },
    scrollToTop() {
      // cancel if already on top
      if (document.scrollingElement.scrollTop === 0) return false;

      const cosParameter = document.scrollingElement.scrollTop / 2;
      let scrollCount = 0;
      let oldTimestamp = null;

      function step(newTimestamp) {
        const duration = 1000;
        if (oldTimestamp !== null) {
          // if duration is 0 scrollCount will be Infinity
          scrollCount += (Math.PI * (newTimestamp - oldTimestamp)) / duration;
          if (scrollCount >= Math.PI) {
            return (document.scrollingElement.scrollTop = 0);
          }
          document.scrollingElement.scrollTop =
            cosParameter + cosParameter * Math.cos(scrollCount);
        }
        oldTimestamp = newTimestamp;
        window.requestAnimationFrame(step);
      }
      window.requestAnimationFrame(step);
    },
  },
};
</script>

<style scoped>
a:hover {
  color: #6c7afa;
  text-decoration: none;
}
.nav-toggle {
  position: absolute;
  right: 15px;
  top: 15px;
  font-family: 'Krub', sans-serif;
  font-weight: 500;
  font-size: 16px;
  z-index: 9998;
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
}
#hero {
  width: 100%;
  height: 100vh;
  background: white;
  text-align: center;
  background: url('../../static/imgs/hero-image-background-ngang.png');
  background-size: cover;
  position: relative;
}
#hero::before {
  content: '';
  background: rgba(0, 0, 0, 0.55);
  position: absolute;
  bottom: 0;
  top: 0;
  left: 0;
  right: 0;
}
#hero .container {
  z-index: 1;
  padding-top: 70px;
}
#hero h1 {
  margin: 0;
  font-size: 48px;
  font-weight: 700;
  line-height: 56px;
  color: #ffffff;
  width: 60%;
}
#hero h2 {
  color: #ffffff;
  margin: 15px 0 0 0;
  font-size: 24px;
}
#hero .btn-get-started {
  font-family: 'Krub', sans-serif;
  font-weight: 500;
  font-size: 16px;
  letter-spacing: 1px;
  display: block;
  padding: 8px 32px 10px 32px;
  margin-top: 25px;
  border-radius: 5px;
  transition: 0.5s;
  color: #fff;
  background: #0372c5;
}
#about {
  background: #233147;
  background-size: cover;
  padding: 60px 0;
  position: relative;
  color: #fff;
}
.about .content {
  padding: 30px 30px 30px 0;
}
.about .content h3 {
  font-weight: 700;
  font-size: 34px;
  color: #fff;
  margin-bottom: 30px;
}
.about .icon-boxes,
.about .icon-box {
  margin-top: 30px;
}
.about .icon-boxes i,
.about .icon-box i {
  font-size: 40px;
  color: #b6bdfc;
  margin-bottom: 10px;
}
.about .icon-box h4 {
  font-size: 20px;
  font-weight: 700;
  margin: 0 0 10px 0;
}
.about .icon-box p {
  font-size: 15px;
}
.team {
  background: #f6f8fb;
  padding: 60px 0;
}
.section-title h2 {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 20px;
  padding-bottom: 20px;
  position: relative;
  color: #2d405f;
}
.section-title h2:after {
  content: '';
  position: absolute;
  display: block;
  width: 50px;
  height: 3px;
  background: #aabbd7;
  bottom: 0;
  left: calc(50% - 25px);
}
.team .member {
  text-align: center;
  margin: 30px 15px;
  background: #fff;
  position: relative;
  overflow: hidden;
  padding: 30px 30px 30px 30px;
  box-shadow: 0px 2px 12px rgb(0 0 0 / 8%);
  box-sizing: content-box;
}
.team .member .member-img {
  width: 200px;
  border-radius: 50%;
  border: 4px solid #fff;
  margin: 0 auto;
}
.team .member h3 {
  font-size: 18px;
  font-weight: bold;
  margin: 10px 0 5px 0;
  color: #111;
}
.team .member h4 {
  font-size: 14px;
  color: #999;
  margin: 0;
}
#footer {
  color: #444444;
  font-size: 14px;
  background: #f1f3ff;
  box-shadow: 0px 2px 15px rgb(0 0 0 / 10%);
}
.back-to-top {
  position: fixed;
  display: block;
  right: 15px;
  bottom: 15px;
  z-index: 99999;
  padding: 0;
  border: none;
  border-radius: 50%;
  transition: all 0.4s;
}
.back-to-top:focus {
  border: none;
  outline: none;
}
.back-to-top i {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  width: 40px;
  height: 40px;
  border-radius: 5px;
  background: #3b4ef8;
  color: #fff;
  transition: all 0.4s;
}
@media (max-width: 1200px) {
  .about .content {
    padding-right: 0;
  }
}

@media (max-width: 992px) {
  #hero {
    width: 100%;
    height: 100vh;
    background: white;
    text-align: center;
    background: url('../../static/imgs/hero-image-background-doc.png');
    background-size: cover;
    position: relative;
  }
}
@media (max-width: 768px) {
  .about {
    text-align: center;
  }
}
</style>
