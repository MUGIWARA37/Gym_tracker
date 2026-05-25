import { defineStore } from 'pinia'

export const useUIStore = defineStore('ui', {
  state: () => ({
    darkMode:
      localStorage.getItem('darkMode') === 'true' ||
      window.matchMedia('(prefers-color-scheme: dark)').matches,
    oled: localStorage.getItem('oled') === 'true',
    sidebarOpen: window.matchMedia('(min-width: 1024px)').matches,
  }),
  actions: {
    toggleDark() {
      this.darkMode = !this.darkMode
      localStorage.setItem('darkMode', this.darkMode)
      document.documentElement.classList.toggle('dark', this.darkMode)
      // if user disables dark mode, also turn off OLED
      if (!this.darkMode && this.oled) {
        this.oled = false
        localStorage.setItem('oled', 'false')
        document.documentElement.classList.remove('oled')
      }
    },
    toggleOled() {
      this.oled = !this.oled
      localStorage.setItem('oled', this.oled)
      document.documentElement.classList.toggle('oled', this.oled)
      if (this.oled) {
        // OLED is a variant of dark mode; ensure dark mode is enabled
        this.darkMode = true
        localStorage.setItem('darkMode', 'true')
        document.documentElement.classList.add('dark')
      }
    },
    toggleSidebar() {
      this.sidebarOpen = !this.sidebarOpen
    },
    closeSidebar() {
      if (window.matchMedia('(min-width: 1024px)').matches) {
        return
      }
      this.sidebarOpen = false
    },
  },
})
