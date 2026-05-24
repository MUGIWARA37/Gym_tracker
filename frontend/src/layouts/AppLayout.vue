<script setup>
import { useUIStore } from '../stores/ui'

const ui = useUIStore()
</script>

<template>
  <div class="min-h-screen bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-100">
    <div class="flex">
      <aside
        class="hidden w-64 flex-col border-r border-slate-200 bg-white px-6 py-8 dark:border-slate-800 dark:bg-slate-900 lg:flex"
      >
        <div class="text-xl font-semibold">Smart Gym</div>
        <nav class="mt-8 flex flex-col gap-3 text-sm text-slate-600 dark:text-slate-300">
          <RouterLink to="/dashboard" class="hover:text-slate-900 dark:hover:text-white">
            Dashboard
          </RouterLink>
          <RouterLink to="/exercises" class="hover:text-slate-900 dark:hover:text-white">
            Exercises
          </RouterLink>
          <RouterLink to="/workouts" class="hover:text-slate-900 dark:hover:text-white">
            Workout Plans
          </RouterLink>
          <RouterLink to="/sessions" class="hover:text-slate-900 dark:hover:text-white">
            Sessions
          </RouterLink>
          <RouterLink to="/progress" class="hover:text-slate-900 dark:hover:text-white">
            Progress
          </RouterLink>
          <RouterLink to="/nutrition" class="hover:text-slate-900 dark:hover:text-white">
            Nutrition
          </RouterLink>
          <RouterLink to="/notifications" class="hover:text-slate-900 dark:hover:text-white">
            Notifications
          </RouterLink>
        </nav>
      </aside>

      <div class="flex-1">
        <header
          class="flex items-center justify-between border-b border-slate-200 bg-white px-6 py-4 dark:border-slate-800 dark:bg-slate-900"
        >
          <div class="text-sm text-slate-600 dark:text-slate-300">
            Welcome back
          </div>
          <button
            class="rounded-md border border-slate-200 px-3 py-1.5 text-sm dark:border-slate-700"
            @click="ui.toggleDark()"
          >
            Toggle theme
          </button>
        </header>

        <main class="px-6 py-8">
          <slot />
        </main>
      </div>
    </div>
  </div>
</template>
