<script setup>
import { computed, onMounted, ref } from 'vue'
import { useAuthStore } from '../../stores/auth'
import { AuthService } from '../../services/auth.service'

const auth = useAuthStore()
const loading = ref(true)
const saving = ref(false)
const error = ref('')
const success = ref('')
const form = ref({ current_password: '', new_password: '', confirm_password: '' })

const user = computed(() => auth.user || {})

const fullName = computed(() => {
  const name = [user.value.first_name, user.value.last_name].filter(Boolean).join(' ')
  return name || '—'
})

const profileInitial = computed(() => {
  const seed = user.value.first_name || user.value.username || ''
  return seed ? seed.charAt(0).toUpperCase() : '?'
})

const formatDate = (dt) =>
  dt ? new Date(dt).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : '—'

const fitnessGoalLabel = computed(() => {
  const map = {
    lose_weight: 'Lose weight',
    build_muscle: 'Build muscle',
    maintain: 'Maintain',
    strength: 'Strength',
    cardio: 'Cardio',
  }
  return map[user.value.fitness_goal] || '—'
})

const parseError = (err) => {
  const data = err?.response?.data
  if (!data) return 'Unable to update password.'
  if (typeof data.detail === 'string') return data.detail
  if (typeof data === 'string') return data
  if (typeof data === 'object') {
    const firstKey = Object.keys(data)[0]
    const value = data[firstKey]
    if (Array.isArray(value)) return value[0]
    if (typeof value === 'string') return value
  }
  return 'Unable to update password.'
}

const changePassword = async () => {
  error.value = ''
  success.value = ''
  if (!form.value.current_password || !form.value.new_password || !form.value.confirm_password) {
    error.value = 'Please fill out all password fields.'
    return
  }
  if (form.value.new_password !== form.value.confirm_password) {
    error.value = 'New passwords do not match.'
    return
  }
  saving.value = true
  try {
    await AuthService.changePassword({
      old_password: form.value.current_password,
      new_password: form.value.new_password,
    })
    success.value = 'Password updated successfully.'
    form.value = { current_password: '', new_password: '', confirm_password: '' }
  } catch (err) {
    error.value = parseError(err)
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  try {
    await auth.fetchProfile()
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="page">
    <div class="page-header">
      <h1 class="page-title">Profile</h1>
      <p class="page-subtitle">Manage your personal and account details</p>
    </div>

    <template v-if="loading">
      <div class="card" style="margin-bottom:16px">
        <div class="skeleton" style="height:76px;border-radius:14px"></div>
      </div>
      <div class="grid-2">
        <div class="card"><div class="skeleton" style="height:200px;border-radius:12px"></div></div>
        <div class="card"><div class="skeleton" style="height:200px;border-radius:12px"></div></div>
      </div>
    </template>

    <template v-else>
      <div class="card" v-scroll-animate>
        <div class="profile-header">
          <div class="profile-avatar">
            <img v-if="user.profile_picture" :src="user.profile_picture" alt="Profile picture" />
            <span v-else>{{ profileInitial }}</span>
          </div>
          <div style="flex:1;min-width:0">
            <div style="font-size:20px;font-weight:800;font-family:var(--font-display);color:var(--text-primary)">
              {{ fullName }}
            </div>
            <div style="font-size:13px;color:var(--text-secondary);margin-top:4px">
              {{ user.email || '—' }}
            </div>
          </div>
          <span class="badge badge-neon" style="text-transform:capitalize">{{ user.role || 'user' }}</span>
        </div>
      </div>

      <div class="grid-2 mt-6">
        <div class="card" v-scroll-animate="{ delay: 60 }">
          <h3 style="font-size:15px;font-weight:700;margin-bottom:16px">Personal info</h3>
          <div class="info-grid">
            <div class="info-row">
              <span class="info-label">Full name</span>
              <span class="info-value">{{ fullName }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Age</span>
              <span class="info-value">{{ user.age ? `${user.age} yrs` : '—' }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Height</span>
              <span class="info-value">{{ user.height_cm ? `${user.height_cm} cm` : '—' }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Weight</span>
              <span class="info-value">{{ user.weight_kg ? `${user.weight_kg} kg` : '—' }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Fitness goal</span>
              <span class="info-value">{{ fitnessGoalLabel }}</span>
            </div>
          </div>
        </div>

        <div class="card" v-scroll-animate="{ delay: 120 }">
          <h3 style="font-size:15px;font-weight:700;margin-bottom:16px">Account info</h3>
          <div class="info-grid">
            <div class="info-row">
              <span class="info-label">Username</span>
              <span class="info-value">{{ user.username || '—' }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Email</span>
              <span class="info-value">{{ user.email || '—' }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Role</span>
              <span class="info-value" style="text-transform:capitalize">{{ user.role || 'user' }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Member since</span>
              <span class="info-value">{{ formatDate(user.created_at) }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Last updated</span>
              <span class="info-value">{{ formatDate(user.updated_at) }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="card mt-6" v-scroll-animate="{ delay: 180 }">
        <div style="display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:16px">
          <div>
            <h3 style="font-size:15px;font-weight:700">Change password</h3>
            <p style="font-size:12px;color:var(--text-secondary);margin-top:4px">
              Use a strong password with at least 8 characters.
            </p>
          </div>
        </div>

        <form @submit.prevent="changePassword" style="display:flex;flex-direction:column;gap:12px;max-width:420px">
          <div class="form-group">
            <label class="form-label">Current password</label>
            <input v-model="form.current_password" type="password" class="form-input" placeholder="••••••••" />
          </div>
          <div class="form-group">
            <label class="form-label">New password</label>
            <input v-model="form.new_password" type="password" class="form-input" placeholder="••••••••" />
          </div>
          <div class="form-group">
            <label class="form-label">Confirm new password</label>
            <input v-model="form.confirm_password" type="password" class="form-input" placeholder="••••••••" />
          </div>

          <div v-if="error" style="background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.2);border-radius:8px;padding:10px 14px;font-size:13px;color:#f87171">
            {{ error }}
          </div>
          <div v-if="success" style="background:rgba(52,211,153,0.12);border:1px solid rgba(52,211,153,0.2);border-radius:8px;padding:10px 14px;font-size:13px;color:#34d399">
            {{ success }}
          </div>

          <button type="submit" class="btn btn-primary" :disabled="saving">
            {{ saving ? 'Updating…' : 'Update password' }}
          </button>
        </form>
      </div>
    </template>
  </div>
</template>
