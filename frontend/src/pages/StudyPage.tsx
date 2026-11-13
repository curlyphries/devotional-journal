import { useEffect, useRef, useState } from 'react'
import { Link, useNavigate, useParams, useSearchParams } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { CheckCircle2, ChevronLeft, LogOut, SearchX } from 'lucide-react'
import { getLesson, getStudy, guidesKeys, guidesLang, leaveStudy } from '../api/guides'
import { toApiError } from '../api/errors'
import ConfirmDialog from '../components/ConfirmDialog'
import InlineError from '../components/InlineError'
import { useToast } from '../components/Toast'
import LessonStepper from '../components/study/LessonStepper'
import LessonView from '../components/study/LessonView'
import { clearDraft } from '../components/study/drafts'

/** `?lesson=3` → 3; anything that is not a positive whole number → null. */
function parseLessonParam(value: string | null): number | null {
  if (!value || !/^\d+$/.test(value)) return null
  const parsed = Number(value)
  return parsed >= 1 ? parsed : null
}

function ReaderSkeleton() {
  const { t } = useTranslation()
  return (
    <div role="status" className="animate-pulse space-y-6">
      <span className="sr-only">{t('common.loading')}</span>
      <div className="h-7 w-3/4 rounded bg-bg-elevated" />
      <div className="space-y-3 rounded-xl border border-border bg-bg-surface p-6">
        <div className="h-5 w-1/3 rounded bg-bg-elevated" />
        <div className="h-4 w-full rounded bg-bg-elevated" />
        <div className="h-4 w-11/12 rounded bg-bg-elevated" />
        <div className="h-4 w-4/5 rounded bg-bg-elevated" />
      </div>
      <div className="space-y-3">
        <div className="h-4 w-full rounded bg-bg-elevated" />
        <div className="h-4 w-full rounded bg-bg-elevated" />
        <div className="h-4 w-2/3 rounded bg-bg-elevated" />
      </div>
    </div>
  )
}

/**
 * A study, one lesson at a time (`/study/:studyId`, optional `?lesson=n`).
 * Without `?lesson` it opens where the person left off.
 */
export default function StudyPage() {
  const { studyId = '' } = useParams()
  const [searchParams] = useSearchParams()
  const { t } = useTranslation()
  const lang = guidesLang()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const toast = useToast()
  const [confirmLeave, setConfirmLeave] = useState(false)
  const lessonTopRef = useRef<HTMLDivElement>(null)

  const requested = parseLessonParam(searchParams.get('lesson'))

  const studyQuery = useQuery({
    queryKey: guidesKeys.study(studyId, lang),
    queryFn: () => getStudy(studyId),
    enabled: !!studyId,
  })
  const study = studyQuery.data

  // Opened without `?lesson`: start where the person left off, and then stay
  // on that lesson. Saving answers moves `study.current_lesson` forward; without
  // pinning, the page would jump to the next lesson before the person had read
  // the reply to what they wrote.
  const [resumeAt, setResumeAt] = useState<{ studyId: string; lesson: number } | null>(null)
  useEffect(() => {
    if (study && requested === null && resumeAt?.studyId !== studyId) {
      setResumeAt({ studyId, lesson: study.current_lesson })
    }
  }, [study, requested, resumeAt, studyId])
  const pinned = resumeAt?.studyId === studyId ? resumeAt.lesson : null

  const lessonNumber = study
    ? Math.min(
        Math.max(requested ?? pinned ?? study.current_lesson, 1),
        Math.max(study.lesson_count, 1),
      )
    : requested

  const lessonQuery = useQuery({
    queryKey: guidesKeys.lesson(studyId, lessonNumber ?? 0, lang),
    queryFn: () => getLesson(studyId, lessonNumber!),
    enabled: !!studyId && lessonNumber !== null,
  })
  const lesson = lessonQuery.data

  // Moving between lessons: start the new one from its top.
  const shownLesson = useRef<number | null>(null)
  useEffect(() => {
    if (lessonNumber === null) return
    if (shownLesson.current !== null && shownLesson.current !== lessonNumber) {
      lessonTopRef.current?.focus()
    }
    shownLesson.current = lessonNumber
  }, [lessonNumber])

  const leave = useMutation({
    mutationFn: () => leaveStudy(studyId),
    onSuccess: () => {
      for (let n = 1; n <= (study?.lesson_count ?? 0); n += 1) clearDraft(studyId, n)
      toast.success(t('study.leave.done'))
      navigate('/study', { replace: true })
      // Forget this study; refresh the lists it appeared in.
      const isThisStudy = (key: readonly unknown[]) =>
        (key[1] === 'study' || key[1] === 'lesson') && key[2] === studyId
      queryClient.removeQueries({ queryKey: guidesKeys.all, predicate: (query) => isThisStudy(query.queryKey) })
      queryClient.invalidateQueries({ queryKey: guidesKeys.all, predicate: (query) => !isThisStudy(query.queryKey) })
    },
    onError: (err) => {
      setConfirmLeave(false)
      toast.fromError(err, t('study.leave.failed'))
    },
  })

  const backLink = (
    <Link
      to="/study"
      className="inline-flex items-center gap-1 rounded text-sm text-text-secondary transition-colors hover:text-text-primary focus:outline-none focus:ring-2 focus:ring-accent-primary"
    >
      <ChevronLeft className="h-4 w-4" aria-hidden="true" />
      {t('study.backToHub')}
    </Link>
  )

  if (studyQuery.isLoading) {
    return (
      <div className="mx-auto max-w-2xl space-y-6">
        {backLink}
        <ReaderSkeleton />
      </div>
    )
  }

  if (studyQuery.isError || !study) {
    const notFound = !studyId || (studyQuery.isError && toApiError(studyQuery.error).status === 404)
    return (
      <div className="mx-auto max-w-2xl space-y-6">
        {backLink}
        {notFound ? (
          <div className="card p-6 text-center sm:p-8">
            <SearchX className="mx-auto h-10 w-10 text-text-secondary" aria-hidden="true" />
            <h1 className="mt-3 text-xl font-semibold text-text-primary">{t('study.notFound.title')}</h1>
            <p className="mx-auto mt-2 max-w-md leading-relaxed text-text-secondary">{t('study.notFound.body')}</p>
            <Link to="/study" className="btn-primary mt-5 inline-flex items-center gap-2">
              {t('study.notFound.cta')}
            </Link>
          </div>
        ) : (
          <InlineError
            error={studyQuery.error ?? new Error(t('study.loadFailed'))}
            title={t('study.loadFailed')}
            onRetry={() => studyQuery.refetch()}
          />
        )}
      </div>
    )
  }

  const total = study.lesson_count
  const lessonMissing = lessonQuery.isError && toApiError(lessonQuery.error).status === 404

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      {backLink}

      <header className="space-y-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wider text-text-secondary">{t('study.eyebrow')}</p>
          <div className="mt-1 flex flex-wrap items-center gap-x-3 gap-y-1">
            <h1 className="break-words text-2xl font-bold text-text-primary">{study.topic.title}</h1>
            {study.status === 'completed' && (
              <span className="inline-flex items-center gap-1 rounded-full border border-success bg-success/20 px-2.5 py-0.5 text-xs font-medium text-text-primary">
                <CheckCircle2 className="h-3.5 w-3.5" aria-hidden="true" />
                {t('study.card.completed')}
              </span>
            )}
          </div>
          {study.stage_note && <p className="mt-2 text-sm leading-relaxed text-text-secondary">{study.stage_note}</p>}
        </div>
        <div className="flex flex-wrap items-center gap-x-4 gap-y-2">
          <LessonStepper studyId={studyId} lessons={study.lessons ?? []} current={lessonNumber ?? 1} />
          <span className="text-sm text-text-secondary">
            {t('study.lessonOf', { current: lessonNumber ?? 1, total })}
          </span>
        </div>
      </header>

      <div ref={lessonTopRef} tabIndex={-1} className="scroll-mt-6 focus:outline-none">
        {lessonQuery.isLoading || lessonNumber === null ? (
          <ReaderSkeleton />
        ) : lessonQuery.isError || !lesson ? (
          <div className="space-y-4">
            <InlineError
              error={lessonQuery.error ?? new Error(t('study.lessonFailed'))}
              title={lessonMissing ? t('study.lessonMissing') : t('study.lessonFailed')}
              onRetry={lessonMissing ? undefined : () => lessonQuery.refetch()}
            />
            {lessonMissing && (
              <Link to={`/study/${studyId}`} className="btn-secondary inline-flex items-center gap-2">
                {t('study.lessonMissingCta')}
              </Link>
            )}
          </div>
        ) : (
          <LessonView
            key={`${studyId}:${lesson.number}:${lang}`}
            studyId={studyId}
            study={study}
            lesson={lesson}
            onReload={() => lessonQuery.refetch()}
            reloading={lessonQuery.isRefetching}
          />
        )}
      </div>

      <footer className="border-t border-border pt-4">
        <button
          type="button"
          onClick={() => setConfirmLeave(true)}
          disabled={leave.isPending}
          className="inline-flex items-center gap-2 rounded text-sm text-text-secondary transition-colors hover:text-text-primary focus:outline-none focus:ring-2 focus:ring-accent-primary"
        >
          <LogOut className="h-4 w-4" aria-hidden="true" />
          {t('study.leave.button')}
        </button>
      </footer>

      <ConfirmDialog
        open={confirmLeave}
        title={t('study.leave.title')}
        message={t('study.leave.message', { title: study.topic.title })}
        confirmLabel={t('study.leave.confirm')}
        destructive
        busy={leave.isPending}
        onConfirm={() => leave.mutate()}
        onCancel={() => setConfirmLeave(false)}
      />
    </div>
  )
}
