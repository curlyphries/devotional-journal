import { useEffect } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import {
  Book, BookOpen, Calendar, HelpCircle, Home, LifeBuoy, Lightbulb, ListChecks, Map as MapIcon, MessagesSquare,
  Mic, PenLine, ScrollText, Settings, ShieldCheck, Sparkles, Sunrise, Trophy, Wrench,
} from 'lucide-react'
import type { LucideIcon } from 'lucide-react'
import { requestTourRestart } from '../components/OnboardingTour'

/**
 * Help & Guide. Section ids are stable deep-link targets:
 * #quick-start, #where, #feedback, #voice, #privacy, #troubleshooting.
 */

const QUICK_START_STEPS = ['1', '2', '3', '4', '5']

const DESTINATIONS: { key: string; to: string; icon: LucideIcon }[] = [
  { key: 'dashboard', to: '/', icon: Home },
  { key: 'journal', to: '/journal/new', icon: PenLine },
  { key: 'history', to: '/journal', icon: BookOpen },
  { key: 'devotional', to: '/devotional', icon: Book },
  { key: 'plans', to: '/plans', icon: Calendar },
  { key: 'bible', to: '/bible', icon: BookOpen },
  { key: 'progress', to: '/progress', icon: Trophy },
  { key: 'reflection', to: '/reflection', icon: Sunrise },
  { key: 'threads', to: '/threads', icon: MessagesSquare },
  { key: 'insights', to: '/insights', icon: Lightbulb },
  { key: 'audit', to: '/audit', icon: ScrollText },
  { key: 'settings', to: '/settings', icon: Settings },
]

/** Error codes shown in error messages; see the API contract. */
const ERROR_CODES = [
  'NETWORK_ERROR',
  'TIMEOUT',
  'NOT_AUTHENTICATED',
  'PERMISSION_DENIED',
  'NOT_FOUND',
  'VALIDATION_ERROR',
  'RATE_LIMITED',
  'SERVER_ERROR',
  'AI_UNAVAILABLE',
  'AI_TIMEOUT',
  'AI_NOT_CONFIGURED',
  'AI_CONSENT_REQUIRED',
  'AI_BAD_RESPONSE',
  'AI_URL_NOT_ALLOWED',
  'SCRIPTURE_UNAVAILABLE',
  'CLIENT_ERROR',
]

const TOC = ['quick-start', 'where', 'feedback', 'voice', 'privacy', 'troubleshooting']

function Section({
  id,
  icon: Icon,
  title,
  children,
}: {
  id: string
  icon: LucideIcon
  title: string
  children: React.ReactNode
}) {
  return (
    <section id={id} aria-labelledby={`${id}-heading`} className="card scroll-mt-6 p-4 sm:p-6">
      <h2 id={`${id}-heading`} className="mb-3 flex items-center gap-2 text-xl font-semibold text-text-primary">
        <Icon className="h-5 w-5 flex-shrink-0 text-accent-primary" aria-hidden="true" />
        {title}
      </h2>
      <div className="space-y-3 leading-relaxed text-text-secondary">{children}</div>
    </section>
  )
}

export default function HelpPage() {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const location = useLocation()

  // Deep links such as /help#troubleshooting: the router does not scroll for us.
  useEffect(() => {
    if (!location.hash) return
    const target = document.getElementById(decodeURIComponent(location.hash.slice(1)))
    if (target && typeof target.scrollIntoView === 'function') target.scrollIntoView({ block: 'start' })
  }, [location.hash])

  const replayTour = () => {
    requestTourRestart()
    navigate('/')
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <header className="space-y-3">
        <div className="flex items-center gap-2">
          <HelpCircle className="h-7 w-7 text-accent-primary" aria-hidden="true" />
          <h1 className="text-2xl font-bold text-text-primary">{t('help.title')}</h1>
        </div>
        <p className="text-text-secondary">{t('help.intro')}</p>
        <div className="flex flex-wrap items-center gap-3">
          <button type="button" onClick={replayTour} className="btn-primary inline-flex items-center gap-2">
            <MapIcon className="h-4 w-4" aria-hidden="true" />
            {t('help.replayTour')}
          </button>
          <Link to="/journal/new" className="btn-secondary inline-flex items-center gap-2">
            <PenLine className="h-4 w-4" aria-hidden="true" />
            {t('help.writeEntry')}
          </Link>
        </div>
        <nav aria-label={t('help.onThisPage')}>
          <ul className="flex flex-wrap gap-x-4 gap-y-1 text-sm">
            {TOC.map((id) => (
              <li key={id}>
                <a href={`#${id}`} className="text-accent-primary underline-offset-2 hover:underline">
                  {t(`help.toc.${id}`)}
                </a>
              </li>
            ))}
          </ul>
        </nav>
      </header>

      <Section id="quick-start" icon={ListChecks} title={t('help.quickStart.title')}>
        <ol className="list-decimal space-y-2 pl-5">
          {QUICK_START_STEPS.map((step) => (
            <li key={step}>
              <span className="font-medium text-text-primary">{t(`help.quickStart.step${step}.title`)}</span>{' '}
              {t(`help.quickStart.step${step}.body`)}
            </li>
          ))}
        </ol>
      </Section>

      <Section id="where" icon={MapIcon} title={t('help.where.title')}>
        <p>{t('help.where.intro')}</p>
        <ul className="grid gap-3 sm:grid-cols-2">
          {DESTINATIONS.map(({ key, to, icon: Icon }) => (
            <li key={key}>
              <Link
                to={to}
                className="flex h-full items-start gap-3 rounded-lg border border-border bg-bg-elevated/50 p-3 transition-colors hover:border-accent-secondary focus:outline-none focus:ring-2 focus:ring-accent-primary"
              >
                <Icon className="mt-0.5 h-5 w-5 flex-shrink-0 text-accent-primary" aria-hidden="true" />
                <span className="min-w-0">
                  <span className="block font-medium text-text-primary">{t(`help.where.${key}.name`)}</span>
                  <span className="block text-sm text-text-secondary">{t(`help.where.${key}.body`)}</span>
                </span>
              </Link>
            </li>
          ))}
        </ul>
      </Section>

      <Section id="feedback" icon={Sparkles} title={t('help.feedback.title')}>
        <p>{t('help.feedback.p1')}</p>
        <p>{t('help.feedback.p2')}</p>
        <p>{t('help.feedback.p3')}</p>
        <p>{t('help.feedback.p4')}</p>
        <p>
          <Link to="/audit" className="text-accent-primary underline-offset-2 hover:underline">
            {t('help.feedback.auditLink')}
          </Link>
        </p>
      </Section>

      <Section id="voice" icon={Mic} title={t('help.voice.title')}>
        <p>{t('help.voice.p1')}</p>
        <p>{t('help.voice.p2')}</p>
        <p>{t('voice.privacy')}</p>
      </Section>

      <Section id="privacy" icon={ShieldCheck} title={t('help.privacy.title')}>
        <ul className="list-disc space-y-2 pl-5">
          <li>{t('help.privacy.local')}</li>
          <li>{t('help.privacy.cloud')}</li>
          <li>{t('help.privacy.consent')}</li>
          <li>{t('help.privacy.encrypted')}</li>
          <li>{t('help.privacy.export')}</li>
        </ul>
        <p>
          <Link to="/settings" className="text-accent-primary underline-offset-2 hover:underline">
            {t('help.privacy.settingsLink')}
          </Link>
        </p>
      </Section>

      <Section id="troubleshooting" icon={Wrench} title={t('help.troubleshooting.title')}>
        <p>{t('help.troubleshooting.intro')}</p>
        <dl className="space-y-3">
          {ERROR_CODES.map((code) => (
            <div key={code} id={`code-${code}`} className="scroll-mt-6 rounded-lg border border-border bg-bg-elevated/50 p-3">
              <dt className="break-all font-mono text-sm font-semibold text-text-primary">{code}</dt>
              <dd className="mt-1 text-sm">
                <p className="text-text-primary">{t(`help.codes.${code}.meaning`)}</p>
                <p className="mt-1 text-text-secondary">
                  <span className="font-medium text-text-primary">{t('help.troubleshooting.whatToDo')}</span>{' '}
                  {t(`help.codes.${code}.fix`)}
                </p>
              </dd>
            </div>
          ))}
        </dl>
        <div className="flex items-start gap-3 rounded-lg border border-accent-secondary bg-accent-secondary/10 p-3">
          <LifeBuoy className="mt-0.5 h-5 w-5 flex-shrink-0 text-accent-primary" aria-hidden="true" />
          <div className="text-sm">
            <p className="font-medium text-text-primary">{t('help.troubleshooting.refTitle')}</p>
            <p>{t('help.troubleshooting.refBody')}</p>
          </div>
        </div>
      </Section>
    </div>
  )
}
