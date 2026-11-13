import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { Check } from 'lucide-react'
import type { StudyLessonSummary } from '../../api/guides'

interface LessonStepperProps {
  studyId: string
  lessons: StudyLessonSummary[]
  /** The lesson being shown (1-based). */
  current: number
}

/** The lessons of a study as numbered steps: done, current, or still ahead. Any lesson can be opened. */
export default function LessonStepper({ studyId, lessons, current }: LessonStepperProps) {
  const { t } = useTranslation()

  return (
    <nav aria-label={t('study.stepper.label')}>
      <ol className="flex flex-wrap items-center gap-2">
        {lessons.map((lesson) => {
          const isCurrent = lesson.number === current
          const label = t(lesson.completed ? 'study.stepper.lessonDone' : 'study.stepper.lesson', {
            number: lesson.number,
            title: lesson.title,
          })
          return (
            <li key={lesson.number}>
              <Link
                to={`/study/${studyId}?lesson=${lesson.number}`}
                aria-current={isCurrent ? 'step' : undefined}
                aria-label={label}
                title={label}
                className={`flex h-9 min-w-[2.25rem] items-center justify-center rounded-full border px-2 text-sm font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-accent-primary focus:ring-offset-2 focus:ring-offset-bg-primary ${
                  isCurrent
                    ? 'border-accent-primary bg-accent-primary text-white'
                    : lesson.completed
                      ? 'border-success bg-success/25 text-text-primary hover:border-accent-primary'
                      : 'border-border bg-bg-surface text-text-secondary hover:border-accent-primary hover:text-text-primary'
                }`}
              >
                {lesson.completed && !isCurrent ? <Check className="h-4 w-4" aria-hidden="true" /> : lesson.number}
              </Link>
            </li>
          )
        })}
      </ol>
    </nav>
  )
}
