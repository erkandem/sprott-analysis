import { createApp } from 'vue'
import HighchartsVue from 'highcharts-vue'

import './style.css'
import App from './App.vue'

const app = createApp(App)
app.use(HighchartsVue)
app.mount('#app')
