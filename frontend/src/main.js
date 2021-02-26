import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from '@/plugins/vuetify';
import VueKonva from 'vue-konva'
import vueFabricWrapper from "vue-fabric-wrapper";

Vue.config.productionTip = false;

Vue.use(VueKonva);
Vue.component("FabricCanvas", vueFabricWrapper.FabricCanvas)
Vue.component("FabricCircle", vueFabricWrapper.FabricCircle)

new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app');
