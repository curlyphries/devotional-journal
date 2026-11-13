import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { ArrowRight, CheckCircle2, HeartHandshake, Loader2, RotateCcw } from 'lucide-react'
import type { TopicCard } from '../../api/guides'

interface TopicCardViewProps {
  topic: TopicCard
  /** Why this study is suggested. When given, always shown in full. */
  reasons?: string[]
  onStart: (topic: TopicCard) => void
  /** This card's study is being started. */
  busy?: boolean
  /** Another start is in flight. */
  disabled?: boolean
  headingLevel?: 'h3' | 'h4'
}

/** One study in the library: what it is, who it is for, and how to start or continue it. */
export default function TopicCardView({
  topic,
  reasons,
  onStart,
  busy = false,
  disabled = false,
  headingLevel: Heading = 'h3',
}: TopicCardViewProps) {
  const { t } = useTranslation()
  const enrollment = topic.enrollment
  const isActive = enrollment?.status === 'active'
  const isCompleted = enrollment?.status === 'completed'

  return (
    <article className="flex h-full min-w-0 flex-col rounded-xl border border-border bg-bg-surface p-4 sm:p-5">
      <div className="flex flex-wrap items-start justify-between gap-x-3 gap-y-1">
        <Heading className="min-w-0 break-words text-base font-semibold leading-snug text-text-primary">
          {topic.title}
        </Heading>
        {isActive && (
          <span className="shrink-0 rounded-full border border-accent-secondary bg-accent-secondary/15 px-2.5 py-0.5 text-xs font-medium text-text-primary">
            {t('study.card.inProgress')}
          </span>
        )}
        {isCompleted && (
          <span className="inline-flex shrink-0 items-center gap-1 rounded-full border border-success bg-success/20 px-2.5 py-0.5 text-xs font-medium text-text-primary">
            <CheckCircle2 className="h-3.5 w-3.5" aria-hidden="true" />
            {t('study.card.completed')}
          </span>
        )}
      </div>

      <p className="mt-2 text-sm leading-relaxed text-text-secondary">{topic.summary}</p>

      <div className="mt-3 flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-text-secondary">
        <span>{t('study.card.lessons', { count: topic.lesson_count })}</span>
        {topic.sensitive && (
          <span className="inline-flex items-center gap-1 text-text-primary" title={t('study.card.sensitiveHelp')}>
            <HeartHandshake className="h-3.5 w-3.5 text-accent-primary" aria-hidden="true" />
            {t('study.card.sensitive')}
            <span className="sr-only"> — {t('study.card.sensitiveHelp')}</span>
          </span>
        )}
      </div>

      {topic.stage_note && (
        <p className="mt-3 border-l-2 border-accent-secondary pl-3 text-sm leading-relaxed text-text-primary">
          {topic.stage_note}
        </p>
      )}

      {reasons && reasons.length > 0 && (
        <div className="mt-3 rounded-lg border border-border bg-bg-elevated/60 p-3">
          <p className="text-xs font-semibold uppercase tracking-wider text-text-secondary">{t('study.card.why')}</p>
          <ul className="mt-1.5 list-disc space-y-1 pl-5 text-sm leading-relaxed text-text-primary">
            {reasons.map((reason) => (
              <li key={reason}>{reason}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="mt-auto flex flex-wrap items-center gap-x-4 gap-y-2 pt-4">
        {isActive && enrollment ? (
          <>
            <Link
              to={`/study/${enrollment.id}`}
              aria-label={t('study.card.continueNamed', { title: topic.title })}
              className="btn-primary inline-flex items-center gap-2 text-sm"
            >
              {t('study.card.continue')}
              <ArrowRight className="h-4 w-4" aria-hidden="true" />
            </Link>
            <span className="text-xs text-text-secondary">
              {t('study.lessonOf', {
                current: Math.min(enrollment.current_lesson, topic.lesson_count),
                total: topic.lesson_count,
              })}
            </span>
          </>
        ) : (
          <>
            <button
              type="button"
              onClick={() => onStart(topic)}
              disabled={busy || disabled}
              aria-label={t(isCompleted ? 'study.card.againNamed' : 'study.card.startNamed', { title: topic.title })}
              className={`${isCompleted ? 'btn-secondary' : 'btn-primary'} inline-flex items-center gap-2 text-sm disabled:opacity-60`}
            >
              {busy ? (
                <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
              ) : isCompleted ? (
                <RotateCcw className="h-4 w-4" aria-hidden="true" />
              ) : null}
              {busy ? t('study.card.starting') : isCompleted ? t('study.card.again') : t('study.card.start')}
            </button>
            {isCompleted && enrollment && (
              <Link
                to={`/study/${enrollment.id}`}
                aria-label={t('study.card.reviewNamed', { title: topic.title })}
                className="text-sm text-accent-primary underline-offset-2 hover:underline"
              >
                {t('study.card.review')}
              </Link>
            )}
          </>
        )}
      </div>
    </article>
  )
}
