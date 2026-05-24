<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import AppLayout from './layouts/AppLayout.vue'
import AuthLayout from './layouts/AuthLayout.vue'
import BlankLayout from './layouts/BlankLayout.vue'
import { useUIStore } from './stores/ui'

const route = useRoute()
const ui = useUIStore()

const layouts = {
  app: AppLayout,
  auth: AuthLayout,
  blank: BlankLayout,
}

const layoutComponent = computed(() => layouts[route.meta.layout] || AppLayout)

onMounted(() => {
  document.documentElement.classList.toggle('dark', ui.darkMode)
})
</script>

<template>
  <component :is="layoutComponent">
    <RouterView />
  </component>
</template>
