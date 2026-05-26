<template>
  <div style="min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;background:var(--bg);text-align:center;padding:24px">
    <div style="font-size:80px;margin-bottom:24px">🚫</div>
    <h1 style="font-family:var(--font-display);font-size:28px;font-weight:800;color:var(--text-primary);margin-bottom:8px">Access Denied</h1>
    <p style="color:var(--text-secondary);margin-bottom:32px">You don't have permission to view this page.</p>
    <RouterLink to="/dashboard" class="btn btn-primary btn-lg">← Back to Dashboard</RouterLink>
  </div>
</template>
