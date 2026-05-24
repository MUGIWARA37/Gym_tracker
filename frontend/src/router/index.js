import { createRouter, createWebHistory } from 'vue-router'
import { authGuard } from './guards'

import DashboardView from '../views/dashboard/DashboardView.vue'
import LoginView from '../views/auth/LoginView.vue'
import RegisterView from '../views/auth/RegisterView.vue'
import ForgotPasswordView from '../views/auth/ForgotPasswordView.vue'
import ExercisesView from '../views/exercises/ExerciseListView.vue'
import WorkoutsView from '../views/workouts/PlanListView.vue'
import SessionsView from '../views/sessions/SessionHistoryView.vue'
import ProgressView from '../views/progress/ProgressView.vue'
import NutritionView from '../views/nutrition/NutritionView.vue'
import NotificationsView from '../views/notifications/NotificationsView.vue'
import ForbiddenView from '../views/errors/ForbiddenView.vue'
import NotFoundView from '../views/errors/NotFoundView.vue'

const routes = [
  {
    path: '/login',
    component: LoginView,
    meta: { layout: 'auth', guestOnly: true },
  },
  {
    path: '/register',
    component: RegisterView,
    meta: { layout: 'auth', guestOnly: true },
  },
  {
    path: '/forgot-password',
    component: ForgotPasswordView,
    meta: { layout: 'auth', guestOnly: true },
  },
  {
    path: '/',
    redirect: '/dashboard',
  },
  {
    path: '/dashboard',
    component: DashboardView,
    meta: { layout: 'app', requiresAuth: true },
  },
  {
    path: '/exercises',
    component: ExercisesView,
    meta: { layout: 'app', requiresAuth: true },
  },
  {
    path: '/workouts',
    component: WorkoutsView,
    meta: { layout: 'app', requiresAuth: true },
  },
  {
    path: '/sessions',
    component: SessionsView,
    meta: { layout: 'app', requiresAuth: true },
  },
  {
    path: '/progress',
    component: ProgressView,
    meta: { layout: 'app', requiresAuth: true },
  },
  {
    path: '/nutrition',
    component: NutritionView,
    meta: { layout: 'app', requiresAuth: true },
  },
  {
    path: '/notifications',
    component: NotificationsView,
    meta: { layout: 'app', requiresAuth: true },
  },
  {
    path: '/403',
    component: ForbiddenView,
    meta: { layout: 'blank' },
  },
  {
    path: '/:pathMatch(.*)*',
    component: NotFoundView,
    meta: { layout: 'blank' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(authGuard)

export default router
