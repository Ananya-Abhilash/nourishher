import React, { createContext, useContext, useEffect, useState } from 'react'
import client from '../api/client'

const AuthContext = createContext(null)
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  useEffect(() => {
    const token = localStorage.getItem('nourishher_token')
    if (!token) { setLoading(false); return }
    client.get('/auth/me/').then(({ data }) => setUser(data)).catch(() => localStorage.removeItem('nourishher_token')).finally(() => setLoading(false))
  }, [])
  const signIn = ({ token, user: signedInUser }) => { localStorage.setItem('nourishher_token', token); setUser(signedInUser) }
  const signOut = async () => { try { await client.post('/auth/logout/') } finally { localStorage.removeItem('nourishher_token'); setUser(null) } }
  return <AuthContext.Provider value={{ user, loading, signIn, signOut }}>{children}</AuthContext.Provider>
}
export const useAuth = () => useContext(AuthContext)
