import { useEffect, useState } from 'react'
import { fetchAnalytics } from '../api'

function Dashboard() {
  const [stats, setStats] = useState<any>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    const token = window.localStorage.getItem('hubspot_clone_token')
    if (!token) {
      setError('Please login first')
      return
    }

    fetchAnalytics(token)
      .then((data) => {
        if (data.deals_by_stage) {
          setStats(data)
        } else {
          setError(data.detail || 'Unable to load analytics')
        }
      })
      .catch(() => setError('Network error'))
  }, [])

  return (
    <section>
      <h1>Dashboard</h1>
      {error && <p>{error}</p>}
      {stats && (
        <div style={{ display: 'grid', gap: '1rem', maxWidth: 600 }}>
          <div>
            <h2>Revenue</h2>
            <p>${stats.revenue.toFixed(2)}</p>
          </div>
          <div>
            <h2>Conversion rate</h2>
            <p>{stats.conversion_rate.toFixed(1)}%</p>
          </div>
          <div>
            <h2>Active contacts</h2>
            <p>{stats.active_contacts}</p>
          </div>
          <div>
            <h2>Deals by stage</h2>
            <ul>
              {Object.entries(stats.deals_by_stage).map(([stage, count]) => (
                <li key={stage}>{stage}: {count}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </section>
  )
}

export default Dashboard
