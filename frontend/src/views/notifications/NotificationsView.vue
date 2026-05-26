<script setup>
import { onMounted, ref, computed } from 'vue'
import { NotificationsService } from '../../services/notifications.service'

const notifications = ref([])
const loading = ref(true)
const filter = ref('all')

const typeIcon = { workout: '🏋️', progress: '📊', nutrition: '🥗', system: '⚙️', achievement: '🏆' }
const typeColor = { workout: 'badge-orange', progress: 'badge-neon', nutrition: 'badge-blue', system: 'badge-muted', achievement: 'badge-purple' }

const formatTime = (dt) => {
  if (!dt) return ''
  const now = new Date()
  const d = new Date(dt)
  const diff = Math.floor((now - d) / 1000)
  if (diff < 60) return 'just now'
  if (diff < 3600) return `${Math.floor(diff/60)}m ago`
  if (diff < 86400) return `${Math.floor(diff/3600)}h ago`
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

const filtered = computed(() => {
  if (filter.value === 'unread') return notifications.value.filter(n => !n.is_read)
  return notifications.value
})

const unreadCount = computed(() => notifications.value.filter(n => !n.is_read).length)

onMounted(async () => {
  try {
    const { data } = await NotificationsService.list()
    notifications.value = Array.isArray(data) ? data : data?.results || []
  } finally { loading.value = false }
})

const markRead = async (notif) => {
  if (notif.is_read) return
  try {
    await NotificationsService.markRead(notif.id)
    notif.is_read = true
  } catch {}
}

const markAllRead = async () => {
  try {
    await NotificationsService.markAllRead()
    notifications.value.forEach(n => n.is_read = true)
  } catch {}
}
</script>

<template>
  <div class="page">
    <div class="page-header">
      <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px">
        <div>
          <h1 class="page-title">Notifications</h1>
          <p class="page-subtitle">
            {{ unreadCount ? `${unreadCount} unread` : 'All caught up' }}
          </p>
        </div>
        <button v-if="unreadCount > 0" class="btn btn-secondary" @click="markAllRead">
          ✓ Mark all read
        </button>
      </div>
    </div>

    <!-- Filter chips -->
    <div style="display:flex;gap:8px;margin-bottom:20px">
      <button class="chip" :class="{ active: filter === 'all' }" @click="filter = 'all'">
        All ({{ notifications.length }})
      </button>
      <button class="chip" :class="{ active: filter === 'unread' }" @click="filter = 'unread'">
        Unread ({{ unreadCount }})
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" style="display:flex;flex-direction:column;gap:10px">
      <div v-for="i in 5" :key="i" class="skeleton" style="height:72px;border-radius:10px"></div>
    </div>

    <!-- Empty -->
    <div v-else-if="!filtered.length" style="text-align:center;padding:64px 24px;color:var(--text-muted)">
      <div style="font-size:48px;margin-bottom:16px">🔔</div>
      <div style="font-size:16px;font-weight:600;color:var(--text-primary);margin-bottom:6px">
        {{ filter === 'unread' ? 'No unread notifications' : 'No notifications yet' }}
      </div>
      <p>Complete workouts and track progress to get notified.</p>
    </div>

    <!-- List -->
    <div v-else style="display:flex;flex-direction:column;gap:8px;animate-fade-up">
      <div
        v-for="notif in filtered"
        :key="notif.id"
        class="notif-item"
        :class="{ unread: !notif.is_read }"
        @click="markRead(notif)"
        style="cursor:pointer"
      >
        <!-- Unread dot -->
        <div v-if="!notif.is_read" class="notif-dot"></div>
        <div v-else style="width:8px;flex-shrink:0"></div>

        <!-- Icon -->
        <div style="width:40px;height:40px;border-radius:10px;background:var(--surface-2);display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0">
          {{ typeIcon[notif.notification_type] || '📣' }}
        </div>

        <!-- Content -->
        <div style="flex:1;min-width:0">
          <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:4px">
            <span style="font-size:13px;font-weight:600;color:var(--text-primary)">{{ notif.title }}</span>
            <span class="badge" :class="typeColor[notif.notification_type] || 'badge-muted'">
              {{ notif.notification_type || 'General' }}
            </span>
          </div>
          <p style="font-size:12px;color:var(--text-secondary);line-height:1.4">{{ notif.message }}</p>
        </div>

        <!-- Time -->
        <div style="font-size:11px;color:var(--text-muted);flex-shrink:0;white-space:nowrap">
          {{ formatTime(notif.created_at) }}
        </div>
      </div>
    </div>
  </div>
</template>
