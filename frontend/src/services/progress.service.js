import api from './api'

export const ProgressService = {
  list(params) {
    return api.get('/progress/', { params })
  },
  create(payload) {
    return api.post('/progress/', payload)
  },
  remove(id) {
    return api.delete(`/progress/${id}/`)
  },
}
