import { computed, ref } from 'vue'

export function useTimer() {
  const elapsed = ref(0)
  let interval = null

  const start = () => {
    interval = setInterval(() => {
      elapsed.value += 1
    }, 1000)
  }

  const pause = () => {
    clearInterval(interval)
  }

  const reset = () => {
    clearInterval(interval)
    elapsed.value = 0
  }

  const formatted = computed(() => {
    const h = Math.floor(elapsed.value / 3600)
    const m = Math.floor((elapsed.value % 3600) / 60)
    const s = elapsed.value % 60
    return [h, m, s].map((n) => String(n).padStart(2, '0')).join(':')
  })

  return {
    elapsed,
    formatted,
    start,
    pause,
    reset,
  }
}
