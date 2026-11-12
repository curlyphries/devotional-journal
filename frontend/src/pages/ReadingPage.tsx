import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { useMutation, useQueries, useQuery, useQueryClient } from '@tanstack/react-query'
import { BookOpen, CheckCircle, ChevronLeft, ExternalLink, Loader2, Save } from 'lucide-react'
import { advanceDay, formatPlanPassage, getPlanDetail, getTodayReading } from '../api/plans'
import { getPassage, parsePassageReference } from '../api/bible'
import { createJournalEntry } from '../api/journal'
import { todayLocalISO } from '../lib/dates'
import InlineError from '../components/InlineError'
import { useToast } from '../components/Toast'

const MOODS = [
  { id: 'grateful', emoji: '🙏' },
  { id: 'struggling', emoji: '😔' },
  { id: 'convicted', emoji: '💭' },
  { id: 'peaceful', emoji: '😌' },
  { id: 'fired_up', emoji: '🔥' },
]

interface SaveResult {
  /** Id of the journal entry that was created, if the user wrote anything. */
  entryId: string | null
  /** Set when the entry was saved but the day could not be marked complete. */
  advanceError: unknown
}

/** Today's reading for one plan enrollment: passages, a prompt, and a journal box. */
export default function ReadingPage() {
  const { t, i18n } = useTranslation()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const toast = useToast()
  const { enrollmentId = '' } = useParams<{ enrollmentId: string }>()
  const [journalContent, setJournalContent] = useState('')
  const [selectedMood, setSelectedMood] = useState('')

  const todayQuery = useQuery({
    queryKey: ['todayReading', enrollmentId],
    queryFn: () => getTodayReading(enrollmentId),
    enabled: !!enrollmentId,
  })

  const enrollment = todayQuery.data?.enrollment
  const day = todayQuery.data?.day
  const planId = enrollment?.plan.id ?? ''

  // The plan detail carries each day's id (needed to link the journal entry to
  // the day) and its reflection seed. The page still works if this fails.
  const planQuery = useQuery({
    queryKey: ['plan', planId],
    queryFn: () => getPlanDetail(planId),
    enabled: !!planId,
  })
  const planDay = planQuery.data?.days.find((d) => d.day_number === day?.day_number)
  const planDayId = day?.id ?? planDay?.id
  const reflectionSeed = (day?.reflection_prompts_seed ?? planDay?.reflection_prompts_seed ?? '').trim()

  const references = (Array.isArray(day?.passages) ? day.passages : []).map(formatPlanPassage).filter(Boolean)
  const translation = i18n.language?.startsWith('es') ? 'RV1960' : 'KJV'

  const passageQueries = useQueries({
    queries: references.map((reference) => {
      const parsed = parsePassageReference(reference)
      return {
        queryKey: ['readingPassage', reference, translation],
        queryFn: () =>
          getPassage(parsed!.book, parsed!.chapter, translation, parsed!.verseStart, parsed!.verseEnd),
        enabled: !!parsed,
        staleTime: Infinity, // Bible text does not change
      }
    }),
  })

  const isCompleted = !!enrollment?.completed_at

  const saveMutation = useMutation<SaveResult>({
    mutationFn: async () => {
      const content = journalContent.trim()
      let entryId: string | null = null

      if (content) {
        const entry = await createJournalEntry({
          date: todayLocalISO(),
          content,
          ...(selectedMood && { mood_tag: selectedMood }),
          plan_enrollment: enrollmentId,
          ...(planDayId && { plan_day: planDayId }),
        })
        entryId = entry.id
      }

      if (isCompleted) return { entryId, advanceError: null }

      try {
        await advanceDay(enrollmentId)
      } catch (err) {
        // Nothing was written, so marking the day complete was the whole action.
        if (!entryId) throw err
        // The writing is safe; report the half that failed without losing it.
        return { entryId, advanceError: err }
      }
      return { entryId, advanceError: null }
    },
    onSuccess: ({ entryId, advanceError }) => {
      queryClient.invalidateQueries({ queryKey: ['todayReading'] })
      queryClient.invalidateQueries({ queryKey: ['enrollments'] })
      queryClient.invalidateQueries({ queryKey: ['enrolledPlans'] })
      queryClient.invalidateQueries({ queryKey: ['dashboard-stats'] })
      queryClient.invalidateQueries({ queryKey: ['journalEntries'] })

      if (advanceError) {
        toast.fromError(advanceError, t('reading.savedButNotAdvanced'))
      } else {
        toast.success(entryId ? t('reading.savedToast') : t('reading.completedToast'))
      }
      // The entry page shows the feedback for what was just written.
      navigate(entryId ? `/journal/${entryId}` : '/')
    },
    // No onError: failures are shown as a toast by the app-wide mutation handler,
    // and the text stays in the box.
  })

  const backButton = (
    <button
      type="button"
      onClick={() => navigate(-1)}
      className="flex items-center gap-2 text-text-secondary hover:text-text-primary transition-colors"
    >
      <ChevronLeft className="w-5 h-5" aria-hidden="true" />
      {t('common.back')}
    </button>
  )

  if (todayQuery.isLoading) {
    return (
      <div className="space-y-8">
        {backButton}
        <div className="card flex items-center gap-3 text-text-secondary" role="status">
          <Loader2 className="w-5 h-5 animate-spin text-accent-primary" aria-hidden="true" />
          {t('reading.loading')}
        </div>
      </div>
    )
  }

  if (todayQuery.isError || !enrollment || !day) {
    return (
      <div className="space-y-8">
        {backButton}
        <InlineError
          error={todayQuery.error ?? new Error(t('reading.notFound'))}
          title={t('reading.loadFailed')}
          onRetry={() => todayQuery.refetch()}
        />
        <Link to="/plans" className="btn-secondary inline-block">
          {t('reading.browsePlans')}
        </Link>
      </div>
    )
  }

  const hasText = journalContent.trim().length > 0
  const canSave = !saveMutation.isPending && (hasText || !isCompleted)
  const saveLabel = saveMutation.isPending
    ? t('common.loading')
    : hasText
      ? isCompleted
        ? t('reading.saveEntry')
        : t('reading.saveAndComplete')
      : t('reading.markComplete')

  return (
    <div className="space-y-8">
      {backButton}

      <div className="card">
        <div className="mb-6">
          <p className="text-sm font-medium text-accent-secondary mb-2">
            {t('reading.dayOf', {
              day: day.day_number,
              total: enrollment.plan.duration_days,
              plan: enrollment.plan.title,
            })}
          </p>
          <h1 className="text-2xl font-bold text-text-primary break-words">
            {day.theme || references.join('; ') || enrollment.plan.title}
          </h1>
          {isCompleted && (
            <p className="mt-2 inline-flex items-center gap-2 text-sm text-success">
              <CheckCircle className="w-4 h-4" aria-hidden="true" />
              {t('reading.planCompleted')}
            </p>
          )}
        </div>

        {references.length === 0 ? (
          <p className="text-text-secondary">{t('reading.noPassages')}</p>
        ) : (
          <div className="space-y-8">
            {references.map((reference, index) => {
              const query = passageQueries[index]
              const parseable = parsePassageReference(reference) !== null
              const readerLink = (
                <Link
                  to={`/bible?passage=${encodeURIComponent(reference)}`}
                  className="text-sm text-accent-primary hover:underline inline-flex items-center gap-1"
                >
                  {t('reading.openInReader')}
                  <ExternalLink className="w-3 h-3" aria-hidden="true" />
                </Link>
              )
              return (
                <section key={reference} aria-label={reference}>
                  <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
                    <h2 className="text-lg font-semibold text-text-primary flex items-center gap-2">
                      <BookOpen className="w-5 h-5 text-accent-primary" aria-hidden="true" />
                      {reference}
                    </h2>
                    {readerLink}
                  </div>
                  {!parseable ? (
                    <p className="text-text-secondary text-sm">{t('reading.passageNotParsed')}</p>
                  ) : query?.isLoading ? (
                    <p className="text-text-secondary text-sm flex items-center gap-2" role="status">
                      <Loader2 className="w-4 h-4 animate-spin" aria-hidden="true" />
                      {t('reading.loadingPassage')}
                    </p>
                  ) : query?.isError ? (
                    <InlineError
                      error={query.error}
                      title={t('reading.passageFailed')}
                      onRetry={() => query.refetch()}
                    />
                  ) : query?.data?.full_text ? (
                    <div className="scripture-text">
                      <p className="text-text-primary leading-relaxed">{query.data.full_text}</p>
                      <p className="text-xs text-text-secondary mt-2 font-sans">
                        {query.data.translation?.name || translation}
                      </p>
                    </div>
                  ) : (
                    <p className="text-text-secondary text-sm">{t('reading.passageEmpty')}</p>
                  )}
                </section>
              )
            })}
          </div>
        )}
      </div>

      <div className="card">
        <h2 className="text-lg font-semibold text-text-primary mb-4">{t('reading.reflectionPrompts')}</h2>
        <ul className="space-y-3 text-text-primary">
          {reflectionSeed && <li>{reflectionSeed}</li>}
          <li>
            {day.theme
              ? t('reading.promptWithTheme', { theme: day.theme })
              : t('reading.promptGeneric')}
          </li>
        </ul>
      </div>

      <div className="card">
        <label htmlFor="reading-journal" className="block text-lg font-semibold text-text-primary mb-1">
          {t('reading.journalEntry')}
        </label>
        <p className="text-sm text-text-secondary mb-4">{t('reading.journalHint')}</p>

        <textarea
          id="reading-journal"
          value={journalContent}
          onChange={(e) => setJournalContent(e.target.value)}
          placeholder={t('reading.journalPlaceholder')}
          className="input w-full h-48 resize-y mb-6"
        />

        <fieldset className="mb-6">
          <legend className="block text-sm font-medium text-text-primary mb-3">{t('reading.moodTag')}</legend>
          <div className="flex flex-wrap gap-2">
            {MOODS.map((mood) => {
              const selected = selectedMood === mood.id
              return (
                <button
                  key={mood.id}
                  type="button"
                  aria-pressed={selected}
                  onClick={() => setSelectedMood(selected ? '' : mood.id)}
                  className={`px-4 py-2 rounded-lg border transition-colors ${
                    selected
                      ? 'border-accent-primary bg-accent-primary/10 text-accent-primary'
                      : 'border-border text-text-secondary hover:border-text-secondary'
                  }`}
                >
                  <span className="mr-2" aria-hidden="true">{mood.emoji}</span>
                  {t(`reading.moods.${mood.id}`)}
                </button>
              )
            })}
          </div>
        </fieldset>

        <button
          type="button"
          onClick={() => saveMutation.mutate()}
          disabled={!canSave}
          className="btn-primary flex items-center gap-2 disabled:opacity-60 disabled:cursor-not-allowed"
        >
          {saveMutation.isPending ? (
            <Loader2 className="w-4 h-4 animate-spin" aria-hidden="true" />
          ) : hasText ? (
            <Save className="w-4 h-4" aria-hidden="true" />
          ) : (
            <CheckCircle className="w-4 h-4" aria-hidden="true" />
          )}
          {saveLabel}
        </button>
      </div>
    </div>
  )
}
