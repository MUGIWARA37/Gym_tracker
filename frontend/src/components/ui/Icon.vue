<script setup>
// Lightweight Heroicons-style SVGs (outline) to keep iconography consistent
// No npm dependency; icons use currentColor for easy theming.

const props = defineProps({
  name: { type: String, required: true },
  size: { type: [Number, String], default: 18 },
  title: { type: String, default: '' },
})

const px = (v) => (typeof v === 'number' ? `${v}px` : v)
</script>

<template>
  <svg
    v-if="name === 'dashboard'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M3 3h8v8H3V3Zm10 0h8v5h-8V3Zm0 7h8v11h-8V10ZM3 13h8v8H3v-8Z" />
  </svg>

  <svg
    v-else-if="name === 'plus-circle'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Z" />
    <path d="M12 8v8M8 12h8" />
  </svg>

  <svg
    v-else-if="name === 'rectangle-stack'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M6 7.5h12M6 12h12M6 16.5h12" />
    <path d="M5 4.5h14a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-11a2 2 0 0 1 2-2Z" />
  </svg>

  <svg
    v-else-if="name === 'play-circle'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Z" />
    <path d="M11 9.5v5l4-2.5-4-2.5Z" fill="currentColor" stroke="none" />
  </svg>

  <svg
    v-else-if="name === 'chart-bar-square'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M4 19V5a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2Z" />
    <path d="M8 17v-6M12 17v-9M16 17v-3" />
  </svg>

  <svg
    v-else-if="name === 'beaker'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M8 3h8" />
    <path d="M10 3v5l-5 9a4 4 0 0 0 3.5 6h7a4 4 0 0 0 3.5-6l-5-9V3" />
    <path d="M8.5 16h7" />
  </svg>

  <svg
    v-else-if="name === 'bell'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M18 8a6 6 0 1 0-12 0c0 7-3 9-3 9h18s-3-2-3-9" />
    <path d="M13.73 21a2 2 0 0 1-3.46 0" />
  </svg>

  <svg
    v-else-if="name === 'user-circle'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Z" />
    <path d="M8 18a4 4 0 0 1 8 0" />
    <path d="M12 12a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z" />
  </svg>

  <svg
    v-else-if="name === 'arrow-left-on-rectangle'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M10 7h8a2 2 0 0 1 2 2v6a2 2 0 0 1-2 2h-8" />
    <path d="M13 12H4" />
    <path d="m7 9-3 3 3 3" />
  </svg>

  <svg
    v-else-if="name === 'calendar-days'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M7 3v2M17 3v2" />
    <path d="M4 8h16" />
    <path d="M6 5h12a2 2 0 0 1 2 2v13a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2Z" />
    <path d="M8 12h.01M12 12h.01M16 12h.01M8 16h.01M12 16h.01" />
  </svg>

  <svg
    v-else-if="name === 'fire'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M12 22c4 0 7-3 7-7 0-2.5-1.3-4.7-3.3-6.2-.8 1.6-2.3 2.7-3.7 3.2.2-2.5-1-4.8-3-6.2C6.6 7 5 9.6 5 12.6 5 18.5 8 22 12 22Z" />
  </svg>

  <svg
    v-else-if="name === 'bolt'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M13 2 3 14h7l-1 8 10-12h-7l1-8Z" />
  </svg>

  <svg
    v-else-if="name === 'check-badge'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M12 2 9.5 4.5H6.2L5 7.8 2.5 10.3 4 13.8 2.5 17.2 5 19.7l1.2 3.3h3.3L12 22l2.5-2.5h3.3l1.2-3.3 2.5-2.5-1.5-3.4 1.5-3.5L19 4.5h-3.3L12 2Z" />
    <path d="m9 12 2 2 4-5" />
  </svg>

  <svg
    v-else-if="name === 'check'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="m5 13 4 4L19 7" />
  </svg>

  <svg
    v-else-if="name === 'check-circle'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Z" />
    <path d="m8.5 12 2.3 2.3L16 9" />
  </svg>

  <svg
    v-else-if="name === 'x-mark'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M6 6l12 12M18 6 6 18" />
  </svg>

  <svg
    v-else-if="name === 'plus'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M12 5v14M5 12h14" />
  </svg>

  <svg
    v-else-if="name === 'minus'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M5 12h14" />
  </svg>

  <svg
    v-else-if="name === 'pencil-square'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L8 18l-4 1 1-4L16.5 3.5Z" />
    <path d="M19 13.5V19a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2h5.5" />
  </svg>

  <svg
    v-else-if="name === 'arrow-right'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M5 12h13" />
    <path d="m13 6 6 6-6 6" />
  </svg>

  <svg
    v-else-if="name === 'arrow-left'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M19 12H6" />
    <path d="m11 6-6 6 6 6" />
  </svg>

  <svg
    v-else-if="name === 'clock'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Z" />
    <path d="M12 7v5l3 2" />
  </svg>

  <svg
    v-else-if="name === 'pause'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M8 6v12M16 6v12" />
  </svg>

  <svg
    v-else-if="name === 'stop'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="currentColor" stroke="none"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <rect x="7" y="7" width="10" height="10" rx="2" />
  </svg>

  <svg
    v-else-if="name === 'play'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="currentColor" stroke="none"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M10 8.5v7l6-3.5-6-3.5Z" />
  </svg>

  <svg
    v-else-if="name === 'square-2-stack'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M9 9h10v10H9V9Z" />
    <path d="M5 15V5h10" />
  </svg>

  <svg
    v-else-if="name === 'trash'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M4 7h16" />
    <path d="M10 11v6M14 11v6" />
    <path d="M6 7l1 14h10l1-14" />
    <path d="M9 7V5a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2" />
  </svg>

  <svg
    v-else-if="name === 'clipboard-document-list'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M9 4h6" />
    <path d="M9 4a2 2 0 0 0-2 2v1h10V6a2 2 0 0 0-2-2" />
    <path d="M7 7H6a2 2 0 0 0-2 2v11a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-1" />
    <path d="M8 12h8M8 16h8" />
    <path d="M8 20h6" />
  </svg>

  <svg
    v-else-if="name === 'cog-6-tooth'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M12 15.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7Z" />
    <path d="M19.4 15a7.9 7.9 0 0 0 .1-2l2-1.2-2-3.5-2.3.6a8.2 8.2 0 0 0-1.7-1L15.2 3h-6.4L8.5 6.9a8.2 8.2 0 0 0-1.7 1L4.5 7.3l-2 3.5L4.5 12a7.9 7.9 0 0 0 .1 2l-2 1.2 2 3.5 2.3-.6a8.2 8.2 0 0 0 1.7 1L8.8 21h6.4l.3-2.9a8.2 8.2 0 0 0 1.7-1l2.3.6 2-3.5-2.1-1.2Z" />
  </svg>

  <svg
    v-else-if="name === 'trophy'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M8 4h8v3a4 4 0 0 1-8 0V4Z" />
    <path d="M6 6H4a2 2 0 0 0 2 5" />
    <path d="M18 6h2a2 2 0 0 1-2 5" />
    <path d="M12 11v4" />
    <path d="M9 21h6" />
    <path d="M10 15h4" />
  </svg>

  <svg
    v-else-if="name === 'megaphone'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M3 11v2a3 3 0 0 0 3 3h2l2 4h2l-1.5-4H16l5-3V11l-5-3H6a3 3 0 0 0-3 3Z" />
    <path d="M16 8v8" />
  </svg>

  <svg
    v-else-if="name === 'scale'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M7 20h10" />
    <path d="M12 20V6" />
    <path d="M6 6h12" />
    <path d="M8 6 5 12h6L8 6Z" />
    <path d="M16 6 13 12h6l-3-6Z" />
  </svg>

  <svg
    v-else-if="name === 'ruler'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M4 20 20 4" />
    <path d="M7 17l-1.5-1.5M10 14l-1.5-1.5M13 11l-1.5-1.5M16 8l-1.5-1.5" />
  </svg>

  <svg
    v-else-if="name === 'droplet'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M12 2S6 9 6 14a6 6 0 0 0 12 0c0-5-6-12-6-12Z" />
  </svg>

  <svg
    v-else-if="name === 'light-bulb'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M9 18h6" />
    <path d="M10 22h4" />
    <path d="M8 14a6 6 0 1 1 8 0c-1 1-1.5 2-1.5 3H9.5c0-1-0.5-2-1.5-3Z" />
  </svg>

  <svg
    v-else-if="name === 'dumbbell'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M6 9v6" />
    <path d="M4 10v4" />
    <path d="M10 8v8" />
    <path d="M14 8v8" />
    <path d="M20 10v4" />
    <path d="M18 9v6" />
    <path d="M10 12h4" />
  </svg>

  <svg
    v-else-if="name === 'flag'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z" />
    <line x1="4" y1="22" x2="4" y2="15" />
  </svg>

  <svg
    v-else-if="name === 'forward'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="m13 17 5-5-5-5" />
    <path d="m6 17 5-5-5-5" />
  </svg>

  <svg
    v-else-if="name === 'ellipsis-horizontal-circle'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Z" />
    <path d="M8 12h.01M12 12h.01M16 12h.01" />
  </svg>

  <svg
    v-else-if="name === 'camera'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M9 3H6a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2h-3" />
    <path d="M9 3a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v1H9V3Z" />
    <path d="M12 17a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z" />
  </svg>

  <svg
    v-else-if="name === 'heart'"
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7 11 4.6a5.5 5.5 0 0 0-7.8 7.8l1 1.1L12 21l7.8-7.5 1-1a5.5 5.5 0 0 0 0-7.8z" />
  </svg>


  <svg
    v-else
    :width="px(size)" :height="px(size)"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true"
  >
    <title v-if="title">{{ title }}</title>
    <path d="M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Z" />
    <path d="M12 16h.01" />
    <path d="M12 12a3 3 0 0 0-3-3" />
  </svg>
</template>
