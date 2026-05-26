<script setup>
import Icon from '../../components/ui/Icon.vue'
</script>

<template>
  <div style="min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;background:var(--bg);text-align:center;padding:24px">
    <div style="font-family:var(--font-display);font-size:120px;font-weight:800;letter-spacing:-0.06em;line-height:1;color:var(--surface-3);margin-bottom:24px">404</div>
    <h1 style="font-family:var(--font-display);font-size:28px;font-weight:800;color:var(--text-primary);margin-bottom:8px">Page not found</h1>
    <p style="color:var(--text-secondary);margin-bottom:32px">The page you're looking for doesn't exist.</p>
    <RouterLink to="/dashboard" class="btn btn-primary btn-lg"><Icon name="arrow-left" :size="16" /> Back to Dashboard</RouterLink>
  </div>
</template>
