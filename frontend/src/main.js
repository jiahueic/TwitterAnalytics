import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import VueApexCharts from "vue3-apexcharts"
//import x5GMaps from 'x5-gmaps'

/** 
createApp(App).use(router, x5GMaps, {
  load: {
    key: "AIzaSyCPzFJ3N0UVDHBHbRaNsx8YxO7EPPp1C_k",
    libraries: "places"
  }
})
.mount('#app')
*/
const app = createApp(App);
app.use(router);
app.use(VueApexCharts);
app.mount('#app');

/** 
createApp(App).use(router, VueGoogleMaps, {
  load: {
    key: "AIzaSyCPzFJ3N0UVDHBHbRaNsx8YxO7EPPp1C_k",
    libraries: "places"
  }
})
.mount('#app')
*/

