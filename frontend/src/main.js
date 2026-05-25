import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './style.css'
import { useUIStore } from './stores/ui'

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
app.use(router)

// apply initial theme classes from stored preferences
const ui = useUIStore()
// ensure OLED implies dark mode
if (ui.oled && !ui.darkMode) {
  ui.darkMode = true
  localStorage.setItem('darkMode', 'true')
}
document.documentElement.classList.toggle('dark', ui.darkMode)
document.documentElement.classList.toggle('oled', ui.oled)

app.mount('#app')
