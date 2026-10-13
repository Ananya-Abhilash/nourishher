import React from 'react'
import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const links = [['/dashboard', 'Dashboard'], ['/profile', 'Health Profile'], ['/lab-results', 'Lab Results'], ['/symptoms', 'Symptoms'], ['/assessment', 'Nutrient Assessment'], ['/plan', 'Nutrition Plan'], ['/research', 'Research'], ['/ai-assistant', 'AI Assistant']]
export default function AppLayout() {
  const { user, signOut } = useAuth(); const navigate = useNavigate()
  const logout = async () => { await signOut(); navigate('/login') }
  return <div className="app-shell"><aside><NavLink to="/dashboard" className="brand">NourishHer <i>AI</i></NavLink><nav>{links.map(([to, label]) => <NavLink key={to} to={to}>{label}</NavLink>)}</nav><div className="user-panel"><strong>{user?.first_name || 'Member'}</strong><span>{user?.email}</span><button className="text-button" onClick={logout}>Log out</button></div></aside><main><Outlet /></main></div>
}
