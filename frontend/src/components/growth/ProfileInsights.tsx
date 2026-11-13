import { useId } from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useMutation } from '@tanstack/react-query'
import { Check, Info, Lightbulb, Loader2, RefreshCw, Sparkles, X } from 'lucide-react'
import {
  generateProfileInsights,
  sendInsightFeedback,
  type GrowthProfile,
  type ProfileInsightItem,
} from '../../api/profile'
import { toApiError } from '../../api/errors'
import { formatDateTime } from '../../lib/dates'
import AiStatusBanner from '../AiStatusBanner'
import InlineError from '../InlineError'
import { useToast } from '../Toast'
import TopicStudyCard from './TopicStudyCard'
import { AiRanLine, useAiWhereSentence } from './aiWhere'
import { Notice } from './primitives'
import { useApplyProfile } from './useGrowthProfile'

const feedbackButton =
  'inline-flex items-center gap-1.5 rounded-lg border px-3 py-1.5 text-sm transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-accent-primary disabled:opacity-60'
// Both answers look the same when chosen: agreeing is not "good" and disagreeing is not "bad".
const feedbackOn = 'border-accent-primary bg-accent-primary/20 text-text-primary'
const feedbackOff = 'border-border text-text-secondary hover:text-text-primary'

/**
 * "What the app notices": the reflection the AI writes from the person's own
 * answers. Each statement shows what it is based on and can be confirmed or
 * rejected. The disclaimer is always visible.
 */
export default function ProfileInsights({ profile }: { profile: GrowthProfile }) {
  const { t, i18n } = useTranslation()
  const toast = useToast()
  const applyProfile = useApplyProfile()
  const whereSentence = useAiWhereSentence()
  const headingId = useId()
  const insights = profile.insights

  const generate = useMutation({
    mutationFn: generateProfileInsights,
    onSuccess: (updated) => applyProfile(updated),
  })

  const feedback = useMutation({
    mutationFn: ({ id, accurate }: { id: string; accurate: boolean | null }) => sendInsightFeedback(id, accurate),
    onSuccess: (updated) => applyProfile(updated),
    onError: (err) => toast.fromError(err, t('profile.insights.feedbackFailed')),
  })

  const generateError = generate.isError ? toApiError(generate.error) : null
  // "Not enough to go on yet" is guidance about what to do next, not a failure.
  const notEnoughYet = generateError?.status === 400

  const answer = (item: ProfileInsightItem, accurate: boolean) =>
    feedback.mutate({ id: item.id, accurate: item.accurate === accurate ? null : accurate })

  const progress = (
    <div role="status" aria-live="polite" className="flex items-start gap-3 py-1">
      <Loader2 className="mt-0.5 h-5 w-5 flex-shrink-0 animate-spin text-accent-primary" aria-hidden="true" />
      <div>
        <p className="font-medium text-text-primary">{t('profile.insights.writing')}</p>
        <p className="mt-1 text-sm text-text-secondary">{t('profile.insights.patience')}</p>
      </div>
    </div>
  )

  const problem =
    generateError && !generate.isPending ? (
      notEnoughYet ? (
        <Notice role="status" icon={<Info className="h-5 w-5" aria-hidden="true" />} title={t('profile.insights.notEnoughTitle')}>
          <p className="text-text-primary">{generateError.suggestion || generateError.message}</p>
          {generateError.suggestion && generateError.message !== generateError.suggestion && (
            <p className="text-text-secondary">{generateError.message}</p>
          )}
        </Notice>
      ) : (
        <InlineError error={generate.error} title={t('profile.insights.failed')} onRetry={() => generate.mutate()} />
      )
    ) : null

  const disclaimer = profile.disclaimer ? (
    <p className="border-t border-border pt-4 text-sm leading-relaxed text-text-secondary">{profile.disclaimer}</p>
  ) : null

  return (
    <section className="card space-y-5 p-4 sm:p-6" aria-labelledby={headingId}>
      <div className="flex items-center gap-2">
        <Sparkles className="h-5 w-5 flex-shrink-0 text-accent-primary" aria-hidden="true" />
        <h2 id={headingId} className="text-lg font-semibold text-text-primary">
          {t('profile.insights.title')}
        </h2>
      </div>

      {!insights ? (
        <>
          <p className="leading-relaxed text-text-secondary">
            {t('profile.insights.explain')} {whereSentence}
          </p>
          <AiStatusBanner />
          {generate.isPending ? (
            progress
          ) : (
            <>
              {problem}
              <button
                type="button"
                className="btn-primary inline-flex items-center gap-2"
                onClick={() => generate.mutate()}
              >
                <Sparkles className="h-4 w-4" aria-hidden="true" />
                {t('profile.insights.generate')}
              </button>
            </>
          )}
        </>
      ) : (
        <>
          {generate.isPending && progress}
          {problem}

          <p className="whitespace-pre-wrap leading-relaxed text-text-primary">{insights.summary}</p>

          {insights.items.length > 0 && (
            <ul className="space-y-3" aria-label={t('profile.insights.itemsLabel')}>
              {insights.items.map((item) => {
                const busy = feedback.isPending && feedback.variables?.id === item.id
                return (
                  <li key={item.id} className="rounded-xl border border-border bg-bg-elevated/50 p-4">
                    <p className="text-xs font-semibold uppercase tracking-wider text-text-secondary">
                      {item.area === 'inner' ? t('profile.inner.title') : t('profile.walk.title')}
                    </p>
                    <h3 className="mt-1 font-semibold text-text-primary">{item.title}</h3>
                    <p className="mt-1 whitespace-pre-wrap leading-relaxed text-text-primary">{item.text}</p>
                    {item.evidence?.length > 0 && (
                      <div className="mt-3">
                        <p className="text-sm font-medium text-text-secondary">{t('profile.insights.basedOn')}</p>
                        <ul className="mt-1 list-disc space-y-0.5 pl-5 text-sm text-text-secondary">
                          {item.evidence.map((line, index) => (
                            <li key={index}>{line}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    <div
                      className="mt-3 flex flex-wrap items-center gap-2"
                      role="group"
                      aria-label={t('profile.insights.feedbackLabel', { title: item.title })}
                    >
                      <button
                        type="button"
                        aria-pressed={item.accurate === true}
                        disabled={busy}
                        onClick={() => answer(item, true)}
                        className={`${feedbackButton} ${item.accurate === true ? feedbackOn : feedbackOff}`}
                      >
                        <Check className="h-4 w-4" aria-hidden="true" />
                        {t('profile.insights.right')}
                      </button>
                      <button
                        type="button"
                        aria-pressed={item.accurate === false}
                        disabled={busy}
                        onClick={() => answer(item, false)}
                        className={`${feedbackButton} ${item.accurate === false ? feedbackOn : feedbackOff}`}
                      >
                        <X className="h-4 w-4" aria-hidden="true" />
                        {t('profile.insights.notMe')}
                      </button>
                      {item.accurate != null && (
                        <span className="text-xs text-text-secondary" role="status">
                          {item.accurate ? t('profile.insights.savedRight') : t('profile.insights.savedNotMe')}
                        </span>
                      )}
                    </div>
                  </li>
                )
              })}
            </ul>
          )}

          {insights.encouragement && (
            <p className="whitespace-pre-wrap rounded-xl border border-border p-4 font-serif text-lg italic leading-relaxed text-text-primary">
              {insights.encouragement}
            </p>
          )}

          {insights.suggested_topics?.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold uppercase tracking-wider text-text-secondary">
                {t('profile.insights.suggestedTopics')}
              </h3>
              <ul className="mt-2 grid gap-3 sm:grid-cols-2">
                {insights.suggested_topics.map((topic) => (
                  <TopicStudyCard key={topic.key} topic={topic} headingLevel="h4" />
                ))}
              </ul>
              <p className="mt-2 text-sm">
                <Link to="/study" className="text-accent-primary underline-offset-2 hover:underline">
                  {t('profile.insights.allStudies')}
                </Link>
              </p>
            </div>
          )}

          {insights.suggested_traits?.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold uppercase tracking-wider text-text-secondary">
                {t('profile.insights.suggestedTraits')}
              </h3>
              <p className="mt-1 text-sm text-text-secondary">{t('profile.insights.suggestedTraitsHint')}</p>
              <ul className="mt-2 flex flex-wrap gap-2">
                {insights.suggested_traits.map((trait) => (
                  <li key={trait.key}>
                    <Link
                      to={`/growth?trait=${encodeURIComponent(trait.key)}`}
                      className="btn-secondary inline-flex items-center gap-2 text-sm"
                      aria-label={t('profile.insights.startPlanFor', { trait: trait.title })}
                    >
                      <Lightbulb className="h-4 w-4 text-accent-primary" aria-hidden="true" />
                      {trait.title}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          )}

          <div className="flex flex-col gap-3 border-t border-border pt-4 sm:flex-row sm:items-center sm:justify-between">
            <div className="min-w-0 space-y-1">
              <AiRanLine provider={insights.provider} model={insights.model} local={insights.local} />
              <p className="text-xs text-text-secondary">
                {t('profile.insights.generatedAt', { date: formatDateTime(insights.generated_at, i18n.language) })}
              </p>
            </div>
            <button
              type="button"
              className="btn-secondary inline-flex items-center gap-2 self-start text-sm disabled:opacity-60 sm:self-auto"
              disabled={generate.isPending}
              onClick={() => generate.mutate()}
              title={whereSentence}
            >
              <RefreshCw className="h-4 w-4" aria-hidden="true" />
              {t('profile.insights.refresh')}
            </button>
          </div>
        </>
      )}

      {disclaimer}
    </section>
  )
}
