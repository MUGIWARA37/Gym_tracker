import api from './api'

export const AuthService = {
  register(payload) {
    return api.post('/auth/register/', payload)
  },
  login(payload) {
    return api.post('/auth/login/', payload)
  },
  refresh(payload) {
    return api.post('/auth/token/refresh/', payload)
  },
  logout(payload) {
    return api.post('/auth/logout/', payload)
  },
  profile() {
    return api.get('/auth/profile/')
  },
  changePassword(payload) {
    return api.post('/auth/password/change/', payload)
  },
}
