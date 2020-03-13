import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify';
import VueKonva from 'vue-konva'

Vue.config.productionTip = false;

Vue.use(VueKonva);

new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app');
