import { defineStore } from 'pinia'

export const useUIStore = defineStore('ui', {
  state: () => ({
    darkMode:
      localStorage.getItem('darkMode') === 'true' ||
      window.matchMedia('(prefers-color-scheme: dark)').matches,
    sidebarOpen: true,
  }),
  actions: {
    toggleDark() {
      this.darkMode = !this.darkMode
      localStorage.setItem('darkMode', this.darkMode)
      document.documentElement.classList.toggle('dark', this.darkMode)
    },
  },
})
