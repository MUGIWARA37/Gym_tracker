<script setup>
import Icon from '../components/ui/Icon.vue'
</script>

<template>
  <div class="auth-wrap">
    <!-- Left decorative panel -->
    <div class="auth-left">
      <div class="auth-left-bg"></div>
      <div style="position:relative;z-index:1;text-align:center;max-width:360px">
        <div style="font-family:var(--font-display);font-size:14px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:var(--neon);margin-bottom:32px">SmartGym</div>
        <!-- Big decorative stat display -->
        <div style="font-family:var(--font-display);font-size:88px;font-weight:800;letter-spacing:-0.06em;color:var(--text-primary);line-height:0.9;margin-bottom:24px">
          Train<br><span style="color:var(--neon)">Smart</span>
        </div>
        <p style="font-size:15px;color:var(--text-secondary);line-height:1.6">
          Track workouts, analyze progress, and hit your goals with data-driven insights.
        </p>
        <!-- Decorative pills -->
        <div style="display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-top:32px">
          <span class="badge badge-neon" style="display:inline-flex;align-items:center;gap:6px"><Icon name="fire" :size="14" /> Calorie Tracking</span>
          <span class="badge badge-blue" style="display:inline-flex;align-items:center;gap:6px"><Icon name="dumbbell" :size="14" /> Exercise Library</span>
          <span class="badge badge-purple" style="display:inline-flex;align-items:center;gap:6px"><Icon name="rectangle-stack" :size="14" /> Workout Plans</span>
          <span class="badge badge-orange" style="display:inline-flex;align-items:center;gap:6px"><Icon name="clock" :size="14" /> Live Timer</span>
        </div>
      </div>
    </div>

    <!-- Right: form -->
    <div class="auth-right">
      <div class="auth-panel">
        <div style="font-family:var(--font-display);font-size:20px;font-weight:800;margin-bottom:32px;color:var(--text-muted)">
          SmartGym
        </div>
        <slot />
      </div>
    </div>
  </div>
</template>
