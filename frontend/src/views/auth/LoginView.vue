<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import Icon from '../../components/ui/Icon.vue'

const auth = useAuthStore()
const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const submit = async () => {
  error.value = ''
  loading.value = true
  try {
    await auth.login({ username: username.value, password: password.value })
    await auth.fetchProfile()
    router.push('/dashboard')
  } catch {
    error.value = 'Invalid credentials. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="animate-fade-up">
    <div class="auth-title">Welcome back</div>
    <div class="auth-sub">Sign in to your account</div>

    <form @submit.prevent="submit" style="display:flex;flex-direction:column;gap:16px">
      <div class="form-group">
        <label class="form-label">Username</label>
        <input v-model="username" type="text" class="form-input" placeholder="username" required />
      </div>
      <div class="form-group">
        <label class="form-label">Password</label>
        <input v-model="password" type="password" class="form-input" placeholder="••••••••" required />
      </div>

      <div v-if="error" style="background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.2);border-radius:8px;padding:10px 14px;font-size:13px;color:#f87171">
        {{ error }}
      </div>

      <button type="submit" class="btn btn-primary btn-lg btn-full" :disabled="loading" style="margin-top:4px">
        <span v-if="loading">Signing in…</span>
        <span v-else>Sign in <Icon name="arrow-right" :size="14" /></span>
      </button>
    </form>

    <div style="display:flex;align-items:center;justify-content:space-between;margin-top:20px;font-size:13px;color:var(--text-secondary)">
      <RouterLink to="/forgot-password" style="color:var(--text-secondary);text-decoration:none;transition:color 0.15s" @mouseover="$event.target.style.color='var(--neon)'" @mouseleave="$event.target.style.color='var(--text-secondary)'">
        Forgot password?
      </RouterLink>
      <RouterLink to="/register" style="color:var(--neon);text-decoration:none;font-weight:600;display:inline-flex;align-items:center;gap:6px">Create account <Icon name="arrow-right" :size="14" /></RouterLink>
    </div>
  </div>
</template>
