import { Routes, Route, Link } from 'react-router-dom'
import Login from './pages/Login'
import Contacts from './pages/Contacts'
import Dashboard from './pages/Dashboard'
import Pipeline from './pages/Pipeline'

function App() {
  return (
    <div>
      <header style={{ padding: '1rem', borderBottom: '1px solid #ddd' }}>
        <nav style={{ display: 'flex', gap: '1rem' }}>
          <Link to="/">Login</Link>
          <Link to="/contacts">Contacts</Link>
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/pipeline">Pipeline</Link>
        </nav>
      </header>
      <main style={{ padding: '1rem' }}>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/contacts" element={<Contacts />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/pipeline" element={<Pipeline />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
