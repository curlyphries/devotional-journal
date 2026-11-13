import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useQuery } from '@tanstack/react-query'
import { ChevronRight, Library, Loader2 } from 'lucide-react'
import { getRecommendations, getStudies, guidesKeys, guidesLang } from '../../api/guides'
import { useStartStudy } from './useStartStudy'

/**
 * Dashboard entry to the Bible study guide: continue the study in progress,
 * or start the top suggestion (with why it is suggested), or browse.
 * If the study service cannot be reached it falls back to the plain
 * "Find a study" link — it never blocks or breaks the dashboard.
 */
export default function StudyDashboardCard() {
  const { t } = useTranslation()
  const lang = guidesLang()
  const start = useStartStudy()

  const studies = useQuery({ queryKey: guidesKeys.studies(lang), queryFn: getStudies, retry: false })
  const active = (studies.data ?? []).find((study) => study.status === 'active') ?? null

  const recommendations = useQuery({
    queryKey: guidesKeys.recommendations(lang),
    queryFn: getRecommendations,
    retry: false,
    // Only needed when there is nothing to continue.
    enabled: !studies.isLoading && !active,
  })
  const suggestion = !active ? (recommendations.data?.results[0] ?? null) : null

  const frame = 'card flex min-w-0 flex-wrap items-center gap-x-4 gap-y-3 p-4 sm:p-5'
  const icon = (
    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-accent-primary/15">
      <Library className="h-5 w-5 text-accent-primary" aria-hidden="true" />
    </div>
  )
  const eyebrow = (
    <p className="text-xs font-semibold uppercase tracking-wider text-text-secondary">{t('dashboard.study.title')}</p>
  )

  if (studies.isLoading || recommendations.isLoading) {
    return (
      <section data-tour-id="study-card" aria-label={t('dashboard.study.title')} aria-busy="true" className={frame}>
        {icon}
        <div className="min-w-0 flex-1 basis-48">
          {eyebrow}
          <div className="mt-2 h-4 w-2/3 animate-pulse rounded bg-bg-elevated" />
          <div className="mt-2 h-3 w-1/2 animate-pulse rounded bg-bg-elevated" />
        </div>
      </section>
    )
  }

  if (active) {
    const current = Math.min(Math.max(active.current_lesson, 1), active.lesson_count)
    return (
      <section data-tour-id="study-card" aria-label={t('dashboard.study.title')} className={frame}>
        {icon}
        <div className="min-w-0 flex-1 basis-48">
          {eyebrow}
          <p className="break-words font-medium text-text-primary">
            {t('dashboard.study.continue', { title: active.topic.title })}
          </p>
          <p className="text-sm text-text-secondary">
            {t('study.lessonOf', { current, total: active.lesson_count })}
          </p>
        </div>
        <Link to={`/study/${active.id}`} className="btn-primary inline-flex items-center gap-1 text-sm">
          {t('study.card.continue')}
          <ChevronRight className="h-4 w-4" aria-hidden="true" />
        </Link>
      </section>
    )
  }

  if (suggestion) {
    return (
      <section data-tour-id="study-card" aria-label={t('dashboard.study.title')} className={frame}>
        {icon}
        <div className="min-w-0 flex-1 basis-48">
          {eyebrow}
          <p className="break-words font-medium text-text-primary">
            {t('dashboard.study.suggested', { title: suggestion.topic.title })}
          </p>
          {suggestion.reasons[0] && (
            <p className="text-sm leading-relaxed text-text-secondary">
              {t('dashboard.study.why')} {suggestion.reasons[0]}
            </p>
          )}
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <button
            type="button"
            onClick={() => start.mutate(suggestion.topic.key)}
            disabled={start.isPending}
            aria-label={t('study.card.startNamed', { title: suggestion.topic.title })}
            className="btn-primary inline-flex items-center gap-2 text-sm disabled:opacity-60"
          >
            {start.isPending && <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />}
            {t('dashboard.study.start')}
          </button>
          <Link to="/study" className="text-sm text-accent-primary underline-offset-2 hover:underline">
            {t('dashboard.study.browse')}
          </Link>
        </div>
      </section>
    )
  }

  return (
    <section data-tour-id="study-card" aria-label={t('dashboard.study.title')} className={frame}>
      {icon}
      <div className="min-w-0 flex-1 basis-48">
        {eyebrow}
        <p className="font-medium text-text-primary">{t('dashboard.study.find')}</p>
        <p className="text-sm leading-relaxed text-text-secondary">{t('dashboard.study.findSub')}</p>
      </div>
      <Link to="/study" className="btn-secondary inline-flex items-center gap-1 text-sm">
        {t('dashboard.study.open')}
        <ChevronRight className="h-4 w-4" aria-hidden="true" />
      </Link>
    </section>
  )
}
