<script setup>
import { onMounted, onUnmounted, ref } from 'vue'

const cloudRef = ref(null)
const dots = ref([])
const WIDTH = 420
const HEIGHT = 420
const CENTER_X = WIDTH / 2
const CENTER_Y = HEIGHT / 2
const RADIUS = Math.min(WIDTH, HEIGHT) * 0.42
const NUM_DOTS = 140

let targetX = typeof window !== 'undefined' ? window.innerWidth / 2 : 0
let targetY = typeof window !== 'undefined' ? window.innerHeight / 2 : 0
let currentX = targetX
let currentY = targetY
let raf = null
const SPEED = 0.09 // follow smoothing factor (0-1)

function randBetween(min, max) { return min + Math.random() * (max - min) }

function onMove(e) {
  targetX = e.clientX
  targetY = e.clientY
}

function animate() {
  currentX += (targetX - currentX) * SPEED
  currentY += (targetY - currentY) * SPEED
  if (cloudRef.value) {
    const w = cloudRef.value.offsetWidth || WIDTH
    const h = cloudRef.value.offsetHeight || HEIGHT
    cloudRef.value.style.transform = `translate3d(${currentX - w / 2}px, ${currentY - h / 2}px, 0)`
  }
  raf = requestAnimationFrame(animate)
}

onMounted(() => {
  // generate dot distribution inside a disk (radial sqrt distribution for uniformity)
  for (let i = 0; i < NUM_DOTS; i++) {
    const r = Math.sqrt(Math.random()) * RADIUS
    const a = Math.random() * Math.PI * 2
    const x = CENTER_X + Math.cos(a) * r
    const y = CENTER_Y + Math.sin(a) * r
    const radius = randBetween(0.6, 2.6)
    const opacity = randBetween(0.04, 0.20)
    dots.value.push({ id: i, x, y, r: radius, o: opacity })
  }

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
  <div ref="cloudRef" class="cloud-bg" aria-hidden="true" style="width: 420px; height: 420px;">
    <svg :viewBox="`0 0 ${WIDTH} ${HEIGHT}`" xmlns="http://www.w3.org/2000/svg" class="cloud-svg" preserveAspectRatio="xMidYMid meet">
      <g>
        <circle v-for="d in dots" :key="d.id" :cx="d.x" :cy="d.y" :r="d.r" fill="#ffffff" :opacity="d.o" />
      </g>
    </svg>
  </div>
</template>

<style>
.cloud-bg { will-change: transform; border-radius: 50%; overflow: hidden; }
</style>
