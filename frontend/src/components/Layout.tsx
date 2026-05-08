import { useState } from 'react'
import { Outlet, Link, useLocation } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useQuery } from '@tanstack/react-query'
import { useAuth } from '../context/AuthContext'
import { getActiveFocusIntentions } from '../api/devotional'
import {
  Home, BookOpen, Settings, LogOut, Flame, Book, Calendar, Trophy,
  PenLine, Lightbulb, HelpCircle, Languages,
} from 'lucide-react'
import QuickCaptureModal from './QuickCaptureModal'
import ErrorBoundary from './ErrorBoundary'

export default function Layout() {
  const { t, i18n } = useTranslation()
  const { logout } = useAuth()
  const location = useLocation()
  const [showQuickCapture, setShowQuickCapture] = useState(false)

  // Fetch active focus for tagging
  const { data: activeFocus = [] } = useQuery({
    queryKey: ['activeFocus'],
    queryFn: getActiveFocusIntentions,
    staleTime: 5 * 60 * 1000,
  })

  const navItems = [
    { path: '/', icon: Home, label: t('nav.dashboard') },
    { path: '/journal', icon: BookOpen, label: t('nav.journal') },
    { path: '/plans', icon: Calendar, label: t('nav.plans') },
    { path: '/devotional', icon: Book, label: t('nav.focus') },
    { path: '/progress', icon: Trophy, label: t('nav.progress') },
    { path: '/insights', icon: Lightbulb, label: t('nav.insights') },
    { path: '/settings', icon: Settings, label: t('nav.settings') },
  ]

  const toggleLanguage = () => {
    const next = i18n.language === 'es' ? 'en' : 'es'
    i18n.changeLanguage(next)
  }

  return (
    <div className="min-h-screen bg-bg-primary">
      {/* Skip-link for keyboard users */}
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:fixed focus:top-2 focus:left-2 focus:z-50 focus:px-3 focus:py-2 focus:bg-bg-elevated focus:text-text-primary focus:rounded-lg focus:outline focus:outline-2 focus:outline-accent-primary"
      >
        {t('common.skipToContent', 'Skip to main content')}
      </a>

      <nav aria-label="Primary" className="bg-bg-surface border-b border-border">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            <Link to="/" className="flex items-center gap-2 focus:outline-none focus:ring-2 focus:ring-accent-primary rounded-lg" aria-label="Devotional Journal home">
              <Flame className="w-8 h-8 text-accent-primary" aria-hidden="true" />
              <span className="text-xl font-bold text-text-primary">
                Devotional Journal
              </span>
            </Link>

            <div className="flex items-center gap-3 lg:gap-5">
              {navItems.map((item) => {
                const isActive = location.pathname === item.path || (item.path !== '/' && location.pathname.startsWith(item.path))
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    aria-current={isActive ? 'page' : undefined}
                    className={`flex items-center gap-2 px-3 py-2 rounded-lg transition-colors whitespace-nowrap ${
                      isActive
                        ? 'bg-bg-elevated text-accent-primary'
                        : 'text-text-secondary hover:text-text-primary'
                    }`}
                  >
                    <item.icon className="w-5 h-5" aria-hidden="true" />
                    <span className="hidden sm:inline">{item.label}</span>
                  </Link>
                )
              })}

              <button
                data-tour-id="language"
                onClick={toggleLanguage}
                className="flex shrink-0 items-center gap-1 rounded-lg px-3 py-2 text-text-secondary transition-colors hover:text-text-primary"
                title={t('nav.changeLanguage', 'Change language')}
                aria-label={t('nav.changeLanguage', 'Change language')}
              >
                <Languages className="w-5 h-5" aria-hidden="true" />
                <span className="text-xs font-medium uppercase">
                  {i18n.language === 'es' ? 'ES' : 'EN'}
                </span>
              </button>

              <Link
                data-tour-id="help"
                to="/help"
                className={`flex shrink-0 items-center gap-2 rounded-lg px-3 py-2 transition-colors whitespace-nowrap ${
                  location.pathname === '/help'
                    ? 'bg-bg-elevated text-accent-primary'
                    : 'text-text-secondary hover:text-text-primary'
                }`}
                title={t('nav.help', 'Help & Guide')}
                aria-label={t('nav.help', 'Help & Guide')}
              >
                <HelpCircle className="w-5 h-5" aria-hidden="true" />
              </Link>

              <button
                onClick={logout}
                className="flex shrink-0 items-center gap-2 rounded-lg px-3 py-2 text-text-secondary transition-colors whitespace-nowrap hover:text-danger"
              >
                <LogOut className="w-5 h-5" aria-hidden="true" />
                <span className="hidden md:inline">{t('auth.logout')}</span>
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main id="main-content" className="max-w-6xl mx-auto px-4 py-8">
        <ErrorBoundary label="route-outlet">
          <Outlet />
        </ErrorBoundary>
      </main>

      {/* Quick Capture FAB */}
      <button
        data-tour-id="fab"
        onClick={() => setShowQuickCapture(true)}
        className="fixed bottom-6 right-6 w-14 h-14 bg-amber-500 hover:bg-amber-400 rounded-full shadow-lg flex items-center justify-center transition-all hover:scale-110 z-40 focus:outline-none focus:ring-2 focus:ring-amber-300 focus:ring-offset-2 focus:ring-offset-bg-primary"
        aria-label={t('nav.quickCapture', 'Quick capture')}
        title={t('nav.quickCapture', 'Quick capture')}
      >
        <PenLine className="w-6 h-6 text-purple-900" aria-hidden="true" />
      </button>

      {/* Quick Capture Modal */}
      <QuickCaptureModal
        isOpen={showQuickCapture}
        onClose={() => setShowQuickCapture(false)}
        activeFocus={activeFocus[0] ? { intention: activeFocus[0].intention_text, themes: activeFocus[0].themes } : undefined}
      />
    </div>
  )
}
