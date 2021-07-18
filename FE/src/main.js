// The Vue build-script version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import i18n from './lang/i18n'
import store from './store/store'
import rate from 'vue-rate'
import AOS from 'aos'
import Notifications from 'vue-notification'

import 'typeface-montserrat'
import 'vue-rate/dist/vue-rate.css'

import {
  BootstrapVue,
  BIconList,
  BIconStarFill,
  BIconInfoCircle,
  BIconCheckCircleFill,
  BIconXCircleFill
} from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import '../static/boxicons/css/boxicons.min.css'
import '../static/icofont/icofont.min.css'

import './assets/css/main.css'
import 'aos/dist/aos.css'

import VueApexCharts from 'vue-apexcharts'

Vue.config.productionTip = false
Vue.config.devtools = false

Vue.use(rate)
Vue.use(BootstrapVue)
Vue.use(VueApexCharts)
Vue.use(Notifications)

Vue.component('BIconCheckCircleFill', BIconCheckCircleFill)
Vue.component('BIconInfoCircle', BIconInfoCircle)
Vue.component('BIconList', BIconList)
Vue.component('BIconXCircleFill', BIconXCircleFill)
Vue.component('BIconStarFill', BIconStarFill)
Vue.component('apexchart', VueApexCharts)
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: {
    App
  },
  created() {
    AOS.init({
      duration: 1000,
      once: true
    });
  },
  template: '<App/>',
  i18n,
  store
})
