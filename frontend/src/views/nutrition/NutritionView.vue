<script setup>
import { onMounted, ref, computed } from 'vue'
import { NutritionService } from '../../services/nutrition.service'

const goal = ref(null)
const loading = ref(true)
const editing = ref(false)
const submitting = ref(false)

const form = ref({ calories_target: 2000, protein_g: 150, carbs_g: 200, fats_g: 65, water_ml: 2500 })

onMounted(async () => {
  try {
    const { data } = await NutritionService.get()
    goal.value = data
    if (data) Object.assign(form.value, data)
  } catch {
    // no goal yet
  } finally { loading.value = false }
})

const saveGoal = async () => {
  submitting.value = true
  try {
    const { data } = goal.value
      ? await NutritionService.update(form.value)
      : await NutritionService.create(form.value)
    goal.value = data
    editing.value = false
  } catch { alert('Failed to save nutrition goal.') }
  finally { submitting.value = false }
}

const totalCalFromMacros = computed(() => {
  const g = goal.value || form.value
  return (parseFloat(g.protein_g) * 4 + parseFloat(g.carbs_g) * 4 + parseFloat(g.fats_g) * 9)
})

const macros = computed(() => {
  const g = goal.value || form.value
  const total = totalCalFromMacros.value
  return [
    { label: 'Protein', val: g.protein_g, unit: 'g', cal: parseFloat(g.protein_g) * 4, pct: Math.round(parseFloat(g.protein_g) * 4 / total * 100), color: '#5b8dff', fill: 'var(--blue)' },
    { label: 'Carbs', val: g.carbs_g, unit: 'g', cal: parseFloat(g.carbs_g) * 4, pct: Math.round(parseFloat(g.carbs_g) * 4 / total * 100), color: '#c8f752', fill: 'var(--neon)' },
    { label: 'Fats', val: g.fats_g, unit: 'g', cal: parseFloat(g.fats_g) * 9, pct: Math.round(parseFloat(g.fats_g) * 9 / total * 100), color: '#ff6b35', fill: 'var(--orange)' },
  ]
})

// Donut chart
const donutSegments = computed(() => {
  const r = 40
  const total = macros.value.reduce((s, m) => s + m.pct, 0) || 100
  let offset = 0
  return macros.value.map(m => {
    const pct = m.pct / total
    const dashArray = `${pct * 2 * Math.PI * r} ${(1 - pct) * 2 * Math.PI * r}`
    const result = { ...m, dashArray, dashOffset: -offset * 2 * Math.PI * r }
    offset += pct
    return result
  })
})
</script>

<template>
  <div class="page">
    <div class="page-header">
      <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px">
        <div>
          <h1 class="page-title">Nutrition</h1>
          <p class="page-subtitle">Manage your daily macro targets</p>
        </div>
        <button class="btn btn-primary" @click="editing = !editing">
          {{ editing ? '✕ Cancel' : (goal ? '✎ Edit Goals' : '+ Set Goals') }}
        </button>
      </div>
    </div>

    <div v-if="loading" style="display:grid;gap:16px;grid-template-columns:repeat(auto-fill,minmax(180px,1fr))">
      <div v-for="i in 5" :key="i" class="card">
        <div class="skeleton" style="height:48px;width:80%"></div>
        <div class="skeleton" style="height:14px;width:60%;margin-top:8px"></div>
      </div>
    </div>

    <!-- Edit Form -->
    <div v-else-if="editing" class="card" style="margin-bottom:24px" v-scroll-animate>
      <h3 style="font-size:15px;font-weight:700;margin-bottom:18px">{{ goal ? 'Edit' : 'Set' }} Daily Goals</h3>
      <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:14px">
        <div class="form-group">
          <label class="form-label">🔥 Calories (kcal)</label>
          <input v-model.number="form.calories_target" type="number" class="form-input" min="1000" max="6000" />
        </div>
        <div class="form-group">
          <label class="form-label">🥩 Protein (g)</label>
          <input v-model.number="form.protein_g" type="number" class="form-input" min="0" />
        </div>
        <div class="form-group">
          <label class="form-label">🌾 Carbs (g)</label>
          <input v-model.number="form.carbs_g" type="number" class="form-input" min="0" />
        </div>
        <div class="form-group">
          <label class="form-label">🥑 Fats (g)</label>
          <input v-model.number="form.fats_g" type="number" class="form-input" min="0" />
        </div>
        <div class="form-group">
          <label class="form-label">💧 Water (ml)</label>
          <input v-model.number="form.water_ml" type="number" class="form-input" min="0" />
        </div>
      </div>
      <button class="btn btn-primary" :disabled="submitting" style="margin-top:16px" @click="saveGoal">
        {{ submitting ? 'Saving…' : 'Save Goals' }}
      </button>
    </div>

    <!-- No goal yet -->
    <div v-else-if="!goal" style="text-align:center;padding:64px 24px;color:var(--text-muted)">
      <div style="font-size:48px;margin-bottom:16px">🥗</div>
      <div style="font-size:18px;font-weight:700;color:var(--text-primary);margin-bottom:8px">No nutrition goals set</div>
      <p style="margin-bottom:20px">Set your daily calorie and macro targets to track your nutrition.</p>
      <button class="btn btn-primary" @click="editing = true">Set Goals →</button>
    </div>

    <!-- Display goals -->
    <template v-else>
      <!-- Calorie overview -->
      <div class="grid-2" style="gap:20px;margin-bottom:20px;align-items:start">
        <!-- Donut chart -->
        <div class="card" style="display:flex;align-items:center;gap:24px" v-scroll-animate>
          <svg width="120" height="120" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="40" fill="none" stroke="var(--surface-3)" stroke-width="12"/>
            <circle
              v-for="seg in donutSegments" :key="seg.label"
              cx="50" cy="50" r="40"
              fill="none" :stroke="seg.color" stroke-width="12"
              :stroke-dasharray="seg.dashArray"
              :stroke-dashoffset="seg.dashOffset"
              style="transform:rotate(-90deg);transform-origin:center;transition:all 0.5s"
            />
            <text x="50" y="44" text-anchor="middle" font-family="var(--font-display)" font-size="14" font-weight="800" fill="var(--text-primary)">{{ goal.calories_target }}</text>
            <text x="50" y="58" text-anchor="middle" font-family="var(--font-body)" font-size="7" fill="var(--text-muted)">kcal / day</text>
          </svg>
          <div style="flex:1;display:flex;flex-direction:column;gap:10px">
            <div v-for="m in macros" :key="m.label">
              <div style="display:flex;justify-content:space-between;margin-bottom:4px;font-size:12px">
                <span style="color:var(--text-secondary);font-weight:600">{{ m.label }}</span>
                <span :style="{ color: m.color, fontWeight: 700 }">{{ m.val }}g</span>
              </div>
              <div class="macro-bar">
                <div class="macro-fill" :style="{ width: m.pct + '%', background: m.color }"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Macro cards -->
        <div style="display:flex;flex-direction:column;gap:12px" v-scroll-animate="{ delay: 120 }">
          <div v-for="(m, i) in macros" :key="m.label" class="card card-sm" style="display:flex;align-items:center;gap:14px" v-scroll-animate="{ delay: i * 60 }">
            <div style="width:40px;height:40px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0" :style="{ background: m.color + '20' }">
              {{ m.label === 'Protein' ? '🥩' : m.label === 'Carbs' ? '🌾' : '🥑' }}
            </div>
            <div style="flex:1">
              <div style="font-size:18px;font-weight:800;font-family:var(--font-display)" :style="{ color: m.color }">{{ m.val }}<span style="font-size:13px">g</span></div>
              <div style="font-size:12px;color:var(--text-muted)">{{ m.label }} · {{ m.cal }} kcal · {{ m.pct }}%</div>
            </div>
          </div>
          <div class="card card-sm" style="display:flex;align-items:center;gap:14px">
            <div style="width:40px;height:40px;border-radius:10px;background:var(--blue-dim);display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0">💧</div>
            <div>
              <div style="font-size:18px;font-weight:800;font-family:var(--font-display);color:var(--blue)">{{ (goal.water_ml / 1000).toFixed(1) }}<span style="font-size:13px">L</span></div>
              <div style="font-size:12px;color:var(--text-muted)">Daily water target</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Tips -->
      <div class="card" v-scroll-animate="{ delay: 180 }">
        <h3 style="font-size:15px;font-weight:700;margin-bottom:14px">💡 Nutrition Tips</h3>
        <div style="display:grid;gap:10px">
          <div style="padding:12px;border-radius:8px;background:var(--surface-2);font-size:13px;color:var(--text-secondary);border-left:3px solid var(--blue)">
            <strong style="color:var(--text-primary)">Protein timing:</strong> Aim for 20–40g protein within 30 minutes post-workout to maximize muscle protein synthesis.
          </div>
          <div style="padding:12px;border-radius:8px;background:var(--surface-2);font-size:13px;color:var(--text-secondary);border-left:3px solid var(--neon)">
            <strong style="color:var(--text-primary)">Hydration:</strong> Drink 500ml of water before training. Dehydration reduces performance by up to 10%.
          </div>
          <div style="padding:12px;border-radius:8px;background:var(--surface-2);font-size:13px;color:var(--text-secondary);border-left:3px solid var(--orange)">
            <strong style="color:var(--text-primary)">Calorie surplus:</strong> For muscle gain, aim for a 200–400 kcal surplus above your TDEE.
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
