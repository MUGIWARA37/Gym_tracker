import api from './api'

export const ProgressService = {
  list: () => api.get('/progress/'),
  create: (data) => api.post('/progress/', data),
  delete: (id) => api.delete(`/progress/${id}/`),
}
