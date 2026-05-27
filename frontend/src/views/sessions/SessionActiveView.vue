<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { SessionsService } from '../../services/sessions.service'
import { WorkoutsService } from '../../services/workouts.service'
import { useTimer } from '../../composables/useTimer'
import Icon from '../../components/ui/Icon.vue'

const route  = useRoute()
const router = useRouter()

/* ─── Session meta ─── */
const session      = ref(null)
const plan         = ref(null)
const loading      = ref(true)
const completing   = ref(false)
const timerState   = ref('active') // active | paused | complete
const showSummary  = ref(false)

const { elapsed, formatted, start, pause, reset } = useTimer()

/* ─── Exercise state ─── */
const currentExIndex = ref(0)
const currentSetIndex = ref(0)
const logForm = ref({ weight_used_kg: '', reps: '', duration_seconds: 0 })
const loggingSet = ref(false)
const loggedSets = ref([])   // { exerciseId, set, weight, reps }
const restCountdown = ref(0)
let restTimer = null

/* ─── Derived ─── */
const exercises = computed(() => {
  if (!plan.value?.exercises) return []
  return [...plan.value.exercises].sort((a, b) => (a.day - b.day) || (a.order - b.order))
})

const currentEx = computed(() => exercises.value[currentExIndex.value] || null)
const totalSets = computed(() => currentEx.value?.sets || 3)

const progressPct = computed(() => {
  const total = exercises.value.reduce((s, e) => s + (e.sets || 3), 0) || 1
  const done  = loggedSets.value.length
  return Math.min(100, Math.round(done / total * 100))
})

/* ─── Init ─── */
onMounted(async () => {
  const id = route.params.id
  try {
    const { data } = await SessionsService.list({ page_size: 100 })
    const all = Array.isArray(data) ? data : data?.results || []
    session.value = all.find(s => String(s.id) === String(id))
    if (!session.value) {
      router.push('/sessions')
      return
    }
    if (session.value.workout_plan) {
      const pd = await WorkoutsService.get(session.value.workout_plan)
      plan.value = pd.data
      if (plan.value?.exercises?.length) {
        const ex = plan.value.exercises[0]
        logForm.value.reps = ex.reps || ''
      }
    }
  } finally { loading.value = false }
  start()
})

onUnmounted(() => {
  clearInterval(restTimer)
})

/* ─── Timer controls ─── */
const togglePause = () => {
  if (timerState.value === 'active') { pause(); timerState.value = 'paused' }
  else { start(); timerState.value = 'active' }
}

/* ─── Log a set ─── */
const logSet = async () => {
  if (!session.value || !currentEx.value) return
  loggingSet.value = true
  try {
    const payload = {
      exercise: currentEx.value.exercise,
      sets: 1,
      reps: parseInt(logForm.value.reps) || currentEx.value.reps || 0,
      weight_used_kg: parseFloat(logForm.value.weight_used_kg) || 0,
      duration_seconds: logForm.value.duration_seconds || 0,
      rest_time_seconds: currentEx.value.rest_time_seconds || 60,
      completed: true,
    }
    await SessionsService.addLog(session.value.id, payload)
    loggedSets.value.push({
      exerciseId: currentEx.value.exercise,
      exerciseName: currentEx.value.exercise_detail?.name || 'Exercise',
      set: currentSetIndex.value + 1,
      reps: payload.reps,
      weight: payload.weight_used_kg,
    })

    // Advance
    if (currentSetIndex.value < totalSets.value - 1) {
      currentSetIndex.value++
      startRest(currentEx.value.rest_time_seconds || 60)
    } else {
      // Move to next exercise
      if (currentExIndex.value < exercises.value.length - 1) {
        currentExIndex.value++
        currentSetIndex.value = 0
        const nextEx = exercises.value[currentExIndex.value]
        logForm.value.reps = nextEx?.reps || ''
        startRest(currentEx.value?.rest_time_seconds || 90)
      } else {
        // All exercises done — prompt finish
        showSummary.value = true
      }
    }
  } finally { loggingSet.value = false }
}

const skipExercise = () => {
  if (currentExIndex.value < exercises.value.length - 1) {
    currentExIndex.value++
    currentSetIndex.value = 0
    const nextEx = exercises.value[currentExIndex.value]
    logForm.value.reps = nextEx?.reps || ''
    logForm.value.weight_used_kg = ''
  }
}

/* ─── Rest countdown ─── */
const startRest = (seconds) => {
  clearInterval(restTimer)
  restCountdown.value = seconds
  restTimer = setInterval(() => {
    if (restCountdown.value <= 0) { clearInterval(restTimer); return }
    restCountdown.value--
  }, 1000)
}

const skipRest = () => {
  clearInterval(restTimer)
  restCountdown.value = 0
}

/* ─── Complete session ─── */
const completeSession = async () => {
  completing.value = true
  pause()
  try {
    await SessionsService.update(session.value.id, {
      end_time: new Date().toISOString(),
      completed: true,
    })
    showSummary.value = true
    timerState.value = 'complete'
  } finally { completing.value = false }
}

const goToHistory = () => router.push('/sessions')

/* ─── Helpers ─── */
const formatRest = (s) => {
  const m = Math.floor(s / 60)
  const sec = s % 60
  return m > 0 ? `${m}:${String(sec).padStart(2, '0')}` : `${sec}s`
}
</script>

<template>
  <div class="page">
    <div class="page-header">
      <div style="display:flex;align-items:center;gap:12px">
        <button class="btn btn-ghost btn-sm" @click="router.push('/sessions')">
          <Icon name="arrow-left" :size="16" /> Back
        </button>
        <div>
          <h1 class="page-title">Active Session</h1>
          <p class="page-subtitle">{{ plan?.title || 'Free Workout' }}</p>
        </div>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" style="display:flex;flex-direction:column;gap:16px">
      <div class="card"><div class="skeleton" style="height:120px;border-radius:12px"></div></div>
      <div class="card"><div class="skeleton" style="height:200px;border-radius:12px"></div></div>
    </div>

    <template v-else-if="!showSummary">
      <!-- Timer bar -->
      <div class="timer-card" style="margin-bottom:20px" v-scroll-animate>
        <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px">
          <div>
            <div style="font-size:12px;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:var(--text-muted);margin-bottom:8px;display:flex;align-items:center;gap:8px">
              <span v-if="timerState === 'active'" style="display:inline-block;width:8px;height:8px;border-radius:999px;background:#ef4444;box-shadow:0 0 12px rgba(239,68,68,0.55);animation:pulse 1.2s infinite"></span>
              {{ timerState === 'paused' ? '⏸ Paused' : '● Live Session' }}
            </div>
            <div class="timer-display">{{ formatted }}</div>
          </div>
          <div style="display:flex;flex-direction:column;align-items:flex-end;gap:8px">
            <!-- Progress -->
            <div style="font-size:13px;color:var(--text-secondary)">
              {{ loggedSets.length }} sets logged · {{ progressPct }}% complete
            </div>
            <div style="width:180px;height:6px;background:var(--surface-3);border-radius:99px;overflow:hidden">
              <div style="height:100%;border-radius:99px;background:var(--neon);transition:width 0.4s" :style="{ width: progressPct + '%' }"></div>
            </div>
          </div>
        </div>
        <div style="display:flex;gap:10px;margin-top:20px;flex-wrap:wrap">
          <button class="btn btn-secondary" @click="togglePause">
            <Icon :name="timerState === 'active' ? 'pause' : 'play'" :size="16" />
            {{ timerState === 'active' ? 'Pause' : 'Resume' }}
          </button>
          <button class="btn btn-danger" :disabled="completing" @click="completeSession">
            <Icon name="flag" :size="16" />
            {{ completing ? 'Finishing…' : 'Finish Session' }}
          </button>
        </div>
      </div>

      <!-- Rest countdown -->
      <div v-if="restCountdown > 0" class="card" style="margin-bottom:20px;border-color:var(--blue);box-shadow:0 0 0 1px var(--blue-dim)" v-scroll-animate>
        <div style="display:flex;align-items:center;justify-content:space-between;gap:12px">
          <div>
            <div style="font-size:12px;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;color:var(--blue);margin-bottom:4px">Rest Period</div>
            <div style="font-size:36px;font-weight:800;font-family:var(--font-display);color:var(--blue)">{{ formatRest(restCountdown) }}</div>
          </div>
          <button class="btn btn-secondary btn-sm" @click="skipRest">Skip Rest</button>
        </div>
      </div>

      <!-- No plan — free workout mode -->
      <div v-if="!exercises.length" class="card" v-scroll-animate>
        <div style="text-align:center;padding:32px;color:var(--text-muted)">
          <Icon name="dumbbell" :size="40" style="display:block;margin:0 auto 12px;opacity:0.5" />
          <p>Free workout — no exercises to track.</p>
          <p style="font-size:12px;margin-top:8px">Finish whenever you're done!</p>
        </div>
      </div>

      <!-- Current exercise -->
      <div v-else class="grid-2" style="gap:20px;align-items:start">
        <!-- Exercise card -->
        <div class="card" v-scroll-animate>
          <div style="font-size:11px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:var(--text-muted);margin-bottom:14px">
            Exercise {{ currentExIndex + 1 }} of {{ exercises.length }}
          </div>

          <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:10px;margin-bottom:16px">
            <div>
              <h2 style="font-size:20px;font-weight:800;font-family:var(--font-display);color:var(--text-primary)">
                {{ currentEx?.exercise_detail?.name || 'Exercise' }}
              </h2>
              <div style="font-size:12px;color:var(--text-muted);margin-top:4px;display:flex;flex-wrap:wrap;gap:6px">
                <span class="badge badge-muted" v-if="currentEx?.exercise_detail?.muscle_group">
                  {{ currentEx.exercise_detail.muscle_group }}
                </span>
                <span class="badge badge-muted" v-if="currentEx?.exercise_detail?.difficulty_level">
                  {{ currentEx.exercise_detail.difficulty_level }}
                </span>
              </div>
            </div>
          </div>

          <!-- Set progress dots -->
          <div style="display:flex;gap:6px;margin-bottom:16px">
            <div
              v-for="s in totalSets"
              :key="s"
              style="flex:1;height:6px;border-radius:99px;transition:background 0.3s"
              :style="{
                background: s <= currentSetIndex ? 'var(--neon)' : s === currentSetIndex + 1 ? 'rgba(200,247,82,0.4)' : 'var(--surface-3)'
              }"
            ></div>
          </div>

          <div style="font-size:15px;font-weight:700;color:var(--text-primary);margin-bottom:14px">
            Set {{ currentSetIndex + 1 }} of {{ totalSets }}
          </div>

          <!-- Log form -->
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px">
            <div class="form-group">
              <label class="form-label">Weight (kg)</label>
              <input v-model.number="logForm.weight_used_kg" type="number" step="0.5" class="form-input" placeholder="0" />
            </div>
            <div class="form-group">
              <label class="form-label">Reps</label>
              <input v-model.number="logForm.reps" type="number" class="form-input" :placeholder="currentEx?.reps || ''" />
            </div>
          </div>

          <div style="display:flex;gap:8px">
            <button
              class="btn btn-primary btn-lg"
              style="flex:1"
              :disabled="loggingSet"
              @click="logSet"
            >
              <Icon name="check" :size="18" />
              {{ loggingSet ? 'Logging…' : 'Log Set' }}
            </button>
            <button class="btn btn-secondary" @click="skipExercise" title="Skip exercise">
              <Icon name="forward" :size="16" />
            </button>
          </div>
        </div>

        <!-- Exercise queue + logged sets -->
        <div style="display:flex;flex-direction:column;gap:16px">
          <!-- Queue -->
          <div class="card" v-scroll-animate="{ delay: 60 }">
            <h3 style="font-size:14px;font-weight:700;margin-bottom:12px;color:var(--text-secondary)">Up next</h3>
            <div style="display:flex;flex-direction:column;gap:8px">
              <div
                v-for="(ex, i) in exercises"
                :key="ex.id"
                style="display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:8px;transition:all 0.2s"
                :style="{
                  background: i === currentExIndex ? 'var(--neon-dim)' : 'var(--surface-2)',
                  borderLeft: i === currentExIndex ? '3px solid var(--neon)' : '3px solid transparent',
                  opacity: i < currentExIndex ? 0.45 : 1,
                }"
              >
                <Icon
                  :name="i < currentExIndex ? 'check-circle' : i === currentExIndex ? 'play-circle' : 'ellipsis-horizontal-circle'"
                  :size="16"
                  :style="{ color: i < currentExIndex ? 'var(--neon)' : i === currentExIndex ? 'var(--neon)' : 'var(--text-muted)' }"
                />
                <div style="flex:1;min-width:0">
                  <div style="font-size:13px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis"
                       :style="{ color: i === currentExIndex ? 'var(--text-primary)' : 'var(--text-secondary)' }">
                    {{ ex.exercise_detail?.name || 'Exercise' }}
                  </div>
                  <div style="font-size:11px;color:var(--text-muted)">
                    {{ ex.sets }} × {{ ex.reps }} · Day {{ ex.day }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Logged sets this session -->
          <div v-if="loggedSets.length" class="card" v-scroll-animate="{ delay: 120 }">
            <h3 style="font-size:14px;font-weight:700;margin-bottom:12px;color:var(--text-secondary)">Logged this session</h3>
            <div style="display:flex;flex-direction:column;gap:6px;max-height:240px;overflow-y:auto">
              <div
                v-for="(ls, i) in [...loggedSets].reverse()"
                :key="i"
                style="display:flex;align-items:center;justify-content:space-between;padding:8px 10px;border-radius:8px;background:var(--surface-2);font-size:12px"
              >
                <span style="font-weight:600;color:var(--text-primary)">{{ ls.exerciseName }}</span>
                <span style="color:var(--text-muted)">
                  Set {{ ls.set }} · {{ ls.reps }} reps
                  <span v-if="ls.weight"> @ {{ ls.weight }} kg</span>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- Summary modal -->
    <div v-if="showSummary" class="modal-overlay">
      <div class="modal" style="max-width:480px;text-align:center;padding:36px 28px">
        <div style="font-size:48px;margin-bottom:12px">🎯</div>
        <h2 style="font-family:var(--font-display);font-size:24px;font-weight:800;margin-bottom:8px">Session Complete!</h2>
        <p style="color:var(--text-secondary);margin-bottom:24px">
          {{ plan?.title || 'Free Workout' }} · {{ formatted }}
        </p>

        <div class="grid-3" style="gap:12px;margin-bottom:28px">
          <div class="stat-card accent-neon">
            <div class="stat-value neon">{{ loggedSets.length }}</div>
            <div class="stat-label">Sets logged</div>
          </div>
          <div class="stat-card accent-orange">
            <div class="stat-value orange">{{ exercises.length }}</div>
            <div class="stat-label">Exercises</div>
          </div>
          <div class="stat-card accent-blue">
            <div class="stat-value blue">{{ formatted }}</div>
            <div class="stat-label">Duration</div>
          </div>
        </div>

        <button class="btn btn-primary btn-full btn-lg" @click="goToHistory">
          <Icon name="check" :size="18" /> Done
        </button>
      </div>
    </div>
  </div>
</template>
