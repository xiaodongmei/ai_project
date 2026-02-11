import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import App from './App.vue'
import router from './router'

// 导入全局样式
import './styles/global.scss'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(ElementPlus)

// 在应用挂载前加载店铺配置
import { useShopConfigStore } from './store/shopConfig'
const shopConfigStore = useShopConfigStore()
shopConfigStore.loadConfig()

app.mount('#app')
