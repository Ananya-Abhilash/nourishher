import React from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const cards = [
  ['Health Profile', 'Keep your key details up to date.', '/profile', 'Complete profile'],
  ['Blood Tests', 'Record your blood-test information.', '/lab-results', 'Add blood test'],
  ['Symptoms', 'Record and review your symptoms over time.', '/symptoms', 'Track symptoms →'],
  ['Nutrient Assessment', 'Review preliminary observations from your recorded blood-test results.', '/assessment', 'View assessment →'],
  ['Nutrition Plan', 'Coming soon', '/plan', 'Explore'],
  ['Research', 'Coming soon', '/research', 'Explore'],
  ['AI Assistant', 'Coming soon', '/ai-assistant', 'Explore'],
]

export default function DashboardPage() {
  const { user } = useAuth()
  return <><p className="eyebrow">YOUR WELLNESS SPACE</p><h1>Hello, {user?.first_name || 'there'}.</h1><p className="lead">A calm place to organise your health information.</p><div className="cards">{cards.map(([title, text, to, action]) => <article className="card" key={title}><h2>{title}</h2><p>{text}</p><Link to={to}>{action}</Link></article>)}</div></>
}
