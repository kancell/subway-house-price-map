import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
//import { Button } from 'ant-design-vue';
//import { Layout } from 'ant-design-vue';
//import { Breadcrumb } from 'ant-design-vue';
//import { Menu } from 'ant-design-vue';
//import { Input } from 'ant-design-vue';
//import { Select  } from 'ant-design-vue';

Vue.config.productionTip = false

//Vue.use(Button)
//Vue.use(Layout)
//Vue.use(Breadcrumb)
//Vue.use(Menu)
//Vue.use(Input)
//Vue.use(Select)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
