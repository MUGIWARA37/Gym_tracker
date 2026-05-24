import api from './api'

export const ExercisesService = {
  list(params) {
    return api.get('/exercises/', { params })
  },
  create(payload) {
    return api.post('/exercises/', payload)
  },
  update(id, payload) {
    return api.patch(`/exercises/${id}/`, payload)
  },
  remove(id) {
    return api.delete(`/exercises/${id}/`)
  },
}
