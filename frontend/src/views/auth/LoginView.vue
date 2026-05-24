<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const auth = useAuthStore()
const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')

const submit = async () => {
  error.value = ''
  try {
    await auth.login({ username: username.value, password: password.value })
    await auth.fetchProfile()
    router.push('/dashboard')
  } catch (err) {
    error.value = 'Login failed. Check your credentials.'
  }
}
</script>

<template>
  <div>
    <h1 class="text-2xl font-semibold text-slate-900">Welcome back</h1>
    <p class="mt-2 text-sm text-slate-500">Sign in to continue</p>

    <form class="mt-6 space-y-4" @submit.prevent="submit">
      <div>
        <label class="text-sm text-slate-600">Username</label>
        <input
          v-model="username"
          type="text"
          class="mt-1 w-full rounded-lg border border-slate-200 px-3 py-2"
          required
        />
      </div>
      <div>
        <label class="text-sm text-slate-600">Password</label>
        <input
          v-model="password"
          type="password"
          class="mt-1 w-full rounded-lg border border-slate-200 px-3 py-2"
          required
        />
      </div>
      <p v-if="error" class="text-sm text-red-500">{{ error }}</p>
      <button
        type="submit"
        class="w-full rounded-lg bg-slate-900 px-4 py-2 text-white"
      >
        Sign in
      </button>
    </form>

    <div class="mt-4 flex items-center justify-between text-sm text-slate-500">
      <RouterLink to="/forgot-password">Forgot password?</RouterLink>
      <RouterLink to="/register">Create account</RouterLink>
    </div>
  </div>
</template>
