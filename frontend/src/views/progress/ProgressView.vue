<script setup>
import { onMounted, ref, computed } from 'vue'
import { ProgressService } from '../../services/progress.service'

const entries = ref([])
const loading = ref(true)
const showForm = ref(false)
const submitting = ref(false)
const selectedMetric = ref('weight_kg')

const form = ref({ weight_kg: '', body_fat_percentage: '', chest_cm: '', waist_cm: '', arm_cm: '', leg_cm: '' })

const metrics = [
  { key: 'weight_kg', label: 'Weight', unit: 'kg', color: 'var(--neon)', emoji: '⚖️' },
  { key: 'body_fat_percentage', label: 'Body Fat', unit: '%', color: 'var(--orange)', emoji: '📊' },
  { key: 'waist_cm', label: 'Waist', unit: 'cm', color: 'var(--blue)', emoji: '📏' },
  { key: 'chest_cm', label: 'Chest', unit: 'cm', color: 'var(--purple)', emoji: '💪' },
  { key: 'arm_cm', label: 'Arms', unit: 'cm', color: 'var(--neon)', emoji: '💪' },
  { key: 'leg_cm', label: 'Legs', unit: 'cm', color: 'var(--orange)', emoji: '🦵' },
]

const formatDate = (dt) => dt ? new Date(dt).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : '—'

const latestEntry = computed(() => entries.value[0] || null)
const previousEntry = computed(() => entries.value[1] || null)

const getDelta = (key) => {
  if (!latestEntry.value || !previousEntry.value) return null
  const curr = parseFloat(latestEntry.value[key])
  const prev = parseFloat(previousEntry.value[key])
  if (isNaN(curr) || isNaN(prev)) return null
  return (curr - prev).toFixed(1)
}

const chartPoints = computed(() => {
  const key = selectedMetric.value
  return entries.value
    .filter(e => e[key] != null)
    .slice(0, 10)
    .reverse()
    .map(e => ({ val: parseFloat(e[key]), date: formatDate(e.recorded_at) }))
})

const chartMax = computed(() => Math.max(...chartPoints.value.map(p => p.val)) * 1.05 || 100)
const chartMin = computed(() => Math.min(...chartPoints.value.map(p => p.val)) * 0.95 || 0)

const toY = (val) => {
  const range = chartMax.value - chartMin.value
  if (range === 0) return 50
  return 100 - ((val - chartMin.value) / range * 80 + 10)
}

const svgPath = computed(() => {
  const pts = chartPoints.value
  if (pts.length < 2) return ''
  const step = 100 / (pts.length - 1)
  return pts.map((p, i) => `${i === 0 ? 'M' : 'L'}${(i * step).toFixed(1)},${toY(p.val).toFixed(1)}`).join(' ')
})

onMounted(async () => {
  try {
    const { data } = await ProgressService.list()
    entries.value = Array.isArray(data) ? data : data?.results || []
  } finally { loading.value = false }
})

const addEntry = async () => {
  submitting.value = true
  try {
    const payload = {}
    for (const [k, v] of Object.entries(form.value)) { if (v !== '') payload[k] = parseFloat(v) }
    const { data } = await ProgressService.create(payload)
    entries.value.unshift(data)
    showForm.value = false
    form.value = { weight_kg: '', body_fat_percentage: '', chest_cm: '', waist_cm: '', arm_cm: '', leg_cm: '' }
  } catch { alert('Failed to save entry.') }
  finally { submitting.value = false }
}

const activeMetric = computed(() => metrics.find(m => m.key === selectedMetric.value))
</script>

<template>
  <div class="page">
    <div class="page-header">
      <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px">
        <div>
          <h1 class="page-title">Progress</h1>
          <p class="page-subtitle">Track your body metrics over time</p>
        </div>
        <button class="btn btn-primary" @click="showForm = !showForm">
          {{ showForm ? '✕ Cancel' : '+ Log Entry' }}
        </button>
      </div>
    </div>

    <!-- Log form -->
    <div v-if="showForm" class="card animate-fade-up" style="margin-bottom:24px">
      <h3 style="font-size:15px;font-weight:700;margin-bottom:18px">New Measurement</h3>
      <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:14px">
        <div v-for="m in metrics" :key="m.key" class="form-group">
          <label class="form-label">{{ m.emoji }} {{ m.label }} ({{ m.unit }})</label>
          <input v-model="form[m.key]" type="number" step="0.1" class="form-input" :placeholder="`e.g. ${m.key === 'body_fat_percentage' ? '18' : m.key.includes('cm') ? '80' : '75'}`" />
        </div>
      </div>
      <button class="btn btn-primary" :disabled="submitting" style="margin-top:16px" @click="addEntry">
        {{ submitting ? 'Saving…' : 'Save Entry' }}
      </button>
    </div>

    <!-- Latest stats grid -->
    <div v-if="latestEntry" class="grid-stats animate-fade-up" style="margin-bottom:24px">
      <div v-for="m in metrics" :key="m.key" class="stat-card" :class="m.key === 'weight_kg' ? 'accent-neon' : ''">
        <div class="stat-icon" :class="m.key === 'weight_kg' ? 'neon' : ''" style="font-size:18px">{{ m.emoji }}</div>
        <div style="display:flex;align-items:baseline;gap:6px">
          <div style="font-family:var(--font-display);font-size:26px;font-weight:800;letter-spacing:-0.04em" :style="{ color: m.color }">
            {{ latestEntry[m.key] != null ? latestEntry[m.key] : '—' }}
          </div>
          <span style="font-size:12px;color:var(--text-muted)">{{ m.unit }}</span>
        </div>
        <div class="stat-label">{{ m.label }}</div>
        <!-- Delta from previous -->
        <div v-if="getDelta(m.key) !== null" style="font-size:11px;margin-top:-8px">
          <span :style="{ color: parseFloat(getDelta(m.key)) < 0 ? 'var(--neon)' : 'var(--orange)' }">
            {{ parseFloat(getDelta(m.key)) > 0 ? '+' : '' }}{{ getDelta(m.key) }} {{ m.unit }}
          </span>
          <span style="color:var(--text-muted)"> vs prev</span>
        </div>
      </div>
    </div>

    <!-- Chart -->
    <div class="card animate-fade-up" style="margin-bottom:24px">
      <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:20px">
        <h3 style="font-size:15px;font-weight:700">Trend</h3>
        <div style="display:flex;flex-wrap:wrap;gap:6px">
          <button
            v-for="m in metrics" :key="m.key"
            class="chip" :class="{ active: selectedMetric === m.key }"
            @click="selectedMetric = m.key"
          >{{ m.emoji }} {{ m.label }}</button>
        </div>
      </div>

      <div v-if="chartPoints.length < 2" style="text-align:center;padding:48px;color:var(--text-muted);font-size:14px">
        Need at least 2 entries to show a chart
      </div>
      <div v-else style="position:relative;height:160px">
        <svg viewBox="0 0 100 100" preserveAspectRatio="none" style="width:100%;height:100%;overflow:visible">
          <!-- Grid lines -->
          <line x1="0" y1="10" x2="100" y2="10" stroke="var(--border)" stroke-width="0.5"/>
          <line x1="0" y1="55" x2="100" y2="55" stroke="var(--border)" stroke-width="0.5"/>
          <line x1="0" y1="100" x2="100" y2="100" stroke="var(--border)" stroke-width="0.5"/>
          <!-- Area fill -->
          <path :d="svgPath + ` L100,100 L0,100 Z`" :fill="activeMetric?.color" opacity="0.06"/>
          <!-- Line -->
          <path :d="svgPath" :stroke="activeMetric?.color" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
          <!-- Dots -->
          <circle
            v-for="(pt, i) in chartPoints" :key="i"
            :cx="(i * 100 / (chartPoints.length - 1)).toFixed(1)"
            :cy="toY(pt.val).toFixed(1)"
            r="2" :fill="activeMetric?.color"
          />
        </svg>
        <!-- X labels -->
        <div style="display:flex;justify-content:space-between;margin-top:8px">
          <span v-if="chartPoints[0]" style="font-size:10px;color:var(--text-muted)">{{ chartPoints[0].date }}</span>
          <span v-if="chartPoints[chartPoints.length-1]" style="font-size:10px;color:var(--text-muted)">{{ chartPoints[chartPoints.length-1].date }}</span>
        </div>
      </div>
    </div>

    <!-- Entry history -->
    <div class="card animate-fade-up">
      <h3 style="font-size:15px;font-weight:700;margin-bottom:16px">All Entries</h3>
      <div v-if="loading" style="display:flex;flex-direction:column;gap:8px">
        <div v-for="i in 3" :key="i" class="skeleton" style="height:56px;border-radius:10px"></div>
      </div>
      <div v-else-if="!entries.length" style="text-align:center;padding:32px;color:var(--text-muted)">
        No entries yet. Log your first measurement above.
      </div>
      <div v-else style="display:flex;flex-direction:column;gap:8px">
        <div
          v-for="entry in entries" :key="entry.id"
          style="display:flex;align-items:center;justify-content:space-between;padding:12px 16px;border-radius:10px;background:var(--surface-2);border:1px solid var(--border);flex-wrap:wrap;gap:10px"
        >
          <span style="font-size:13px;color:var(--text-muted)">{{ formatDate(entry.recorded_at) }}</span>
          <div style="display:flex;flex-wrap:wrap;gap:8px">
            <span v-for="m in metrics" :key="m.key" v-if="entry[m.key] != null" class="badge badge-muted">
              {{ m.emoji }} {{ entry[m.key] }} {{ m.unit }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
