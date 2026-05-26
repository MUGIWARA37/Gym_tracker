<script setup>
import { onMounted, ref, computed } from 'vue'
import { WorkoutsService } from '../../services/workouts.service'
import Icon from '../../components/ui/Icon.vue'

const plans = ref([])
const loading = ref(true)
const error = ref('')
const showForm = ref(false)
const submitting = ref(false)
const formError = ref('')
const filterGoal = ref(null)
const detailPlan = ref(null)

const form = ref({
  title: '',
  description: '',
  goal: 'build_muscle',
  difficulty: 'beginner',
  days_per_week: 4,
  estimated_duration: 60,
  is_public: false,
  auto_generate: true,
})

const goals = ['lose_weight', 'build_muscle', 'maintain', 'strength', 'cardio']
const difficulties = ['beginner', 'intermediate', 'advanced']
const daysOptions = [4, 5, 6]
const goalColors = { lose_weight: 'badge-orange', build_muscle: 'badge-neon', maintain: 'badge-blue', strength: 'badge-purple', cardio: 'badge-red' }
const difficultyColors = { beginner: 'badge-green', intermediate: 'badge-orange', advanced: 'badge-red' }
// Icons intentionally omitted here to keep filters/badges clean and consistent

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
    const payload = {
      title: form.value.title,
      description: form.value.description,
      goal: form.value.goal,
      difficulty: form.value.difficulty,
      days_per_week: form.value.days_per_week,
      estimated_duration: form.value.estimated_duration,
      is_public: form.value.is_public,
      auto_generate: form.value.auto_generate,
    }

    const { data } = await WorkoutsService.create(payload)
    plans.value.unshift(data)
    showForm.value = false
    detailPlan.value = data
    form.value = {
      title: '',
      description: '',
      goal: 'build_muscle',
      difficulty: 'beginner',
      days_per_week: 4,
      estimated_duration: 60,
      is_public: false,
      auto_generate: true,
    }
  } catch {
    formError.value = 'Failed to create plan.'
  } finally {
    submitting.value = false
  }
}

const closeDetails = () => { detailPlan.value = null }

const planDays = (plan) => plan?.days_per_week || plan?.structure?.split?.length || ''

const dayGroups = computed(() => {
  const plan = detailPlan.value
  if (!plan) return []

  const split = plan?.structure?.split || []
  const groups = {}
  for (const link of (plan.exercises || [])) {
    const d = link.day || 1
    if (!groups[d]) groups[d] = []
    groups[d].push(link)
  }
  for (const d of Object.keys(groups)) {
    groups[d].sort((a, b) => (a.order ?? 0) - (b.order ?? 0))
  }

  if (split.length) {
    return split.map(s => ({ day: s.day, name: s.name, items: groups[s.day] || [] }))
  }

  return Object.keys(groups)
    .map(d => ({ day: Number(d), name: `Day ${d}`, items: groups[d] }))
    .sort((a, b) => a.day - b.day)
})

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
          <Icon v-if="showForm" name="x-mark" :size="16" />
          <Icon v-else name="plus" :size="16" />
          {{ showForm ? 'Cancel' : 'New Plan' }}
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
            <label class="form-label">Days / Week</label>
            <select v-model.number="form.days_per_week" class="form-select">
              <option v-for="d in daysOptions" :key="d" :value="d">{{ d }} days</option>
            </select>
          </div>
        </div>
        <div class="form-group">
          <label class="form-label">Difficulty</label>
          <select v-model="form.difficulty" class="form-select">
            <option v-for="d in difficulties" :key="d" :value="d">{{ formatLabel(d) }}</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Estimated Duration (minutes)</label>
          <input v-model.number="form.estimated_duration" type="number" class="form-input" min="5" max="300" />
        </div>
        <label style="display:flex;align-items:center;gap:8px;font-size:13px;color:var(--text-secondary);cursor:pointer">
          <input type="checkbox" v-model="form.auto_generate" style="accent-color:var(--neon)" />
          Auto-generate detailed plan (exercises + nutrition)
        </label>
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
        {{ formatLabel(g) }}
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
      <div style="margin-bottom:12px;display:flex;justify-content:center;color:var(--text-secondary)">
        <Icon name="clipboard-document-list" :size="40" />
      </div>
      No plans yet.
      <button class="btn btn-primary btn-sm" @click="showForm = true" style="margin-left:8px">
        Create one <Icon name="arrow-right" :size="14" />
      </button>
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
          <span class="badge" :class="goalColors[plan.goal]">{{ formatLabel(plan.goal) }}</span>
          <span class="badge" :class="difficultyColors[plan.difficulty]">{{ formatLabel(plan.difficulty) }}</span>
          <span v-if="planDays(plan)" class="badge badge-muted">{{ planDays(plan) }} days / week</span>
          <span class="badge badge-muted" style="display:inline-flex;align-items:center;gap:6px">
            <Icon name="clock" :size="14" />
            {{ plan.estimated_duration }}m
          </span>
        </div>

        <div style="display:flex;gap:8px;margin-top:auto;padding-top:12px;border-top:1px solid var(--border);flex-wrap:wrap">
          <button class="btn btn-secondary btn-sm" @click="detailPlan = plan"><Icon name="rectangle-stack" :size="14" /> View</button>
          <button class="btn btn-secondary btn-sm" @click="duplicatePlan(plan)"><Icon name="square-2-stack" :size="14" /> Duplicate</button>
          <button class="btn btn-danger btn-sm" @click="deletePlan(plan)"><Icon name="trash" :size="14" /> Delete</button>
        </div>
      </div>
    </div>

    <!-- Details modal -->
    <div v-if="detailPlan" class="modal-overlay" @click.self="closeDetails">
      <div class="modal">
        <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:10px;margin-bottom:14px">
          <div>
            <div style="font-family:var(--font-display);font-size:18px;font-weight:800;color:var(--text-primary)">
              {{ detailPlan.title }}
            </div>
            <div style="margin-top:6px;display:flex;flex-wrap:wrap;gap:6px">
              <span class="badge" :class="goalColors[detailPlan.goal]">{{ formatLabel(detailPlan.goal) }}</span>
              <span class="badge" :class="difficultyColors[detailPlan.difficulty]">{{ formatLabel(detailPlan.difficulty) }}</span>
              <span v-if="planDays(detailPlan)" class="badge badge-muted">{{ planDays(detailPlan) }} days / week</span>
              <span class="badge badge-muted" style="display:inline-flex;align-items:center;gap:6px"><Icon name="clock" :size="14" /> {{ detailPlan.estimated_duration }}m</span>
            </div>
          </div>
          <button class="btn btn-ghost btn-sm" @click="closeDetails"><Icon name="x-mark" :size="16" /> Close</button>
        </div>

        <div v-if="detailPlan.nutrition_guidance && Object.keys(detailPlan.nutrition_guidance).length" class="card" style="margin-bottom:14px">
          <div style="font-size:12px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:var(--text-muted);margin-bottom:10px;display:flex;align-items:center;gap:8px">
            <Icon name="beaker" :size="14" /> Daily nutrition guidance
          </div>
          <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;font-size:13px;color:var(--text-secondary)">
            <div><strong style="color:var(--text-primary)">Calories:</strong> {{ detailPlan.nutrition_guidance.calories }}</div>
            <div><strong style="color:var(--text-primary)">Protein:</strong> {{ detailPlan.nutrition_guidance.protein }}</div>
            <div><strong style="color:var(--text-primary)">Carbs:</strong> {{ detailPlan.nutrition_guidance.carbs }}</div>
            <div><strong style="color:var(--text-primary)">Fats:</strong> {{ detailPlan.nutrition_guidance.fats }}</div>
            <div><strong style="color:var(--text-primary)">Water:</strong> {{ detailPlan.nutrition_guidance.water }}</div>
          </div>
          <div v-if="detailPlan.nutrition_guidance.notes" style="margin-top:10px;color:var(--text-muted);font-size:12px">
            {{ detailPlan.nutrition_guidance.notes }}
          </div>
        </div>

        <div class="card">
          <div style="font-size:12px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:var(--text-muted);margin-bottom:10px;display:flex;align-items:center;gap:8px">
            <Icon name="dumbbell" :size="14" /> Training split & exercises
          </div>

          <div v-if="!detailPlan.exercises?.length" style="color:var(--text-muted);font-size:13px">
            No exercises in this plan yet.
          </div>

          <div v-else style="display:flex;flex-direction:column;gap:14px">
            <div v-for="day in dayGroups" :key="day.day" style="padding:12px;border-radius:10px;background:var(--surface-2);border:1px solid var(--border)">
              <div style="display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:10px">
                <div style="font-weight:800;color:var(--text-primary)">Day {{ day.day }} · {{ day.name }}</div>
                <div style="font-size:12px;color:var(--text-muted)">{{ day.items.length }} exercises</div>
              </div>

              <div style="display:flex;flex-direction:column;gap:8px">
                <div v-for="ex in day.items" :key="ex.id" style="display:flex;align-items:flex-start;justify-content:space-between;gap:12px">
                  <div style="min-width:0">
                    <div style="font-size:13px;font-weight:700;color:var(--text-primary);white-space:nowrap;overflow:hidden;text-overflow:ellipsis">
                      {{ ex.exercise_detail?.name || 'Exercise' }}
                    </div>
                    <div style="font-size:12px;color:var(--text-muted)">
                      {{ ex.sets }} sets · {{ ex.reps }} reps · rest {{ ex.rest_time_seconds }}s
                    </div>
                  </div>
                  <span class="badge badge-muted" style="flex-shrink:0">#{{ ex.order }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
