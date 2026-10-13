import React, { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import { GuestRoute, ProtectedRoute } from './components/RouteGuards'
import AppLayout from './components/AppLayout'
import LandingPage from './pages/LandingPage'
import { LoginPage, RegisterPage } from './pages/AuthPages'
import { Dashboard, Labs, Placeholder, Profile } from './pages/AppPages'
import { AssessmentPage, SymptomsPage } from './pages/Day3Pages'
import './styles.css'

createRoot(document.getElementById('root')).render(<StrictMode><BrowserRouter><AuthProvider><Routes>
  <Route path="/" element={<LandingPage/>}/>
  <Route path="/login" element={<GuestRoute><LoginPage/></GuestRoute>}/><Route path="/register" element={<GuestRoute><RegisterPage/></GuestRoute>}/>
  <Route element={<ProtectedRoute><AppLayout/></ProtectedRoute>}><Route path="/dashboard" element={<Dashboard/>}/><Route path="/profile" element={<Profile/>}/><Route path="/lab-results" element={<Labs/>}/><Route path="/symptoms" element={<SymptomsPage/>}/><Route path="/plan" element={<AssessmentPage/>}/><Route path="/research" element={<Placeholder kind="Research"/>}/><Route path="/ai-assistant" element={<Placeholder kind="Assistant"/>}/></Route>
</Routes></AuthProvider></BrowserRouter></StrictMode>)
