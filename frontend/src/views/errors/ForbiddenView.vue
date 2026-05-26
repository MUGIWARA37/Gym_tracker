<script setup>
import Icon from '../../components/ui/Icon.vue'
</script>

<template>
  <div style="min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;background:var(--bg);text-align:center;padding:24px">
    <div style="margin-bottom:24px;color:#f87171">
      <Icon name="x-mark" :size="56" />
    </div>
    <h1 style="font-family:var(--font-display);font-size:28px;font-weight:800;color:var(--text-primary);margin-bottom:8px">Access Denied</h1>
    <p style="color:var(--text-secondary);margin-bottom:32px">You don't have permission to view this page.</p>
    <RouterLink to="/dashboard" class="btn btn-primary btn-lg"><Icon name="arrow-left" :size="16" /> Back to Dashboard</RouterLink>
  </div>
</template>
