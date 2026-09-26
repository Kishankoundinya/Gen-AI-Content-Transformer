const API_BASE = '/api'

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const body = await res.text()
    throw new Error(`Request failed (${res.status}): ${body}`)
  }
  return res.json()
}

export async function fetchHealth() {
  return request('/health')
}

export async function fetchModelInfo() {
  return request('/model-info')
}

export async function fetchOutputTypes() {
  return request('/output-types')
}

export async function generateContent(payload) {
  return request('/generate', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}