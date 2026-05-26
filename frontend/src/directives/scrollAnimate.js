// Scroll-triggered reveal animations (IntersectionObserver)
// Usage:
//   <div v-scroll-animate>...</div>
//   <div v-scroll-animate="'fade'">...</div>
//   <div v-scroll-animate="{ animation: 'fade-up', delay: 120, duration: 650, once: true }">...</div>

const DEFAULTS = {
  animation: 'fade-up',
  once: true,
  threshold: 0.15,
  rootMargin: '0px 0px -10% 0px',
  delay: 0,
  duration: 520,
  distance: 12,
}

const state = new WeakMap()

function normalizeOptions(value) {
  if (!value) return { ...DEFAULTS }
  if (typeof value === 'string') return { ...DEFAULTS, animation: value }
  return { ...DEFAULTS, ...value }
}

function applyBase(el, opts) {
  el.classList.add('sa', `sa--${opts.animation}`)
  el.style.setProperty('--sa-delay', `${Number(opts.delay) || 0}ms`)
  el.style.setProperty('--sa-duration', `${Number(opts.duration) || 0}ms`)
  el.style.setProperty('--sa-distance', `${Number(opts.distance) || 0}px`)
}

function cleanup(el) {
  const s = state.get(el)
  if (!s) return
  if (s.observer) s.observer.disconnect()
  state.delete(el)
}

function setup(el, binding) {
  cleanup(el)

  const opts = normalizeOptions(binding.value)
  applyBase(el, opts)

  // If user prefers reduced motion, just show the element.
  if (typeof window !== 'undefined' && window.matchMedia?.('(prefers-reduced-motion: reduce)').matches) {
    el.classList.add('sa--in')
    return
  }

  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          entry.target.classList.add('sa--in')
          if (opts.once) observer.unobserve(entry.target)
        } else if (!opts.once) {
          entry.target.classList.remove('sa--in')
        }
      }
    },
    {
      threshold: opts.threshold,
      rootMargin: opts.rootMargin,
    },
  )

  observer.observe(el)
  state.set(el, { observer })
}

export const scrollAnimate = {
  mounted(el, binding) {
    setup(el, binding)
  },
  updated(el, binding) {
    // Re-init if options object/string changes
    if (binding.value !== binding.oldValue) setup(el, binding)
  },
  unmounted(el) {
    cleanup(el)
  },
}
