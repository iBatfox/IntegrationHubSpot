import { useState, type FormEvent } from 'react'
import { login } from '../api'

function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [message, setMessage] = useState('')

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    try {
      const result = await login(email, password)
      if (result.access_token) {
        window.localStorage.setItem('hubspot_clone_token', result.access_token)
        setMessage('Login successful')
      } else {
        setMessage(result.detail || 'Login failed')
      }
    } catch (error) {
      setMessage('Unable to login')
    }
  }

  return (
    <section>
      <h1>HubSpot Clone</h1>
      <form onSubmit={handleSubmit} style={{ display: 'grid', gap: '0.75rem', maxWidth: 360 }}>
        <label>
          Email
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </label>
        <label>
          Password
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </label>
        <button type="submit">Login</button>
      </form>
      {message && <p>{message}</p>}
    </section>
  )
}

export default Login
