<script setup>
import { onMounted, ref, computed } from 'vue'
import { WorkoutsService } from '../../services/workouts.service'

const plans = ref([])
const loading = ref(true)
const error = ref('')
const showForm = ref(false)
const submitting = ref(false)
const formError = ref('')
const filterGoal = ref(null)

const form = ref({ title: '', description: '', goal: 'build_muscle', difficulty: 'beginner', estimated_duration: 60, is_public: false })

const goals = ['lose_weight', 'build_muscle', 'maintain', 'strength', 'cardio']
const difficulties = ['beginner', 'intermediate', 'advanced']
const goalColors = { lose_weight: 'badge-orange', build_muscle: 'badge-neon', maintain: 'badge-blue', strength: 'badge-purple', cardio: 'badge-red' }
const difficultyColors = { beginner: 'badge-green', intermediate: 'badge-orange', advanced: 'badge-red' }
const goalEmoji = { lose_weight: '🏃', build_muscle: '💪', maintain: '⚖️', strength: '🏋️', cardio: '❤️' }

const filteredPlans = computed(() => {
  if (!filterGoal.value) return plans.value
  return plans.value.filter(p => p.goal === filterGoal.value)
})

const formatLabel = v => v ? v.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase()) : ''

const fetchPlans = async () => {
  loading.value = true
  try {
    const { data } = await WorkoutsService.list()
    plans.value = Array.isArray(data) ? data : data?.results || []
  } catch { error.value = 'Failed to load plans.' }
  finally { loading.value = false }
}

const createPlan = async () => {
  formError.value = ''
  submitting.value = true
  try {
    const { data } = await WorkoutsService.create(form.value)
    plans.value.unshift(data)
    showForm.value = false
    form.value = { title: '', description: '', goal: 'build_muscle', difficulty: 'beginner', estimated_duration: 60, is_public: false }
  } catch { formError.value = 'Failed to create plan.' }
  finally { submitting.value = false }
}

const duplicatePlan = async (plan) => {
  try {
    const { data } = await WorkoutsService.duplicate(plan.id)
    plans.value.unshift(data)
  } catch { alert('Failed to duplicate.') }
}

const deletePlan = async (plan) => {
  if (!confirm(`Delete "${plan.title}"?`)) return
  try {
    await WorkoutsService.delete(plan.id)
    plans.value = plans.value.filter(p => p.id !== plan.id)
  } catch { alert('Failed to delete.') }
}

onMounted(fetchPlans)
</script>

<template>
  <div class="page">
    <div class="page-header">
      <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px">
        <div>
          <h1 class="page-title">Workout Plans</h1>
          <p class="page-subtitle">Build and manage your training programs</p>
        </div>
        <button class="btn btn-primary" @click="showForm = !showForm">
          {{ showForm ? '✕ Cancel' : '+ New Plan' }}
        </button>
      </div>
    </div>

    <!-- Create form -->
    <div v-if="showForm" class="card" style="margin-bottom:24px" v-scroll-animate>
      <h3 style="font-size:15px;font-weight:700;margin-bottom:18px">Create New Plan</h3>
      <div style="display:grid;gap:14px">
        <div class="form-group">
          <label class="form-label">Plan Title</label>
          <input v-model="form.title" type="text" class="form-input" placeholder="e.g. Upper Body Power" required />
        </div>
        <div class="form-group">
          <label class="form-label">Description</label>
          <textarea v-model="form.description" class="form-input" rows="2" placeholder="Brief description…" style="resize:vertical"></textarea>
        </div>
        <div class="grid-2" style="gap:12px">
          <div class="form-group">
            <label class="form-label">Goal</label>
            <select v-model="form.goal" class="form-select">
              <option v-for="g in goals" :key="g" :value="g">{{ formatLabel(g) }}</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Difficulty</label>
            <select v-model="form.difficulty" class="form-select">
              <option v-for="d in difficulties" :key="d" :value="d">{{ formatLabel(d) }}</option>
            </select>
          </div>
        </div>
        <div class="form-group">
          <label class="form-label">Estimated Duration (minutes)</label>
          <input v-model.number="form.estimated_duration" type="number" class="form-input" min="5" max="300" />
        </div>
        <label style="display:flex;align-items:center;gap:8px;font-size:13px;color:var(--text-secondary);cursor:pointer">
          <input type="checkbox" v-model="form.is_public" style="accent-color:var(--neon)" />
          Make this plan public
        </label>
        <div v-if="formError" style="font-size:13px;color:#f87171">{{ formError }}</div>
        <button class="btn btn-primary" :disabled="submitting || !form.title" @click="createPlan">
          {{ submitting ? 'Creating…' : 'Create Plan' }}
        </button>
      </div>
    </div>

    <!-- Filter chips -->
    <div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:20px">
      <button class="chip" :class="{ active: !filterGoal }" @click="filterGoal = null">All Goals</button>
      <button v-for="g in goals" :key="g" class="chip" :class="{ active: filterGoal === g }" @click="filterGoal = g">
        {{ goalEmoji[g] }} {{ formatLabel(g) }}
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="grid-cards">
      <div v-for="i in 4" :key="i" class="card" style="display:flex;flex-direction:column;gap:12px">
        <div class="skeleton" style="height:20px;width:70%"></div>
        <div class="skeleton" style="height:14px"></div>
        <div class="skeleton" style="height:14px;width:50%"></div>
      </div>
    </div>

    <div v-else-if="!filteredPlans.length" style="text-align:center;padding:48px;color:var(--text-muted)">
      <div style="font-size:40px;margin-bottom:12px">📋</div>
      No plans yet. <button class="btn btn-primary btn-sm" @click="showForm = true" style="margin-left:8px">Create one →</button>
    </div>

    <div v-else class="grid-cards">
      <div
        v-for="(plan, i) in filteredPlans"
        :key="plan.id"
        class="card"
        style="display:flex;flex-direction:column;gap:14px"
        v-scroll-animate="{ delay: (i % 12) * 50 }"
      >
        <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:8px">
          <h3 style="font-size:15px;font-weight:700;color:var(--text-primary);line-height:1.3">{{ plan.title }}</h3>
          <span v-if="plan.is_public" class="badge badge-neon" style="flex-shrink:0">Public</span>
        </div>

        <p style="font-size:13px;color:var(--text-secondary);line-height:1.5;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden">
          {{ plan.description || 'No description provided.' }}
        </p>

        <div style="display:flex;flex-wrap:wrap;gap:6px">
          <span class="badge" :class="goalColors[plan.goal]">{{ goalEmoji[plan.goal] }} {{ formatLabel(plan.goal) }}</span>
          <span class="badge" :class="difficultyColors[plan.difficulty]">{{ formatLabel(plan.difficulty) }}</span>
          <span class="badge badge-muted">⏱ {{ plan.estimated_duration }}m</span>
        </div>

        <div style="display:flex;gap:8px;margin-top:auto;padding-top:12px;border-top:1px solid var(--border)">
          <button class="btn btn-secondary btn-sm" @click="duplicatePlan(plan)">⎘ Duplicate</button>
          <button class="btn btn-danger btn-sm" @click="deletePlan(plan)">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>
