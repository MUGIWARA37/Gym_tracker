<script setup>
import { onMounted, ref } from 'vue'
import api from '../../services/api'

const stats = ref(null)

onMounted(async () => {
  const { data } = await api.get('/dashboard/stats/')
  stats.value = data
})
</script>

<template>
  <div>
    <h1 class="text-2xl font-semibold">Dashboard</h1>
    <div v-if="stats" class="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
      <div class="rounded-xl p-4 card-life">
        <p class="text-sm text-slate-500 dark:text-slate-400">Weekly sessions</p>
        <p class="text-2xl font-semibold text-slate-900 dark:text-white">{{ stats.weekly_sessions }}</p>
      </div>
      <div class="rounded-xl p-4 card-life">
        <p class="text-sm text-slate-500 dark:text-slate-400">Calories burned</p>
        <p class="text-2xl font-semibold text-slate-900 dark:text-white">{{ stats.weekly_calories_burned }}</p>
      </div>
      <div class="rounded-xl p-4 card-life">
        <p class="text-sm text-slate-500 dark:text-slate-400">Current streak</p>
        <p class="text-2xl font-semibold text-slate-900 dark:text-white">{{ stats.current_streak_days }} days</p>
      </div>
      <div class="rounded-xl p-4 card-life">
        <p class="text-sm text-slate-500 dark:text-slate-400">Goal completion</p>
        <p class="text-2xl font-semibold text-slate-900 dark:text-white">{{ stats.goal_completion_percent }}%</p>
      </div>
    </div>
  </div>
</template>
