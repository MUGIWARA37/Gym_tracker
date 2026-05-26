<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../../stores/auth'

const auth = useAuthStore()
const username = ref('')
const email = ref('')
const password = ref('')
const passwordConfirm = ref('')
const error = ref('')
const loading = ref(false)

const submit = async () => {
  error.value = ''
  if (password.value !== passwordConfirm.value) {
    error.value = 'Passwords do not match.'
    return
  }
  loading.value = true
  try {
    await auth.register({ username: username.value, email: email.value, password: password.value, password_confirm: passwordConfirm.value })
  } catch {
    error.value = 'Registration failed. Please check your details.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="animate-fade-up">
    <div class="auth-title">Create account</div>
    <div class="auth-sub">Start your fitness journey today</div>

    <form @submit.prevent="submit" style="display:flex;flex-direction:column;gap:14px">
      <div class="form-group">
        <label class="form-label">Username</label>
        <input v-model="username" type="text" class="form-input" placeholder="athlete_name" required />
      </div>
      <div class="form-group">
        <label class="form-label">Email</label>
        <input v-model="email" type="email" class="form-input" placeholder="you@example.com" />
      </div>
      <div class="grid-2" style="gap:12px">
        <div class="form-group">
          <label class="form-label">Password</label>
          <input v-model="password" type="password" class="form-input" placeholder="••••••••" required />
        </div>
        <div class="form-group">
          <label class="form-label">Confirm</label>
          <input v-model="passwordConfirm" type="password" class="form-input" placeholder="••••••••" required />
        </div>
      </div>

      <div v-if="error" style="background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.2);border-radius:8px;padding:10px 14px;font-size:13px;color:#f87171">
        {{ error }}
      </div>

      <button type="submit" class="btn btn-primary btn-lg btn-full" :disabled="loading" style="margin-top:4px">
        <span v-if="loading">Creating account…</span>
        <span v-else>Create account →</span>
      </button>
    </form>

    <div style="margin-top:20px;font-size:13px;color:var(--text-secondary);text-align:center">
      Already have an account?
      <RouterLink to="/login" style="color:var(--neon);text-decoration:none;font-weight:600;margin-left:4px">Sign in →</RouterLink>
    </div>
  </div>
</template>
