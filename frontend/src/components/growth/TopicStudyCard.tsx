import { Link, useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { ArrowRight, BookOpen, Loader2 } from 'lucide-react'
import { guidesKeys, startStudy, type TopicCard } from '../../api/guides'
import { useToast } from '../Toast'

/**
 * A study from the library, with one action: continue it when the person has
 * already started, otherwise start it and go straight to the study.
 */
export default function TopicStudyCard({
  topic,
  headingLevel: Heading = 'h3',
}: {
  topic: TopicCard
  /** Heading level for the study's title, so it fits the section it sits in. */
  headingLevel?: 'h3' | 'h4'
}) {
  const { t } = useTranslation()
  const toast = useToast()
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  const start = useMutation({
    mutationFn: () => startStudy(topic.key),
    onSuccess: (study) => {
      queryClient.invalidateQueries({ queryKey: guidesKeys.all })
      navigate(`/study/${study.id}`)
    },
    onError: (err) => toast.fromError(err, t('growth.topic.startFailed')),
  })

  const enrollment = topic.enrollment
  const done = enrollment?.completed_lessons?.length ?? 0

  return (
    <li className="flex flex-col rounded-xl border border-border bg-bg-elevated/50 p-4">
      <div className="flex items-start gap-2">
        <BookOpen className="mt-0.5 h-4 w-4 flex-shrink-0 text-accent-primary" aria-hidden="true" />
        <Heading className="min-w-0 break-words font-medium text-text-primary">{topic.title}</Heading>
      </div>
      {topic.summary && <p className="mt-1 text-sm text-text-secondary">{topic.summary}</p>}
      <p className="mt-2 text-xs text-text-secondary">
        {enrollment
          ? enrollment.status === 'completed'
            ? t('growth.topic.completed')
            : t('growth.topic.progress', { done, total: topic.lesson_count })
          : t('growth.topic.lessons', { count: topic.lesson_count })}
        {topic.sensitive && <> · {t('growth.topic.sensitive')}</>}
      </p>
      <div className="mt-3 flex flex-1 items-end">
        {enrollment ? (
          <Link
            to={`/study/${enrollment.id}`}
            className="inline-flex items-center gap-1.5 text-sm font-medium text-accent-primary underline-offset-2 hover:underline"
            aria-label={t(
              enrollment.status === 'completed' ? 'growth.topic.reviewNamed' : 'growth.topic.continueNamed',
              { title: topic.title },
            )}
          >
            {enrollment.status === 'completed' ? t('growth.topic.review') : t('growth.topic.continue')}
            <ArrowRight className="h-4 w-4" aria-hidden="true" />
          </Link>
        ) : (
          <button
            type="button"
            className="btn-secondary inline-flex items-center gap-2 text-sm disabled:opacity-60"
            disabled={start.isPending}
            onClick={() => start.mutate()}
            aria-label={t('growth.topic.startNamed', { title: topic.title })}
          >
            {start.isPending && <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />}
            {t('growth.topic.start')}
          </button>
        )}
      </div>
    </li>
  )
}
