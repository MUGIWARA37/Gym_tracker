import api from './api'

export const WorkoutsService = {
  list(params) {
    return api.get('/workout-plans/', { params })
  },
  create(payload) {
    return api.post('/workout-plans/', payload)
  },
  update(id, payload) {
    return api.patch(`/workout-plans/${id}/`, payload)
  },
  delete(id) {
    return api.delete(`/workout-plans/${id}/`)
  },
  remove(id) {
    return api.delete(`/workout-plans/${id}/`)
  },
  duplicate(id) {
    return api.post(`/workout-plans/${id}/duplicate/`)
  },
  addExercise(id, payload) {
    return api.post(`/workout-plans/${id}/exercises/`, payload)
  },
  removeExercise(planId, exerciseId) {
    return api.delete(`/workout-plans/${planId}/exercises/${exerciseId}/`)
  },
  reorder(planId, payload) {
    return api.patch(`/workout-plans/${planId}/exercises/reorder/`, payload)
  },
}
// alias
