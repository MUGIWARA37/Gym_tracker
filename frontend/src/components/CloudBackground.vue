<script setup>
import { onMounted, onUnmounted, ref } from 'vue'

const cloudRef = ref(null)
let targetX = typeof window !== 'undefined' ? window.innerWidth / 2 : 0
let targetY = typeof window !== 'undefined' ? window.innerHeight / 2 : 0
let currentX = targetX
let currentY = targetY
let raf = null
const speed = 0.08 // follow smoothing factor (0-1)

function onMove(e) {
  targetX = e.clientX
  targetY = e.clientY
}

function animate() {
  currentX += (targetX - currentX) * speed
  currentY += (targetY - currentY) * speed
  if (cloudRef.value) {
    const w = cloudRef.value.offsetWidth || 480
    const h = cloudRef.value.offsetHeight || 240
    cloudRef.value.style.transform = `translate3d(${currentX - w / 2}px, ${currentY - h / 2}px, 0)`
  }
  raf = requestAnimationFrame(animate)
}

onMounted(() => {
  window.addEventListener('mousemove', onMove, { passive: true })
  window.addEventListener('mouseout', () => {
    targetX = window.innerWidth / 2
    targetY = window.innerHeight / 2
  })
  raf = requestAnimationFrame(animate)
})

onUnmounted(() => {
  window.removeEventListener('mousemove', onMove)
  cancelAnimationFrame(raf)
})
</script>

<template>
  <div ref="cloudRef" class="cloud-bg" aria-hidden="true">
    <svg viewBox="0 0 480 240" xmlns="http://www.w3.org/2000/svg" class="cloud-svg" preserveAspectRatio="xMidYMid meet">
      <path d="M120 140c-22 0-40-18-40-40 0-19 13-35 31-39 4-25 25-44 51-44 8 0 16 2 23 6 10-11 25-18 41-18 31 0 56 25 56 56 0 2 0 4-0.2 6 31 3 56 29 56 60 0 34-28 62-62 62H120z" />
    </svg>
  </div>
</template>

<style>
/* Cloud base styling — sizes and blur live in global style.css */
.cloud-bg { will-change: transform; }
</style>
