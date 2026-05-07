import { useEffect, useState } from 'react'
import { fetchContacts } from '../api'

function Contacts() {
  const [contacts, setContacts] = useState<any[]>([])
  const [error, setError] = useState('')

  useEffect(() => {
    const token = window.localStorage.getItem('hubspot_clone_token')
    if (!token) {
      setError('Please login first')
      return
    }

    fetchContacts(token)
      .then((data) => {
        if (Array.isArray(data)) {
          setContacts(data)
        } else {
          setError(data.detail || 'Unable to load contacts')
        }
      })
      .catch(() => setError('Network error'))
  }, [])

  return (
    <section>
      <h1>Contacts</h1>
      {error ? (
        <p>{error}</p>
      ) : (
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Phone</th>
            </tr>
          </thead>
          <tbody>
            {contacts.map((contact) => (
              <tr key={contact.id}>
                <td>{contact.id}</td>
                <td>{contact.first_name} {contact.last_name}</td>
                <td>{contact.email}</td>
                <td>{contact.phone}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  )
}

export default Contacts
