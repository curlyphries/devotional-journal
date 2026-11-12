import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { Info } from 'lucide-react'
import { isAiUsable, useAiStatus } from '../hooks/useAiStatus'

/**
 * One-line notice shown when AI features will not work right now
 * (provider unreachable, not configured, or cloud consent missing).
 * Renders nothing while loading or when AI is available.
 */
export default function AiStatusBanner({ className = '' }: { className?: string }) {
  const { t } = useTranslation()
  const { data: status } = useAiStatus()

  if (!status || isAiUsable(status)) return null

  const reason = status.consent_required
    ? t('errors.ai.consentRequired')
    : !status.configured
      ? t('errors.ai.notConfigured')
      : t('errors.ai.unreachable', { backend: status.backend })

  return (
    <div
      role="status"
      className={`rounded-xl border border-border bg-bg-surface px-4 py-3 flex items-start gap-3 text-sm ${className}`}
    >
      <Info className="w-5 h-5 text-accent-primary shrink-0 mt-0.5" aria-hidden="true" />
      <p className="min-w-0 flex-1 text-text-primary break-words">
        {reason}{' '}
        <span className="text-text-secondary">{status.suggestion || t('errors.ai.fallbackNote')}</span>{' '}
        <Link to="/settings#ai-provider" className="text-accent-primary hover:underline whitespace-nowrap">
          {t('errors.ai.settingsLink')}
        </Link>
      </p>
    </div>
  )
}
