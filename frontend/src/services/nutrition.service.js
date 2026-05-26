import api from './api'

export const NutritionService = {
  get() { return api.get('/nutrition/') },
  create(payload) { return api.post('/nutrition/', payload) },
  update(payload) { return api.put('/nutrition/', payload) },
  patch(payload) { return api.patch('/nutrition/', payload) },
}
