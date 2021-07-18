<template>
  <div class="language__dropdown__container">
    <b-dropdown
      variant="link"
      toggle-class="text-decoration-none"
      no-caret
      right
    >
      <template v-slot:button-content>
        <img
          v-if="$i18n._vm.locale === 'jp'"
          alt="Japanese flag"
          class="lang__icon"
          src="static/imgs/jp-flag.png"
        />
        <img
          v-if="$i18n._vm.locale === 'en'"
          alt="UK flag"
          class="lang__icon"
          src="static/imgs/uk-flag.png"
        />
      </template>
      <b-dropdown-item
        class="item__dropdown__custom"
        @click="setLanguage('en')"
        v-if="!isEng"
      >
        <div>
          <span class="mr-1">{{ $t('en_jp_language') }}</span
          ><img
            alt="UK flag"
            class="lang__icon ml-1"
            src="static/imgs/uk-flag.png"
          />
        </div>
      </b-dropdown-item>
      <b-dropdown-item
        class="item__dropdown__custom"
        @click="setLanguage('jp')"
        v-if="isEng"
      >
        <div>
          <span class="mr-1">{{ $t('en_jp_language') }}</span
          ><img
            alt="Japanese flag"
            class="lang__icon ml-1"
            src="static/imgs/jp-flag.png"
          />
        </div>
      </b-dropdown-item>
    </b-dropdown>
  </div>
</template>

<script>
import { mapActions } from 'vuex';
export default {
  name: 'LanguageDropdown',
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
.lang__icon {
  width: 40px;
  height: auto;
}
.item__dropdown__custom {
  text-align: center;
}
.language__dropdown__container {
  display: flex;
  justify-content: center;
  align-items: center;
}
@media screen and (max-width: 425px) {
  .language__dropdown__container {
    flex-direction: column;
  }
}
</style>
