import Vue from 'vue'
import Router from 'vue-router'
import Predict from '@/components/Predict'
import Result from '@/components/Result'
import Home from '@/components/Home'
import Visualize from '@/components/Visualize'

Vue.use(Router)

export default new Router({
  routes: [{
      path: '/home',
      redirect: '/'
    },
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/predicts',
      name: 'Predict',
      component: Predict
    },
    {
      path: '/results',
      name: 'Result',
      component: Result
    },
    {
      path: '/visualize',
      name: 'Visualize',
      component: Visualize
    }
  ],
  // Remove /#/ in your url
  mode: 'history'
})
