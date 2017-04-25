import Vue from 'vue'
import VueRouter from 'vue-router'

import App from './components/App.vue'
import Buy from './components/Buy.vue'
import Login from './components/Login.vue'
import Sell from './components/Sell.vue'
import Signup from './components/Signup.vue'

Vue.use(VueRouter)

let router = new VueRouter({
  routes: [
    { path: '/buy', component: Buy },
    { path: '/sell', component: Sell},
    { path: '/login', component: Login},
    { path: '/signup', component: Signup}
  ]
})

new Vue({
  el: '#app',
  router,
  render: h => h(App)
})