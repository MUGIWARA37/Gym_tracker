<script setup>
import { onMounted, ref, computed, watch } from 'vue'
import { ProgressService } from '../../services/progress.service'
import { useFileUpload } from '../../composables/useFileUpload'
import Icon from '../../components/ui/Icon.vue'

/* ── State ── */
const entries   = ref([])
const loading   = ref(true)
const showForm  = ref(false)
const submitting= ref(false)
const formError = ref('')
const selectedMetric = ref('weight_kg')

const form = ref({
  weight_kg: '',
  body_fat_percentage: '',
  chest_cm: '',
  waist_cm: '',
  arm_cm: '',
  leg_cm: '',
})

const { file, preview, error: uploadError, pick, clear: clearFile, toFormData } = useFileUpload()

/* ── Metrics config ── */
const metrics = [
  { key: 'weight_kg',           label: 'Weight',    unit: 'kg',  color: '#c8f752', icon: 'scale' },
  { key: 'body_fat_percentage', label: 'Body Fat',  unit: '%',   color: '#5b8dff', icon: 'beaker' },
  { key: 'chest_cm',            label: 'Chest',     unit: 'cm',  color: '#ff6b35', icon: 'heart' },
  { key: 'waist_cm',            label: 'Waist',     unit: 'cm',  color: '#a855f7', icon: 'minus' },
  { key: 'arm_cm',              label: 'Arms',      unit: 'cm',  color: '#34d399', icon: 'dumbbell' },
  { key: 'leg_cm',              label: 'Legs',      unit: 'cm',  color: '#f59e0b', icon: 'bolt' },
]
const metricMap = Object.fromEntries(metrics.map(m => [m.key, m]))

/* ── Chart data ── */
const chartData = computed(() => {
  const m = selectedMetric.value
  const sorted = [...entries.value]
    .filter(e => e[m] != null)
    .sort((a, b) => new Date(a.recorded_at) - new Date(b.recorded_at))
  return sorted.map(e => ({
    date: new Date(e.recorded_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    value: parseFloat(e[m]),
  }))
})

const chartMeta = computed(() => metricMap[selectedMetric.value] || metrics[0])

const chartMin = computed(() => {
  if (!chartData.value.length) return 0
  const min = Math.min(...chartData.value.map(d => d.value))
  return Math.max(0, min * 0.95)
})
const chartMax = computed(() => {
  if (!chartData.value.length) return 100
  const max = Math.max(...chartData.value.map(d => d.value))
  return max * 1.05
})

/* Polyline points for SVG chart (600×180 viewport) */
const svgPoints = computed(() => {
  const data = chartData.value
  if (data.length < 2) return ''
  const W = 600, H = 180, pad = { t: 12, b: 28, l: 40, r: 16 }
  const iW = W - pad.l - pad.r
  const iH = H - pad.t - pad.b
  const range = chartMax.value - chartMin.value || 1
  return data.map((d, i) => {
    const x = pad.l + (i / (data.length - 1)) * iW
    const y = pad.t + iH - ((d.value - chartMin.value) / range) * iH
    return `${x},${y}`
  }).join(' ')
})

const svgDots = computed(() => {
  const data = chartData.value
  if (!data.length) return []
  const W = 600, H = 180, pad = { t: 12, b: 28, l: 40, r: 16 }
  const iW = W - pad.l - pad.r
  const iH = H - pad.t - pad.b
  const range = chartMax.value - chartMin.value || 1
  return data.map((d, i) => ({
    x: pad.l + (i / Math.max(data.length - 1, 1)) * iW,
    y: pad.t + iH - ((d.value - chartMin.value) / range) * iH,
    value: d.value,
    date: d.date,
  }))
})

/* Y-axis labels */
const yLabels = computed(() => {
  const steps = 4
  const range = chartMax.value - chartMin.value || 1
  const H = 180, pad = { t: 12, b: 28 }
  const iH = H - pad.t - pad.b
  return Array.from({ length: steps + 1 }, (_, i) => {
    const frac = i / steps
    const val = chartMin.value + range * frac
    const y = pad.t + iH * (1 - frac)
    return { y, label: val.toFixed(1) }
  })
})

/* ── Latest values ── */
const latest = computed(() => {
  if (!entries.value.length) return {}
  const sorted = [...entries.value].sort((a, b) => new Date(b.recorded_at) - new Date(a.recorded_at))
  return sorted[0]
})

/* ── Delta vs previous ── */
const delta = computed(() => {
  const sorted = [...entries.value].sort((a, b) => new Date(b.recorded_at) - new Date(a.recorded_at))
  if (sorted.length < 2) return null
  const curr = parseFloat(sorted[0][selectedMetric.value])
  const prev = parseFloat(sorted[1][selectedMetric.value])
  if (isNaN(curr) || isNaN(prev)) return null
  return (curr - prev).toFixed(1)
})

/* ── CRUD ── */
const fetchEntries = async () => {
  loading.value = true
  try {
    const { data } = await ProgressService.list()
    entries.value = Array.isArray(data) ? data : data?.results || []
  } finally { loading.value = false }
}

const submitEntry = async () => {
  submitting.value = true
  formError.value = ''
  try {
    const fd = toFormData(
      Object.fromEntries(
        Object.entries(form.value).filter(([, v]) => v !== '' && v !== null)
      )
    )
    const { data } = await ProgressService.create(fd)
    entries.value.unshift(data)
    showForm.value = false
    clearFile()
    form.value = { weight_kg: '', body_fat_percentage: '', chest_cm: '', waist_cm: '', arm_cm: '', leg_cm: '' }
  } catch { formError.value = 'Failed to save entry.' }
  finally { submitting.value = false }
}

const deleteEntry = async (entry) => {
  if (!confirm('Delete this progress entry?')) return
  try {
    await ProgressService.delete(entry.id)
    entries.value = entries.value.filter(e => e.id !== entry.id)
  } catch { alert('Failed to delete.') }
}

const formatDate = (dt) => dt
  ? new Date(dt).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
  : '—'

onMounted(fetchEntries)
</script>

<template>
  <div class="page">
    <!-- Header -->
    <div class="page-header">
      <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px">
        <div>
          <h1 class="page-title">Progress</h1>
          <p class="page-subtitle">Track your body measurements over time</p>
        </div>
        <button class="btn btn-primary" @click="showForm = !showForm">
          <Icon :name="showForm ? 'x-mark' : 'plus'" :size="16" />
          {{ showForm ? 'Cancel' : 'Log Entry' }}
        </button>
      </div>
    </div>

    <!-- Add Entry Form -->
    <div v-if="showForm" class="card" style="margin-bottom:24px" v-scroll-animate>
      <h3 style="font-size:15px;font-weight:700;margin-bottom:18px">New Progress Entry</h3>
      <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:14px">
        <div class="form-group">
          <label class="form-label">Weight (kg)</label>
          <input v-model.number="form.weight_kg" type="number" step="0.1" class="form-input" placeholder="e.g. 75.5" />
        </div>
        <div class="form-group">
          <label class="form-label">Body Fat %</label>
          <input v-model.number="form.body_fat_percentage" type="number" step="0.1" class="form-input" placeholder="e.g. 18.5" />
        </div>
        <div class="form-group">
          <label class="form-label">Chest (cm)</label>
          <input v-model.number="form.chest_cm" type="number" step="0.1" class="form-input" placeholder="e.g. 100" />
        </div>
        <div class="form-group">
          <label class="form-label">Waist (cm)</label>
          <input v-model.number="form.waist_cm" type="number" step="0.1" class="form-input" placeholder="e.g. 80" />
        </div>
        <div class="form-group">
          <label class="form-label">Arms (cm)</label>
          <input v-model.number="form.arm_cm" type="number" step="0.1" class="form-input" placeholder="e.g. 35" />
        </div>
        <div class="form-group">
          <label class="form-label">Legs (cm)</label>
          <input v-model.number="form.leg_cm" type="number" step="0.1" class="form-input" placeholder="e.g. 55" />
        </div>
      </div>

      <!-- Photo upload -->
      <div class="form-group" style="margin-top:14px">
        <label class="form-label">Progress photo (optional)</label>
        <div
          style="border:1px dashed var(--border-strong);border-radius:10px;padding:20px;text-align:center;cursor:pointer;transition:border-color 0.2s"
          @click="$refs.photoInput.click()"
        >
          <img v-if="preview" :src="preview" style="max-height:160px;max-width:100%;border-radius:8px;object-fit:cover" />
          <div v-else style="color:var(--text-muted);font-size:13px">
            <Icon name="camera" :size="28" style="display:block;margin:0 auto 8px" />
            Click to select photo (JPG, PNG, WEBP — max 5 MB)
          </div>
        </div>
        <input ref="photoInput" type="file" accept="image/jpeg,image/png,image/webp" style="display:none" @change="pick" />
        <div v-if="uploadError" style="font-size:12px;color:#f87171;margin-top:6px">{{ uploadError }}</div>
      </div>

      <div v-if="formError" style="font-size:13px;color:#f87171;margin-top:8px">{{ formError }}</div>
      <button class="btn btn-primary" style="margin-top:14px" :disabled="submitting" @click="submitEntry">
        {{ submitting ? 'Saving…' : 'Save Entry' }}
      </button>
    </div>

    <!-- Loading -->
    <template v-if="loading">
      <div class="card" style="margin-bottom:20px">
        <div class="skeleton" style="height:200px;border-radius:10px"></div>
      </div>
    </template>

    <template v-else-if="!entries.length">
      <div style="text-align:center;padding:64px 24px;color:var(--text-muted)">
        <div style="display:flex;justify-content:center;margin-bottom:16px;color:var(--text-secondary)">
          <Icon name="chart-bar-square" :size="46" />
        </div>
        <div style="font-size:18px;font-weight:700;color:var(--text-primary);margin-bottom:8px">No progress entries yet</div>
        <p style="margin-bottom:20px">Start logging your measurements to track your body composition over time.</p>
        <button class="btn btn-primary" @click="showForm = true">Log First Entry <Icon name="arrow-right" :size="14" /></button>
      </div>
    </template>

    <template v-else>
      <!-- Latest snapshot cards -->
      <div class="grid-stats" style="margin-bottom:24px" v-scroll-animate>
        <div
          v-for="m in metrics"
          :key="m.key"
          class="stat-card"
          :class="{ 'selected-metric': selectedMetric === m.key }"
          style="cursor:pointer;transition:all 0.2s"
          :style="selectedMetric === m.key ? { borderColor: m.color, boxShadow: `0 0 0 1px ${m.color}40` } : {}"
          @click="selectedMetric = m.key"
        >
          <div class="stat-icon" :style="{ background: m.color + '20', color: m.color }">
            <Icon :name="m.icon" :size="18" />
          </div>
          <div class="stat-value" :style="{ color: selectedMetric === m.key ? m.color : 'var(--text-primary)' }">
            {{ latest[m.key] != null ? parseFloat(latest[m.key]).toFixed(1) : '—' }}
            <span style="font-size:14px;opacity:0.6">{{ m.unit }}</span>
          </div>
          <div class="stat-label">{{ m.label }}</div>
        </div>
      </div>

      <!-- Chart card -->
      <div class="card" style="margin-bottom:24px" v-scroll-animate="{ delay: 60 }">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;flex-wrap:wrap;gap:10px">
          <div>
            <h3 style="font-size:15px;font-weight:700">
              {{ chartMeta.label }} over time
            </h3>
            <div v-if="delta !== null" style="font-size:12px;margin-top:4px" :style="{ color: parseFloat(delta) < 0 ? '#34d399' : '#f87171' }">
              {{ parseFloat(delta) > 0 ? '+' : '' }}{{ delta }} {{ chartMeta.unit }} vs previous entry
            </div>
          </div>
          <div style="display:flex;flex-wrap:wrap;gap:6px">
            <button
              v-for="m in metrics"
              :key="m.key"
              class="chip"
              :class="{ active: selectedMetric === m.key }"
              style="font-size:11px;padding:4px 10px"
              @click="selectedMetric = m.key"
            >{{ m.label }}</button>
          </div>
        </div>

        <div v-if="chartData.length < 2" style="text-align:center;padding:40px;color:var(--text-muted);font-size:13px">
          Log at least 2 entries with {{ chartMeta.label }} data to see the chart.
        </div>

        <div v-else style="position:relative;overflow-x:auto">
          <svg viewBox="0 0 600 180" style="width:100%;min-width:320px;height:auto;overflow:visible">
            <!-- Grid lines -->
            <line v-for="l in yLabels" :key="l.y" x1="40" :y1="l.y" x2="584" :y2="l.y"
              stroke="var(--border)" stroke-width="1" />

            <!-- Y labels -->
            <text v-for="l in yLabels" :key="'yl'+l.y" x="36" :y="l.y + 4"
              text-anchor="end" font-size="9" fill="var(--text-muted)" font-family="var(--font-body)">
              {{ l.label }}
            </text>

            <!-- Area fill -->
            <defs>
              <linearGradient :id="`grad-${selectedMetric}`" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" :stop-color="chartMeta.color" stop-opacity="0.25" />
                <stop offset="100%" :stop-color="chartMeta.color" stop-opacity="0.02" />
              </linearGradient>
            </defs>
            <polygon
              v-if="svgPoints"
              :points="`40,152 ${svgPoints} 584,152`"
              :fill="`url(#grad-${selectedMetric})`"
            />

            <!-- Line -->
            <polyline
              v-if="svgPoints"
              :points="svgPoints"
              fill="none"
              :stroke="chartMeta.color"
              stroke-width="2"
              stroke-linejoin="round"
              stroke-linecap="round"
            />

            <!-- Dots -->
            <g v-for="(dot, i) in svgDots" :key="i">
              <circle :cx="dot.x" :cy="dot.y" r="5" :fill="chartMeta.color" opacity="0.85" />
              <circle :cx="dot.x" :cy="dot.y" r="2.5" fill="var(--bg)" />
            </g>

            <!-- X labels (show max 6) -->
            <text
              v-for="(d, i) in chartData.filter((_, i, a) => i === 0 || i === a.length-1 || a.length <= 6 || i % Math.ceil(a.length/5) === 0)"
              :key="'xl'+i"
              :x="40 + (chartData.indexOf(d) / Math.max(chartData.length - 1, 1)) * 544"
              y="174"
              text-anchor="middle"
              font-size="9"
              fill="var(--text-muted)"
              font-family="var(--font-body)"
            >{{ d.date }}</text>
          </svg>
        </div>
      </div>

      <!-- Entry history -->
      <div class="card" v-scroll-animate="{ delay: 120 }">
        <h3 style="font-size:15px;font-weight:700;margin-bottom:16px">Entry History</h3>
        <div style="display:flex;flex-direction:column;gap:10px">
          <div
            v-for="entry in [...entries].sort((a,b) => new Date(b.recorded_at) - new Date(a.recorded_at))"
            :key="entry.id"
            style="padding:14px 16px;border-radius:10px;background:var(--surface-2);border:1px solid var(--border)"
          >
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px">
              <div style="font-size:13px;font-weight:600;color:var(--text-primary)">{{ formatDate(entry.recorded_at) }}</div>
              <button class="btn btn-ghost btn-sm" @click="deleteEntry(entry)" style="color:#f87171;padding:2px 8px">
                <Icon name="trash" :size="14" />
              </button>
            </div>

            <!-- Photo -->
            <img v-if="entry.photo" :src="entry.photo" style="width:100%;max-height:200px;object-fit:cover;border-radius:8px;margin-bottom:10px" />

            <div style="display:flex;flex-wrap:wrap;gap:8px">
              <span v-if="entry.weight_kg != null" class="badge badge-neon" style="display:inline-flex;align-items:center;gap:5px">
                <Icon name="scale" :size="12" /> {{ parseFloat(entry.weight_kg).toFixed(1) }} kg
              </span>
              <span v-if="entry.body_fat_percentage != null" class="badge badge-blue" style="display:inline-flex;align-items:center;gap:5px">
                <Icon name="beaker" :size="12" /> {{ parseFloat(entry.body_fat_percentage).toFixed(1) }}% BF
              </span>
              <span v-if="entry.chest_cm != null" class="badge badge-muted">Chest {{ parseFloat(entry.chest_cm).toFixed(1) }} cm</span>
              <span v-if="entry.waist_cm != null" class="badge badge-muted">Waist {{ parseFloat(entry.waist_cm).toFixed(1) }} cm</span>
              <span v-if="entry.arm_cm != null" class="badge badge-muted">Arms {{ parseFloat(entry.arm_cm).toFixed(1) }} cm</span>
              <span v-if="entry.leg_cm != null" class="badge badge-muted">Legs {{ parseFloat(entry.leg_cm).toFixed(1) }} cm</span>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
