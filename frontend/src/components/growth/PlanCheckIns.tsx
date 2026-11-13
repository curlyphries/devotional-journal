import { useId, useRef, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { BellRing, Loader2, MessageSquareText } from 'lucide-react'
import { addGrowthCheckIn, type GrowthPlan } from '../../api/growthPlans'
import { formatDate } from '../../lib/dates'
import DictationButton from '../DictationButton'
import { useToast } from '../Toast'
import { RatingDots, ScaleInput } from './primitives'
import { usePlanMutation } from './useGrowthPlans'

/**
 * Check-ins: the plan's one question, a 1-5 answer for this week and an
 * optional note. Prominent when one is due; the history is listed newest first.
 */
export default function PlanCheckIns({ plan }: { plan: GrowthPlan }) {
  const { t, i18n } = useTranslation()
  const toast = useToast()
  const id = useId()
  const noteRef = useRef<HTMLTextAreaElement>(null)
  const due = !!plan.progress?.check_in_due && plan.status === 'active'
  const [open, setOpen] = useState(false)
  const [rating, setRating] = useState<number | null>(null)
  const [note, setNote] = useState('')

  const save = usePlanMutation(
    (checkIn: { rating: number; note?: string }) => addGrowthCheckIn(plan.id, checkIn),
    {
      errorTitle: t('growth.checkIns.failed'),
      onSuccess: () => {
        setRating(null)
        setNote('')
        setOpen(false)
        toast.success(t('growth.checkIns.saved'))
      },
    },
  )

  const showForm = due || open
  const checkins = plan.checkins ?? []

  return (
    <section
      className={`card space-y-5 p-4 sm:p-6 ${due ? 'border-2 border-accent-primary' : ''}`}
      aria-labelledby={`${id}-title`}
    >
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          {due ? (
            <BellRing className="h-5 w-5 flex-shrink-0 text-accent-primary" aria-hidden="true" />
          ) : (
            <MessageSquareText className="h-5 w-5 flex-shrink-0 text-accent-primary" aria-hidden="true" />
          )}
          <h2 id={`${id}-title`} className="text-lg font-semibold text-text-primary">
            {t('growth.checkIns.title')}
          </h2>
          {due && (
            <span className="rounded-full border border-accent-primary bg-accent-primary/15 px-2.5 py-0.5 text-xs font-medium text-text-primary">
              {t('growth.checkInDue')}
            </span>
          )}
        </div>
        {!showForm && plan.status === 'active' && (
          <button type="button" className="btn-secondary text-sm" onClick={() => setOpen(true)}>
            {t('growth.checkIns.checkInNow')}
          </button>
        )}
      </div>

      {showForm && (
        <form
          className="space-y-4"
          onSubmit={(event) => {
            event.preventDefault()
            if (rating == null) return
            save.mutate({ rating, ...(note.trim() ? { note: note.trim() } : {}) })
          }}
        >
          {due && <p className="text-sm text-text-secondary">{t('growth.checkIns.dueIntro')}</p>}
          {plan.check_in_question && (
            <p className="scripture-text whitespace-pre-wrap text-text-primary">{plan.check_in_question}</p>
          )}
          <ScaleInput
            label={<span className="font-medium">{t('growth.checkIns.ratingLabel')}</span>}
            hint={t('growth.checkIns.ratingHint')}
            value={rating}
            onChange={setRating}
          />
          <div>
            <label htmlFor={`${id}-note`} className="block font-medium text-text-primary">
              {t('growth.checkIns.noteLabel')} <span className="font-normal text-text-secondary">{t('growth.optional')}</span>
            </label>
            <textarea
              id={`${id}-note`}
              ref={noteRef}
              className="input mt-2 min-h-[5rem] w-full"
              maxLength={2000}
              value={note}
              onChange={(event) => setNote(event.target.value)}
            />
            <DictationButton value={note} onChange={setNote} textareaRef={noteRef} hidePrivacyNote className="mt-2" />
          </div>
          <div className="flex flex-wrap justify-end gap-3">
            {!due && (
              <button type="button" className="btn-secondary" disabled={save.isPending} onClick={() => setOpen(false)}>
                {t('common.cancel')}
              </button>
            )}
            <button
              type="submit"
              className="btn-primary inline-flex items-center gap-2 disabled:cursor-not-allowed disabled:opacity-60"
              disabled={rating == null || save.isPending}
            >
              {save.isPending && <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />}
              {t('growth.checkIns.save')}
            </button>
          </div>
        </form>
      )}

      <div>
        <h3 className="text-sm font-semibold uppercase tracking-wider text-text-secondary">
          {t('growth.checkIns.history')}
        </h3>
        {checkins.length > 0 ? (
          <ul className="mt-2 divide-y divide-border">
            {checkins.map((checkIn) => (
              <li key={checkIn.id} className="py-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-sm text-text-primary">{formatDate(checkIn.date, i18n.language)}</span>
                  <RatingDots rating={checkIn.rating} />
                </div>
                {checkIn.note && (
                  <p className="mt-1 whitespace-pre-wrap break-words text-sm text-text-secondary">{checkIn.note}</p>
                )}
              </li>
            ))}
          </ul>
        ) : (
          <p className="mt-1 text-sm text-text-secondary">{t('growth.checkIns.empty')}</p>
        )}
      </div>
    </section>
  )
}
