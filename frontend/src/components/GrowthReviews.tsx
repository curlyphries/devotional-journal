import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useTranslation } from 'react-i18next'
import { Loader2, ScrollText, Sparkles } from 'lucide-react'
import { generateGrowthReview, getGrowthReviews } from '../api/reviews'
import { formatDate } from '../lib/dates'
import InlineError from './InlineError'
import { useToast } from './Toast'

const REVIEWS_QUERY_KEY = ['growthReviews'] as const

/** Weekly/monthly reviews of the user's journaling, with a button to write this week's. */
export default function GrowthReviews() {
  const { t, i18n } = useTranslation()
  const queryClient = useQueryClient()
  const toast = useToast()

  const reviewsQuery = useQuery({ queryKey: REVIEWS_QUERY_KEY, queryFn: getGrowthReviews })

  const generateMutation = useMutation({
    mutationFn: () => generateGrowthReview('week'),
    meta: { silent: true }, // the error is rendered inline, next to the button
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: REVIEWS_QUERY_KEY })
      toast.success(t('progress.reviews.generated'))
    },
  })

  const reviews = reviewsQuery.data ?? []

  return (
    <div className="space-y-4">
      <div className="card">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div className="min-w-0">
            <h2 className="text-lg font-semibold text-text-primary flex items-center gap-2">
              <ScrollText className="w-5 h-5 text-accent-primary" aria-hidden="true" />
              {t('progress.reviews.heading')}
            </h2>
            <p className="text-sm text-text-secondary mt-1">{t('progress.reviews.intro')}</p>
          </div>
          <button
            type="button"
            onClick={() => generateMutation.mutate()}
            disabled={generateMutation.isPending}
            className="btn-primary inline-flex items-center gap-2 disabled:opacity-60"
          >
            {generateMutation.isPending ? (
              <Loader2 className="w-4 h-4 animate-spin" aria-hidden="true" />
            ) : (
              <Sparkles className="w-4 h-4" aria-hidden="true" />
            )}
            {generateMutation.isPending ? t('progress.reviews.generating') : t('progress.reviews.generate')}
          </button>
        </div>
        {generateMutation.isPending && (
          <p className="text-sm text-text-secondary mt-3" role="status">
            {t('progress.reviews.generatingHint')}
          </p>
        )}
        {generateMutation.isError && (
          <InlineError
            error={generateMutation.error}
            title={t('progress.reviews.generateFailed')}
            className="mt-4"
          />
        )}
      </div>

      {reviewsQuery.isLoading ? (
        <div className="card flex items-center gap-3 text-text-secondary" role="status">
          <Loader2 className="w-5 h-5 animate-spin text-accent-primary" aria-hidden="true" />
          {t('progress.reviews.loading')}
        </div>
      ) : reviewsQuery.isError ? (
        <InlineError
          error={reviewsQuery.error}
          title={t('progress.reviews.loadFailed')}
          onRetry={() => reviewsQuery.refetch()}
        />
      ) : reviews.length === 0 ? (
        <div className="card text-center">
          <p className="text-text-primary">{t('progress.reviews.emptyTitle')}</p>
          <p className="text-sm text-text-secondary mt-2">{t('progress.reviews.emptyBody')}</p>
        </div>
      ) : (
        <ul className="space-y-4">
          {reviews.map((review) => (
            <li key={review.id} className="card">
              <p className="text-sm font-medium text-accent-primary">
                {review.period_type === 'month'
                  ? t('progress.reviews.periodMonth')
                  : t('progress.reviews.periodWeek')}
                {' · '}
                <span className="text-text-secondary">
                  {t('progress.reviews.range', {
                    start: formatDate(review.period_start, i18n.language, { month: 'short', day: 'numeric' }),
                    end: formatDate(review.period_end, i18n.language, {
                      month: 'short',
                      day: 'numeric',
                      year: 'numeric',
                    }),
                  })}
                </span>
              </p>
              <p className="text-text-primary mt-3 whitespace-pre-wrap leading-relaxed break-words">
                {review.content}
              </p>
              <p className="text-xs text-text-secondary mt-4">
                {t('progress.reviews.generatedBy', {
                  provider: review.provider || t('progress.reviews.unknownProvider'),
                  model: review.model || t('progress.reviews.unknownModel'),
                })}
              </p>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
