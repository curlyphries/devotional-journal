import { useId, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { ArrowRight, ChevronRight, Library, Loader2, RotateCcw, Search, Sparkles, Users, X } from 'lucide-react'
import {
  getCatalog,
  getProfileBasics,
  getRecommendations,
  getStudies,
  guidesKeys,
  guidesLang,
  setLifeStage,
  type LifeStage,
  type Study,
  type TopicCard,
} from '../api/guides'
import InlineError from '../components/InlineError'
import { useToast } from '../components/Toast'
import TopicCardView from '../components/study/TopicCardView'
import { useStartStudy } from '../components/study/useStartStudy'
import { formatDate } from '../lib/dates'

/** Lower-case and strip accents, so "oracion" finds "oración". */
function fold(value: string): string {
  return value
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .toLowerCase()
}

function SectionHeading({ id, title, hint }: { id: string; title: string; hint?: string }) {
  return (
    <div className="mb-3">
      <h2 id={id} className="text-lg font-semibold text-text-primary">
        {title}
      </h2>
      {hint && <p className="mt-1 text-sm leading-relaxed text-text-secondary">{hint}</p>}
    </div>
  )
}

function CardSkeleton({ count = 3 }: { count?: number }) {
  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3" aria-hidden="true">
      {Array.from({ length: count }, (_, index) => (
        <div key={index} className="animate-pulse rounded-xl border border-border bg-bg-surface p-5">
          <div className="h-4 w-2/3 rounded bg-bg-elevated" />
          <div className="mt-3 h-3 w-full rounded bg-bg-elevated" />
          <div className="mt-2 h-3 w-5/6 rounded bg-bg-elevated" />
          <div className="mt-5 h-9 w-28 rounded-lg bg-bg-elevated" />
        </div>
      ))}
    </div>
  )
}

/** First visit: ask who the studies are for before showing the library. */
function LifeStagePrompt({
  stages,
  savingStage,
  onChoose,
  onSkip,
}: {
  stages: LifeStage[]
  savingStage: string | null
  onChoose: (stage: string) => void
  onSkip: () => void
}) {
  const { t } = useTranslation()
  const headingId = useId()

  return (
    <section aria-labelledby={headingId} className="card p-4 sm:p-6">
      <div className="flex items-start gap-3">
        <Users className="mt-0.5 h-6 w-6 shrink-0 text-accent-primary" aria-hidden="true" />
        <div className="min-w-0">
          <h2 id={headingId} className="text-lg font-semibold text-text-primary">
            {t('study.firstRun.title')}
          </h2>
          <p className="mt-1 leading-relaxed text-text-secondary">{t('study.firstRun.body')}</p>
        </div>
      </div>

      <ul className="mt-4 grid gap-3 sm:grid-cols-2">
        {stages.map((stage) => (
          <li key={stage.key}>
            <button
              type="button"
              onClick={() => onChoose(stage.key)}
              disabled={savingStage !== null}
              className="flex h-full w-full items-start gap-3 rounded-xl border border-border bg-bg-elevated/60 p-4 text-left transition-colors hover:border-accent-primary focus:outline-none focus:ring-2 focus:ring-accent-primary disabled:opacity-60"
            >
              <span className="min-w-0 flex-1">
                <span className="block font-medium text-text-primary">{stage.title}</span>
                <span className="mt-1 block text-sm leading-relaxed text-text-secondary">{stage.note}</span>
              </span>
              {savingStage === stage.key ? (
                <Loader2 className="mt-0.5 h-4 w-4 shrink-0 animate-spin text-accent-primary" aria-hidden="true" />
              ) : (
                <ChevronRight className="mt-0.5 h-4 w-4 shrink-0 text-text-secondary" aria-hidden="true" />
              )}
            </button>
          </li>
        ))}
      </ul>

      <div className="mt-4 flex flex-wrap items-center gap-x-5 gap-y-2 text-sm">
        <Link to="/profile" className="text-accent-primary underline-offset-2 hover:underline">
          {t('study.tellUsMore')}
        </Link>
        <button
          type="button"
          onClick={onSkip}
          className="text-text-secondary underline-offset-2 hover:text-text-primary hover:underline"
        >
          {t('study.firstRun.skip')}
        </button>
      </div>
      <p className="mt-3 text-xs leading-relaxed text-text-secondary">{t('study.firstRun.privacy')}</p>
    </section>
  )
}

function ContinueCard({ study }: { study: Study }) {
  const { t } = useTranslation()
  const current = Math.min(Math.max(study.current_lesson, 1), study.lesson_count)
  const percent = Math.min(Math.max(study.progress_percent, 0), 100)

  return (
    <article className="flex min-w-0 flex-col rounded-xl border border-border bg-bg-surface p-4 sm:p-5">
      <h3 className="break-words text-base font-semibold leading-snug text-text-primary">{study.topic.title}</h3>
      <p className="mt-1 text-sm text-text-secondary">{t('study.lessonOf', { current, total: study.lesson_count })}</p>
      <div
        className="mt-3 h-2 w-full overflow-hidden rounded-full bg-bg-elevated"
        role="progressbar"
        aria-valuemin={0}
        aria-valuemax={100}
        aria-valuenow={percent}
        aria-label={t('study.hub.progressLabel', { title: study.topic.title })}
      >
        <div className="h-full rounded-full bg-accent-primary transition-all" style={{ width: `${percent}%` }} />
      </div>
      <div className="mt-4">
        <Link
          to={`/study/${study.id}`}
          aria-label={t('study.card.continueNamed', { title: study.topic.title })}
          className="btn-primary inline-flex items-center gap-2 text-sm"
        >
          {t('study.card.continue')}
          <ArrowRight className="h-4 w-4" aria-hidden="true" />
        </Link>
      </div>
    </article>
  )
}

/**
 * Bible study guide (`/study`): the front door to the library. Asks who the
 * studies are for, then shows what is in progress, what is suggested (and
 * why), and the whole catalog to browse or search.
 */
export default function StudyHubPage() {
  const { t, i18n } = useTranslation()
  const lang = guidesLang()
  const queryClient = useQueryClient()
  const toast = useToast()
  const stageSelectId = useId()
  const searchId = useId()
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState<string | null>(null)
  const [everyAge, setEveryAge] = useState(false)
  const [stageSkipped, setStageSkipped] = useState(false)

  const profile = useQuery({ queryKey: guidesKeys.profileBasics(), queryFn: getProfileBasics })
  const catalog = useQuery({ queryKey: guidesKeys.catalog(lang), queryFn: getCatalog })
  const recommendations = useQuery({ queryKey: guidesKeys.recommendations(lang), queryFn: getRecommendations })
  const studies = useQuery({ queryKey: guidesKeys.studies(lang), queryFn: getStudies })
  const start = useStartStudy()

  const stageMutation = useMutation({
    mutationFn: (stage: string) => setLifeStage(stage),
    onSuccess: (basics) => {
      queryClient.setQueryData(guidesKeys.profileBasics(), basics)
      // Stage notes, suggestions and which studies fit all depend on the life stage.
      // (The profile basics were just set from the server's answer.)
      const basicsKey = guidesKeys.profileBasics().join('/')
      queryClient.invalidateQueries({
        queryKey: guidesKeys.all,
        predicate: (query) => query.queryKey.join('/') !== basicsKey,
      })
    },
    onError: (err) => toast.fromError(err, t('study.hub.stageFailed')),
  })

  const lifeStage = profile.data?.life_stage ?? null
  const stages = catalog.data?.life_stages ?? []
  const currentStage = stages.find((stage) => stage.key === lifeStage) ?? null
  const needsStage = profile.isSuccess && !lifeStage && !stageSkipped
  const filterByStage = !!lifeStage && !everyAge

  const groups = useMemo(() => {
    const needle = fold(search.trim())
    return (catalog.data?.categories ?? [])
      .filter((group) => !category || group.key === category)
      .map((group) => ({
        ...group,
        topics: group.topics.filter(
          (topic) =>
            (!filterByStage || topic.stages.includes(lifeStage!)) &&
            (!needle || fold(`${topic.title} ${topic.summary}`).includes(needle))
        ),
      }))
      .filter((group) => group.topics.length > 0)
  }, [catalog.data, category, search, filterByStage, lifeStage])

  const matchCount = groups.reduce((sum, group) => sum + group.topics.length, 0)
  const selectedCategory = catalog.data?.categories.find((group) => group.key === category) ?? null
  const activeStudies = (studies.data ?? []).filter((study) => study.status === 'active')
  const completedStudies = (studies.data ?? []).filter((study) => study.status === 'completed')
  const startingKey = start.isPending ? start.variables : null
  const onStart = (topic: TopicCard) => start.mutate(topic.key)

  const chipClass = (selected: boolean) =>
    `rounded-full border px-3.5 py-1.5 text-sm transition-colors focus:outline-none focus:ring-2 focus:ring-accent-primary ${
      selected
        ? 'border-accent-primary bg-accent-primary/15 font-medium text-text-primary'
        : 'border-border bg-bg-surface text-text-secondary hover:border-text-secondary hover:text-text-primary'
    }`

  const header = (
    <header className="space-y-2">
      <div className="flex items-center gap-2">
        <Library className="h-7 w-7 shrink-0 text-accent-primary" aria-hidden="true" />
        <h1 className="text-2xl font-bold text-text-primary">{t('study.hub.title')}</h1>
      </div>
      <p className="max-w-2xl leading-relaxed text-text-secondary">{t('study.hub.intro')}</p>
    </header>
  )

  if (catalog.isLoading || profile.isLoading) {
    return (
      <div className="space-y-6">
        {header}
        <div role="status">
          <span className="sr-only">{t('common.loading')}</span>
          <CardSkeleton count={6} />
        </div>
      </div>
    )
  }

  if (catalog.isError || !catalog.data) {
    return (
      <div className="space-y-6">
        {header}
        <InlineError
          error={catalog.error ?? new Error(t('study.hub.catalogFailed'))}
          title={t('study.hub.catalogFailed')}
          onRetry={() => catalog.refetch()}
        />
      </div>
    )
  }

  if (needsStage) {
    return (
      <div className="space-y-6">
        {header}
        <LifeStagePrompt
          stages={stages}
          savingStage={stageMutation.isPending ? (stageMutation.variables ?? null) : null}
          onChoose={(stage) => stageMutation.mutate(stage)}
          onSkip={() => setStageSkipped(true)}
        />
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {header}

      {profile.isError && (
        <InlineError
          error={profile.error}
          title={t('study.hub.profileFailed')}
          onRetry={() => profile.refetch()}
        />
      )}

      {/* Who is this for? */}
      <div className="rounded-xl border border-border bg-bg-surface px-4 py-3 text-sm">
        <div className="flex flex-wrap items-center gap-x-3 gap-y-2">
          <label htmlFor={stageSelectId} className="flex items-center gap-2 font-medium text-text-primary">
            <Users className="h-4 w-4 text-accent-primary" aria-hidden="true" />
            {t('study.whoFor.label')}
          </label>
          <select
            id={stageSelectId}
            value={lifeStage ?? ''}
            disabled={stageMutation.isPending}
            onChange={(event) => event.target.value && stageMutation.mutate(event.target.value)}
            className="input max-w-full py-1.5 pl-3 pr-8 text-sm"
          >
            {!lifeStage && <option value="">{t('study.whoFor.choose')}</option>}
            {stages.map((stage) => (
              <option key={stage.key} value={stage.key}>
                {stage.title}
              </option>
            ))}
          </select>
          {stageMutation.isPending && (
            <Loader2 className="h-4 w-4 animate-spin text-accent-primary" aria-hidden="true" />
          )}
          <Link to="/profile" className="text-accent-primary underline-offset-2 hover:underline">
            {t('study.tellUsMore')}
          </Link>
        </div>
        <p className="mt-2 leading-relaxed text-text-secondary">
          {currentStage ? currentStage.note : t('study.whoFor.unset')}
        </p>
      </div>

      {/* Continue */}
      {studies.isError && (
        <InlineError error={studies.error} title={t('study.hub.studiesFailed')} onRetry={() => studies.refetch()} />
      )}
      {activeStudies.length > 0 && (
        <section aria-labelledby="study-continue">
          <SectionHeading id="study-continue" title={t('study.hub.continueTitle')} />
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {activeStudies.map((study) => (
              <ContinueCard key={study.id} study={study} />
            ))}
          </div>
        </section>
      )}

      {/* Suggested for you */}
      <section aria-labelledby="study-suggested">
        <div className="mb-3 flex items-start gap-2">
          <Sparkles className="mt-1 h-5 w-5 shrink-0 text-accent-primary" aria-hidden="true" />
          <div className="min-w-0">
            <h2 id="study-suggested" className="text-lg font-semibold text-text-primary">
              {t('study.hub.suggestedTitle')}
            </h2>
            <p className="mt-1 text-sm leading-relaxed text-text-secondary">{t('study.hub.suggestedHint')}</p>
          </div>
        </div>

        {recommendations.isLoading ? (
          <div role="status">
            <span className="sr-only">{t('common.loading')}</span>
            <CardSkeleton />
          </div>
        ) : recommendations.isError ? (
          <InlineError
            error={recommendations.error}
            title={t('study.hub.suggestedFailed')}
            onRetry={() => recommendations.refetch()}
          />
        ) : recommendations.data && recommendations.data.results.length > 0 ? (
          <>
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {recommendations.data.results.map((item) => (
                <TopicCardView
                  key={item.topic.key}
                  topic={item.topic}
                  reasons={item.reasons}
                  onStart={onStart}
                  busy={startingKey === item.topic.key}
                  disabled={start.isPending}
                />
              ))}
            </div>
            <p className="mt-3 text-xs leading-relaxed text-text-secondary">
              {recommendations.data.based_on.entries_considered > 0
                ? t('study.hub.basedOnEntries', { count: recommendations.data.based_on.entries_considered })
                : t('study.hub.basedOnNoEntries')}{' '}
              {recommendations.data.based_on.has_profile ? t('study.hub.basedOnProfile') : t('study.hub.basedOnNoProfile')}{' '}
              <Link to="/profile" className="text-accent-primary underline-offset-2 hover:underline">
                {t('study.hub.profileLink')}
              </Link>
            </p>
          </>
        ) : (
          <div className="rounded-xl border border-dashed border-border bg-bg-surface p-5 text-sm leading-relaxed">
            <p className="font-medium text-text-primary">{t('study.hub.suggestedEmptyTitle')}</p>
            <p className="mt-1 text-text-secondary">{t('study.hub.suggestedEmptyBody')}</p>
            <div className="mt-3 flex flex-wrap gap-x-5 gap-y-2">
              <Link to="/journal/new" className="text-accent-primary underline-offset-2 hover:underline">
                {t('study.hub.writeEntry')}
              </Link>
              <Link to="/profile" className="text-accent-primary underline-offset-2 hover:underline">
                {t('study.tellUsMore')}
              </Link>
            </div>
          </div>
        )}
      </section>

      {/* Find a study */}
      <section aria-labelledby="study-find">
        <SectionHeading id="study-find" title={t('study.hub.findTitle')} hint={t('study.hub.findHint')} />

        <div className="space-y-4">
          <div className="relative max-w-md">
            <label htmlFor={searchId} className="sr-only">
              {t('study.hub.searchLabel')}
            </label>
            <Search
              className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-text-secondary"
              aria-hidden="true"
            />
            <input
              id={searchId}
              type="search"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder={t('study.hub.searchPlaceholder')}
              className="input w-full pl-9"
            />
          </div>

          <div>
            <p id="study-need-label" className="mb-2 text-sm font-medium text-text-primary">
              {t('study.hub.needLabel')}
            </p>
            <div className="flex flex-wrap gap-2" role="group" aria-labelledby="study-need-label">
              <button
                type="button"
                aria-pressed={category === null}
                onClick={() => setCategory(null)}
                className={chipClass(category === null)}
              >
                {t('study.hub.allCategories')}
              </button>
              {catalog.data.categories.map((group) => (
                <button
                  key={group.key}
                  type="button"
                  aria-pressed={category === group.key}
                  title={group.summary}
                  onClick={() => setCategory(category === group.key ? null : group.key)}
                  className={chipClass(category === group.key)}
                >
                  {group.title}
                </button>
              ))}
            </div>
            {selectedCategory && (
              <p className="mt-2 text-sm leading-relaxed text-text-secondary">{selectedCategory.summary}</p>
            )}
          </div>

          <div className="flex flex-wrap items-center justify-between gap-x-6 gap-y-2 text-sm">
            {lifeStage ? (
              <label className="inline-flex cursor-pointer items-center gap-2 text-text-primary">
                <input
                  type="checkbox"
                  checked={everyAge}
                  onChange={(event) => setEveryAge(event.target.checked)}
                  className="h-4 w-4 rounded border-border accent-accent-primary"
                />
                {t('study.hub.everyAge')}
              </label>
            ) : (
              <span className="text-text-secondary">{t('study.hub.everyAgeShown')}</span>
            )}
            <p role="status" className="text-text-secondary">
              {t('study.hub.matchCount', { count: matchCount })}
            </p>
          </div>
        </div>

        {groups.length === 0 ? (
          <div className="mt-5 rounded-xl border border-dashed border-border bg-bg-surface p-5 text-sm leading-relaxed">
            <p className="font-medium text-text-primary">{t('study.hub.noMatchTitle')}</p>
            <p className="mt-1 text-text-secondary">
              {filterByStage ? t('study.hub.noMatchBodyStage') : t('study.hub.noMatchBody')}
            </p>
            <div className="mt-3 flex flex-wrap gap-3">
              {(search || category) && (
                <button
                  type="button"
                  className="btn-secondary inline-flex items-center gap-2 text-sm"
                  onClick={() => {
                    setSearch('')
                    setCategory(null)
                  }}
                >
                  <X className="h-4 w-4" aria-hidden="true" />
                  {t('study.hub.clearFilters')}
                </button>
              )}
              {filterByStage && (
                <button type="button" className="btn-secondary text-sm" onClick={() => setEveryAge(true)}>
                  {t('study.hub.everyAge')}
                </button>
              )}
            </div>
          </div>
        ) : (
          <div className="mt-6 space-y-8">
            {groups.map((group) => (
              <section key={group.key} aria-labelledby={`study-category-${group.key}`}>
                <h3 id={`study-category-${group.key}`} className="text-base font-semibold text-text-primary">
                  {group.title}
                </h3>
                <p className="mb-3 mt-0.5 text-sm text-text-secondary">{group.summary}</p>
                <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                  {group.topics.map((topic) => (
                    <TopicCardView
                      key={topic.key}
                      topic={topic}
                      headingLevel="h4"
                      onStart={onStart}
                      busy={startingKey === topic.key}
                      disabled={start.isPending}
                    />
                  ))}
                </div>
              </section>
            ))}
          </div>
        )}
      </section>

      {/* Completed */}
      {completedStudies.length > 0 && (
        <details className="group rounded-xl border border-border bg-bg-surface">
          <summary className="flex cursor-pointer list-none items-center gap-2 rounded-xl px-4 py-3 font-medium text-text-primary hover:bg-bg-elevated focus:outline-none focus-visible:ring-2 focus-visible:ring-accent-primary [&::-webkit-details-marker]:hidden">
            <ChevronRight
              className="h-4 w-4 shrink-0 text-text-secondary transition-transform group-open:rotate-90"
              aria-hidden="true"
            />
            {t('study.hub.completedTitle', { count: completedStudies.length })}
          </summary>
          <ul className="divide-y divide-border border-t border-border">
            {completedStudies.map((study) => (
              <li key={study.id} className="flex flex-wrap items-center justify-between gap-x-4 gap-y-2 px-4 py-3">
                <div className="min-w-0">
                  <Link
                    to={`/study/${study.id}`}
                    className="break-words font-medium text-text-primary underline-offset-2 hover:text-accent-primary hover:underline"
                  >
                    {study.topic.title}
                  </Link>
                  {study.completed_at && (
                    <p className="text-xs text-text-secondary">
                      {t('study.hub.completedOn', { date: formatDate(study.completed_at, i18n.language) })}
                    </p>
                  )}
                </div>
                <button
                  type="button"
                  onClick={() => start.mutate(study.topic.key)}
                  disabled={start.isPending}
                  aria-label={t('study.card.againNamed', { title: study.topic.title })}
                  className="btn-secondary inline-flex items-center gap-2 text-sm disabled:opacity-60"
                >
                  {startingKey === study.topic.key ? (
                    <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
                  ) : (
                    <RotateCcw className="h-4 w-4" aria-hidden="true" />
                  )}
                  {t('study.card.again')}
                </button>
              </li>
            ))}
          </ul>
        </details>
      )}
    </div>
  )
}
