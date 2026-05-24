<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../../stores/auth'

const auth = useAuthStore()
const username = ref('')
const email = ref('')
const password = ref('')
const passwordConfirm = ref('')
const error = ref('')

const submit = async () => {
  error.value = ''
  if (password.value !== passwordConfirm.value) {
    error.value = 'Passwords do not match.'
    return
  }
  try {
    await auth.register({
      username: username.value,
      email: email.value,
      password: password.value,
      password_confirm: passwordConfirm.value,
    })
  } catch (err) {
    error.value = 'Registration failed. Check your input.'
  }
}
</script>

<template>
  <div>
    <h1 class="text-2xl font-semibold text-slate-900">Create account</h1>
    <p class="mt-2 text-sm text-slate-500">Start tracking your workouts</p>

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
        <label class="text-sm text-slate-600">Email</label>
        <input
          v-model="email"
          type="email"
          class="mt-1 w-full rounded-lg border border-slate-200 px-3 py-2"
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
      <div>
        <label class="text-sm text-slate-600">Confirm password</label>
        <input
          v-model="passwordConfirm"
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
        Create account
      </button>
    </form>

    <div class="mt-4 text-sm text-slate-500">
      <RouterLink to="/login">Already have an account?</RouterLink>
    </div>
  </div>
</template>
