import { useId, useState } from 'react'
import { Link, useLocation, useNavigate, useParams } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import {
  ArrowLeft,
  BookOpen,
  Check,
  Compass,
  ExternalLink,
  Info,
  Loader2,
  Pause,
  Pencil,
  Play,
  RotateCcw,
  Trash2,
  TrendingUp,
} from 'lucide-react'
import {
  deleteGrowthPlan,
  updateGrowthPlan,
  type GrowthPlan,
  type GrowthPlanStatus,
  type PlanNotice,
} from '../api/growthPlans'
import { toApiError } from '../api/errors'
import { growthKeys } from '../api/profile'
import { formatDate } from '../lib/dates'
import ConfirmDialog from '../components/ConfirmDialog'
import InlineError from '../components/InlineError'
import { useToast } from '../components/Toast'
import PlanCheckIns from '../components/growth/PlanCheckIns'
import { AddGoalForm, GoalGroup } from '../components/growth/PlanGoals'
import TopicStudyCard from '../components/growth/TopicStudyCard'
import { MeterBar, Notice } from '../components/growth/primitives'
import { useGrowthPlan, usePlanMutation } from '../components/growth/useGrowthPlans'

const bibleLink = (reference: string) => `/bible?passage=${encodeURIComponent(reference)}`

function BackLink() {
  const { t } = useTranslation()
  return (
    <Link
      to="/growth"
      className="inline-flex items-center gap-1.5 text-sm text-text-secondary underline-offset-2 hover:text-text-primary hover:underline"
    >
      <ArrowLeft className="h-4 w-4" aria-hidden="true" />
      {t('growth.plan.back')}
    </Link>
  )
}

function ScriptureLink({ reference }: { reference: string }) {
  const { t } = useTranslation()
  return (
    <Link
      to={bibleLink(reference)}
      className="inline-flex items-center gap-1.5 text-accent-primary underline-offset-2 hover:underline"
      aria-label={t('growth.plan.openInBible', { reference })}
    >
      {reference}
      <ExternalLink className="h-3.5 w-3.5" aria-hidden="true" />
    </Link>
  )
}

// ---------------------------------------------------------------------------
// Header: what the plan is for, and its status
// ---------------------------------------------------------------------------

function PlanHeader({ plan }: { plan: GrowthPlan }) {
  const { t, i18n } = useTranslation()
  const toast = useToast()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const id = useId()
  const [editingWhy, setEditingWhy] = useState(false)
  const [why, setWhy] = useState(plan.why ?? '')
  const [confirmingDelete, setConfirmingDelete] = useState(false)

  const setStatus = usePlanMutation((status: GrowthPlanStatus) => updateGrowthPlan(plan.id, { status }), {
    errorTitle: t('growth.plan.statusFailed'),
    onSuccess: (_plan, status) => toast.success(t(`growth.plan.statusChanged.${status}`)),
  })
  const saveWhy = usePlanMutation(() => updateGrowthPlan(plan.id, { why: why.trim() }), {
    errorTitle: t('growth.plan.whyFailed'),
    onSuccess: () => setEditingWhy(false),
  })
  const remove = useMutation({
    mutationFn: () => deleteGrowthPlan(plan.id),
    onSuccess: () => {
      queryClient.removeQueries({ queryKey: growthKeys.plan(plan.id, i18n.language) })
      queryClient.invalidateQueries({ queryKey: growthKeys.plans(i18n.language) })
      toast.success(t('growth.plan.deleted'))
      navigate('/growth')
    },
    onError: (err) => {
      setConfirmingDelete(false)
      toast.fromError(err, t('growth.plan.deleteFailed'))
    },
  })

  const busy = setStatus.isPending

  return (
    <header className="space-y-4">
      <BackLink />
      <div>
        <div className="flex flex-wrap items-center gap-3">
          <h1 className="min-w-0 break-words text-2xl font-bold text-text-primary">{plan.trait.title}</h1>
          <span className="rounded-full border border-border px-2.5 py-0.5 text-xs text-text-secondary">
            {t(`growth.status.${plan.status}`)}
          </span>
        </div>
        <p className="mt-2 leading-relaxed text-text-secondary">{plan.trait.definition}</p>
      </div>

      <div className="rounded-xl border border-border bg-bg-surface p-4">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <h2 id={`${id}-why`} className="text-sm font-semibold uppercase tracking-wider text-text-secondary">
            {t('growth.plan.why')}
          </h2>
          {!editingWhy && (
            <button
              type="button"
              className="inline-flex items-center gap-1.5 rounded text-sm text-accent-primary underline-offset-2 hover:underline focus:outline-none focus-visible:ring-2 focus-visible:ring-accent-primary"
              onClick={() => {
                setWhy(plan.why ?? '')
                setEditingWhy(true)
              }}
              aria-label={t('growth.plan.editWhy')}
            >
              <Pencil className="h-3.5 w-3.5" aria-hidden="true" />
              {plan.why ? t('common.edit') : t('growth.plan.addWhy')}
            </button>
          )}
        </div>
        {editingWhy ? (
          <form
            className="mt-2 space-y-2"
            onSubmit={(event) => {
              event.preventDefault()
              saveWhy.mutate()
            }}
          >
            <textarea
              aria-labelledby={`${id}-why`}
              className="input min-h-[5rem] w-full"
              maxLength={1000}
              autoFocus
              value={why}
              onChange={(event) => setWhy(event.target.value)}
            />
            <div className="flex flex-wrap gap-2">
              <button type="submit" className="btn-primary px-3 py-1.5 text-sm disabled:opacity-60" disabled={saveWhy.isPending}>
                {t('common.save')}
              </button>
              <button type="button" className="btn-secondary px-3 py-1.5 text-sm" onClick={() => setEditingWhy(false)}>
                {t('common.cancel')}
              </button>
            </div>
          </form>
        ) : plan.why ? (
          <p className="mt-1 whitespace-pre-wrap break-words leading-relaxed text-text-primary">{plan.why}</p>
        ) : (
          <p className="mt-1 text-sm text-text-secondary">{t('growth.plan.noWhy')}</p>
        )}
      </div>

      <div className="flex flex-wrap items-center gap-2" role="group" aria-label={t('growth.plan.actions')}>
        {plan.status === 'active' && (
          <button
            type="button"
            className="btn-secondary inline-flex items-center gap-2 text-sm disabled:opacity-60"
            disabled={busy}
            onClick={() => setStatus.mutate('paused')}
          >
            <Pause className="h-4 w-4" aria-hidden="true" />
            {t('growth.plan.pause')}
          </button>
        )}
        {plan.status === 'paused' && (
          <button
            type="button"
            className="btn-primary inline-flex items-center gap-2 text-sm disabled:opacity-60"
            disabled={busy}
            onClick={() => setStatus.mutate('active')}
          >
            <Play className="h-4 w-4" aria-hidden="true" />
            {t('growth.plan.resume')}
          </button>
        )}
        {plan.status !== 'completed' ? (
          <button
            type="button"
            className="btn-secondary inline-flex items-center gap-2 text-sm disabled:opacity-60"
            disabled={busy}
            onClick={() => setStatus.mutate('completed')}
          >
            <Check className="h-4 w-4" aria-hidden="true" />
            {t('growth.plan.complete')}
          </button>
        ) : (
          <button
            type="button"
            className="btn-secondary inline-flex items-center gap-2 text-sm disabled:opacity-60"
            disabled={busy}
            onClick={() => setStatus.mutate('active')}
          >
            <RotateCcw className="h-4 w-4" aria-hidden="true" />
            {t('growth.plan.reopen')}
          </button>
        )}
        <button
          type="button"
          className="btn-secondary inline-flex items-center gap-2 text-sm"
          onClick={() => setConfirmingDelete(true)}
        >
          <Trash2 className="h-4 w-4" aria-hidden="true" />
          {t('common.delete')}
        </button>
        {busy && <Loader2 className="h-4 w-4 animate-spin text-text-secondary" aria-hidden="true" />}
      </div>

      <ConfirmDialog
        open={confirmingDelete}
        title={t('growth.plan.deleteTitle')}
        message={t('growth.plan.deleteBody', { trait: plan.trait.title })}
        confirmLabel={t('growth.plan.deleteConfirm')}
        destructive
        busy={remove.isPending}
        onConfirm={() => remove.mutate()}
        onCancel={() => setConfirmingDelete(false)}
      />
    </header>
  )
}

// ---------------------------------------------------------------------------
// Progress
// ---------------------------------------------------------------------------

function ProgressCard({ plan }: { plan: GrowthPlan }) {
  const { t, i18n } = useTranslation()
  const progress = plan.progress
  const rating =
    plan.baseline_rating != null && plan.current_rating != null
      ? t('growth.progress.ratingFromTo', { from: plan.baseline_rating, to: plan.current_rating })
      : plan.baseline_rating != null
        ? t('growth.progress.ratingStart', { rating: plan.baseline_rating })
        : plan.current_rating != null
          ? t('growth.progress.ratingNow', { rating: plan.current_rating })
          : t('growth.progress.ratingNone')

  const facts = [
    { label: t('growth.progress.time'), value: t('growth.progress.day', { day: progress.days_in, total: progress.days_total }) },
    { label: t('growth.progress.rating'), value: rating },
    { label: t('growth.progress.goals'), value: t('growth.progress.goalsValue', { done: progress.goals_done, total: progress.goals_total }) },
    { label: t('growth.progress.lessons'), value: String(progress.lessons_done) },
  ]

  return (
    <section className="card space-y-4 p-4 sm:p-6" aria-labelledby="plan-progress-heading">
      <div className="flex items-center gap-2">
        <TrendingUp className="h-5 w-5 flex-shrink-0 text-accent-primary" aria-hidden="true" />
        <h2 id="plan-progress-heading" className="text-lg font-semibold text-text-primary">
          {t('growth.progress.title')}
        </h2>
      </div>
      <MeterBar
        tone="accent"
        label={progress.stage_label}
        value={progress.percent}
        max={100}
        valueText={t('growth.percent', { percent: progress.percent })}
      />
      {progress.summary && <p className="leading-relaxed text-text-primary">{progress.summary}</p>}
      <dl className="grid grid-cols-2 gap-3 sm:grid-cols-4">
        {facts.map((fact) => (
          <div key={fact.label} className="rounded-lg border border-border bg-bg-elevated/50 p-3">
            <dt className="text-xs text-text-secondary">{fact.label}</dt>
            <dd className="mt-1 break-words font-medium text-text-primary">{fact.value}</dd>
          </div>
        ))}
      </dl>
      {plan.target_date && (
        <p className="text-xs text-text-secondary">
          {t('growth.progress.dates', {
            start: formatDate(plan.started_at, i18n.language),
            target: formatDate(plan.target_date, i18n.language),
          })}
        </p>
      )}
    </section>
  )
}

// ---------------------------------------------------------------------------
// Page
// ---------------------------------------------------------------------------

/** One growth plan: why it matters, where it stands, its goals, studies and check-ins. */
export default function GrowthPlanPage() {
  const { t } = useTranslation()
  const { planId } = useParams<{ planId: string }>()
  const location = useLocation()
  const query = useGrowthPlan(planId)

  if (query.isLoading) {
    return (
      <div className="mx-auto max-w-3xl space-y-6">
        <BackLink />
        <div role="status" className="space-y-4">
          <span className="sr-only">{t('common.loading')}</span>
          <div className="animate-pulse space-y-3" aria-hidden="true">
            <div className="h-7 w-1/2 rounded bg-bg-elevated" />
            <div className="h-3 w-full rounded bg-bg-elevated" />
          </div>
          {[0, 1, 2].map((row) => (
            <div key={row} className="card animate-pulse space-y-3" aria-hidden="true">
              <div className="h-5 w-1/3 rounded bg-bg-elevated" />
              <div className="h-3 w-full rounded bg-bg-elevated" />
              <div className="h-3 w-2/3 rounded bg-bg-elevated" />
            </div>
          ))}
        </div>
      </div>
    )
  }

  if (query.isError || !query.data) {
    const notFound = toApiError(query.error).status === 404
    return (
      <div className="mx-auto max-w-3xl space-y-6">
        <BackLink />
        {notFound ? (
          <div className="card text-center">
            <Compass className="mx-auto mb-3 h-10 w-10 text-accent-primary" aria-hidden="true" />
            <h1 className="text-xl font-semibold text-text-primary">{t('growth.plan.notFoundTitle')}</h1>
            <p className="mt-2 text-text-secondary">{t('growth.plan.notFoundBody')}</p>
            <Link to="/growth" className="btn-primary mt-5 inline-block">
              {t('growth.plan.back')}
            </Link>
          </div>
        ) : (
          <InlineError error={query.error} title={t('growth.plan.loadFailed')} onRetry={() => query.refetch()} />
        )}
      </div>
    )
  }

  const plan = query.data
  // The create response carries the notice; keep it if a later read of the plan does not.
  const carried = (location.state as { personalizeError?: PlanNotice | null } | null)?.personalizeError
  const personalizeError = plan.personalize_error ?? carried ?? null
  const scripture = plan.scripture ?? []
  const topics = plan.topics ?? []

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <PlanHeader plan={plan} />

      {personalizeError && (
        <Notice icon={<Info className="h-5 w-5" aria-hidden="true" />} title={t('growth.plan.personalizeErrorTitle')}>
          <p className="text-text-primary">{personalizeError.message}</p>
          {personalizeError.suggestion && <p className="text-text-secondary">{personalizeError.suggestion}</p>}
        </Notice>
      )}

      <ProgressCard plan={plan} />

      <PlanCheckIns plan={plan} />

      <section className="card space-y-4 p-4 sm:p-6" aria-labelledby="plan-scripture-heading">
        <div className="flex items-center gap-2">
          <BookOpen className="h-5 w-5 flex-shrink-0 text-accent-primary" aria-hidden="true" />
          <h2 id="plan-scripture-heading" className="text-lg font-semibold text-text-primary">
            {t('growth.scripture.title')}
          </h2>
        </div>
        {scripture.length > 0 && (
          <ul className="flex flex-wrap gap-x-5 gap-y-2">
            {scripture.map((item) => (
              <li key={item.reference}>
                <ScriptureLink reference={item.reference} />
              </li>
            ))}
          </ul>
        )}
        {plan.jesus?.note && (
          <div className="rounded-xl border border-border bg-bg-elevated/50 p-4">
            <h3 className="text-sm font-semibold uppercase tracking-wider text-text-secondary">
              {t('growth.scripture.jesus')}
            </h3>
            <p className="mt-2 leading-relaxed text-text-primary">{plan.jesus.note}</p>
            {plan.jesus.reference && (
              <p className="mt-2 text-sm">
                <ScriptureLink reference={plan.jesus.reference} />
              </p>
            )}
          </div>
        )}
      </section>

      <GoalGroup plan={plan} horizon="short" />
      <GoalGroup plan={plan} horizon="long" />
      <div className="space-y-2">
        <AddGoalForm planId={plan.id} />
        <p className="text-xs text-text-secondary">
          {plan.goal_source === 'ai' ? t('growth.plan.goalSourceAi') : t('growth.plan.goalSourceCatalog')}
        </p>
      </div>

      {topics.length > 0 && (
        <section className="card space-y-4 p-4 sm:p-6" aria-labelledby="plan-studies-heading">
          <div>
            <h2 id="plan-studies-heading" className="text-lg font-semibold text-text-primary">
              {t('growth.studies.title')}
            </h2>
            <p className="mt-1 text-sm text-text-secondary">{t('growth.studies.hint')}</p>
          </div>
          <ul className="grid gap-3 sm:grid-cols-2">
            {topics.map((topic) => (
              <TopicStudyCard key={topic.key} topic={topic} />
            ))}
          </ul>
        </section>
      )}
    </div>
  )
}
