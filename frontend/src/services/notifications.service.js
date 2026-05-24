import api from './api'

export const NotificationsService = {
  list() {
    return api.get('/notifications/')
  },
  markRead(id) {
    return api.patch(`/notifications/${id}/read/`)
  },
  markAllRead() {
    return api.post('/notifications/mark-all-read/')
  },
}
