import React, { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import { GuestRoute, ProtectedRoute } from './components/RouteGuards'
import AppLayout from './components/AppLayout'
import LandingPage from './pages/LandingPage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'
import ProfilePage from './pages/ProfilePage'
import LabResultsPage from './pages/LabResultsPage'
import SymptomsPage from './pages/SymptomsPage'
import NutrientAssessmentPage from './pages/NutrientAssessmentPage'
import NutritionPlanPage from './pages/NutritionPlanPage'
import ResearchPage from './pages/ResearchPage'
import AIAssistantPage from './pages/AIAssistantPage'
import './styles.css'

createRoot(document.getElementById('root')).render(<StrictMode><BrowserRouter><AuthProvider><Routes>
  <Route path="/" element={<LandingPage/>}/>
  <Route path="/login" element={<GuestRoute><LoginPage/></GuestRoute>}/><Route path="/register" element={<GuestRoute><RegisterPage/></GuestRoute>}/>
  <Route element={<ProtectedRoute><AppLayout/></ProtectedRoute>}><Route path="/dashboard" element={<DashboardPage/>}/><Route path="/profile" element={<ProfilePage/>}/><Route path="/lab-results" element={<LabResultsPage/>}/><Route path="/symptoms" element={<SymptomsPage/>}/><Route path="/assessment" element={<NutrientAssessmentPage/>}/><Route path="/plan" element={<NutritionPlanPage/>}/><Route path="/research" element={<ResearchPage/>}/><Route path="/ai-assistant" element={<AIAssistantPage/>}/></Route>
</Routes></AuthProvider></BrowserRouter></StrictMode>)
