<script setup>
import { onMounted, ref, computed } from 'vue'
import { ExercisesService } from '../../services/exercises.service'
import { useDebounce } from '../../composables/useDebounce'
import Icon from '../../components/ui/Icon.vue'

const exercises = ref([])
const loading = ref(true)
const error = ref('')
const selectedMuscle = ref(null)
const selectedDifficulty = ref(null)
const searchQuery = ref('')

const muscleGroups = [
  { key: 'chest', label: 'Chest' },
  { key: 'back', label: 'Back' },
  { key: 'legs', label: 'Legs' },
  { key: 'shoulders', label: 'Shoulders' },
  { key: 'arms', label: 'Arms' },
  { key: 'core', label: 'Core' },
  { key: 'full_body', label: 'Full Body' },
]

const difficulties = ['beginner', 'intermediate', 'advanced']

const difficultyColor = { beginner: 'badge-green', intermediate: 'badge-orange', advanced: 'badge-red' }
const muscleIcon = { chest: 'dumbbell', back: 'dumbbell', legs: 'dumbbell', shoulders: 'dumbbell', arms: 'dumbbell', core: 'bolt', full_body: 'fire' }

const debouncedSearch = useDebounce(searchQuery, 400)

const filteredExercises = computed(() => {
  let list = exercises.value
  if (selectedMuscle.value) list = list.filter(ex => ex.muscle_group === selectedMuscle.value)
  if (selectedDifficulty.value) list = list.filter(ex => ex.difficulty_level === selectedDifficulty.value)
  const q = (debouncedSearch.value || '').toLowerCase().trim()
  if (q) list = list.filter(ex => ex.name.toLowerCase().includes(q) || ex.description?.toLowerCase().includes(q))
  return list
})

const formatLabel = (v) => v ? v.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase()) : ''

onMounted(async () => {
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
})
</script>

<template>
  <div class="page">
    <div class="page-header">
      <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px">
        <div>
          <h1 class="page-title">Exercises</h1>
          <p class="page-subtitle">{{ exercises.length }} exercises in the library</p>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="card" style="margin-bottom:24px" v-scroll-animate>
      <div style="display:flex;flex-wrap:wrap;gap:16px;align-items:flex-end">
        <!-- Search -->
        <div class="form-group" style="flex:1;min-width:200px">
          <label class="form-label">Search</label>
          <input v-model="searchQuery" type="text" class="form-input" placeholder="Search exercises…" />
        </div>
        <!-- Difficulty -->
        <div class="form-group" style="min-width:150px">
          <label class="form-label">Difficulty</label>
          <select v-model="selectedDifficulty" class="form-select">
            <option :value="null">All levels</option>
            <option v-for="d in difficulties" :key="d" :value="d">{{ formatLabel(d) }}</option>
          </select>
        </div>
      </div>

      <!-- Muscle group chips -->
      <div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:14px">
        <button
          class="chip"
          :class="{ active: selectedMuscle === null }"
          @click="selectedMuscle = null"
        >All muscles</button>
        <button
          v-for="m in muscleGroups"
          :key="m.key"
          class="chip"
          :class="{ active: selectedMuscle === m.key }"
          @click="selectedMuscle = m.key"
        >
          {{ m.label }}
        </button>
      </div>

      <div style="margin-top:12px;font-size:12px;color:var(--text-muted)">
        Showing <strong style="color:var(--text-primary)">{{ filteredExercises.length }}</strong> of {{ exercises.length }} exercises
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="grid-cards">
      <div v-for="i in 6" :key="i" class="exercise-card" v-scroll-animate="{ delay: i * 40 }">
        <div class="skeleton" style="height:140px"></div>
        <div style="padding:16px;display:flex;flex-direction:column;gap:10px">
          <div class="skeleton" style="height:16px;width:60%"></div>
          <div class="skeleton" style="height:12px"></div>
          <div class="skeleton" style="height:12px;width:70%"></div>
        </div>
      </div>
    </div>

    <!-- Error -->
    <div v-else-if="error" style="text-align:center;padding:48px;color:#f87171">{{ error }}</div>

    <!-- Empty -->
    <div v-else-if="!filteredExercises.length" style="text-align:center;padding:48px;color:var(--text-muted)">
      No exercises found. Try adjusting your filters.
    </div>

    <!-- Grid -->
    <div v-else class="grid-cards">
      <div
        v-for="(exercise, i) in filteredExercises"
        :key="exercise.id"
        class="exercise-card"
        v-scroll-animate="{ delay: (i % 12) * 50 }"
      >
        <!-- Thumb -->
        <div class="exercise-thumb">
          <img v-if="exercise.image" :src="exercise.image" :alt="exercise.name" />
          <div v-else class="muscle-bg">
            <span style="display:inline-flex;align-items:center;color:rgba(255,255,255,0.75)"><Icon :name="muscleIcon[exercise.muscle_group] || 'dumbbell'" :size="44" /></span>
          </div>
          <!-- Difficulty badge overlay -->
          <span
            class="badge"
            :class="difficultyColor[exercise.difficulty_level]"
            style="position:absolute;top:10px;right:10px;backdrop-filter:blur(8px)"
          >{{ formatLabel(exercise.difficulty_level) }}</span>
        </div>

        <!-- Body -->
        <div style="padding:16px;display:flex;flex-direction:column;gap:10px;flex:1">
          <div>
            <h2 style="font-size:15px;font-weight:700;color:var(--text-primary);margin-bottom:4px">{{ exercise.name }}</h2>
            <p style="font-size:12px;color:var(--text-secondary);line-height:1.5;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden">
              {{ exercise.description || 'No description provided.' }}
            </p>
          </div>

          <!-- Tags -->
          <div style="display:flex;flex-wrap:wrap;gap:6px">
            <span class="badge badge-muted">{{ formatLabel(exercise.muscle_group) }}</span>
            <span v-if="exercise.equipment_needed" class="badge badge-muted">{{ exercise.equipment_needed }}</span>
          </div>

          <!-- Calories & video -->
          <div style="display:flex;align-items:center;justify-content:space-between;margin-top:auto;padding-top:8px;border-top:1px solid var(--border)">
            <span style="font-size:12px;color:var(--text-muted);display:inline-flex;align-items:center;gap:6px">
              <Icon name="fire" :size="14" />
              {{ exercise.calories_burn_estimate }} kcal / 30m
            </span>
            <a
              v-if="exercise.video_url"
              :href="exercise.video_url"
              target="_blank"
              rel="noopener"
              class="btn btn-ghost btn-sm"
              style="font-size:11px;padding:4px 10px"
            ><Icon name="play" :size="14" /> Watch</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
