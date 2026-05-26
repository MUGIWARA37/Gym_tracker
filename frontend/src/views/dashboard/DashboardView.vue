<script setup>
import { onMounted, ref } from 'vue'
import api from '../../services/api'
import Icon from '../../components/ui/Icon.vue'

const stats = ref(null)
const loading = ref(true)
const recentSessions = ref([])

onMounted(async () => {
  try {
    const [statsRes, sessionsRes] = await Promise.allSettled([
      api.get('/dashboard/stats/'),
      api.get('/sessions/?ordering=-start_time&page_size=5'),
    ])
    if (statsRes.status === 'fulfilled') stats.value = statsRes.value.data
    if (sessionsRes.status === 'fulfilled') {
      const d = sessionsRes.value.data
      recentSessions.value = Array.isArray(d) ? d.slice(0, 5) : (d?.results || []).slice(0, 5)
    }
  } finally {
    loading.value = false
  }
})

const formatDate = (dt) => {
  if (!dt) return '—'
  return new Date(dt).toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

const formatDuration = (start, end) => {
  if (!start || !end) return '—'
  const mins = Math.round((new Date(end) - new Date(start)) / 60000)
  if (mins < 60) return `${mins}m`
  return `${Math.floor(mins/60)}h ${mins%60}m`
}

const moodIcon = { motivated: 'fire', tired: 'clock', excellent: 'bolt', average: 'minus' }
</script>

<template>
  <div class="page">
    <!-- Header -->
    <div class="page-header">
      <h1 class="page-title">Dashboard</h1>
      <p class="page-subtitle">Your fitness overview at a glance</p>
    </div>

    <!-- Skeleton loading -->
    <template v-if="loading">
      <div class="grid-stats">
        <div v-for="i in 4" :key="i" class="stat-card">
          <div class="skeleton" style="width:40px;height:40px;border-radius:10px"></div>
          <div class="skeleton" style="width:80px;height:32px;border-radius:6px"></div>
          <div class="skeleton" style="width:120px;height:12px;border-radius:4px"></div>
        </div>
      </div>
    </template>

    <!-- Stats grid -->
    <template v-else>
      <div class="grid-stats">
        <div class="stat-card accent-neon" v-scroll-animate>
          <div class="stat-icon neon"><Icon name="calendar-days" :size="18" /></div>
          <div class="stat-value neon">{{ stats?.weekly_sessions ?? '—' }}</div>
          <div class="stat-label">Weekly Sessions</div>
        </div>
        <div class="stat-card accent-orange" v-scroll-animate="{ delay: 60 }">
          <div class="stat-icon orange"><Icon name="fire" :size="18" /></div>
          <div class="stat-value orange">{{ stats?.weekly_calories_burned ? Math.round(stats.weekly_calories_burned).toLocaleString() : '—' }}</div>
          <div class="stat-label">Calories Burned</div>
        </div>
        <div class="stat-card accent-blue" v-scroll-animate="{ delay: 120 }">
          <div class="stat-icon blue"><Icon name="bolt" :size="18" /></div>
          <div class="stat-value blue">{{ stats?.current_streak_days ?? '—' }}</div>
          <div class="stat-label">Day Streak</div>
        </div>
        <div class="stat-card accent-purple" v-scroll-animate="{ delay: 180 }">
          <div class="stat-icon purple"><Icon name="check-badge" :size="18" /></div>
          <div class="stat-value purple">{{ stats?.goal_completion_percent ?? '—' }}<span style="font-size:18px">%</span></div>
          <div class="stat-label">Goal Completion</div>
        </div>
      </div>

      <!-- Goal progress ring + quick actions -->
      <div class="grid-2 mt-8" style="gap:20px;align-items:start">
        <!-- Progress ring card -->
        <div class="card" v-scroll-animate="{ delay: 120 }">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px">
            <h3 style="font-size:15px;font-weight:700">Weekly Goal</h3>
            <span class="badge badge-neon">{{ stats?.goal_completion_percent ?? 0 }}%</span>
          </div>
          <div style="display:flex;align-items:center;gap:24px">
            <svg width="96" height="96" viewBox="0 0 96 96">
              <circle cx="48" cy="48" r="40" fill="none" stroke="var(--surface-3)" stroke-width="8"/>
              <circle
                cx="48" cy="48" r="40" fill="none"
                stroke="var(--neon)" stroke-width="8"
                stroke-linecap="round"
                class="progress-ring"
                :stroke-dasharray="`${2 * Math.PI * 40}`"
                :stroke-dashoffset="`${2 * Math.PI * 40 * (1 - (stats?.goal_completion_percent ?? 0) / 100)}`"
                style="transition: stroke-dashoffset 0.8s ease"
              />
              <text x="48" y="48" text-anchor="middle" dominant-baseline="central"
                font-family="var(--font-display)" font-size="18" font-weight="800"
                fill="var(--neon)" transform="rotate(90, 48, 48)">
                {{ stats?.goal_completion_percent ?? 0 }}%
              </text>
            </svg>
            <div style="flex:1">
              <div style="font-size:22px;font-weight:800;font-family:var(--font-display);color:var(--text-primary)">
                {{ stats?.weekly_sessions ?? 0 }} / 5
              </div>
              <div style="font-size:13px;color:var(--text-secondary);margin-top:4px">Sessions this week</div>
              <div class="divider"></div>
              <div style="font-size:22px;font-weight:800;font-family:var(--font-display);color:var(--orange);display:flex;align-items:center;gap:6px">
                <span>{{ stats?.current_streak_days ?? 0 }}</span>
                <Icon name="fire" :size="16" />
              </div>
              <div style="font-size:13px;color:var(--text-secondary);margin-top:4px">Day streak</div>
            </div>
          </div>
        </div>

        <!-- Quick links -->
        <div class="card" v-scroll-animate="{ delay: 180 }">
          <h3 style="font-size:15px;font-weight:700;margin-bottom:16px">Quick Actions</h3>
          <div style="display:flex;flex-direction:column;gap:10px">
            <RouterLink to="/sessions" class="btn btn-primary btn-full" style="justify-content:space-between">
              <span style="display:inline-flex;align-items:center;gap:8px"><Icon name="play" :size="16" /> Start Workout</span>
              <span style="font-size:12px;opacity:0.7">Log a session</span>
            </RouterLink>
            <RouterLink to="/exercises" class="btn btn-secondary btn-full" style="justify-content:space-between">
              <span style="display:inline-flex;align-items:center;gap:8px"><Icon name="dumbbell" :size="16" /> Browse Exercises</span>
              <span style="font-size:12px;opacity:0.7">{{ stats?.total_exercises ?? '' }} exercises</span>
            </RouterLink>
            <RouterLink to="/nutrition" class="btn btn-secondary btn-full" style="justify-content:space-between">
              <span style="display:inline-flex;align-items:center;gap:8px"><Icon name="beaker" :size="16" /> Nutrition Goals</span>
              <span style="font-size:12px;opacity:0.7">Macros & calories</span>
            </RouterLink>
          </div>
        </div>
      </div>

      <!-- Recent Sessions -->
      <div class="card mt-8" v-scroll-animate="{ delay: 240 }">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px">
          <h3 style="font-size:15px;font-weight:700">Recent Sessions</h3>
          <RouterLink to="/sessions" class="btn btn-ghost btn-sm">View all <Icon name="arrow-right" :size="14" /></RouterLink>
        </div>

        <div v-if="!recentSessions.length" style="text-align:center;padding:32px;color:var(--text-muted);font-size:14px">
          No sessions yet.
          <RouterLink to="/sessions" style="color:var(--neon);text-decoration:none;display:inline-flex;align-items:center;gap:6px">
            Start your first workout <Icon name="arrow-right" :size="14" />
          </RouterLink>
        </div>

        <div v-else style="display:flex;flex-direction:column;gap:10px">
          <div
            v-for="session in recentSessions"
            :key="session.id"
            style="display:flex;align-items:center;justify-content:space-between;padding:14px 16px;border-radius:10px;background:var(--surface-2);border:1px solid var(--border)"
          >
            <div style="display:flex;align-items:center;gap:12px">
              <span style="display:inline-flex;align-items:center;color:var(--text-secondary)"><Icon :name="moodIcon[session.mood] || 'dumbbell'" :size="18" /></span>
              <div>
                <div style="font-size:13px;font-weight:600;color:var(--text-primary)">{{ session.workout_plan_name || 'Free Session' }}</div>
                <div style="font-size:12px;color:var(--text-muted);margin-top:2px">{{ formatDate(session.start_time) }}</div>
              </div>
            </div>
            <div style="text-align:right">
              <div style="font-size:13px;font-weight:600;color:var(--neon)">{{ formatDuration(session.start_time, session.end_time) }}</div>
              <div style="font-size:12px;color:var(--text-muted);margin-top:2px">{{ session.calories_burned ? Math.round(session.calories_burned) + ' kcal' : '' }}</div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
