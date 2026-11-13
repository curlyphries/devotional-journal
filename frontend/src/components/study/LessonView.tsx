import { useEffect, useId, useRef, useState, type FormEvent, type ReactNode, type RefObject } from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import type { LucideIcon } from 'lucide-react'
import {
  ArrowRight,
  BookOpen,
  CheckCircle2,
  Cloud,
  Footprints,
  HardDrive,
  HeartHandshake,
  Info,
  Lightbulb,
  Loader2,
  MessageCircle,
  PartyPopper,
  PenLine,
  Pencil,
  Save,
  Sparkles,
  Sprout,
  Users,
  Wand2,
} from 'lucide-react'
import {
  guidesKeys,
  guidesLang,
  personalizeLesson,
  respondToLesson,
  simplifyLesson,
  type Lesson,
  type LessonAnswersPayload,
  type LessonReply,
  type LessonResponse,
  type LessonResult,
  type StudyDetail,
} from '../../api/guides'
import { getSpeechRecognitionConstructor } from '../../hooks/useSpeechToText'
import InlineError from '../InlineError'
import PassageCard from './PassageCard'
import ReflectField from './ReflectField'
import ScaleField from './ScaleField'
import TopicCardView from './TopicCardView'
import { clearDraft, isDraftEmpty, loadDraft, saveDraft } from './drafts'
import { useStartStudy } from './useStartStudy'

interface LessonViewProps {
  /** The id from the URL; used for every request and link. */
  studyId: string
  study: StudyDetail
  lesson: Lesson
  /** Fetch the lesson again (used when the Bible text was missing). */
  onReload: () => void
  reloading: boolean
}

interface FormState {
  answers: Record<string, string>
  stoodOut: string
  understanding: number | null
  resonance: number | null
  /** The form is open (as opposed to showing saved answers read-only). */
  editing: boolean
  fromDraft: boolean
}

function formFromResponse(response: LessonResponse): Omit<FormState, 'editing' | 'fromDraft'> {
  const answers: Record<string, string> = {}
  for (const item of response.answers ?? []) answers[item.question] = item.answer
  return {
    answers,
    stoodOut: response.stood_out ?? '',
    understanding: response.understanding ?? null,
    resonance: response.resonance ?? null,
  }
}

/** A draft left on this device wins; then saved answers (read-only); else an empty form. */
function initialForm(studyId: string, lesson: Lesson): FormState {
  const draft = loadDraft(studyId, lesson.number)
  if (draft) return { ...draft, editing: true, fromDraft: true }
  if (lesson.response) return { ...formFromResponse(lesson.response), editing: false, fromDraft: false }
  return { answers: {}, stoodOut: '', understanding: null, resonance: null, editing: true, fromDraft: false }
}

function SectionLabel({
  id,
  icon: Icon,
  children,
  headingRef,
}: {
  id: string
  icon: LucideIcon
  children: ReactNode
  headingRef?: RefObject<HTMLHeadingElement>
}) {
  return (
    <h3
      id={id}
      ref={headingRef}
      tabIndex={headingRef ? -1 : undefined}
      className="mb-3 flex items-center gap-2 text-sm font-semibold uppercase tracking-wider text-text-secondary focus:outline-none"
    >
      <Icon className="h-4 w-4 shrink-0 text-accent-primary" aria-hidden="true" />
      {children}
    </h3>
  )
}

const proseClass = 'whitespace-pre-wrap text-base leading-8 text-text-primary sm:text-[1.0625rem]'

/**
 * One lesson of a study: read the passage, understand it, reflect in writing,
 * then a practice and a prayer. Saving the reflection brings a reply and the
 * next step. Mounted per study + lesson, so its form state starts fresh.
 */
export default function LessonView({ studyId, study, lesson, onReload, reloading }: LessonViewProps) {
  const { t } = useTranslation()
  const queryClient = useQueryClient()
  const baseId = useId()
  const number = lesson.number
  const lessonKey = guidesKeys.lesson(studyId, number, guidesLang())
  const start = useStartStudy()

  const [initial] = useState(() => initialForm(studyId, lesson))
  const [answers, setAnswers] = useState(initial.answers)
  const [stoodOut, setStoodOut] = useState(initial.stoodOut)
  const [understanding, setUnderstanding] = useState(initial.understanding)
  const [resonance, setResonance] = useState(initial.resonance)
  const [editing, setEditing] = useState(initial.editing)
  const [dirty, setDirty] = useState(initial.fromDraft)
  const [draftRestored, setDraftRestored] = useState(initial.fromDraft)
  const [validation, setValidation] = useState<string | null>(null)
  const [result, setResult] = useState<LessonResult | null>(null)
  const [submitted, setSubmitted] = useState<LessonAnswersPayload | null>(null)
  const [justSimplified, setJustSimplified] = useState(false)

  const understandRef = useRef<HTMLHeadingElement>(null)
  const replyRef = useRef<HTMLHeadingElement>(null)
  const reflectRef = useRef<HTMLHeadingElement>(null)
  const [speechSupported] = useState(() => getSpeechRecognitionConstructor() !== null)

  // Keep a draft on this device while the form has unsaved changes.
  useEffect(() => {
    if (!editing || !dirty) return
    const draft = { answers, stoodOut, understanding, resonance }
    if (isDraftEmpty(draft)) clearDraft(studyId, number)
    else saveDraft(studyId, number, draft)
  }, [editing, dirty, answers, stoodOut, understanding, resonance, studyId, number])

  const simplify = useMutation({
    mutationFn: () => simplifyLesson(studyId, number),
    onSuccess: (updated) => {
      queryClient.setQueryData(lessonKey, updated)
      setJustSimplified(true)
      understandRef.current?.focus()
    },
    // Shown inline next to the button.
    meta: { silent: true },
  })

  const personalize = useMutation({
    mutationFn: () => personalizeLesson(studyId, number),
    onSuccess: (updated) => queryClient.setQueryData(lessonKey, updated),
    // Shown inline; the standard lesson stays usable.
    meta: { silent: true },
  })

  const respond = useMutation({
    mutationFn: (payload: LessonAnswersPayload) => respondToLesson(studyId, number, payload),
    onSuccess: (saved, payload) => {
      clearDraft(studyId, number)
      setDirty(false)
      setDraftRestored(false)
      setEditing(false)
      setSubmitted(payload)
      setResult(saved)
      queryClient.setQueryData(lessonKey, saved.lesson)
      // Progress, enrolment and suggestions all move; this lesson was just set above.
      const ownKey = lessonKey.join('/')
      queryClient.invalidateQueries({
        queryKey: guidesKeys.all,
        predicate: (query) => query.queryKey.join('/') !== ownKey,
      })
    },
    meta: { silent: true },
  })

  // After saving, take the reader (and screen readers) to the reply.
  useEffect(() => {
    if (result) replyRef.current?.focus()
  }, [result])

  // Personal questions replace the standard ones. A question that already has
  // an answer written under it stays visible, so nothing typed is ever dropped.
  const personal = lesson.personal
  const activeQuestions = personal?.questions?.length ? personal.questions : lesson.questions
  const keptQuestions = Object.keys(answers).filter((question) => !activeQuestions.includes(question))
  const questions = [...activeQuestions, ...keptQuestions]

  const change = () => {
    setDirty(true)
    setValidation(null)
  }

  const submit = (event: FormEvent) => {
    event.preventDefault()
    if (respond.isPending) return
    const filled = questions
      .map((question) => ({ question, answer: (answers[question] ?? '').trim() }))
      .filter((item) => item.answer)
    if (filled.length === 0 && !stoodOut.trim()) {
      setValidation(t('study.reflect.needAnswer'))
      return
    }
    if (understanding === null || resonance === null) {
      setValidation(t('study.reflect.needScales'))
      return
    }
    setValidation(null)
    respond.mutate({ answers: filled, stood_out: stoodOut.trim(), understanding, resonance })
  }

  // What is saved: the server's copy, or (if it did not echo it) what was just sent.
  const saved: LessonResponse | null =
    lesson.response ??
    (submitted && result ? { ...submitted, reply: result.reply, completed_at: '' } : null)
  const reply: LessonReply | null = result?.reply ?? lesson.response?.reply ?? null

  const startEditing = () => {
    if (saved) {
      const form = formFromResponse(saved)
      setAnswers(form.answers)
      setStoodOut(form.stoodOut)
      setUnderstanding(form.understanding)
      setResonance(form.resonance)
    }
    setValidation(null)
    setEditing(true)
    requestAnimationFrame(() => reflectRef.current?.focus())
  }

  const cancelEditing = () => {
    clearDraft(studyId, number)
    setDirty(false)
    setDraftRestored(false)
    setValidation(null)
    setEditing(false)
  }

  const nextStep = result?.next_step ?? null
  const nextNumber =
    nextStep?.kind === 'next_lesson' ? nextStep.number : !nextStep && lesson.next ? lesson.next.number : null
  const completedNow = nextStep?.kind === 'study_complete'
  const completedEarlier = !nextStep && !lesson.next && study.status === 'completed'
  const canSimplify = lesson.explanation_level !== 'simple'
  const offerSimpler = !editing && !!saved && saved.understanding <= 2 && canSimplify
  const startingKey = start.isPending ? start.variables : null

  const simplifyButton = (prominent: boolean) => (
    <button
      type="button"
      onClick={() => simplify.mutate()}
      disabled={simplify.isPending}
      className={`${prominent ? 'btn-primary' : 'btn-secondary'} inline-flex items-center gap-2 text-sm disabled:opacity-60`}
    >
      {simplify.isPending ? (
        <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
      ) : (
        <Lightbulb className="h-4 w-4" aria-hidden="true" />
      )}
      {t('study.understand.simpler')}
    </button>
  )

  return (
    <article aria-labelledby={`${baseId}-title`} className="space-y-8">
      <h2 id={`${baseId}-title`} className="text-xl font-semibold leading-snug text-text-primary sm:text-2xl">
        {t('study.lessonTitle', { number, title: lesson.title })}
      </h2>

      {lesson.with_grown_up && (
        <div role="note" className="flex items-start gap-3 rounded-xl border border-accent-secondary bg-accent-secondary/10 p-4">
          <Users className="mt-0.5 h-5 w-5 shrink-0 text-accent-primary" aria-hidden="true" />
          <div className="min-w-0">
            <p className="font-medium text-text-primary">{t('study.grownUp.title')}</p>
            <p className="mt-0.5 text-sm leading-relaxed text-text-secondary">{t('study.grownUp.body')}</p>
          </div>
        </div>
      )}

      {lesson.support_note && (
        <div role="note" className="flex items-start gap-3 rounded-xl border border-border bg-bg-surface p-4">
          <HeartHandshake className="mt-0.5 h-5 w-5 shrink-0 text-accent-primary" aria-hidden="true" />
          <p className="min-w-0 text-sm leading-relaxed text-text-primary">{lesson.support_note}</p>
        </div>
      )}

      {/* Read */}
      <section aria-labelledby={`${baseId}-read`}>
        <SectionLabel id={`${baseId}-read`} icon={BookOpen}>
          {t('study.read.title')}
        </SectionLabel>
        <PassageCard
          reference={lesson.reference}
          passage={lesson.passage}
          error={lesson.passage_error}
          onRetry={onReload}
          retrying={reloading}
        />
      </section>

      {/* Understand */}
      <section aria-labelledby={`${baseId}-understand`}>
        <SectionLabel id={`${baseId}-understand`} icon={Lightbulb} headingRef={understandRef}>
          {t('study.understand.title')}
        </SectionLabel>
        {lesson.explanation_level === 'simple' && (
          <p role={justSimplified ? 'status' : undefined} className="mb-2 text-xs text-text-secondary">
            {t('study.understand.simpleShown')}
          </p>
        )}
        <p className={proseClass}>{lesson.explanation}</p>

        {personal && (
          <div className="mt-5 rounded-xl border border-accent-secondary/70 bg-bg-surface p-4 sm:p-5">
            <h4 className="flex items-center gap-2 text-sm font-semibold text-text-primary">
              <Sparkles className="h-4 w-4 shrink-0 text-accent-primary" aria-hidden="true" />
              {t('study.personal.title')}
            </h4>
            {personal.connection && <p className={`mt-3 ${proseClass}`}>{personal.connection}</p>}
            {personal.explanation && <p className={`mt-3 ${proseClass}`}>{personal.explanation}</p>}
            <p className="mt-4 flex items-start gap-2 text-xs leading-relaxed text-text-secondary">
              {personal.local ? (
                <HardDrive className="mt-0.5 h-3.5 w-3.5 shrink-0" aria-hidden="true" />
              ) : (
                <Cloud className="mt-0.5 h-3.5 w-3.5 shrink-0" aria-hidden="true" />
              )}
              <span className="min-w-0 break-words">
                {t(personal.local ? 'study.personal.byLocal' : 'study.personal.byCloud', {
                  engine: [personal.provider, personal.model].filter(Boolean).join(' · '),
                })}
              </span>
            </p>
          </div>
        )}

        {(canSimplify || !personal) && (
          <div className="mt-5 flex flex-wrap gap-3">
            {canSimplify && simplifyButton(false)}
            {!personal && (
              <button
                type="button"
                onClick={() => personalize.mutate()}
                disabled={personalize.isPending}
                className="btn-secondary inline-flex items-center gap-2 text-sm disabled:opacity-60"
              >
                <Wand2 className="h-4 w-4" aria-hidden="true" />
                {t('study.personal.button')}
              </button>
            )}
          </div>
        )}
        {!personal && !personalize.isPending && !personalize.isError && (
          <p className="mt-2 text-xs leading-relaxed text-text-secondary">{t('study.personal.hint')}</p>
        )}

        {personalize.isPending && (
          <div role="status" aria-live="polite" className="mt-4 flex items-start gap-3">
            <Loader2 className="mt-0.5 h-5 w-5 shrink-0 animate-spin text-accent-primary" aria-hidden="true" />
            <div>
              <p className="font-medium text-text-primary">{t('study.personal.working')}</p>
              <p className="mt-1 text-sm text-text-secondary">{t('study.personal.patience')}</p>
            </div>
          </div>
        )}
        {personalize.isError && !personalize.isPending && (
          <div className="mt-4 space-y-2">
            <InlineError
              error={personalize.error}
              title={t('study.personal.failed')}
              onRetry={() => personalize.mutate()}
            />
            <p className="text-sm text-text-secondary">{t('study.personal.failedNote')}</p>
          </div>
        )}
        {simplify.isError && !simplify.isPending && (
          <InlineError
            className="mt-4"
            error={simplify.error}
            title={t('study.understand.simplerFailed')}
            onRetry={() => simplify.mutate()}
          />
        )}
      </section>

      {/* Reflect, practice and prayer, then save: one form, so the button comes after the whole lesson. */}
      <form onSubmit={submit} noValidate className="space-y-8">
      <section aria-labelledby={`${baseId}-reflect`} className="card p-4 sm:p-6">
        <SectionLabel id={`${baseId}-reflect`} icon={PenLine} headingRef={reflectRef}>
          {t('study.reflect.title')}
        </SectionLabel>

        {editing ? (
          <div className="space-y-6">
            <p className="text-sm leading-relaxed text-text-secondary">{t('study.reflect.intro')}</p>
            {draftRestored && (
              <p role="status" className="rounded-lg border border-border bg-bg-elevated px-3 py-2 text-sm text-text-primary">
                {t('study.reflect.draftRestored')}
              </p>
            )}

            {questions.map((question, index) => (
              <ReflectField
                key={question}
                label={question}
                value={answers[question] ?? ''}
                disabled={respond.isPending}
                dictation={speechSupported || index === 0}
                onChange={(value) => {
                  setAnswers((current) => ({ ...current, [question]: value }))
                  change()
                }}
              />
            ))}

            <ReflectField
              label={t('study.reflect.stoodOut')}
              value={stoodOut}
              disabled={respond.isPending}
              dictation={speechSupported}
              onChange={(value) => {
                setStoodOut(value)
                change()
              }}
            />

            {speechSupported && <p className="text-xs leading-relaxed text-text-secondary">{t('voice.privacy')}</p>}

            <div className="space-y-6 border-t border-border pt-6">
              <ScaleField
                legend={t('study.reflect.understanding')}
                lowLabel={t('study.reflect.understandingLow')}
                highLabel={t('study.reflect.understandingHigh')}
                value={understanding}
                disabled={respond.isPending}
                onChange={(value) => {
                  setUnderstanding(value)
                  change()
                }}
              />
              <ScaleField
                legend={t('study.reflect.resonance')}
                lowLabel={t('study.reflect.resonanceLow')}
                highLabel={t('study.reflect.resonanceHigh')}
                value={resonance}
                disabled={respond.isPending}
                onChange={(value) => {
                  setResonance(value)
                  change()
                }}
              />
            </div>

          </div>
        ) : saved ? (
          <div className="space-y-5">
            <p className="flex items-center gap-2 text-sm text-text-secondary">
              <CheckCircle2 className="h-4 w-4 shrink-0 text-accent-primary" aria-hidden="true" />
              {t('study.saved.note')}
            </p>
            <dl className="space-y-4">
              {saved.answers.map((item) => (
                <div key={item.question}>
                  <dt className="font-medium leading-snug text-text-primary">{item.question}</dt>
                  <dd className="mt-1 whitespace-pre-wrap font-serif leading-relaxed text-text-primary">{item.answer}</dd>
                </div>
              ))}
              {saved.stood_out && (
                <div>
                  <dt className="font-medium leading-snug text-text-primary">{t('study.reflect.stoodOut')}</dt>
                  <dd className="mt-1 whitespace-pre-wrap font-serif leading-relaxed text-text-primary">
                    {saved.stood_out}
                  </dd>
                </div>
              )}
            </dl>
            <ul className="flex flex-wrap gap-2 text-sm">
              <li className="rounded-full border border-border bg-bg-elevated px-3 py-1 text-text-primary">
                {t('study.saved.understanding', { value: saved.understanding })}
              </li>
              <li className="rounded-full border border-border bg-bg-elevated px-3 py-1 text-text-primary">
                {t('study.saved.resonance', { value: saved.resonance })}
              </li>
            </ul>
            <button type="button" onClick={startEditing} className="btn-secondary inline-flex items-center gap-2 text-sm">
              <Pencil className="h-4 w-4" aria-hidden="true" />
              {t('study.saved.edit')}
            </button>
          </div>
        ) : null}
      </section>

      {/* Practice and prayer */}
      {lesson.practice && (
        <section aria-labelledby={`${baseId}-practice`} className="card p-4 sm:p-6">
          <SectionLabel id={`${baseId}-practice`} icon={Footprints}>
            {t('study.practice.title')}
          </SectionLabel>
          <p className={proseClass}>{lesson.practice}</p>
        </section>
      )}
      {lesson.prayer && (
        <section aria-labelledby={`${baseId}-pray`} className="card p-4 sm:p-6">
          <SectionLabel id={`${baseId}-pray`} icon={HeartHandshake}>
            {t('study.pray.title')}
          </SectionLabel>
          <p className="whitespace-pre-wrap font-serif text-lg italic leading-relaxed text-text-primary">{lesson.prayer}</p>
        </section>
      )}

      {editing && (
        <div className="space-y-4">
          {validation && (
            <p role="alert" className="rounded-lg border border-danger bg-danger/15 px-3 py-2 text-sm text-text-primary">
              {validation}
            </p>
          )}
          {respond.isError && !respond.isPending && (
            <InlineError error={respond.error} title={t('study.reflect.saveFailed')} />
          )}

          <div className="flex flex-wrap items-center gap-3">
            <button
              type="submit"
              disabled={respond.isPending}
              className="btn-primary inline-flex items-center gap-2 disabled:opacity-60"
            >
              {respond.isPending ? (
                <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
              ) : (
                <Save className="h-4 w-4" aria-hidden="true" />
              )}
              {respond.isPending ? t('study.reflect.saving') : t('study.reflect.save')}
            </button>
            {saved && !respond.isPending && (
              <button type="button" onClick={cancelEditing} className="btn-secondary">
                {t('common.cancel')}
              </button>
            )}
          </div>
          {respond.isPending ? (
            <p role="status" aria-live="polite" className="text-sm text-text-secondary">
              {t('study.reflect.savingNote')}
            </p>
          ) : (
            <p className="text-xs leading-relaxed text-text-secondary">{t('study.reflect.keptNote')}</p>
          )}
        </div>
      )}
      </form>

      {/* Reply */}
      {!editing && saved && (
        <section aria-labelledby={`${baseId}-reply`} className="rounded-xl border border-accent-secondary/70 bg-bg-surface p-4 sm:p-6">
          <SectionLabel id={`${baseId}-reply`} icon={MessageCircle} headingRef={replyRef}>
            {t('study.reply.title')}
          </SectionLabel>
          {reply ? (
            <>
              <p className={proseClass}>{reply.text}</p>
              {reply.follow_up && (
                <div className="mt-5">
                  <h4 className="text-sm font-semibold text-text-secondary">{t('study.reply.followUp')}</h4>
                  <p className="mt-1 whitespace-pre-wrap font-serif text-lg italic leading-relaxed text-text-primary">
                    {reply.follow_up}
                  </p>
                </div>
              )}
              {reply.source === 'built_in' ? (
                <div role="note" className="mt-5 flex items-start gap-3 rounded-lg border border-border bg-bg-elevated p-3 text-sm">
                  <Info className="mt-0.5 h-4 w-4 shrink-0 text-accent-primary" aria-hidden="true" />
                  <div className="min-w-0 space-y-1">
                    <p className="text-text-primary">{t('study.reply.builtIn')}</p>
                    {reply.fallback_reason?.message && (
                      <p className="text-text-secondary">
                        {t('feedback.fallback.reason')} {reply.fallback_reason.message}
                      </p>
                    )}
                    {reply.fallback_reason?.suggestion && (
                      <p className="text-text-secondary">{reply.fallback_reason.suggestion}</p>
                    )}
                    <Link to="/settings#ai-provider" className="inline-block text-accent-primary underline-offset-2 hover:underline">
                      {t('feedback.fallback.settings')}
                    </Link>
                  </div>
                </div>
              ) : (
                <p className="mt-4 text-xs text-text-secondary">{t('study.reply.byAi')}</p>
              )}
            </>
          ) : (
            <p className="text-text-primary">{t('study.reply.none')}</p>
          )}

          {offerSimpler && (
            <div className="mt-5 rounded-lg border border-accent-secondary bg-accent-secondary/10 p-4">
              <p className="font-medium text-text-primary">{t('study.reply.simplerTitle')}</p>
              <p className="mt-1 text-sm leading-relaxed text-text-secondary">{t('study.reply.simplerBody')}</p>
              <div className="mt-3">{simplifyButton(true)}</div>
            </div>
          )}
        </section>
      )}

      {/* Next step */}
      {!editing && saved && nextNumber !== null && (
        <div className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-border bg-bg-surface p-4 sm:p-5">
          <p className="min-w-0 text-text-primary">{t('study.next.ready')}</p>
          <Link to={`/study/${studyId}?lesson=${nextNumber}`} className="btn-primary inline-flex items-center gap-2">
            {t('study.next.lesson')}
            <ArrowRight className="h-4 w-4" aria-hidden="true" />
          </Link>
        </div>
      )}

      {!editing && saved && (completedNow || completedEarlier) && (
        <section
          aria-labelledby={`${baseId}-complete`}
          className="rounded-xl border border-success bg-success/10 p-4 sm:p-6"
        >
          <div className="flex items-start gap-3">
            <PartyPopper className="mt-0.5 h-6 w-6 shrink-0 text-accent-primary" aria-hidden="true" />
            <div className="min-w-0">
              <h3 id={`${baseId}-complete`} className="text-lg font-semibold text-text-primary">
                {t('study.complete.title', { title: study.topic.title })}
              </h3>
              <p className="mt-1 leading-relaxed text-text-secondary">
                {t(completedNow ? 'study.complete.body' : 'study.complete.bodyEarlier')}
              </p>
            </div>
          </div>

          {nextStep?.kind === 'study_complete' && nextStep.suggestions.length > 0 && (
            <div className="mt-5">
              <h4 className="mb-3 text-sm font-semibold text-text-primary">{t('study.complete.next')}</h4>
              <div className="grid gap-4 sm:grid-cols-2">
                {nextStep.suggestions.map((topic) => (
                  <TopicCardView
                    key={topic.key}
                    topic={topic}
                    headingLevel="h4"
                    onStart={(chosen) => start.mutate(chosen.key)}
                    busy={startingKey === topic.key}
                    disabled={start.isPending}
                  />
                ))}
              </div>
            </div>
          )}

          <div className="mt-5 flex flex-wrap gap-3">
            <Link to="/growth" className="btn-secondary inline-flex items-center gap-2 text-sm">
              <Sprout className="h-4 w-4" aria-hidden="true" />
              {t('study.complete.growth')}
            </Link>
            <Link to="/journal/new" className="btn-secondary inline-flex items-center gap-2 text-sm">
              <PenLine className="h-4 w-4" aria-hidden="true" />
              {t('study.complete.journal')}
            </Link>
            <Link to="/study" className="btn-secondary inline-flex items-center gap-2 text-sm">
              {t('study.complete.more')}
            </Link>
          </div>
        </section>
      )}
    </article>
  )
}
