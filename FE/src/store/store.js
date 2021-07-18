import Vue from 'vue'
import Vuex from 'vuex'
import Constant from '../common/constant/common-constant'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    lang: Constant.DEFAULT_LANGUAGE
  },
  getters: {
    getLang: (state) => state.lang,
    getActiveIndex: (state) => state.activeIndex,
    getChangeNav: (state) => state.changeNav
  },
  mutations: {
    SET_LANG: (state, payload) => {
      payload.context.$i18n._vm.locale = payload.lang
      state.lang = payload.lang
    }
  },
  actions: {
    setLang({ commit }, payload) {
      commit('SET_LANG', payload)
    }
  }
})

export default store
