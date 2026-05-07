import { useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { Navigate, useSearchParams } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { requestMagicLink, devLogin } from '../api/auth'
import { Flame, Mail, Zap, Lock, Languages, Sparkles, Github } from 'lucide-react'

const API_URL = import.meta.env.VITE_API_URL || 'https://devotionaljournal.net/api/v1'

export default function LoginPage() {
  const { t, i18n } = useTranslation()
  const { isAuthenticated, login } = useAuth()
  const [searchParams] = useSearchParams()
  const [email, setEmail] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isSent, setIsSent] = useState(false)
  const [error, setError] = useState('')
  const [showEmailForm, setShowEmailForm] = useState(false)

  // Handle Google OAuth errors from redirect
  useEffect(() => {
    const errorParam = searchParams.get('error')
    if (errorParam) {
      const errorMessages: Record<string, string> = {
        'google_auth_failed': 'Google authentication failed. Please try again.',
        'no_code': 'Authentication was cancelled.',
        'invalid_state': 'Security validation failed. Please try again.',
        'token_exchange_failed': 'Failed to complete authentication.',
        'userinfo_failed': 'Failed to get user information from Google.',
        'no_email': 'No email provided by Google.',
        'timeout': 'Authentication timed out. Please try again.',
        'server_error': 'Server error. Please try again later.',
      }
      setError(errorMessages[errorParam] || 'Authentication failed.')
    }
  }, [searchParams])

  if (isAuthenticated) {
    return <Navigate to="/" />
  }

  const handleGoogleLogin = () => {
    window.location.href = `${API_URL}/auth/google/login/`
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      await requestMagicLink(email)
      setIsSent(true)
    } catch {
      setError('Failed to send magic link. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleDevLogin = async () => {
    setIsLoading(true)
    setError('')

    try {
      const tokens = await devLogin(email || 'dev@homelab.local')
      login(tokens.access_token, tokens.refresh_token)
    } catch {
      setError('Dev login failed. Is the backend running in DEBUG mode?')
    } finally {
      setIsLoading(false)
    }
  }

  const toggleLanguage = () => {
    const next = i18n.language === 'es' ? 'en' : 'es'
    i18n.changeLanguage(next)
  }

  return (
    <div className="min-h-screen bg-bg-primary flex flex-col items-center justify-center px-4 py-8">
      {/* Top-right utilities */}
      <div className="absolute top-4 right-4 flex items-center gap-2">
        <button
          onClick={toggleLanguage}
          className="flex items-center gap-1.5 px-3 py-1.5 text-sm text-text-secondary hover:text-text-primary border border-border rounded-lg transition-colors"
          aria-label="Change language"
        >
          <Languages className="w-4 h-4" />
          <span>{i18n.language === 'es' ? 'EN' : 'ES'}</span>
        </button>
      </div>

      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <Flame className="w-16 h-16 text-accent-primary mx-auto mb-4" />
          <h1 className="text-3xl font-bold text-text-primary mb-2">
            {t('login.title', 'Devotional Journal')}
          </h1>
          <p className="text-text-secondary text-base">
            {t('login.tagline', 'Daily Bible rhythm. Spiritual focus. Encrypted journaling.')}
          </p>
        </div>

        <div className="card">
          {isSent ? (
            <div className="text-center py-8">
              <Mail className="w-12 h-12 text-success mx-auto mb-4" />
              <h2 className="text-xl font-semibold text-text-primary mb-2">
                {t('login.checkEmailHeading', 'Check your email')}
              </h2>
              <p className="text-text-secondary">
                {t('auth.magicLinkSent')}
              </p>
              <button
                type="button"
                onClick={() => { setIsSent(false); setEmail(''); setError('') }}
                className="text-sm text-accent-primary hover:underline mt-4"
              >
                {t('login.useAnotherEmail', 'Use a different email')}
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              {/* Google — primary method */}
              <button
                type="button"
                onClick={handleGoogleLogin}
                disabled={isLoading}
                className="w-full py-3 px-4 bg-white text-gray-700 border border-gray-300 rounded-lg font-medium hover:bg-gray-50 disabled:opacity-50 flex items-center justify-center gap-3 transition-colors"
              >
                <svg className="w-5 h-5" viewBox="0 0 24 24" aria-hidden="true">
                  <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
                  <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
                  <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
                  <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
                </svg>
                {t('login.continueWithGoogle', 'Continue with Google')}
              </button>

              <div className="relative my-2">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-border-primary"></div>
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-2 bg-bg-secondary text-text-secondary">{t('login.or', 'or')}</span>
                </div>
              </div>

              {/* Magic link — secondary */}
              {!showEmailForm ? (
                <button
                  type="button"
                  onClick={() => setShowEmailForm(true)}
                  className="w-full py-3 px-4 bg-bg-elevated text-text-primary border border-border rounded-lg font-medium hover:bg-bg-surface flex items-center justify-center gap-2 transition-colors"
                >
                  <Mail className="w-4 h-4" />
                  {t('login.continueWithEmail', 'Continue with email')}
                </button>
              ) : (
                <form onSubmit={handleSubmit} className="space-y-3">
                  <div>
                    <label htmlFor="email" className="sr-only">{t('auth.email')}</label>
                    <input
                      type="email"
                      id="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder={t('auth.emailPlaceholder')}
                      className="input w-full"
                      required
                      autoFocus
                    />
                  </div>

                  <button
                    type="submit"
                    disabled={isLoading}
                    className="btn-primary w-full"
                  >
                    {isLoading ? t('common.loading') : t('auth.sendMagicLink')}
                  </button>

                  <p className="text-xs text-text-secondary text-center">
                    {t('login.magicLinkExplainer', "We'll email you a one-tap sign-in link. No password to remember.")}
                  </p>
                </form>
              )}

              {error && (
                <p className="text-danger text-sm text-center">{error}</p>
              )}

              {import.meta.env.DEV && (
                <>
                  <div className="relative my-3">
                    <div className="absolute inset-0 flex items-center">
                      <div className="w-full border-t border-yellow-500/30"></div>
                    </div>
                    <div className="relative flex justify-center text-sm">
                      <span className="px-2 bg-bg-secondary text-yellow-500">dev only</span>
                    </div>
                  </div>

                  <button
                    type="button"
                    onClick={handleDevLogin}
                    disabled={isLoading}
                    className="w-full py-2 px-4 bg-yellow-500/20 text-yellow-500 border border-yellow-500/30 rounded-lg font-medium hover:bg-yellow-500/30 flex items-center justify-center gap-2"
                  >
                    <Zap className="w-4 h-4" />
                    Dev Login (DEBUG only)
                  </button>
                </>
              )}
            </div>
          )}
        </div>

        {/* Trust signals */}
        <div className="mt-6 grid grid-cols-3 gap-3 text-center">
          <div className="flex flex-col items-center gap-1.5 p-3 rounded-lg border border-border/60">
            <Lock className="w-5 h-5 text-accent-primary" aria-hidden="true" />
            <span className="text-xs text-text-secondary leading-tight">
              {t('login.trust.encrypted', 'End-to-end encrypted journal')}
            </span>
          </div>
          <div className="flex flex-col items-center gap-1.5 p-3 rounded-lg border border-border/60">
            <Languages className="w-5 h-5 text-accent-primary" aria-hidden="true" />
            <span className="text-xs text-text-secondary leading-tight">
              {t('login.trust.bilingual', 'Bilingual EN / ES')}
            </span>
          </div>
          <div className="flex flex-col items-center gap-1.5 p-3 rounded-lg border border-border/60">
            <Sparkles className="w-5 h-5 text-accent-primary" aria-hidden="true" />
            <span className="text-xs text-text-secondary leading-tight">
              {t('login.trust.byoai', 'Bring your own AI')}
            </span>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-6 flex items-center justify-center gap-4 text-xs text-text-secondary">
          <a
            href="https://github.com/curlyphries/devotional-journal"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1 hover:text-text-primary transition-colors"
          >
            <Github className="w-3.5 h-3.5" />
            <span>{t('login.footer.source', 'Source')}</span>
          </a>
          <span aria-hidden="true">·</span>
          <a
            href="https://github.com/curlyphries/devotional-journal/blob/master/PRIVACY.md"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-text-primary transition-colors"
          >
            {t('login.footer.privacy', 'Privacy')}
          </a>
          <span aria-hidden="true">·</span>
          <a
            href="https://github.com/curlyphries/devotional-journal/blob/master/LICENSE"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-text-primary transition-colors"
          >
            AGPL-3.0
          </a>
        </div>
      </div>
    </div>
  )
}
