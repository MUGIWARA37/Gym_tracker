import { ref } from 'vue'

export function useFileUpload(options = {}) {
  const { maxMB = 5, accept = 'image/jpeg,image/png,image/webp' } = options

  const file = ref(null)
  const preview = ref(null)
  const error = ref('')

  const pick = (event) => {
    const f = event.target.files?.[0]
    if (!f) return
    error.value = ''

    const allowed = accept.split(',').map(s => s.trim())
    if (!allowed.includes(f.type)) {
      error.value = `Unsupported file type. Allowed: ${accept}`
      return
    }
    if (f.size > maxMB * 1024 * 1024) {
      error.value = `File too large. Maximum size is ${maxMB} MB.`
      return
    }

    file.value = f
    const reader = new FileReader()
    reader.onload = (e) => { preview.value = e.target.result }
    reader.readAsDataURL(f)
  }

  const clear = () => {
    file.value = null
    preview.value = null
    error.value = ''
  }

  const toFormData = (existingData = {}) => {
    const fd = new FormData()
    for (const [k, v] of Object.entries(existingData)) {
      if (v !== null && v !== undefined) fd.append(k, v)
    }
    if (file.value) fd.append('photo', file.value)
    return fd
  }

  return { file, preview, error, pick, clear, toFormData }
}
