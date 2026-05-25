<script setup>
import { onMounted, ref } from 'vue'
import { ExercisesService } from '../../services/exercises.service'

const exercises = ref([])
const loading = ref(true)
const error = ref('')

const formatLabel = (value) => {
  if (!value) return ''
  return value.replace(/_/g, ' ')
}

const fetchExercises = async () => {
  loading.value = true
  error.value = ''
  try {
    const { data } = await ExercisesService.list()
    exercises.value = Array.isArray(data) ? data : data?.results || []
  } catch {
    error.value = 'Failed to load exercises.'
  } finally {
    loading.value = false
  }
}

onMounted(fetchExercises)
</script>

<template>
  <div>
    <h1 class="text-2xl font-semibold">Exercises</h1>
    <p class="mt-2 text-sm text-slate-500">Browse and manage exercises.</p>

    <p v-if="loading" class="mt-6 text-sm text-slate-500">Loading exercises...</p>
    <p v-else-if="error" class="mt-6 text-sm text-red-500">{{ error }}</p>
    <p v-else-if="!exercises.length" class="mt-6 text-sm text-slate-500">
      No exercises yet.
    </p>

    <div v-else class="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
      <div
        v-for="exercise in exercises"
        :key="exercise.id"
        class="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm dark:border-slate-800 dark:bg-slate-900"
      >
        <div class="h-36 bg-slate-100 dark:bg-slate-800">
          <img
            v-if="exercise.image"
            :src="exercise.image"
            :alt="exercise.name"
            class="h-full w-full object-cover"
          />
        </div>
        <div class="space-y-2 p-4">
          <div class="flex items-center justify-between gap-2">
            <h2 class="text-base font-semibold text-slate-900 dark:text-white">
              {{ exercise.name }}
            </h2>
            <span class="rounded-full bg-slate-100 px-2 py-0.5 text-xs text-slate-600 dark:bg-slate-800 dark:text-slate-200">
              {{ formatLabel(exercise.difficulty_level) }}
            </span>
          </div>
          <p class="text-sm text-slate-500 dark:text-slate-300">
            {{ exercise.description || 'No description provided.' }}
          </p>
          <div class="flex flex-wrap gap-2 text-xs text-slate-600 dark:text-slate-300">
            <span class="rounded-full bg-slate-100 px-2 py-0.5 dark:bg-slate-800">
              {{ formatLabel(exercise.muscle_group) }}
            </span>
            <span
              v-if="exercise.equipment_needed"
              class="rounded-full bg-slate-100 px-2 py-0.5 dark:bg-slate-800"
            >
              {{ exercise.equipment_needed }}
            </span>
            <span class="rounded-full bg-slate-100 px-2 py-0.5 dark:bg-slate-800">
              {{ exercise.calories_burn_estimate }} kcal / 30m
            </span>
          </div>
          <a
            v-if="exercise.video_url"
            :href="exercise.video_url"
            target="_blank"
            rel="noopener"
            class="text-xs font-medium text-slate-700 underline dark:text-slate-200"
          >
            Watch demo
          </a>
        </div>
      </div>
    </div>
  </div>
</template>
