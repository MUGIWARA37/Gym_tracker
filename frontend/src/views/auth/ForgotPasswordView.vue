<script setup>
import { ref } from 'vue'
import api from '../../services/api'
import Icon from '../../components/ui/Icon.vue'

const email = ref('')
const sent = ref(false)
const loading = ref(false)
const error = ref('')

const submit = async () => {
  loading.value = true
  error.value = ''
  try {
    await api.post('/auth/password-reset/', { email: email.value })
    sent.value = true
  } catch {
    error.value = 'Failed to send reset email. Please check the address.'
  } finally { loading.value = false }
}
</script>

<template>
  <div class="animate-fade-up">
    <div class="auth-title">Reset Password</div>
    <div class="auth-sub">We'll send a reset link to your email</div>

    <div v-if="sent" style="background:rgba(200,247,82,0.1);border:1px solid rgba(200,247,82,0.2);border-radius:10px;padding:16px;font-size:14px;color:var(--neon);margin-bottom:20px;display:flex;align-items:center;gap:10px">
      <Icon name="check-circle" :size="18" />
      Reset link sent! Check your inbox.
    </div>

    <form v-else @submit.prevent="submit" style="display:flex;flex-direction:column;gap:16px">
      <div class="form-group">
        <label class="form-label">Email address</label>
        <input v-model="email" type="email" class="form-input" placeholder="you@example.com" required />
      </div>
      <div v-if="error" style="font-size:13px;color:#f87171">{{ error }}</div>
      <button type="submit" class="btn btn-primary btn-lg btn-full" :disabled="loading">
        {{ loading ? 'Sending…' : 'Send Reset Link' }}
      </button>
    </form>

    <div style="margin-top:20px;text-align:center;font-size:13px">
      <RouterLink to="/login" style="color:var(--neon);text-decoration:none;font-weight:600;display:inline-flex;align-items:center;gap:8px">
        <Icon name="arrow-left" :size="14" />
        Back to sign in
      </RouterLink>
    </div>
  </div>
</template>
