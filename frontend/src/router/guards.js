import { useAuthStore } from '../stores/auth'

export function authGuard(to, from, next) {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return next('/login')
  }
  if (to.meta.requiresRole && auth.user?.role !== to.meta.requiresRole) {
    return next('/403')
  }
  if (to.meta.guestOnly && auth.isAuthenticated) {
    return next('/dashboard')
  }
  return next()
}
