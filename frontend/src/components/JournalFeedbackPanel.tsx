import { useEffect, useId, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import {
  BookOpen,
  ExternalLink,
  Footprints,
  Info,
  Loader2,
  RefreshCw,
  ShieldCheck,
  Sparkles,
  ThumbsDown,
  ThumbsUp,
  TrendingUp,
} from 'lucide-react'
import {
  generateJournalFeedback,
  getJournalFeedback,
  rateJournalFeedback,
  type JournalFeedback,
} from '../api/journal'
import { toApiError } from '../api/errors'
import { useToast } from './Toast'
import InlineError from './InlineError'
import DecisionRecord from './DecisionRecord'

// Re-exported so pages can import the disclosure from either place.
export { default as DecisionRecord } from './DecisionRecord'

export const feedbackQueryKey = (entryId: string) => ['journalFeedback', entryId] as const

const PROGRESS_KEYS = [
  'feedback.progress.reading',
  'feedback.progress.choosing',
  'feedback.progress.checking',
]
const PROGRESS_STEP_MS = 7000

interface JournalFeedbackPanelProps {
  entryId: string
  /** Generate feedback straight away when the entry has none yet. */
  autoGenerate?: boolean
  /** The entry's text was edited after this feedback was written: offer "Update feedback". */
  entryChanged?: boolean
  /** Called after feedback is (re)generated. */
  onGenerated?: (feedback: JournalFeedback) => void
}

/**
 * The response to a journal entry: a reflection, a scripture whose text comes
 * from the Bible source, why it was chosen, and the full decision record.
 */
export default function JournalFeedbackPanel({
  entryId,
  autoGenerate = false,
  entryChanged = false,
  onGenerated,
}: JournalFeedbackPanelProps) {
  const { t } = useTranslation()
  const toast = useToast()
  const queryClient = useQueryClient()
  const headingId = useId()
  const [confirmingRegenerate, setConfirmingRegenerate] = useState(false)
  const [progressStep, setProgressStep] = useState(0)
  const autoStartedFor = useRef<string | null>(null)

  // null = no feedback has been generated for this entry yet (the server's 404).
  const existing = useQuery<JournalFeedback | null>({
    queryKey: feedbackQueryKey(entryId),
    queryFn: async () => {
      try {
        return await getJournalFeedback(entryId)
      } catch (err) {
        if (toApiError(err).status === 404) return null
        throw err
      }
    },
    retry: false,
    staleTime: 60_000,
  })

  const generate = useMutation({
    mutationFn: (regenerate: boolean) => generateJournalFeedback(entryId, { regenerate }),
    onSuccess: (feedback) => {
      queryClient.setQueryData(feedbackQueryKey(entryId), feedback)
      queryClient.invalidateQueries({ queryKey: ['journalEntries'] })
      queryClient.invalidateQueries({ queryKey: ['feedbackLog'] })
      queryClient.invalidateQueries({ queryKey: ['journalThemes'] })
      setConfirmingRegenerate(false)
      onGenerated?.(feedback)
    },
  })

  const rate = useMutation({
    mutationFn: ({ id, helpful }: { id: string; helpful: boolean | null }) => rateJournalFeedback(id, helpful),
    onSuccess: (feedback) => {
      queryClient.setQueryData(feedbackQueryKey(entryId), feedback)
      queryClient.invalidateQueries({ queryKey: ['feedbackLog'] })
    },
    onError: (err) => toast.fromError(err, t('feedback.rateFailed')),
  })

  const { mutate: runGenerate, isPending: isGenerating } = generate
  const hasNoFeedback = existing.isSuccess && existing.data === null

  // First visit after saving: start generating without making the user ask.
  useEffect(() => {
    if (!autoGenerate || !hasNoFeedback) return
    if (autoStartedFor.current === entryId) return
    autoStartedFor.current = entryId
    runGenerate(false)
  }, [autoGenerate, hasNoFeedback, entryId, runGenerate])

  // Walk through the progress messages while waiting; stay on the last one.
  useEffect(() => {
    if (!isGenerating) {
      setProgressStep(0)
      return
    }
    const timer = setInterval(() => {
      setProgressStep((step) => Math.min(step + 1, PROGRESS_KEYS.length - 1))
    }, PROGRESS_STEP_MS)
    return () => clearInterval(timer)
  }, [isGenerating])

  const feedback = existing.data ?? null

  const header = (
    <div className="mb-4 flex items-center gap-2">
      <Sparkles className="h-5 w-5 text-accent-primary" aria-hidden="true" />
      <h2 id={headingId} className="text-lg font-semibold text-text-primary">
        {t('feedback.title')}
      </h2>
    </div>
  )

  const progress = (
    <div role="status" aria-live="polite" className="flex items-start gap-3 py-2">
      <Loader2 className="mt-0.5 h-5 w-5 flex-shrink-0 animate-spin text-accent-primary" aria-hidden="true" />
      <div>
        <p className="font-medium text-text-primary">{t(PROGRESS_KEYS[progressStep])}</p>
        <p className="mt-1 text-sm text-text-secondary">{t('feedback.progress.patience')}</p>
      </div>
    </div>
  )

  let body: React.ReactNode

  if (existing.isLoading) {
    body = (
      <div role="status" className="flex items-center gap-3 py-2 text-text-secondary">
        <Loader2 className="h-5 w-5 animate-spin" aria-hidden="true" />
        {t('feedback.loading')}
      </div>
    )
  } else if (existing.isError) {
    body = (
      <InlineError
        error={existing.error}
        title={t('feedback.loadFailed')}
        onRetry={() => existing.refetch()}
      />
    )
  } else if (!feedback) {
    body = isGenerating ? (
      progress
    ) : generate.isError ? (
      <InlineError
        error={generate.error}
        title={t('feedback.generateFailed')}
        onRetry={() => runGenerate(false)}
      />
    ) : (
      <div className="space-y-3">
        <p className="text-text-secondary">{t('feedback.emptyBody')}</p>
        <button type="button" className="btn-primary inline-flex items-center gap-2" onClick={() => runGenerate(false)}>
          <Sparkles className="h-4 w-4" aria-hidden="true" />
          {t('feedback.get')}
        </button>
      </div>
    )
  } else {
    const isFallback = feedback.status === 'fallback'
    const scripture = feedback.scripture
    const fallbackReason = feedback.audit?.fallback_reason

    body = (
      <div className="space-y-6">
        {isGenerating && progress}

        {generate.isError && !isGenerating && (
          <InlineError
            error={generate.error}
            title={t('feedback.generateFailed')}
            onRetry={() => runGenerate(true)}
          />
        )}

        {isFallback && (
          <div role="note" className="rounded-xl border border-accent-secondary bg-accent-secondary/10 p-4 text-sm">
            <div className="flex items-start gap-3">
              <Info className="mt-0.5 h-5 w-5 flex-shrink-0 text-accent-primary" aria-hidden="true" />
              <div className="min-w-0 space-y-1">
                <p className="font-semibold text-text-primary">{t('feedback.fallback.title')}</p>
                <p className="text-text-primary">{t('feedback.fallback.body')}</p>
                {fallbackReason?.message && (
                  <p className="text-text-secondary">
                    {t('feedback.fallback.reason')} {fallbackReason.message}
                  </p>
                )}
                {fallbackReason?.suggestion && <p className="text-text-secondary">{fallbackReason.suggestion}</p>}
                <div className="flex flex-wrap items-center gap-3 pt-2">
                  <button
                    type="button"
                    className="btn-secondary inline-flex items-center gap-2 text-sm"
                    disabled={isGenerating}
                    onClick={() => runGenerate(true)}
                  >
                    <RefreshCw className="h-4 w-4" aria-hidden="true" />
                    {t('feedback.fallback.retry')}
                  </button>
                  <Link to="/settings" className="text-accent-primary underline-offset-2 hover:underline">
                    {t('feedback.fallback.settings')}
                  </Link>
                </div>
              </div>
            </div>
          </div>
        )}

        {entryChanged && !isGenerating && (
          <div className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-border bg-bg-elevated p-4 text-sm">
            <p className="text-text-primary">{t('feedback.changed')}</p>
            <button
              type="button"
              className="btn-secondary inline-flex items-center gap-2 text-sm"
              onClick={() => runGenerate(true)}
            >
              <RefreshCw className="h-4 w-4" aria-hidden="true" />
              {t('feedback.update')}
            </button>
          </div>
        )}

        {/* Reflection */}
        <section aria-labelledby={`${headingId}-reflection`}>
          <h3 id={`${headingId}-reflection`} className="mb-2 text-sm font-semibold uppercase tracking-wider text-text-secondary">
            {t('feedback.reflection')}
          </h3>
          <p className="whitespace-pre-wrap leading-relaxed text-text-primary">{feedback.reflection}</p>
          {!feedback.is_spiritual && (
            <p className="mt-2 text-sm text-text-secondary">{t('feedback.everyday')}</p>
          )}
          {feedback.themes?.length > 0 && (
            <ul className="mt-3 flex flex-wrap gap-2" aria-label={t('feedback.themes')}>
              {feedback.themes.map((theme) => (
                <li
                  key={theme}
                  className="rounded-full border border-border bg-bg-elevated px-3 py-1 text-xs text-text-primary"
                >
                  {theme}
                </li>
              ))}
            </ul>
          )}
        </section>

        {/* Scripture */}
        <section aria-labelledby={`${headingId}-scripture`} className="rounded-xl border border-border bg-bg-elevated/50 p-4 sm:p-5">
          <div className="mb-3 flex flex-wrap items-start justify-between gap-2">
            <div className="flex items-center gap-2">
              <BookOpen className="h-5 w-5 flex-shrink-0 text-accent-primary" aria-hidden="true" />
              <h3 id={`${headingId}-scripture`} className="text-lg font-semibold text-text-primary">
                {scripture ? scripture.reference : t('feedback.scripture.heading')}
              </h3>
            </div>
            {scripture?.verified && (
              <span
                className="inline-flex items-center gap-1.5 rounded-full border border-success bg-success/20 px-2.5 py-1 text-xs font-medium text-text-primary"
                title={t('feedback.scripture.verifiedHelp')}
              >
                <ShieldCheck className="h-3.5 w-3.5" aria-hidden="true" />
                {t('feedback.scripture.verified', { translation: scripture.translation_name || scripture.translation })}
                <span className="sr-only"> — {t('feedback.scripture.verifiedHelp')}</span>
              </span>
            )}
          </div>

          {scripture ? (
            <>
              <blockquote className="scripture-text whitespace-pre-wrap text-text-primary">{scripture.text}</blockquote>
              <div className="mt-3 flex flex-wrap items-center justify-between gap-2 text-sm">
                <span className="text-text-secondary">
                  {scripture.translation_name || scripture.translation}
                  {scripture.translation_name && scripture.translation ? ` (${scripture.translation})` : ''}
                </span>
                <Link
                  to={`/bible?passage=${encodeURIComponent(scripture.reference)}`}
                  className="inline-flex items-center gap-1.5 text-accent-primary underline-offset-2 hover:underline"
                >
                  {t('feedback.scripture.open')}
                  <ExternalLink className="h-3.5 w-3.5" aria-hidden="true" />
                </Link>
              </div>
              {!scripture.verified && (
                <p className="mt-2 text-xs text-text-secondary">{t('feedback.scripture.unverified')}</p>
              )}
            </>
          ) : (
            <p className="text-sm text-text-secondary">{t('feedback.scripture.missing')}</p>
          )}
        </section>

        {feedback.why_this_passage && (
          <section aria-labelledby={`${headingId}-why`}>
            <h3 id={`${headingId}-why`} className="mb-2 text-sm font-semibold uppercase tracking-wider text-text-secondary">
              {t('feedback.why')}
            </h3>
            <p className="whitespace-pre-wrap leading-relaxed text-text-primary">{feedback.why_this_passage}</p>
          </section>
        )}

        {feedback.meditation_prompt && (
          <section aria-labelledby={`${headingId}-meditate`}>
            <h3 id={`${headingId}-meditate`} className="mb-2 text-sm font-semibold uppercase tracking-wider text-text-secondary">
              {t('feedback.meditate')}
            </h3>
            <p className="whitespace-pre-wrap font-serif text-lg italic leading-relaxed text-text-primary">
              {feedback.meditation_prompt}
            </p>
          </section>
        )}

        {feedback.christlike_step && (
          <section aria-labelledby={`${headingId}-step`} className="rounded-xl border border-border p-4">
            <h3 id={`${headingId}-step`} className="mb-2 flex items-center gap-2 text-sm font-semibold uppercase tracking-wider text-text-secondary">
              <Footprints className="h-4 w-4 text-accent-primary" aria-hidden="true" />
              {t('feedback.step')}
            </h3>
            <p className="whitespace-pre-wrap leading-relaxed text-text-primary">{feedback.christlike_step}</p>
          </section>
        )}

        {feedback.growth_note?.trim() && (
          <section aria-labelledby={`${headingId}-growth`}>
            <h3 id={`${headingId}-growth`} className="mb-2 flex items-center gap-2 text-sm font-semibold uppercase tracking-wider text-text-secondary">
              <TrendingUp className="h-4 w-4 text-accent-primary" aria-hidden="true" />
              {t('feedback.growth')}
            </h3>
            <p className="whitespace-pre-wrap leading-relaxed text-text-primary">{feedback.growth_note}</p>
          </section>
        )}

        <DecisionRecord feedback={feedback} />

        {/* Rating and regenerate */}
        <div className="flex flex-col gap-4 border-t border-border pt-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex flex-wrap items-center gap-2" role="group" aria-label={t('feedback.helpful.question')}>
            <span className="mr-1 text-sm text-text-secondary">{t('feedback.helpful.question')}</span>
            <button
              type="button"
              aria-pressed={feedback.helpful === true}
              disabled={rate.isPending}
              onClick={() => rate.mutate({ id: feedback.id, helpful: feedback.helpful === true ? null : true })}
              className={`inline-flex items-center gap-1.5 rounded-lg border px-3 py-1.5 text-sm transition-colors focus:outline-none focus:ring-2 focus:ring-accent-primary ${
                feedback.helpful === true
                  ? 'border-success bg-success/25 text-text-primary'
                  : 'border-border text-text-secondary hover:text-text-primary'
              }`}
            >
              <ThumbsUp className="h-4 w-4" aria-hidden="true" />
              {t('feedback.helpful.yes')}
            </button>
            <button
              type="button"
              aria-pressed={feedback.helpful === false}
              disabled={rate.isPending}
              onClick={() => rate.mutate({ id: feedback.id, helpful: feedback.helpful === false ? null : false })}
              className={`inline-flex items-center gap-1.5 rounded-lg border px-3 py-1.5 text-sm transition-colors focus:outline-none focus:ring-2 focus:ring-accent-primary ${
                feedback.helpful === false
                  ? 'border-danger bg-danger/25 text-text-primary'
                  : 'border-border text-text-secondary hover:text-text-primary'
              }`}
            >
              <ThumbsDown className="h-4 w-4" aria-hidden="true" />
              {t('feedback.helpful.no')}
            </button>
            {feedback.helpful !== null && feedback.helpful !== undefined && (
              <span className="text-xs text-text-secondary" role="status">
                {t('feedback.helpful.saved')}
              </span>
            )}
          </div>

          {confirmingRegenerate ? (
            <div className="flex flex-wrap items-center gap-2 text-sm" role="group" aria-label={t('feedback.regenerate.confirm')}>
              <span className="text-text-primary">{t('feedback.regenerate.confirm')}</span>
              <button
                type="button"
                className="btn-primary px-3 py-1.5 text-sm"
                disabled={isGenerating}
                onClick={() => runGenerate(true)}
              >
                {t('feedback.regenerate.yes')}
              </button>
              <button
                type="button"
                className="btn-secondary px-3 py-1.5 text-sm"
                onClick={() => setConfirmingRegenerate(false)}
              >
                {t('common.cancel')}
              </button>
            </div>
          ) : (
            <button
              type="button"
              className="inline-flex items-center gap-2 self-start text-sm text-text-secondary hover:text-text-primary disabled:opacity-50 sm:self-auto"
              disabled={isGenerating}
              onClick={() => setConfirmingRegenerate(true)}
            >
              <RefreshCw className="h-4 w-4" aria-hidden="true" />
              {t('feedback.regenerate.button')}
            </button>
          )}
        </div>
      </div>
    )
  }

  return (
    <section className="card" aria-labelledby={headingId}>
      {header}
      {body}
    </section>
  )
}
