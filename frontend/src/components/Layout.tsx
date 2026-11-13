import { useEffect, useRef, useState } from 'react'
import { Outlet, Link, useLocation } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useQuery } from '@tanstack/react-query'
import { useAuth } from '../context/AuthContext'
import { getActiveFocusIntentions } from '../api/devotional'
import {
  Home, BookOpen, Settings, LogOut, Flame, Book, Calendar, Trophy,
  PenLine, Lightbulb, HelpCircle, Languages, Menu, X, MoreHorizontal, ChevronDown,
  Sunrise, MessageCircle, ClipboardList, Library, Sprout, UserRound,
} from 'lucide-react'
import { setLanguage } from '../i18n/language'
import ErrorBoundary from './ErrorBoundary'
import QuickCaptureModal from './QuickCaptureModal'

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

  const [mobileOpen, setMobileOpen] = useState(false)
  const [moreOpen, setMoreOpen] = useState(false)
  const moreRef = useRef<HTMLDivElement>(null)
  const moreButtonRef = useRef<HTMLButtonElement>(null)
  const mobileButtonRef = useRef<HTMLButtonElement>(null)

  // `tourId` becomes data-tour-id. The same id appears on the desktop link and on
  // the phone-menu link; only one of the two is ever visible, and the onboarding
  // tour spotlights the visible one.
  // Shown in the desktop row.
  const primaryItems = [
    { path: '/', tourId: 'nav-dashboard', icon: Home, label: t('nav.dashboard') },
    { path: '/journal', tourId: 'nav-journal', icon: BookOpen, label: t('nav.journal') },
    { path: '/study', tourId: 'nav-study', icon: Library, label: t('nav.study') },
    { path: '/devotional', tourId: 'nav-devotional', icon: Book, label: t('nav.focus') },
    { path: '/progress', tourId: 'nav-progress', icon: Trophy, label: t('nav.progress') },
  ]
  // Under "More" on desktop; listed in full in the mobile menu.
  // Reading plans moved here to make room for Study in the row.
  const secondaryItems = [
    { path: '/profile', tourId: 'nav-profile', icon: UserRound, label: t('nav.profile') },
    { path: '/growth', tourId: 'nav-growth', icon: Sprout, label: t('nav.growth') },
    { path: '/plans', tourId: 'nav-plans', icon: Calendar, label: t('nav.readingPlans') },
    { path: '/reflection', tourId: 'nav-reflection', icon: Sunrise, label: t('nav.reflection') },
    { path: '/threads', tourId: 'nav-threads', icon: MessageCircle, label: t('nav.threads') },
    { path: '/insights', tourId: 'nav-insights', icon: Lightbulb, label: t('nav.insights') },
    { path: '/audit', tourId: 'nav-audit', icon: ClipboardList, label: t('audit.navLabel') },
  ]
  const settingsItem = { path: '/settings', tourId: 'nav-settings', icon: Settings, label: t('nav.settings') }

  const isActivePath = (path: string) =>
    location.pathname === path || (path !== '/' && location.pathname.startsWith(`${path}/`))

  const toggleLanguage = () => {
    // Saved on this device so the choice survives a reload.
    setLanguage(i18n.language === 'es' ? 'en' : 'es')
  }

  // Menus close when the route changes.
  useEffect(() => {
    setMobileOpen(false)
    setMoreOpen(false)
  }, [location.pathname])

  // Esc closes whichever menu is open and returns focus to its button;
  // a click outside closes the desktop "More" menu.
  useEffect(() => {
    if (!mobileOpen && !moreOpen) return
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key !== 'Escape') return
      if (mobileOpen) {
        setMobileOpen(false)
        mobileButtonRef.current?.focus()
      }
      if (moreOpen) {
        setMoreOpen(false)
        moreButtonRef.current?.focus()
      }
    }
    const onPointerDown = (event: MouseEvent) => {
      if (moreOpen && moreRef.current && !moreRef.current.contains(event.target as Node)) {
        setMoreOpen(false)
      }
    }
    document.addEventListener('keydown', onKeyDown)
    document.addEventListener('mousedown', onPointerDown)
    return () => {
      document.removeEventListener('keydown', onKeyDown)
      document.removeEventListener('mousedown', onPointerDown)
    }
  }, [mobileOpen, moreOpen])

  const linkClass = (active: boolean) =>
    `flex items-center gap-2 px-3 py-2 rounded-lg transition-colors whitespace-nowrap focus:outline-none focus:ring-2 focus:ring-accent-primary ${
      active ? 'bg-bg-elevated text-accent-primary' : 'text-text-secondary hover:text-text-primary'
    }`
  const iconButtonClass =
    'flex shrink-0 items-center gap-1 rounded-lg px-2.5 py-2 text-text-secondary transition-colors hover:text-text-primary focus:outline-none focus:ring-2 focus:ring-accent-primary'
  const moreActive = secondaryItems.some((item) => isActivePath(item.path))

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
          <div className="flex items-center justify-between gap-2 h-16">
            <Link
              to="/"
              className="flex min-w-0 items-center gap-2 focus:outline-none focus:ring-2 focus:ring-accent-primary rounded-lg"
              aria-label={t('nav.homeLabel')}
            >
              <Flame className="w-8 h-8 shrink-0 text-accent-primary" aria-hidden="true" />
              <span className="truncate text-lg sm:text-xl font-bold text-text-primary">
                Devotional Journal
              </span>
            </Link>

            <div className="flex shrink-0 items-center gap-1">
              {/* Desktop row (md and up). Labels appear once there is room for them. */}
              <div className="hidden md:flex items-center gap-1">
                {primaryItems.map((item) => {
                  const active = isActivePath(item.path)
                  return (
                    <Link
                      key={item.path}
                      to={item.path}
                      data-tour-id={item.tourId}
                      aria-current={active ? 'page' : undefined}
                      title={item.label}
                      className={linkClass(active)}
                    >
                      <item.icon className="w-5 h-5" aria-hidden="true" />
                      <span className="sr-only xl:not-sr-only">{item.label}</span>
                    </Link>
                  )
                })}

                <div className="relative" ref={moreRef}>
                  <button
                    ref={moreButtonRef}
                    type="button"
                    onClick={() => setMoreOpen((open) => !open)}
                    aria-expanded={moreOpen}
                    aria-controls="nav-more-menu"
                    data-tour-id="nav-more"
                    title={t('nav.more')}
                    className={linkClass(moreActive)}
                  >
                    <MoreHorizontal className="w-5 h-5" aria-hidden="true" />
                    <span className="sr-only xl:not-sr-only">{t('nav.more')}</span>
                    <ChevronDown
                      className={`w-4 h-4 transition-transform ${moreOpen ? 'rotate-180' : ''}`}
                      aria-hidden="true"
                    />
                  </button>
                  {moreOpen && (
                    <ul
                      id="nav-more-menu"
                      className="absolute right-0 top-full z-50 mt-2 w-56 rounded-xl border border-border bg-bg-surface p-2 shadow-lg"
                    >
                      {secondaryItems.map((item) => {
                        const active = isActivePath(item.path)
                        return (
                          <li key={item.path}>
                            <Link
                              to={item.path}
                              data-tour-id={item.tourId}
                              aria-current={active ? 'page' : undefined}
                              onClick={() => setMoreOpen(false)}
                              className={linkClass(active)}
                            >
                              <item.icon className="w-5 h-5" aria-hidden="true" />
                              <span>{item.label}</span>
                            </Link>
                          </li>
                        )
                      })}
                    </ul>
                  )}
                </div>
              </div>

              {/* Always visible on every screen size (onboarding tour targets). */}
              <button
                type="button"
                data-tour-id="language"
                onClick={toggleLanguage}
                className={iconButtonClass}
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
                aria-current={location.pathname === '/help' ? 'page' : undefined}
                className={`${iconButtonClass} ${location.pathname === '/help' ? 'bg-bg-elevated !text-accent-primary' : ''}`}
                title={t('nav.help', 'Help & Guide')}
                aria-label={t('nav.help', 'Help & Guide')}
              >
                <HelpCircle className="w-5 h-5" aria-hidden="true" />
              </Link>

              <Link
                to={settingsItem.path}
                data-tour-id={settingsItem.tourId}
                aria-current={isActivePath(settingsItem.path) ? 'page' : undefined}
                className={`hidden md:flex ${iconButtonClass} ${isActivePath(settingsItem.path) ? 'bg-bg-elevated !text-accent-primary' : ''}`}
                title={settingsItem.label}
                aria-label={settingsItem.label}
              >
                <Settings className="w-5 h-5" aria-hidden="true" />
              </Link>

              <button
                type="button"
                onClick={logout}
                className={`hidden md:flex ${iconButtonClass} hover:!text-danger`}
                title={t('auth.logout')}
              >
                <LogOut className="w-5 h-5" aria-hidden="true" />
                <span className="sr-only xl:not-sr-only">{t('auth.logout')}</span>
              </button>

              {/* Phone: everything else lives behind the menu button. */}
              <button
                ref={mobileButtonRef}
                type="button"
                onClick={() => setMobileOpen((open) => !open)}
                aria-expanded={mobileOpen}
                aria-controls="nav-mobile-menu"
                data-tour-id="nav-menu"
                aria-label={mobileOpen ? t('nav.closeMenu') : t('nav.openMenu')}
                className={`md:hidden ${iconButtonClass}`}
              >
                {mobileOpen ? (
                  <X className="w-6 h-6" aria-hidden="true" />
                ) : (
                  <Menu className="w-6 h-6" aria-hidden="true" />
                )}
              </button>
            </div>
          </div>

          {mobileOpen && (
            <ul id="nav-mobile-menu" className="md:hidden border-t border-border py-2 space-y-1">
              {[...primaryItems, ...secondaryItems, settingsItem].map((item) => {
                const active = isActivePath(item.path)
                return (
                  <li key={item.path}>
                    <Link
                      to={item.path}
                      data-tour-id={item.tourId}
                      aria-current={active ? 'page' : undefined}
                      onClick={() => setMobileOpen(false)}
                      className={linkClass(active)}
                    >
                      <item.icon className="w-5 h-5" aria-hidden="true" />
                      <span>{item.label}</span>
                    </Link>
                  </li>
                )
              })}
              <li>
                <button
                  type="button"
                  onClick={logout}
                  className="flex w-full items-center gap-2 px-3 py-2 rounded-lg text-text-secondary transition-colors hover:text-danger focus:outline-none focus:ring-2 focus:ring-accent-primary"
                >
                  <LogOut className="w-5 h-5" aria-hidden="true" />
                  <span>{t('auth.logout')}</span>
                </button>
              </li>
            </ul>
          )}
        </div>
      </nav>

      <main id="main-content" className="max-w-6xl mx-auto px-4 py-8">
        {/* A crash in one page shows a recovery card instead of a blank app. */}
        <ErrorBoundary resetKey={location.pathname}>
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
