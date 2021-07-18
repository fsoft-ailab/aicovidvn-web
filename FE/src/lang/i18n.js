import Vue from 'vue'
import VueI18n from 'vue-i18n'
import JpLang from './jp.json'
import EnLang from './en.json'
import ViLang from './vi.json'
import Constant from '../common/constant/common-constant'

Vue.use(VueI18n)

const messages = {
  jp: JpLang,
  en: EnLang,
  vi: ViLang
}

export default new VueI18n({
  locale: Constant.DEFAULT_LANGUAGE,
  messages,
  fallbackLocale: 'en'
})
