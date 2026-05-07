import { useState } from 'react'

const stages = ['Lead', 'Qualified', 'Proposal', 'Won', 'Lost']
const exampleDeals = [
  { id: 1, title: 'Demo deal', stage: 'Lead', amount: 5000 },
  { id: 2, title: 'Follow-up call', stage: 'Qualified', amount: 12000 },
  { id: 3, title: 'Proposal review', stage: 'Proposal', amount: 4300 },
]

function Pipeline() {
  const [deals] = useState(exampleDeals)

  return (
    <section>
      <h1>Pipeline</h1>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, minmax(0, 1fr))', gap: '1rem' }}>
        {stages.map((stage) => (
          <div key={stage} style={{ padding: '1rem', border: '1px solid #ccc', borderRadius: 8 }}>
            <h2>{stage}</h2>
            <ul style={{ listStyle: 'none', padding: 0 }}>
              {deals.filter((deal) => deal.stage === stage).map((deal) => (
                <li key={deal.id} style={{ marginBottom: 8 }}>
                  <strong>{deal.title}</strong>
                  <div>${deal.amount.toFixed(2)}</div>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </section>
  )
}

export default Pipeline
