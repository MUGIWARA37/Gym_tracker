import api from './api'

export const NutritionService = {
  get() {
    return api.get('/nutrition/')
  },
  upsert(payload) {
    return api.put('/nutrition/', payload)
  },
  patch(payload) {
    return api.patch('/nutrition/', payload)
  },
}
