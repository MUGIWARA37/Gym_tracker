<script setup>
import { computed } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { useUIStore } from '../stores/ui'
import { useAuthStore } from '../stores/auth'

const ui = useUIStore()
const auth = useAuthStore()
const route = useRoute()

const navLinks = [
  { to: '/dashboard', label: 'Dashboard', icon: '▦' },
  { to: '/exercises', label: 'Exercises', icon: '⊕' },
  { to: '/workouts', label: 'Workout Plans', icon: '≡' },
  { to: '/sessions', label: 'Sessions', icon: '▷' },
  { to: '/progress', label: 'Progress', icon: '↗' },
  { to: '/nutrition', label: 'Nutrition', icon: '◎' },
  { to: '/notifications', label: 'Notifications', icon: '◯' },
]

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 12) return 'Good morning'
  if (h < 17) return 'Good afternoon'
  return 'Good evening'
})

const username = computed(() => auth.user?.username || auth.user?.first_name || 'Athlete')
</script>

<template>
  <div class="app-shell">
    <!-- Sidebar Overlay -->
    <div
      v-if="ui.sidebarOpen && !isDesktop"
      class="sidebar-overlay"
      @click="ui.closeSidebar()"
    />

    <!-- Sidebar -->
    <aside :class="['sidebar', { open: ui.sidebarOpen }]">
      <div class="sidebar-logo">
        <div class="logo-mark">G</div>
        <span>SmartGym</span>
      </div>

      <div class="sidebar-section-label">Main</div>
      <nav style="display:flex;flex-direction:column;gap:2px;margin-bottom:24px">
        <RouterLink
          v-for="link in navLinks"
          :key="link.to"
          :to="link.to"
          class="nav-link"
          @click="ui.closeSidebar()"
        >
          <span style="font-size:15px;width:18px;text-align:center;flex-shrink:0">{{ link.icon }}</span>
          {{ link.label }}
        </RouterLink>
      </nav>

      <div class="sidebar-footer">
        <button
          class="nav-link btn-ghost w-full"
          style="border:none;cursor:pointer;width:100%;background:transparent"
          @click="auth.logout()"
        >
          <span style="font-size:15px;width:18px;text-align:center">⏻</span>
          Sign out
        </button>
      </div>
    </aside>

    <!-- Main content -->
    <div class="main-wrap">
      <!-- Topbar -->
      <header class="topbar">
        <div class="topbar-left">
          <button class="burger-btn" @click="ui.toggleSidebar()">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/>
            </svg>
          </button>
          <span class="topbar-greeting">
            {{ greeting }}, <strong>{{ username }}</strong>
          </span>
        </div>
        <div class="topbar-right">
          <RouterLink to="/notifications" class="btn btn-ghost btn-sm" style="position:relative">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
              <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
            </svg>
          </RouterLink>
          <RouterLink to="/profile" class="btn btn-secondary btn-sm" style="gap:6px">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
            Profile
          </RouterLink>
        </div>
      </header>

      <!-- Page slot -->
      <main style="flex:1;display:flex;flex-direction:column">
        <slot />
      </main>
    </div>
  </div>
</template>

<script>
export default { computed: { isDesktop() { return window.innerWidth >= 1024 } } }
</script>
