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

// Modal state
const selectedExercise = ref(null)
const showModal = ref(false)

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

// Convert any YouTube URL to embed format
function getEmbedUrl(url) {
  if (!url) return null
  // Handle youtu.be short links
  let match = url.match(/youtu\.be\/([^?&]+)/)
  if (match) return `https://www.youtube.com/embed/${match[1]}?autoplay=1&rel=0`
  // Handle youtube.com/watch?v=
  match = url.match(/[?&]v=([^&]+)/)
  if (match) return `https://www.youtube.com/embed/${match[1]}?autoplay=1&rel=0`
  // Handle youtube.com/embed/ already
  if (url.includes('youtube.com/embed/')) return url
  // For other URLs (Vimeo, etc.) try to return as-is for iframe
  return url
}

function openModal(exercise) {
  selectedExercise.value = exercise
  showModal.value = true
  document.body.style.overflow = 'hidden'
}

function closeModal() {
  showModal.value = false
  selectedExercise.value = null
  document.body.style.overflow = ''
}

function onOverlayClick(e) {
  if (e.target === e.currentTarget) closeModal()
}

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
        class="exercise-card ex-clickable"
        v-scroll-animate="{ delay: (i % 12) * 50 }"
        @click="openModal(exercise)"
        :title="`Click to view ${exercise.name}`"
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
          <!-- Play button overlay if video exists -->
          <div v-if="exercise.video_url" class="play-overlay">
            <div class="play-btn-circle">
              <Icon name="play" :size="22" />
            </div>
          </div>
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

          <!-- Calories & video hint -->
          <div style="display:flex;align-items:center;justify-content:space-between;margin-top:auto;padding-top:8px;border-top:1px solid var(--border)">
            <span style="font-size:12px;color:var(--text-muted);display:inline-flex;align-items:center;gap:6px">
              <Icon name="fire" :size="14" />
              {{ exercise.calories_burn_estimate }} kcal / 30m
            </span>
            <span v-if="exercise.video_url" style="font-size:11px;color:var(--neon);display:inline-flex;align-items:center;gap:5px;font-weight:600">
              <Icon name="play" :size="13" /> Video
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- ─── Exercise Video Modal ─── -->
    <Teleport to="body">
      <Transition name="modal-fade">
        <div
          v-if="showModal && selectedExercise"
          class="modal-overlay ex-modal-overlay"
          @click="onOverlayClick"
        >
          <div class="modal ex-modal" @click.stop>
            <!-- Header -->
            <div class="ex-modal-header">
              <div style="flex:1;min-width:0">
                <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:6px">
                  <h2 class="ex-modal-title">{{ selectedExercise.name }}</h2>
                  <span class="badge" :class="difficultyColor[selectedExercise.difficulty_level]">
                    {{ formatLabel(selectedExercise.difficulty_level) }}
                  </span>
                  <span class="badge badge-muted">{{ formatLabel(selectedExercise.muscle_group) }}</span>
                </div>
                <p style="font-size:13px;color:var(--text-secondary)">{{ selectedExercise.description || 'No description provided.' }}</p>
              </div>
              <button class="ex-close-btn" @click="closeModal" aria-label="Close">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
                  <path d="M18 6L6 18M6 6l12 12"/>
                </svg>
              </button>
            </div>

            <!-- Video area -->
            <div class="ex-video-area">
              <iframe
                v-if="getEmbedUrl(selectedExercise.video_url)"
                :src="getEmbedUrl(selectedExercise.video_url)"
                class="ex-video-frame"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen
                frameborder="0"
                title="Exercise video"
              ></iframe>
              <div v-else class="ex-no-video">
                <div class="ex-no-video-inner">
                  <Icon :name="muscleIcon[selectedExercise.muscle_group] || 'dumbbell'" :size="56" />
                  <p style="margin-top:16px;font-size:15px;font-weight:600;color:var(--text-secondary)">No video available</p>
                  <p style="font-size:12px;color:var(--text-muted);margin-top:4px">This exercise doesn't have a video yet.</p>
                </div>
              </div>
            </div>

            <!-- Stats row -->
            <div class="ex-stats-row">
              <div class="ex-stat">
                <span class="ex-stat-label">Calories / 30 min</span>
                <span class="ex-stat-value"><Icon name="fire" :size="14" style="color:var(--orange)" /> {{ selectedExercise.calories_burn_estimate }} kcal</span>
              </div>
              <div class="ex-stat">
                <span class="ex-stat-label">MET Value</span>
                <span class="ex-stat-value">{{ selectedExercise.met_value }}</span>
              </div>
              <div v-if="selectedExercise.equipment_needed" class="ex-stat">
                <span class="ex-stat-label">Equipment</span>
                <span class="ex-stat-value">{{ selectedExercise.equipment_needed }}</span>
              </div>
            </div>

            <div style="text-align:right;margin-top:12px">
              <button class="btn btn-ghost btn-sm" @click="closeModal">Close</button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
/* Clickable card */
.ex-clickable {
  cursor: pointer;
  transition: transform 0.18s, border-color 0.18s, box-shadow 0.18s;
}
.ex-clickable:hover {
  border-color: var(--neon) !important;
  box-shadow: 0 0 0 1px var(--neon), 0 8px 32px rgba(200,247,82,0.08);
}

/* Play overlay on thumbnail */
.play-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0,0,0,0);
  transition: background 0.2s;
}
.exercise-thumb:hover .play-overlay {
  background: rgba(0,0,0,0.38);
}
.play-btn-circle {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--neon);
  color: #0a0a0f;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transform: scale(0.7);
  transition: opacity 0.2s, transform 0.2s;
  box-shadow: 0 4px 20px rgba(200,247,82,0.5);
}
.exercise-thumb:hover .play-btn-circle {
  opacity: 1;
  transform: scale(1);
}

/* Modal overlay extras */
.ex-modal-overlay {
  z-index: 999;
}
.ex-modal {
  width: min(780px, 100%);
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  gap: 0;
  padding: 0;
  overflow: hidden;
}

/* Header */
.ex-modal-header {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 22px 24px 18px;
  border-bottom: 1px solid var(--border);
}
.ex-modal-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  font-family: var(--font-display);
}
.ex-close-btn {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: var(--surface-3);
  border: 1px solid var(--border);
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s, color 0.15s;
}
.ex-close-btn:hover {
  background: var(--surface-2);
  color: var(--text-primary);
}

/* Video */
.ex-video-area {
  width: 100%;
  aspect-ratio: 16/9;
  background: #000;
  position: relative;
}
.ex-video-frame {
  width: 100%;
  height: 100%;
  display: block;
  border: none;
}
.ex-no-video {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--surface-2);
}
.ex-no-video-inner {
  text-align: center;
  color: var(--text-muted);
}

/* Stats */
.ex-stats-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid var(--border);
  background: var(--surface-2);
}
.ex-stat {
  display: flex;
  flex-direction: column;
  gap: 3px;
  padding: 10px 14px;
  background: var(--surface-3);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  min-width: 100px;
}
.ex-stat-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-muted);
  font-weight: 600;
}
.ex-stat-value {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

/* Close btn in footer */
.ex-modal > [style*="text-align:right"] {
  padding: 0 24px 18px;
}

/* Transition */
.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.22s ease;
}
.modal-fade-enter-active .ex-modal,
.modal-fade-leave-active .ex-modal {
  transition: opacity 0.22s ease, transform 0.22s ease;
}
.modal-fade-enter-from, .modal-fade-leave-to {
  opacity: 0;
}
.modal-fade-enter-from .ex-modal,
.modal-fade-leave-to .ex-modal {
  opacity: 0;
  transform: scale(0.95) translateY(16px);
}
</style>
