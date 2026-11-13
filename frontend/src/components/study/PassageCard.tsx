import { useId } from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { BookOpen, ExternalLink, RefreshCw, ShieldCheck } from 'lucide-react'
import type { GuideNotice, LessonPassage } from '../../api/guides'

interface PassageCardProps {
  /** Always known, even when the text could not be fetched. */
  reference: string
  passage: LessonPassage | null
  /** Why the text is missing, when it is. */
  error: GuideNotice | null
  onRetry: () => void
  retrying?: boolean
}

/**
 * The lesson's Bible passage. The text comes from the Bible source (never from
 * the AI); when it could not be fetched the reference is still shown, with
 * what happened and a way to try again.
 */
export default function PassageCard({ reference, passage, error, onRetry, retrying = false }: PassageCardProps) {
  const { t } = useTranslation()
  const headingId = useId()
  const shownReference = passage?.reference || reference
  const bibleLink = (
    <Link
      to={`/bible?passage=${encodeURIComponent(shownReference)}`}
      className="inline-flex items-center gap-1.5 text-accent-primary underline-offset-2 hover:underline"
    >
      {t('feedback.scripture.open')}
      <ExternalLink className="h-3.5 w-3.5" aria-hidden="true" />
    </Link>
  )

  return (
    <section aria-labelledby={headingId} className="rounded-xl border border-border bg-bg-elevated/50 p-4 sm:p-6">
      <div className="mb-4 flex flex-wrap items-start justify-between gap-2">
        <div className="flex min-w-0 items-center gap-2">
          <BookOpen className="h-5 w-5 shrink-0 text-accent-primary" aria-hidden="true" />
          <h3 id={headingId} className="break-words text-lg font-semibold text-text-primary">
            {shownReference}
          </h3>
        </div>
        {passage?.verified && (
          <span
            className="inline-flex items-center gap-1.5 rounded-full border border-success bg-success/20 px-2.5 py-1 text-xs font-medium text-text-primary"
            title={t('feedback.scripture.verifiedHelp')}
          >
            <ShieldCheck className="h-3.5 w-3.5" aria-hidden="true" />
            {t('feedback.scripture.verified', { translation: passage.translation_name || passage.translation })}
            <span className="sr-only"> — {t('feedback.scripture.verifiedHelp')}</span>
          </span>
        )}
      </div>

      {passage ? (
        <>
          <blockquote className="scripture-text whitespace-pre-wrap text-text-primary sm:text-xl sm:leading-9">
            {passage.text}
          </blockquote>
          <div className="mt-4 flex flex-wrap items-center justify-between gap-2 text-sm">
            <span className="text-text-secondary">
              {passage.translation_name || passage.translation}
              {passage.translation_name && passage.translation ? ` (${passage.translation})` : ''}
            </span>
            {bibleLink}
          </div>
          {!passage.verified && (
            <p className="mt-2 text-xs text-text-secondary">{t('feedback.scripture.unverified')}</p>
          )}
        </>
      ) : (
        <div role="alert" className="space-y-1 text-sm leading-relaxed">
          <p className="font-medium text-text-primary">{t('study.passage.missingTitle')}</p>
          <p className="text-text-primary">{error?.message || t('feedback.scripture.missing')}</p>
          {error?.suggestion && <p className="text-text-secondary">{error.suggestion}</p>}
          {error?.code && <p className="font-mono text-xs text-text-secondary/80">{error.code}</p>}
          <div className="flex flex-wrap items-center gap-x-4 gap-y-2 pt-2">
            <button
              type="button"
              onClick={onRetry}
              disabled={retrying}
              className="btn-secondary inline-flex items-center gap-2 text-sm disabled:opacity-60"
            >
              <RefreshCw className={`h-4 w-4 ${retrying ? 'animate-spin' : ''}`} aria-hidden="true" />
              {t('errors.retry')}
            </button>
            {bibleLink}
          </div>
        </div>
      )}
    </section>
  )
}
