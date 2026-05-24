<script setup>
import { ref } from 'vue'
import api from '../../services/api'

const email = ref('')
const statusMessage = ref('')

const submit = async () => {
  statusMessage.value = ''
  await api.post('/auth/password/reset/', { email: email.value })
  statusMessage.value = 'Reset link sent. Check your email.'
}
</script>

<template>
  <div>
    <h1 class="text-2xl font-semibold text-slate-900">Reset password</h1>
    <p class="mt-2 text-sm text-slate-500">We will email you a reset link.</p>

    <form class="mt-6 space-y-4" @submit.prevent="submit">
      <div>
        <label class="text-sm text-slate-600">Email</label>
        <input
          v-model="email"
          type="email"
          class="mt-1 w-full rounded-lg border border-slate-200 px-3 py-2"
          required
        />
      </div>
      <p v-if="statusMessage" class="text-sm text-green-600">{{ statusMessage }}</p>
      <button
        type="submit"
        class="w-full rounded-lg bg-slate-900 px-4 py-2 text-white"
      >
        Send reset link
      </button>
    </form>
  </div>
</template>
