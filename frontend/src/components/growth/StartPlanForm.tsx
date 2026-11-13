import { useId, useRef, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { Loader2, Sprout } from 'lucide-react'
import type { CatalogTrait } from '../../api/guides'
import { createGrowthPlan, type CreateGrowthPlanPayload, type GrowthPlan } from '../../api/growthPlans'
import { growthKeys } from '../../api/profile'
import AiStatusBanner from '../AiStatusBanner'
import DictationButton from '../DictationButton'
import InlineError from '../InlineError'
import { useAiWhereSentence } from './aiWhere'
import { Chip, Notice, ScaleInput } from './primitives'

interface StartPlanFormProps {
  traits: CatalogTrait[]
  /** The chosen characteristic (owned by the page so suggestions elsewhere can set it). */
  trait: string | null
  onTraitChange: (trait: string | null) => void
  /** Plans the person already has, to point at instead of starting a duplicate. */
  plans: GrowthPlan[]
}

/** Choose one characteristic, say why, and start a plan for it. */
export default function StartPlanForm({ traits, trait, onTraitChange, plans }: StartPlanFormProps) {
  const { t, i18n } = useTranslation()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const whereSentence = useAiWhereSentence()
  const id = useId()
  const whyRef = useRef<HTMLTextAreaElement>(null)

  const [why, setWhy] = useState('')
  const [rating, setRating] = useState<number | null>(null)
  const [personalize, setPersonalize] = useState(false)

  const selected = traits.find((item) => item.key === trait) ?? null
  const existing = selected ? plans.find((plan) => plan.trait.key === selected.key && plan.status === 'active') : undefined

  const create = useMutation({
    mutationFn: (payload: CreateGrowthPlanPayload) => createGrowthPlan(payload),
    onSuccess: (plan) => {
      queryClient.setQueryData(growthKeys.plan(plan.id, i18n.language), plan)
      queryClient.invalidateQueries({ queryKey: growthKeys.plans(i18n.language) })
      // Carried along in case a later read of the plan no longer includes it.
      navigate(`/growth/${plan.id}`, { state: { personalizeError: plan.personalize_error ?? null } })
    },
  })

  const submit = (event: React.FormEvent) => {
    event.preventDefault()
    if (!selected || existing) return
    const payload: CreateGrowthPlanPayload = { trait: selected.key }
    if (why.trim()) payload.why = why.trim()
    if (rating != null) payload.baseline_rating = rating
    if (personalize) payload.personalize = true
    create.mutate(payload)
  }

  return (
    <form className="space-y-6" onSubmit={submit}>
      <div role="group" aria-labelledby={`${id}-trait`}>
        <p id={`${id}-trait`} className="font-medium text-text-primary">
          {t('growth.start.chooseTrait')}
        </p>
        <p className="mt-0.5 text-sm text-text-secondary">{t('growth.start.chooseTraitHint')}</p>
        <div className="mt-3 flex flex-wrap gap-2">
          {traits.map((item) => (
            <Chip
              key={item.key}
              selected={item.key === trait}
              onToggle={() => onTraitChange(item.key === trait ? null : item.key)}
            >
              {item.title}
            </Chip>
          ))}
        </div>
        <p aria-live="polite" className="mt-3 min-h-[2.5rem] rounded-lg border border-border bg-bg-elevated px-3 py-2 text-sm text-text-secondary">
          {selected ? (
            <>
              <span className="font-medium text-text-primary">{selected.title}: </span>
              {selected.definition}
            </>
          ) : (
            t('growth.start.noTrait')
          )}
        </p>
      </div>

      {existing ? (
        <Notice>
          <p className="text-text-primary">{t('growth.start.alreadyActive', { trait: existing.trait.title })}</p>
          <Link to={`/growth/${existing.id}`} className="font-medium text-accent-primary underline-offset-2 hover:underline">
            {t('growth.start.openExisting')}
          </Link>
        </Notice>
      ) : (
        <>
          <div>
            <label htmlFor={`${id}-why`} className="block font-medium text-text-primary">
              {t('growth.start.why')} <span className="font-normal text-text-secondary">{t('growth.optional')}</span>
            </label>
            <p id={`${id}-why-hint`} className="mt-0.5 text-sm text-text-secondary">
              {t('growth.start.whyHint')}
            </p>
            <textarea
              id={`${id}-why`}
              ref={whyRef}
              aria-describedby={`${id}-why-hint`}
              className="input mt-2 min-h-[5rem] w-full"
              maxLength={1000}
              value={why}
              onChange={(event) => setWhy(event.target.value)}
            />
            <DictationButton value={why} onChange={setWhy} textareaRef={whyRef} hidePrivacyNote className="mt-2" />
          </div>

          <ScaleInput
            label={<span className="font-medium">{t('growth.start.baseline')}</span>}
            hint={t('growth.start.baselineHint')}
            value={rating}
            onChange={setRating}
          />

          <div>
            <label className="flex cursor-pointer items-start gap-3">
              <input
                type="checkbox"
                className="mt-1 h-4 w-4 flex-shrink-0 accent-accent-primary"
                checked={personalize}
                onChange={(event) => setPersonalize(event.target.checked)}
                aria-describedby={`${id}-ai-hint`}
              />
              <span className="font-medium text-text-primary">{t('growth.start.personalize')}</span>
            </label>
            <p id={`${id}-ai-hint`} className="ml-7 mt-1 text-sm text-text-secondary">
              {t('growth.start.personalizeHint')} {whereSentence}
            </p>
            {personalize && <AiStatusBanner className="ml-7 mt-2" />}
          </div>

          {create.isError && <InlineError error={create.error} title={t('growth.start.failed')} />}

          {create.isPending && personalize && (
            <p role="status" className="flex items-start gap-2 text-sm text-text-secondary">
              <Loader2 className="mt-0.5 h-4 w-4 flex-shrink-0 animate-spin text-accent-primary" aria-hidden="true" />
              {t('growth.start.personalizing')}
            </p>
          )}

          <button
            type="submit"
            className="btn-primary inline-flex items-center gap-2 disabled:cursor-not-allowed disabled:opacity-60"
            disabled={!selected || create.isPending}
          >
            {create.isPending ? (
              <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
            ) : (
              <Sprout className="h-4 w-4" aria-hidden="true" />
            )}
            {selected ? t('growth.start.submitNamed', { trait: selected.title }) : t('growth.start.submit')}
          </button>
        </>
      )}
    </form>
  )
}
