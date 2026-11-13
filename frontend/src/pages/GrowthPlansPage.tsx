import { useEffect, useRef, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { ArrowRight, BellRing, Plus, Sprout } from 'lucide-react'
import type { GrowthPlan } from '../api/growthPlans'
import InlineError from '../components/InlineError'
import StartPlanForm from '../components/growth/StartPlanForm'
import { MeterBar } from '../components/growth/primitives'
import { useGrowthPlans } from '../components/growth/useGrowthPlans'
import { useGrowthProfile, useGuidesCatalog } from '../components/growth/useGrowthProfile'

function PlanRow({ plan }: { plan: GrowthPlan }) {
  const { t } = useTranslation()
  const progress = plan.progress
  return (
    <li className="card space-y-3 p-4 sm:p-5">
      <div className="flex flex-wrap items-start justify-between gap-2">
        <h3 className="min-w-0 text-lg font-semibold text-text-primary">
          <Link to={`/growth/${plan.id}`} className="break-words underline-offset-2 hover:underline">
            {plan.trait.title}
          </Link>
        </h3>
        <div className="flex flex-wrap items-center gap-2">
          {plan.status !== 'active' && (
            <span className="rounded-full border border-border px-2.5 py-0.5 text-xs text-text-secondary">
              {t(`growth.status.${plan.status}`)}
            </span>
          )}
          {progress?.check_in_due && plan.status === 'active' && (
            <span className="inline-flex items-center gap-1.5 rounded-full border border-accent-primary bg-accent-primary/15 px-2.5 py-0.5 text-xs font-medium text-text-primary">
              <BellRing className="h-3.5 w-3.5" aria-hidden="true" />
              {t('growth.checkInDue')}
            </span>
          )}
        </div>
      </div>
      {plan.why && <p className="line-clamp-2 break-words text-sm text-text-secondary">{plan.why}</p>}
      {progress && (
        <MeterBar
          tone="accent"
          label={progress.stage_label}
          value={progress.percent}
          max={100}
          valueText={t('growth.percent', { percent: progress.percent })}
        />
      )}
      <Link
        to={`/growth/${plan.id}`}
        className="inline-flex items-center gap-1.5 text-sm font-medium text-accent-primary underline-offset-2 hover:underline"
        aria-label={t('growth.list.openNamed', { trait: plan.trait.title })}
      >
        {t('growth.list.open')}
        <ArrowRight className="h-4 w-4" aria-hidden="true" />
      </Link>
    </li>
  )
}

/** Growth plans: the characteristics a person has chosen to grow in, and a way to start another. */
export default function GrowthPlansPage() {
  const { t } = useTranslation()
  const [searchParams] = useSearchParams()
  const requestedTrait = searchParams.get('trait')
  const plans = useGrowthPlans()
  const catalog = useGuidesCatalog()
  // Only used to suggest what the person already said they want to grow in; fine if it fails.
  const profile = useGrowthProfile()

  const [trait, setTrait] = useState<string | null>(requestedTrait)
  const [formOpen, setFormOpen] = useState(!!requestedTrait)
  const formRef = useRef<HTMLElement>(null)

  // Follow the link when it changes (e.g. a second suggestion clicked from the profile).
  useEffect(() => {
    if (requestedTrait) {
      setTrait(requestedTrait)
      setFormOpen(true)
    }
  }, [requestedTrait])

  const list = plans.data ?? []
  const traits = catalog.data?.traits ?? []
  const hasPlans = list.length > 0
  const showForm = formOpen || (plans.isSuccess && !hasPlans)
  const desired = (profile.data?.desired_traits ?? [])
    .map((key) => traits.find((item) => item.key === key))
    .filter((item): item is NonNullable<typeof item> => !!item)
    // Not for something already under way (or paused): that plan is in the list above.
    .filter((item) => !list.some((plan) => plan.trait.key === item.key && plan.status !== 'completed'))

  const choose = (key: string) => {
    setTrait(key)
    setFormOpen(true)
    // Wait for the form to be on the page before moving to it.
    requestAnimationFrame(() => {
      formRef.current?.scrollIntoView?.({ block: 'start', behavior: 'smooth' })
      formRef.current?.focus()
    })
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <header>
        <div className="flex items-center gap-2">
          <Sprout className="h-6 w-6 flex-shrink-0 text-accent-primary" aria-hidden="true" />
          <h1 className="text-2xl font-bold text-text-primary">{t('growth.title')}</h1>
        </div>
        <p className="mt-2 leading-relaxed text-text-secondary">{t('growth.intro')}</p>
      </header>

      <section aria-labelledby="growth-plans-heading" className="space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <h2 id="growth-plans-heading" className="text-lg font-semibold text-text-primary">
            {t('growth.list.title')}
          </h2>
          {hasPlans && !showForm && (
            <button
              type="button"
              className="btn-secondary inline-flex items-center gap-2 text-sm"
              onClick={() => {
                setFormOpen(true)
                requestAnimationFrame(() => formRef.current?.focus())
              }}
            >
              <Plus className="h-4 w-4" aria-hidden="true" />
              {t('growth.list.startAnother')}
            </button>
          )}
        </div>

        {plans.isLoading ? (
          <div role="status" className="space-y-4">
            <span className="sr-only">{t('common.loading')}</span>
            {[0, 1].map((row) => (
              <div key={row} className="card animate-pulse space-y-3" aria-hidden="true">
                <div className="h-5 w-1/3 rounded bg-bg-elevated" />
                <div className="h-3 w-2/3 rounded bg-bg-elevated" />
                <div className="h-2 w-full rounded bg-bg-elevated" />
              </div>
            ))}
          </div>
        ) : plans.isError ? (
          <InlineError error={plans.error} title={t('growth.list.failed')} onRetry={() => plans.refetch()} />
        ) : !hasPlans ? (
          <div className="card space-y-3 p-4 sm:p-6">
            <p className="font-medium text-text-primary">{t('growth.list.emptyTitle')}</p>
            <p className="text-text-secondary">{t('growth.list.emptyBody')}</p>
          </div>
        ) : (
          <ul className="space-y-4">
            {list.map((plan) => (
              <PlanRow key={plan.id} plan={plan} />
            ))}
          </ul>
        )}

        {desired.length > 0 && (
          <div className="rounded-xl border border-border bg-bg-elevated/50 p-4" role="group" aria-labelledby="growth-suggested-heading">
            <p id="growth-suggested-heading" className="text-sm text-text-primary">
              {t('growth.list.fromProfile')}
            </p>
            <div className="mt-2 flex flex-wrap gap-2">
              {desired.map((item) => (
                <button
                  key={item.key}
                  type="button"
                  className="btn-secondary text-sm"
                  onClick={() => choose(item.key)}
                  aria-label={t('growth.list.chooseNamed', { trait: item.title })}
                >
                  {item.title}
                </button>
              ))}
            </div>
          </div>
        )}
      </section>

      {showForm && (
        <section
          ref={formRef}
          tabIndex={-1}
          className="card space-y-5 p-4 focus:outline-none sm:p-6"
          aria-labelledby="growth-start-heading"
        >
          <div>
            <h2 id="growth-start-heading" className="text-lg font-semibold text-text-primary">
              {t('growth.start.title')}
            </h2>
            <p className="mt-1 text-sm text-text-secondary">{t('growth.start.intro')}</p>
          </div>
          {catalog.isLoading ? (
            <p role="status" className="text-sm text-text-secondary">
              {t('common.loading')}
            </p>
          ) : catalog.isError || !catalog.data ? (
            <InlineError error={catalog.error} title={t('growth.start.catalogFailed')} onRetry={() => catalog.refetch()} />
          ) : (
            <StartPlanForm traits={traits} trait={trait} onTraitChange={setTrait} plans={list} />
          )}
        </section>
      )}
    </div>
  )
}
