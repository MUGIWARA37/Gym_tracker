import api from './api'

export const SessionsService = {
  list(params) { return api.get('/sessions/', { params }) },
  create(payload) { return api.post('/sessions/', payload) },
  start(payload) { return api.post('/sessions/', payload) },
  update(id, payload) { return api.patch(`/sessions/${id}/`, payload) },
  addLog(id, payload) { return api.post(`/sessions/${id}/logs/`, payload) },
  updateLog(sessionId, logId, payload) { return api.patch(`/sessions/${sessionId}/logs/${logId}/`, payload) },
}
