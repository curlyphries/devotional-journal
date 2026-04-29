import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './context/AuthContext'
import Layout from './components/Layout'
import LoginPage from './pages/LoginPage'
import VerifyPage from './pages/VerifyPage'
import AuthCallbackPage from './pages/AuthCallbackPage'
import DashboardPage from './pages/DashboardPage'
import ReadingPage from './pages/ReadingPage'
import JournalPage from './pages/JournalPage'
import JournalHistoryPage from './pages/JournalHistoryPage'
import SettingsPage from './pages/SettingsPage'
import ReflectionPage from './pages/ReflectionPage'
import JourneyPage from './pages/JourneyPage'
import ThreadsPage from './pages/ThreadsPage'
import DevotionalPage from './pages/DevotionalPage'
import PlansPage from './pages/PlansPage'
import BiblePage from './pages/BiblePage'
import ProgressPage from './pages/ProgressPage'
import InsightsHistoryPage from './pages/InsightsHistoryPage'

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth()

  if (isLoading) {
    return (
      <div className="min-h-screen bg-bg-primary flex items-center justify-center">
        <div className="text-text-primary">Loading...</div>
      </div>
    )
  }

  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />
}

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/auth/verify" element={<VerifyPage />} />
      <Route path="/auth/callback" element={<AuthCallbackPage />} />
      <Route
        path="/"
        element={
          <PrivateRoute>
            <Layout />
          </PrivateRoute>
        }
      >
        <Route index element={<DashboardPage />} />
        <Route path="reading/:enrollmentId" element={<ReadingPage />} />
        <Route path="journal/new" element={<JournalPage />} />
        <Route path="journal/:entryId" element={<JournalPage />} />
        <Route path="journal" element={<JournalHistoryPage />} />
        <Route path="reflection" element={<ReflectionPage />} />
        <Route path="reflection/:id" element={<ReflectionPage />} />
        <Route path="journey" element={<JourneyPage />} />
        <Route path="threads" element={<ThreadsPage />} />
        <Route path="devotional" element={<DevotionalPage />} />
        <Route path="plans" element={<PlansPage />} />
        <Route path="bible" element={<BiblePage />} />
        <Route path="progress" element={<ProgressPage />} />
        <Route path="insights" element={<InsightsHistoryPage />} />
        <Route path="settings" element={<SettingsPage />} />
      </Route>
    </Routes>
  )
}

export default App
