import Vue from 'vue'
import VueRouter from 'vue-router'
import Settings from '@/views/Settings.vue'
import Dashboard from '@/views/Dashboard'
import Camera from "@/views/Camera";
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'dashboard',
    component: Dashboard
  },
  {
    path: '/settings',
    name: 'settings',
    component: Settings
  },
  {
    path: '/camera',
    name: 'camera',
    component: Camera
  }
]

const router = new VueRouter({
  routes
})

export default router
