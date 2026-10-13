import React from 'react'
import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
export function ProtectedRoute({ children }) { const { user, loading } = useAuth(); if (loading) return <div className="page-center">Loading…</div>; return user ? children : <Navigate to="/login" replace /> }
export function GuestRoute({ children }) { const { user, loading } = useAuth(); if (loading) return <div className="page-center">Loading…</div>; return user ? <Navigate to="/dashboard" replace /> : children }
