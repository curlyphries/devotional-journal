import { useState } from 'react'
import { Outlet, Link, useLocation } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useQuery } from '@tanstack/react-query'
import { useAuth } from '../context/AuthContext'
import { getActiveFocusIntentions } from '../api/devotional'
import { Home, BookOpen, Settings, LogOut, Flame, Book, Calendar, Trophy, PenLine } from 'lucide-react'
import QuickCaptureModal from './QuickCaptureModal'

export default function Layout() {
  const { t } = useTranslation()
  const { user, logout } = useAuth()
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
    { path: '/plans', icon: Calendar, label: 'Plans' },
    { path: '/devotional', icon: Book, label: 'Focus' },
    { path: '/progress', icon: Trophy, label: 'Progress' },
    { path: '/settings', icon: Settings, label: t('nav.settings') },
  ]

  return (
    <div className="min-h-screen bg-bg-primary">
      <nav className="bg-bg-surface border-b border-border">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-2">
              <Flame className="w-8 h-8 text-accent-primary" />
              <span className="text-xl font-bold text-text-primary">
                Devotional Journal
              </span>
            </div>

            <div className="flex items-center gap-3 lg:gap-5">
              {navItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center gap-2 px-3 py-2 rounded-lg transition-colors whitespace-nowrap ${
                    location.pathname === item.path || (item.path !== '/' && location.pathname.startsWith(item.path))
                      ? 'bg-bg-elevated text-accent-primary'
                      : 'text-text-secondary hover:text-text-primary'
                  }`}
                >
                  <item.icon className="w-5 h-5" />
                  <span className="hidden sm:inline">{item.label}</span>
                </Link>
              ))}

              <button
                onClick={logout}
                className="flex shrink-0 items-center gap-2 rounded-lg px-3 py-2 text-text-secondary transition-colors whitespace-nowrap hover:text-danger"
              >
                <LogOut className="w-5 h-5" />
                <span className="hidden md:inline">{t('auth.logout')}</span>
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-6xl mx-auto px-4 py-8">
        <Outlet />
      </main>

      {/* Quick Capture FAB */}
      <button
        onClick={() => setShowQuickCapture(true)}
        className="fixed bottom-6 right-6 w-14 h-14 bg-amber-500 hover:bg-amber-400 rounded-full shadow-lg flex items-center justify-center transition-all hover:scale-110 z-40"
        aria-label="Quick capture"
      >
        <PenLine className="w-6 h-6 text-purple-900" />
      </button>

      {/* Quick Capture Modal */}
      <QuickCaptureModal
        isOpen={showQuickCapture}
        onClose={() => setShowQuickCapture(false)}
        activeFocus={activeFocus[0]}
      />
    </div>
  )
}
