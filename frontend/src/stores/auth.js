import { defineStore } from 'pinia'
import api from '../services/api'
import router from '../router'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    accessToken: null,
    refreshTokenValue: localStorage.getItem('refreshToken'),
  }),
  getters: {
    isAuthenticated: (state) => !!state.accessToken,
  },
  actions: {
    async login(credentials) {
      const { data } = await api.post('/auth/login/', credentials)
      this.accessToken = data.access
      this.refreshTokenValue = data.refresh
      this.user = data.user
      localStorage.setItem('refreshToken', data.refresh)
    },
    async register(payload) {
      await api.post('/auth/register/', payload)
      router.push('/login')
    },
    async refreshToken() {
      if (!this.refreshTokenValue) {
        throw new Error('Missing refresh token')
      }
      const { data } = await api.post('/auth/token/refresh/', {
        refresh: this.refreshTokenValue,
      })
      this.accessToken = data.access
    },
    async logout() {
      if (this.refreshTokenValue) {
        await api.post('/auth/logout/', { refresh: this.refreshTokenValue })
      }
      this.$reset()
      localStorage.removeItem('refreshToken')
      router.push('/login')
    },
    async fetchProfile() {
      const { data } = await api.get('/auth/profile/')
      this.user = data
    },
  },
})
