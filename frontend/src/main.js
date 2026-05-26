import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './style.css'
import { useUIStore } from './stores/ui'
import { scrollAnimate } from './directives/scrollAnimate'

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
app.use(router)

app.directive('scroll-animate', scrollAnimate)

// apply initial theme classes from stored preferences
const ui = useUIStore()
document.documentElement.classList.toggle('dark', ui.darkMode)

app.mount('#app')
