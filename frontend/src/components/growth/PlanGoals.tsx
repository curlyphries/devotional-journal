import { useId, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { CalendarClock, Check, ChevronRight, Loader2, Pencil, Plus, RotateCcw, SkipForward, Trash2 } from 'lucide-react'
import {
  addGrowthGoal,
  deleteGrowthGoal,
  updateGrowthGoal,
  type GoalHorizon,
  type GoalPatch,
  type GrowthGoal,
  type GrowthPlan,
  type NewGoalPayload,
} from '../../api/growthPlans'
import { formatDate } from '../../lib/dates'
import ConfirmDialog from '../ConfirmDialog'
import { MeterBar } from './primitives'
import { usePlanMutation } from './useGrowthPlans'

const smallButton =
  'inline-flex items-center gap-1.5 rounded-lg border border-border bg-bg-elevated px-3 py-1.5 text-sm text-text-primary transition-colors hover:border-accent-primary focus:outline-none focus-visible:ring-2 focus-visible:ring-accent-primary disabled:opacity-50'
const shortDate: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'short', day: 'numeric' }

// ---------------------------------------------------------------------------
// One goal
// ---------------------------------------------------------------------------

function GoalItem({ planId, goal }: { planId: string; goal: GrowthGoal }) {
  const { t, i18n } = useTranslation()
  const id = useId()
  const [editing, setEditing] = useState(false)
  const [title, setTitle] = useState(goal.title)
  const [confirmingRemove, setConfirmingRemove] = useState(false)

  const update = usePlanMutation((patch: GoalPatch) => updateGrowthGoal(planId, goal.id, patch), {
    errorTitle: t('growth.goals.updateFailed'),
    onSuccess: () => setEditing(false),
  })
  const remove = usePlanMutation(() => deleteGrowthGoal(planId, goal.id), {
    errorTitle: t('growth.goals.removeFailed'),
  })

  const active = goal.status === 'active'
  const busy = update.isPending || remove.isPending
  const named = (key: string) => t(key, { title: goal.title })

  return (
    <li className="rounded-xl border border-border bg-bg-elevated/40 p-4">
      {editing ? (
        <form
          className="space-y-2"
          onSubmit={(event) => {
            event.preventDefault()
            if (title.trim()) update.mutate({ title: title.trim() })
          }}
        >
          <label htmlFor={`${id}-title`} className="block text-sm text-text-secondary">
            {t('growth.goals.titleLabel')}
          </label>
          <input
            id={`${id}-title`}
            className="input w-full"
            value={title}
            maxLength={200}
            autoFocus
            onChange={(event) => setTitle(event.target.value)}
          />
          <div className="flex flex-wrap gap-2">
            <button type="submit" className="btn-primary px-3 py-1.5 text-sm disabled:opacity-60" disabled={busy || !title.trim()}>
              {t('common.save')}
            </button>
            <button
              type="button"
              className="btn-secondary px-3 py-1.5 text-sm"
              onClick={() => {
                setTitle(goal.title)
                setEditing(false)
              }}
            >
              {t('common.cancel')}
            </button>
          </div>
        </form>
      ) : (
        <div className="flex flex-wrap items-start justify-between gap-2">
          <p className={`min-w-0 break-words font-medium ${active ? 'text-text-primary' : 'text-text-secondary'}`}>
            {goal.title}
          </p>
          <div className="flex flex-wrap items-center gap-1.5">
            <span className="rounded-full border border-border px-2 py-0.5 text-xs text-text-secondary">
              {t(`growth.goals.kind.${goal.kind}`, { defaultValue: goal.kind })}
            </span>
            {!active && (
              <span className="rounded-full border border-border bg-bg-surface px-2 py-0.5 text-xs text-text-primary">
                {t(`growth.goals.status.${goal.status}`)}
              </span>
            )}
            {active && goal.overdue && (
              <span className="rounded-full border border-accent-secondary bg-accent-secondary/15 px-2 py-0.5 text-xs text-text-primary">
                {t('growth.goals.overdue')}
              </span>
            )}
          </div>
        </div>
      )}

      {active && (
        <>
          <MeterBar
            className="mt-3"
            tone="accent"
            label={t('growth.goals.progressLabel')}
            value={goal.progress_count}
            max={Math.max(1, goal.target_count)}
            valueText={t('growth.goals.count', { done: goal.progress_count, total: goal.target_count })}
          />
          <div className="mt-2 flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-text-secondary">
            {goal.due_date && (
              <span className="inline-flex items-center gap-1.5">
                <CalendarClock className="h-3.5 w-3.5" aria-hidden="true" />
                {t(goal.overdue ? 'growth.goals.wasDue' : 'growth.goals.due', {
                  date: formatDate(goal.due_date, i18n.language, shortDate),
                })}
              </span>
            )}
            {goal.auto && <span>{t('growth.goals.auto')}</span>}
          </div>
        </>
      )}

      {!editing && (
        <div className="mt-3 flex flex-wrap items-center gap-2">
          {active ? (
            <>
              {!goal.auto && (
                <button
                  type="button"
                  className={smallButton}
                  disabled={busy}
                  onClick={() => update.mutate({ add: 1 })}
                  aria-label={named('growth.goals.addOneNamed')}
                >
                  <Plus className="h-4 w-4" aria-hidden="true" />
                  {t('growth.goals.addOne')}
                </button>
              )}
              {/* A study goal is finished by completing lessons, not by ticking it. */}
              {!goal.auto && (
                <button
                  type="button"
                  className={smallButton}
                  disabled={busy}
                  onClick={() => update.mutate({ status: 'done' })}
                  aria-label={named('growth.goals.doneNamed')}
                >
                  <Check className="h-4 w-4" aria-hidden="true" />
                  {t('common.done')}
                </button>
              )}
              <button
                type="button"
                className={smallButton}
                disabled={busy}
                onClick={() => update.mutate({ status: 'skipped' })}
                aria-label={named('growth.goals.skipNamed')}
              >
                <SkipForward className="h-4 w-4" aria-hidden="true" />
                {t('common.skip')}
              </button>
              <button
                type="button"
                className={smallButton}
                disabled={busy}
                onClick={() => {
                  setTitle(goal.title)
                  setEditing(true)
                }}
                aria-label={named('growth.goals.editNamed')}
              >
                <Pencil className="h-4 w-4" aria-hidden="true" />
                {t('common.edit')}
              </button>
            </>
          ) : (
            <button
              type="button"
              className={smallButton}
              disabled={busy}
              onClick={() => update.mutate({ status: 'active' })}
              aria-label={named('growth.goals.reopenNamed')}
            >
              <RotateCcw className="h-4 w-4" aria-hidden="true" />
              {t('growth.goals.reopen')}
            </button>
          )}
          <button
            type="button"
            className={smallButton}
            disabled={busy}
            onClick={() => setConfirmingRemove(true)}
            aria-label={named('growth.goals.removeNamed')}
          >
            <Trash2 className="h-4 w-4" aria-hidden="true" />
            {t('growth.goals.remove')}
          </button>
          {busy && <Loader2 className="h-4 w-4 animate-spin text-text-secondary" aria-hidden="true" />}
        </div>
      )}

      <ConfirmDialog
        open={confirmingRemove}
        title={t('growth.goals.removeTitle')}
        message={t('growth.goals.removeBody', { title: goal.title })}
        confirmLabel={t('growth.goals.remove')}
        destructive
        busy={remove.isPending}
        onConfirm={() => remove.mutate(undefined, { onSettled: () => setConfirmingRemove(false) })}
        onCancel={() => setConfirmingRemove(false)}
      />
    </li>
  )
}

// ---------------------------------------------------------------------------
// A group of goals (short- or long-term)
// ---------------------------------------------------------------------------

interface GoalGroupProps {
  plan: GrowthPlan
  horizon: GoalHorizon
}

/** The goals of one horizon: active ones first, finished and skipped ones folded away below. */
export function GoalGroup({ plan, horizon }: GoalGroupProps) {
  const { t } = useTranslation()
  const id = useId()
  const goals = plan.goals.filter((goal) => goal.horizon === horizon)
  const active = goals.filter((goal) => goal.status === 'active')
  const finished = goals.filter((goal) => goal.status !== 'active')
  const percent = horizon === 'short' ? plan.progress.short_percent : plan.progress.long_percent

  return (
    <section className="card space-y-4 p-4 sm:p-6" aria-labelledby={`${id}-title`}>
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <h2 id={`${id}-title`} className="text-lg font-semibold text-text-primary">
          {t(`growth.goals.${horizon}Title`)}
        </h2>
        {goals.length > 0 && (
          <span className="text-sm text-text-secondary">{t('growth.goals.groupPercent', { percent: percent ?? 0 })}</span>
        )}
      </div>
      <p className="text-sm text-text-secondary">{t(`growth.goals.${horizon}Hint`)}</p>

      {active.length > 0 ? (
        <ul className="space-y-3" aria-labelledby={`${id}-title`}>
          {active.map((goal) => (
            <GoalItem key={goal.id} planId={plan.id} goal={goal} />
          ))}
        </ul>
      ) : (
        <p className="text-sm text-text-secondary">
          {goals.length > 0 ? t('growth.goals.noneActive') : t('growth.goals.empty')}
        </p>
      )}

      {finished.length > 0 && (
        <details className="group rounded-xl border border-border">
          <summary className="flex cursor-pointer list-none items-center gap-2 rounded-xl px-4 py-3 text-sm font-medium text-text-primary hover:bg-bg-elevated focus:outline-none focus-visible:ring-2 focus-visible:ring-accent-primary [&::-webkit-details-marker]:hidden">
            <ChevronRight className="h-4 w-4 flex-shrink-0 text-text-secondary transition-transform group-open:rotate-90" aria-hidden="true" />
            {t('growth.goals.finished', { count: finished.length })}
          </summary>
          <ul className="space-y-3 border-t border-border p-3">
            {finished.map((goal) => (
              <GoalItem key={goal.id} planId={plan.id} goal={goal} />
            ))}
          </ul>
        </details>
      )}
    </section>
  )
}

// ---------------------------------------------------------------------------
// Add a goal
// ---------------------------------------------------------------------------

const DEFAULT_DAYS: Record<GoalHorizon, number> = { short: 14, long: 90 }

/** A goal of the person's own: what, how many times, and within how many days. */
export function AddGoalForm({ planId }: { planId: string }) {
  const { t } = useTranslation()
  const id = useId()
  const [open, setOpen] = useState(false)
  const [title, setTitle] = useState('')
  const [horizon, setHorizon] = useState<GoalHorizon>('short')
  const [targetCount, setTargetCount] = useState('1')
  const [days, setDays] = useState(String(DEFAULT_DAYS.short))

  const add = usePlanMutation((goal: NewGoalPayload) => addGrowthGoal(planId, goal), {
    errorTitle: t('growth.goals.addFailed'),
    onSuccess: () => {
      setTitle('')
      setTargetCount('1')
      setOpen(false)
    },
  })

  const count = Math.floor(Number(targetCount))
  const dayCount = Math.floor(Number(days))
  const valid = title.trim().length > 0 && count >= 1 && dayCount >= 1

  if (!open) {
    return (
      <button type="button" className="btn-secondary inline-flex items-center gap-2" onClick={() => setOpen(true)}>
        <Plus className="h-4 w-4" aria-hidden="true" />
        {t('growth.goals.add')}
      </button>
    )
  }

  return (
    <section className="card p-4 sm:p-6" aria-labelledby={`${id}-heading`}>
      <h2 id={`${id}-heading`} className="text-lg font-semibold text-text-primary">
        {t('growth.goals.add')}
      </h2>
      <form
        className="mt-4 space-y-4"
        onSubmit={(event) => {
          event.preventDefault()
          if (valid) add.mutate({ title: title.trim(), horizon, target_count: count, days: dayCount })
        }}
      >
        <div>
          <label htmlFor={`${id}-title`} className="block text-sm font-medium text-text-primary">
            {t('growth.goals.titleLabel')}
          </label>
          <input
            id={`${id}-title`}
            className="input mt-1 w-full"
            value={title}
            maxLength={200}
            required
            autoFocus
            placeholder={t('growth.goals.titlePlaceholder')}
            onChange={(event) => setTitle(event.target.value)}
          />
        </div>
        <fieldset>
          <legend className="text-sm font-medium text-text-primary">{t('growth.goals.horizonLabel')}</legend>
          <div className="mt-1 flex flex-wrap gap-x-5 gap-y-1">
            {(['short', 'long'] as const).map((option) => (
              <label key={option} className="flex cursor-pointer items-center gap-2 text-text-primary">
                <input
                  type="radio"
                  name={`${id}-horizon`}
                  className="h-4 w-4 accent-accent-primary"
                  checked={horizon === option}
                  onChange={() => {
                    setHorizon(option)
                    // Keep a number the person typed; only swap one default for the other.
                    if (days === String(DEFAULT_DAYS[horizon])) setDays(String(DEFAULT_DAYS[option]))
                  }}
                />
                {t(`growth.goals.horizon.${option}`)}
              </label>
            ))}
          </div>
        </fieldset>
        <div className="grid gap-4 sm:grid-cols-2">
          <div>
            <label htmlFor={`${id}-count`} className="block text-sm font-medium text-text-primary">
              {t('growth.goals.targetLabel')}
            </label>
            <input
              id={`${id}-count`}
              type="number"
              inputMode="numeric"
              min={1}
              max={365}
              className="input mt-1 w-full"
              value={targetCount}
              onChange={(event) => setTargetCount(event.target.value)}
            />
          </div>
          <div>
            <label htmlFor={`${id}-days`} className="block text-sm font-medium text-text-primary">
              {t('growth.goals.daysLabel')}
            </label>
            <input
              id={`${id}-days`}
              type="number"
              inputMode="numeric"
              min={1}
              max={730}
              className="input mt-1 w-full"
              value={days}
              onChange={(event) => setDays(event.target.value)}
            />
          </div>
        </div>
        <div className="flex flex-wrap justify-end gap-3">
          <button type="button" className="btn-secondary" onClick={() => setOpen(false)} disabled={add.isPending}>
            {t('common.cancel')}
          </button>
          <button
            type="submit"
            className="btn-primary inline-flex items-center gap-2 disabled:opacity-60"
            disabled={!valid || add.isPending}
          >
            {add.isPending && <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />}
            {t('growth.goals.addSubmit')}
          </button>
        </div>
      </form>
    </section>
  )
}
