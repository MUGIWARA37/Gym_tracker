<script setup>
import { onMounted, ref, computed } from 'vue'
import { SessionsService } from '../../services/sessions.service'
import { WorkoutsService } from '../../services/workouts.service'
import { useTimer } from '../../composables/useTimer'

const sessions = ref([])
const plans = ref([])
const loading = ref(true)
const showForm = ref(false)
const submitting = ref(false)
const activeSession = ref(null)
const timerState = ref('idle') // idle | active | paused | complete

const { elapsed, formatted, start, pause, reset } = useTimer()

const form = ref({ workout_plan: '', mood: 'motivated', notes: '' })
const moods = ['motivated', 'excellent', 'average', 'tired']
const moodEmoji = { motivated: '🔥', tired: '😴', excellent: '⚡', average: '😐' }
const moodColors = { motivated: 'badge-orange', excellent: 'badge-neon', average: 'badge-muted', tired: 'badge-blue' }

const formatDate = (dt) => dt ? new Date(dt).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit' }) : '—'
const formatDuration = (start, end) => {
  if (!start || !end) return '—'
  const mins = Math.round((new Date(end) - new Date(start)) / 60000)
  if (mins < 60) return `${mins} min`
  return `${Math.floor(mins/60)}h ${mins%60}m`
}
const formatLabel = v => v ? v.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase()) : ''

onMounted(async () => {
  try {
    const [sessRes, planRes] = await Promise.allSettled([
      SessionsService.list(),
      WorkoutsService.list(),
    ])
    if (sessRes.status === 'fulfilled') {
      const d = sessRes.value.data
      sessions.value = Array.isArray(d) ? d : d?.results || []
    }
    if (planRes.status === 'fulfilled') {
      const d = planRes.value.data
      plans.value = Array.isArray(d) ? d : d?.results || []
    }
  } finally { loading.value = false }
})

const startSession = async () => {
  submitting.value = true
  try {
    const payload = {
      start_time: new Date().toISOString(),
      mood: form.value.mood,
      notes: form.value.notes,
    }
    if (form.value.workout_plan) payload.workout_plan = form.value.workout_plan
    const { data } = await SessionsService.create(payload)
    activeSession.value = data
    showForm.value = false
    timerState.value = 'active'
    start()
  } catch { alert('Failed to start session.') }
  finally { submitting.value = false }
}

const pauseTimer = () => {
  if (timerState.value === 'active') { pause(); timerState.value = 'paused' }
  else { start(); timerState.value = 'active' }
}

const stopSession = async () => {
  pause()
  timerState.value = 'complete'
  if (!activeSession.value) return
  try {
    const { data } = await SessionsService.update(activeSession.value.id, {
      end_time: new Date().toISOString(),
      completed: true,
    })
    sessions.value.unshift(data)
    activeSession.value = null
    reset()
    timerState.value = 'idle'
  } catch { alert('Failed to save session.') }
}

const totalCalories = computed(() => sessions.value.reduce((s, x) => s + parseFloat(x.calories_burned || 0), 0))
</script>

<template>
  <div class="page">
    <div class="page-header">
      <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px">
        <div>
          <h1 class="page-title">Sessions</h1>
          <p class="page-subtitle">{{ sessions.length }} sessions logged</p>
        </div>
        <button v-if="!activeSession" class="btn btn-primary" @click="showForm = !showForm">
          {{ showForm ? '✕ Cancel' : '▷ Start Session' }}
        </button>
      </div>
    </div>

    <!-- Active Session Timer -->
    <div v-if="activeSession" class="timer-card animate-fade-up" style="margin-bottom:24px">
      <div style="font-size:12px;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:var(--text-muted);margin-bottom:16px">
        🔴 Live Session
      </div>
      <div class="timer-display">{{ formatted }}</div>
      <div style="margin-top:8px;font-size:14px;color:var(--text-secondary)">
        {{ plans.find(p => p.id === activeSession.workout_plan)?.title || 'Free Workout' }}
      </div>
      <div style="display:flex;justify-content:center;gap:12px;margin-top:20px">
        <button class="btn btn-secondary btn-lg" @click="pauseTimer">
          {{ timerState === 'active' ? '⏸ Pause' : '▷ Resume' }}
        </button>
        <button class="btn btn-danger btn-lg" @click="stopSession">⏹ Finish</button>
      </div>
    </div>

    <!-- Start Session Form -->
    <div v-if="showForm && !activeSession" class="card animate-fade-up" style="margin-bottom:24px">
      <h3 style="font-size:15px;font-weight:700;margin-bottom:18px">New Session</h3>
      <div style="display:grid;gap:14px">
        <div class="form-group">
          <label class="form-label">Workout Plan (optional)</label>
          <select v-model="form.workout_plan" class="form-select">
            <option value="">Free workout</option>
            <option v-for="p in plans" :key="p.id" :value="p.id">{{ p.title }}</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">How are you feeling?</label>
          <div style="display:flex;gap:8px;flex-wrap:wrap">
            <button
              v-for="m in moods" :key="m"
              class="btn btn-sm"
              :class="form.mood === m ? 'btn-primary' : 'btn-secondary'"
              @click="form.mood = m"
            >{{ moodEmoji[m] }} {{ formatLabel(m) }}</button>
          </div>
        </div>
        <div class="form-group">
          <label class="form-label">Notes</label>
          <textarea v-model="form.notes" class="form-input" rows="2" placeholder="Optional notes…" style="resize:vertical"></textarea>
        </div>
        <button class="btn btn-primary btn-lg" :disabled="submitting" @click="startSession">
          {{ submitting ? 'Starting…' : '▷ Start Session' }}
        </button>
      </div>
    </div>

    <!-- Stats bar -->
    <div class="grid-stats animate-fade-up" style="margin-bottom:24px">
      <div class="stat-card accent-blue">
        <div class="stat-icon blue">📋</div>
        <div class="stat-value blue">{{ sessions.length }}</div>
        <div class="stat-label">Total Sessions</div>
      </div>
      <div class="stat-card accent-orange">
        <div class="stat-icon orange">🔥</div>
        <div class="stat-value orange">{{ Math.round(totalCalories).toLocaleString() }}</div>
        <div class="stat-label">Total Calories</div>
      </div>
      <div class="stat-card accent-neon">
        <div class="stat-icon neon">✅</div>
        <div class="stat-value neon">{{ sessions.filter(s => s.completed).length }}</div>
        <div class="stat-label">Completed</div>
      </div>
    </div>

    <!-- Session History -->
    <div class="card animate-fade-up">
      <h3 style="font-size:15px;font-weight:700;margin-bottom:16px">History</h3>

      <div v-if="loading" style="display:flex;flex-direction:column;gap:10px">
        <div v-for="i in 4" :key="i" class="skeleton" style="height:64px;border-radius:10px"></div>
      </div>

      <div v-else-if="!sessions.length" style="text-align:center;padding:32px;color:var(--text-muted)">
        No sessions yet. Start your first workout above!
      </div>

      <div v-else style="display:flex;flex-direction:column;gap:8px">
        <div
          v-for="session in sessions"
          :key="session.id"
          style="display:flex;align-items:center;gap:14px;padding:14px 16px;border-radius:10px;background:var(--surface-2);border:1px solid var(--border)"
        >
          <span style="font-size:22px">{{ moodEmoji[session.mood] || '💪' }}</span>
          <div style="flex:1;min-width:0">
            <div style="font-size:13px;font-weight:600;color:var(--text-primary);white-space:nowrap;overflow:hidden;text-overflow:ellipsis">
              {{ session.workout_plan_name || 'Free Workout' }}
            </div>
            <div style="font-size:12px;color:var(--text-muted);margin-top:2px">{{ formatDate(session.start_time) }}</div>
          </div>
          <div style="display:flex;flex-wrap:wrap;gap:6px;justify-content:flex-end">
            <span class="badge" :class="moodColors[session.mood]">{{ formatLabel(session.mood) }}</span>
            <span class="badge badge-muted">{{ formatDuration(session.start_time, session.end_time) }}</span>
            <span v-if="session.calories_burned" class="badge badge-orange">🔥 {{ Math.round(session.calories_burned) }}</span>
            <span v-if="session.completed" class="badge badge-green">✓</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
