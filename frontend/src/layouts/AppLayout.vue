<script setup>
import { computed } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { useUIStore } from '../stores/ui'
import { useAuthStore } from '../stores/auth'
import Icon from '../components/ui/Icon.vue'

const ui = useUIStore()
const auth = useAuthStore()
const route = useRoute()

const navLinks = [
  { to: '/dashboard', label: 'Dashboard', icon: 'dashboard' },
  { to: '/exercises', label: 'Exercises', icon: 'plus-circle' },
  { to: '/workouts', label: 'Workout Plans', icon: 'rectangle-stack' },
  { to: '/sessions', label: 'Sessions', icon: 'play-circle' },
  { to: '/nutrition', label: 'Nutrition', icon: 'beaker' },
  { to: '/notifications', label: 'Notifications', icon: 'bell' },
  { to: '/profile', label: 'Profile', icon: 'user-circle' },
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

      <div class="sidebar-main">
        <div class="sidebar-section-label">Main</div>
        <nav class="sidebar-nav">
          <RouterLink
            v-for="link in navLinks"
            :key="link.to"
            :to="link.to"
            class="nav-link"
            @click="ui.closeSidebar()"
          >
            <Icon :name="link.icon" class="nav-icon" :size="18" />
            {{ link.label }}
          </RouterLink>
        </nav>
      </div>

      <div class="sidebar-footer">
        <button
          class="nav-link btn-ghost w-full"
          style="border:none;cursor:pointer;width:100%;background:transparent"
          @click="auth.logout()"
        >
          <Icon name="arrow-left-on-rectangle" class="nav-icon" :size="18" />
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
            <Icon name="bell" :size="16" />
          </RouterLink>
          <RouterLink to="/profile" class="btn btn-secondary btn-sm" style="gap:6px">
            <Icon name="user-circle" :size="16" />
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
