import Vue from 'vue'
import VueRouter from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import ParkingLots from "../views/ParkingLots";
import ParkingLot from "../views/ParkingLot";
import NewLot from "../views/NewLot";

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/addLot',
    name: 'Add Lot',
    component: NewLot
  },
  {
    path: '/lots',
    name: 'Parking Lots',
    component: ParkingLots
  },
  {
    path: '/lot/:id',
    name: 'Parking Lot Detail',
    component: ParkingLot
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
