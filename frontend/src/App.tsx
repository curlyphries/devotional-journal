import { Routes, Route, Navigate, useLocation } from 'react-router-dom'
import { useAuth } from './context/AuthContext'
import Layout from './components/Layout'
import LandingPage from './pages/LandingPage'
import LoginPage from './pages/LoginPage'
import VerifyPage from './pages/VerifyPage'
import AuthCallbackPage from './pages/AuthCallbackPage'
import DashboardPage from './pages/DashboardPage'
import ReadingPage from './pages/ReadingPage'
import JournalPage from './pages/JournalPage'
import JournalHistoryPage from './pages/JournalHistoryPage'
import StudyHubPage from './pages/StudyHubPage'
import StudyPage from './pages/StudyPage'
import SettingsPage from './pages/SettingsPage'
import ReflectionPage from './pages/ReflectionPage'
import JourneyPage from './pages/JourneyPage'
import ThreadsPage from './pages/ThreadsPage'
import DevotionalPage from './pages/DevotionalPage'
import PlansPage from './pages/PlansPage'
import BiblePage from './pages/BiblePage'
import ProgressPage from './pages/ProgressPage'
import InsightsHistoryPage from './pages/InsightsHistoryPage'
import HelpPage from './pages/HelpPage'
import NotFoundPage from './pages/NotFoundPage'
import ErrorBoundary from './components/ErrorBoundary'
import AuditLogPage from './pages/AuditLogPage'
import ProfilePage from './pages/ProfilePage'
import GrowthPlansPage from './pages/GrowthPlansPage'
import GrowthPlanPage from './pages/GrowthPlanPage'

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth()

  if (isLoading) {
    return (
      <div className="min-h-screen bg-bg-primary flex items-center justify-center">
        <div className="text-text-primary">Loading...</div>
      </div>
    )
  }

  return isAuthenticated ? <>{children}</> : <Navigate to="/welcome" replace />
}

function App() {
  const location = useLocation()
  return (
    // Outer safety net for the public pages and the layout itself; the Layout
    // has its own boundary around page content so the nav stays usable.
    <ErrorBoundary resetKey={location.pathname}>
    <Routes>
      <Route path="/welcome" element={<LandingPage />} />
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
        <Route path="study" element={<StudyHubPage />} />
        <Route path="study/:studyId" element={<StudyPage />} />
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
        <Route path="audit" element={<AuditLogPage />} />
        <Route path="profile" element={<ProfilePage />} />
        <Route path="growth" element={<GrowthPlansPage />} />
        <Route path="growth/:planId" element={<GrowthPlanPage />} />
        <Route path="help" element={<HelpPage />} />
        {/* Unknown URL: a "not found" page inside the normal layout */}
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
    </ErrorBoundary>
  )
}

export default App
