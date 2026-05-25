<script setup>
import { useUIStore } from '../stores/ui'

const ui = useUIStore()
</script>

<template>
  <div
    class="min-h-screen overflow-x-hidden bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-100"
  >
    <div class="flex min-h-screen">
      <div
        v-if="ui.sidebarOpen"
        class="fixed inset-0 z-30 bg-black/50 lg:hidden"
        @click="ui.closeSidebar()"
      ></div>
      <aside
        :class="[
          'fixed inset-y-0 left-0 z-40 w-64 transform border-r border-slate-200 bg-white px-6 py-8 shadow-lg transition-transform duration-300 dark:border-slate-800 dark:bg-slate-900 lg:static lg:shadow-none lg:transition-none',
          ui.sidebarOpen ? 'translate-x-0' : '-translate-x-full',
          'lg:translate-x-0 lg:flex lg:flex-col',
        ]"
      >
        <div class="text-xl font-semibold">Smart Gym</div>
        <nav class="mt-8 flex flex-col gap-3 text-sm text-slate-600 dark:text-slate-300">
          <RouterLink
            to="/dashboard"
            class="hover:text-slate-900 dark:hover:text-white"
            @click="ui.closeSidebar()"
          >
            Dashboard
          </RouterLink>
          <RouterLink
            to="/exercises"
            class="hover:text-slate-900 dark:hover:text-white"
            @click="ui.closeSidebar()"
          >
            Exercises
          </RouterLink>
          <RouterLink
            to="/workouts"
            class="hover:text-slate-900 dark:hover:text-white"
            @click="ui.closeSidebar()"
          >
            Workout Plans
          </RouterLink>
          <RouterLink
            to="/sessions"
            class="hover:text-slate-900 dark:hover:text-white"
            @click="ui.closeSidebar()"
          >
            Sessions
          </RouterLink>
          <RouterLink
            to="/progress"
            class="hover:text-slate-900 dark:hover:text-white"
            @click="ui.closeSidebar()"
          >
            Progress
          </RouterLink>
          <RouterLink
            to="/nutrition"
            class="hover:text-slate-900 dark:hover:text-white"
            @click="ui.closeSidebar()"
          >
            Nutrition
          </RouterLink>
          <RouterLink
            to="/notifications"
            class="hover:text-slate-900 dark:hover:text-white"
            @click="ui.closeSidebar()"
          >
            Notifications
          </RouterLink>
        </nav>
      </aside>

      <div class="flex min-h-screen flex-1 flex-col">
        <header
          class="flex items-center justify-between gap-3 border-b border-slate-200 bg-white px-4 py-4 dark:border-slate-800 dark:bg-slate-900 sm:px-6"
        >
          <div class="flex items-center gap-3">
            <button
              class="rounded-md border border-slate-200 px-3 py-1.5 text-sm dark:border-slate-700 lg:hidden"
              type="button"
              @click="ui.toggleSidebar()"
            >
              Menu
            </button>
            <div class="text-sm text-slate-600 dark:text-slate-300">
              Welcome back
            </div>
          </div>
          <button
            class="rounded-md border border-slate-200 px-3 py-1.5 text-sm dark:border-slate-700"
            @click="ui.toggleDark()"
          >
            Toggle theme
          </button>
        </header>

        <main class="flex-1 px-4 py-6 sm:px-6 sm:py-8">
          <slot />
        </main>
      </div>
    </div>
  </div>
</template>
