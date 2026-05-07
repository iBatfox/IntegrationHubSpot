const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

export async function login(username: string, password: string) {
  const data = new URLSearchParams()
  data.set('username', username)
  data.set('password', password)

  const response = await fetch(`${apiBase}/auth/login`, {
    method: 'POST',
    body: data,
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  })
  return response.json()
}

export async function fetchContacts(token: string) {
  const response = await fetch(`${apiBase}/contacts/`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
  return response.json()
}

export async function fetchAnalytics(token: string) {
  const response = await fetch(`${apiBase}/analytics/overview`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
  return response.json()
}
