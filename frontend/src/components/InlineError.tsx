import { AlertTriangle, RefreshCw } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import { toApiError } from '../api/errors'

interface InlineErrorProps {
  /** Whatever the request threw; normalised through toApiError. */
  error: unknown
  /** When given, a "Try again" button is shown. */
  onRetry?: () => void
  /** Short heading saying what could not be done, e.g. "Couldn't load your reviews". */
  title?: string
  className?: string
}

/** Inline error block for a failed query or action: what happened, what to do, and a reference. */
export default function InlineError({ error, onRetry, title, className = '' }: InlineErrorProps) {
  const { t } = useTranslation()
  const apiError = toApiError(error)
  const reference = [apiError.code, apiError.requestId && t('errors.reference', { ref: apiError.requestId })]
    .filter(Boolean)
    .join(' · ')

  return (
    <div
      role="alert"
      className={`rounded-xl border border-danger bg-bg-surface p-4 flex gap-3 text-sm ${className}`}
    >
      <AlertTriangle className="w-5 h-5 text-red-400 shrink-0 mt-0.5" aria-hidden="true" />
      <div className="min-w-0 flex-1">
        <p className="font-medium text-text-primary break-words">{title ?? t('errors.defaultTitle')}</p>
        <p className="text-text-primary mt-1 break-words">{apiError.message}</p>
        {apiError.suggestion && (
          <p className="text-text-secondary mt-1 break-words">{apiError.suggestion}</p>
        )}
        {reference && (
          <p className="text-text-secondary/80 mt-1 text-xs font-mono break-all">{reference}</p>
        )}
        {onRetry && (
          <button
            type="button"
            onClick={onRetry}
            className="btn-secondary mt-3 inline-flex items-center gap-2 text-sm"
          >
            <RefreshCw className="w-4 h-4" aria-hidden="true" />
            {t('errors.retry')}
          </button>
        )}
      </div>
    </div>
  )
}
