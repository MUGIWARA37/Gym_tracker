import { defineStore } from 'pinia'

export const useUIStore = defineStore('ui', {
  state: () => ({
    darkMode:
      localStorage.getItem('darkMode') === 'true' ||
      window.matchMedia('(prefers-color-scheme: dark)').matches,
    sidebarOpen: window.matchMedia('(min-width: 1024px)').matches,
  }),
  actions: {
    toggleDark() {
      this.darkMode = !this.darkMode
      localStorage.setItem('darkMode', this.darkMode)
      document.documentElement.classList.toggle('dark', this.darkMode)
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
