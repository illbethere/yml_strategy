import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import Signal from '../components/Signal.vue'
import Order from '../components/Order.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/Signal', component: Signal },
  { path: '/Order', component: Order }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router