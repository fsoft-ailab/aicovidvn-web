<template>
  <div>
    <nav
      id="mainNav"
      :class="{ nav__update: getChangeNav }"
      class="navbar navbar-expand-xl"
    >
      <b-container class="nav-container">
        <div class="logo__container">
          <div class="logo__img__wrap">
            <img
              class="logo__img__custom"
              src="../../static/imgs/doctor.png"
              alt="logo"
            />
            <span>SoundDR</span>
          </div>
          <div class="toggle__menu__button">
            <language-dropdown />
            <b-button v-b-toggle.navbarResponsive class="navbar-toggler">
              <span><b-icon-list /></span>
            </b-button>
          </div>
        </div>
        <b-collapse id="navbarResponsive" class="navbar-collapse">
          <ul class="responsive-hidden-menu navbar-nav ml-auto">
            <li
              :class="{ active__item: getActiveIndex === 1 }"
              class="nav-item"
            >
              <a class="nav-link" @click="setActiveIndex(1)" href="#overview">{{
                $t('overview')
              }}</a>
            </li>
            <li><language-dropdown /></li>
          </ul>
          <ul class="responsive-show-menu navbar-nav ml-auto">
            <li class="nav-item" v-b-toggle.navbarResponsive>
              <a class="nav-link" href="#overview">{{ $t('overview') }}</a>
            </li>
          </ul>
        </b-collapse>
      </b-container>
    </nav>
  </div>
</template>
<script>
import LanguageDropdown from './child-components/LanguageDropdown'
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'NavBar',
  components: {
    'language-dropdown': LanguageDropdown
  },
  computed: {
    ...mapGetters({
      getActiveIndex: 'getActiveIndex',
      getChangeNav: 'getChangeNav'
    })
  },
  methods: {
    ...mapActions({ setActiveIndex: 'setActiveIndex' })
  }
}
</script>

<style scoped>
.active__item {
  color: white !important;
  background-color: var(--highlight-color);
  border-radius: 5px;
}
.active__item a {
  color: white !important;
}
.nav__update {
  background-color: var(--main-bg-color);
  outline: 1px solid var(--bottom-outline-color);
}
#mainNav {
  padding: 21.5px 0;
}
#mainNav .nav-container {
  height: 57px;
  padding: 0;
}
.toggle__menu__button {
  display: flex;
  align-items: center;
}
.toggle__menu__button span {
  font-size: 2rem;
  color: var(--main-text-color);
}
.logo__container {
  display: flex;
  justify-content: space-between;
}
.logo__img__wrap {
  width: 100%;
  display: flex;
  align-items: center;
}
.logo__img__wrap span {
  margin-left: 1rem;
  font-weight: bold;
  font-size: 1.25rem;
  text-transform: uppercase;
}
.logo__img__custom {
  max-width: 70px;
  height: auto;
}
.responsive-show-menu {
  padding: 0 10% !important;
  background-color: white !important;
  width: 100%;
}
@media screen and (max-width: 1200px) {
  #mainNav .navbar-nav {
    margin-top: 21px;
    border-bottom: 1px solid var(--bottom-outline-color);
  }
}

@media screen and (max-width: 1024px) {
  #mainNav {
    padding: 10px 0;
  }
  #mainNav .navbar-nav {
    margin-top: 11px;
  }
}
@media screen and (max-width: 768px) {
  .toggle__menu__button span {
    font-size: 1.5rem;
  }
  #mainNav .nav-container {
    height: 45px;
  }
  .logo__container {
    height: 100%;
  }
  #mainNav {
    padding: 5px 0;
  }
  #mainNav .navbar-nav {
    margin-top: 5px;
  }
}
</style>
