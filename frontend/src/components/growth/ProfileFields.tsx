import { useId, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { ChevronDown } from 'lucide-react'
import type { AssessmentItem, Catalog, CatalogTrait } from '../../api/guides'
import { Chip, ScaleInput } from './primitives'

export const MAX_DESIRED_TRAITS = 3
/** How many characteristics to offer for self-rating when the person has not chosen any. */
const DEFAULT_RATED_TRAITS = 4

function toggle(list: string[], key: string): string[] {
  return list.includes(key) ? list.filter((item) => item !== key) : [...list, key]
}

const groupLabel = 'text-sm font-semibold text-text-primary'
const groupHint = 'mt-0.5 text-sm text-text-secondary'

// ---------------------------------------------------------------------------
// About you
// ---------------------------------------------------------------------------

export interface AboutValues {
  lifeStage: string | null
  situations: string[]
  faithBackground: string | null
}

interface AboutFieldsProps {
  catalog: Catalog
  values: AboutValues
  onChange: (values: AboutValues) => void
}

/** Life stage, walks of life and faith background. Everything is optional. */
export function AboutFields({ catalog, values, onChange }: AboutFieldsProps) {
  const { t } = useTranslation()
  const id = useId()

  return (
    <div className="space-y-6">
      <fieldset>
        <legend className={groupLabel}>{t('profile.fields.lifeStage')}</legend>
        <p className={groupHint}>{t('profile.fields.lifeStageHint')}</p>
        <div className="mt-3 grid gap-2 sm:grid-cols-2">
          {catalog.life_stages.map((stage) => {
            const checked = values.lifeStage === stage.key
            return (
              <label
                key={stage.key}
                className={`flex cursor-pointer items-start gap-3 rounded-lg border p-3 transition-colors focus-within:ring-2 focus-within:ring-accent-primary ${
                  checked ? 'border-accent-primary bg-accent-primary/10' : 'border-border bg-bg-elevated hover:border-accent-primary'
                }`}
              >
                <input
                  type="radio"
                  name={`${id}-stage`}
                  value={stage.key}
                  checked={checked}
                  onChange={() => onChange({ ...values, lifeStage: stage.key })}
                  className="mt-1 h-4 w-4 flex-shrink-0 accent-accent-primary"
                />
                <span className="min-w-0">
                  <span className="block font-medium text-text-primary">{stage.title}</span>
                  {stage.note && <span className="block text-sm text-text-secondary">{stage.note}</span>}
                </span>
              </label>
            )
          })}
        </div>
      </fieldset>

      <div role="group" aria-labelledby={`${id}-situations`}>
        <p id={`${id}-situations`} className={groupLabel}>
          {t('profile.fields.situations')}
        </p>
        <p className={groupHint}>{t('profile.fields.situationsHint')}</p>
        <div className="mt-3 flex flex-wrap gap-2">
          {catalog.situations.map((situation) => (
            <Chip
              key={situation.key}
              selected={values.situations.includes(situation.key)}
              onToggle={() => onChange({ ...values, situations: toggle(values.situations, situation.key) })}
            >
              {situation.title}
            </Chip>
          ))}
        </div>
      </div>

      <fieldset>
        <legend className={groupLabel}>{t('profile.fields.faithBackground')}</legend>
        <p className={groupHint}>{t('profile.fields.faithBackgroundHint')}</p>
        <div className="mt-3 space-y-1.5">
          {catalog.faith_backgrounds.map((background) => (
            <label key={background.key} className="flex cursor-pointer items-start gap-3 rounded-lg px-1 py-1 text-text-primary">
              <input
                type="radio"
                name={`${id}-faith`}
                value={background.key}
                checked={values.faithBackground === background.key}
                onChange={() => onChange({ ...values, faithBackground: background.key })}
                className="mt-1 h-4 w-4 flex-shrink-0 accent-accent-primary"
              />
              <span className="min-w-0">{background.title}</span>
            </label>
          ))}
        </div>
      </fieldset>
    </div>
  )
}

// ---------------------------------------------------------------------------
// What you are looking for
// ---------------------------------------------------------------------------

export interface LookingForValues {
  needs: string[]
  desiredTraits: string[]
}

interface LookingForFieldsProps {
  catalog: Catalog
  values: LookingForValues
  onChange: (values: LookingForValues) => void
}

/** Topics the person wants help with, and up to three characteristics to grow in. */
export function LookingForFields({ catalog, values, onChange }: LookingForFieldsProps) {
  const { t } = useTranslation()
  const id = useId()
  const [focusedTrait, setFocusedTrait] = useState<string | null>(values.desiredTraits[0] ?? null)
  const atLimit = values.desiredTraits.length >= MAX_DESIRED_TRAITS
  const shownTrait = catalog.traits.find((trait) => trait.key === focusedTrait)

  return (
    <div className="space-y-6">
      <div role="group" aria-labelledby={`${id}-needs`}>
        <p id={`${id}-needs`} className={groupLabel}>
          {t('profile.fields.needs')}
        </p>
        <p className={groupHint}>{t('profile.fields.needsHint')}</p>
        <div className="mt-3 space-y-4">
          {catalog.categories.map((category) => (
            <div key={category.key} role="group" aria-labelledby={`${id}-cat-${category.key}`}>
              <p id={`${id}-cat-${category.key}`} className="text-xs font-semibold uppercase tracking-wider text-text-secondary">
                {category.title}
              </p>
              <div className="mt-2 flex flex-wrap gap-2">
                {category.topics.map((topic) => (
                  <Chip
                    key={topic.key}
                    selected={values.needs.includes(topic.key)}
                    onToggle={() => onChange({ ...values, needs: toggle(values.needs, topic.key) })}
                  >
                    {topic.title}
                  </Chip>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div role="group" aria-labelledby={`${id}-traits`} aria-describedby={`${id}-traits-hint`}>
        <p id={`${id}-traits`} className={groupLabel}>
          {t('profile.fields.desiredTraits')}
        </p>
        <p id={`${id}-traits-hint`} className={groupHint}>
          {t('profile.fields.desiredTraitsHint', { max: MAX_DESIRED_TRAITS, chosen: values.desiredTraits.length })}
        </p>
        <div className="mt-3 flex flex-wrap gap-2">
          {catalog.traits.map((trait) => {
            const selected = values.desiredTraits.includes(trait.key)
            return (
              <Chip
                key={trait.key}
                selected={selected}
                disabled={!selected && atLimit}
                onFocus={() => setFocusedTrait(trait.key)}
                onMouseEnter={() => setFocusedTrait(trait.key)}
                onToggle={() => {
                  setFocusedTrait(trait.key)
                  onChange({ ...values, desiredTraits: toggle(values.desiredTraits, trait.key) })
                }}
              >
                {trait.title}
              </Chip>
            )
          })}
        </div>
        <p aria-live="polite" className="mt-3 min-h-[2.5rem] rounded-lg border border-border bg-bg-elevated px-3 py-2 text-sm text-text-secondary">
          {shownTrait ? (
            <>
              <span className="font-medium text-text-primary">{shownTrait.title}: </span>
              {shownTrait.definition}
            </>
          ) : (
            t('profile.fields.traitDefinitionEmpty')
          )}
        </p>
      </div>
    </div>
  )
}

// ---------------------------------------------------------------------------
// A look inward
// ---------------------------------------------------------------------------

interface InwardFieldsProps {
  items: AssessmentItem[]
  /** The scale legend, e.g. "1 = not at all … 5 = very much". Shown once. */
  scale: string
  answers: Record<string, number>
  onChange: (answers: Record<string, number>) => void
}

/** The self-assessment items under their two headings. Any item can be left blank. */
export function InwardFields({ items, scale, answers, onChange }: InwardFieldsProps) {
  const { t } = useTranslation()
  const groups = [
    { area: 'practices' as const, title: t('profile.walk.title') },
    { area: 'inner' as const, title: t('profile.inner.title') },
  ]

  const setAnswer = (key: string, value: number | null) => {
    const next = { ...answers }
    if (value == null) delete next[key]
    else next[key] = value
    onChange(next)
  }

  return (
    <div className="space-y-6">
      <p className="rounded-lg border border-border bg-bg-elevated px-3 py-2 text-sm text-text-secondary">
        <span className="font-medium text-text-primary">{t('profile.fields.scaleLabel')} </span>
        {scale}
      </p>
      {groups.map((group) => {
        const groupItems = items.filter((item) => item.area === group.area)
        if (groupItems.length === 0) return null
        return (
          <section key={group.area} aria-label={group.title}>
            <h3 className="text-base font-semibold text-text-primary">{group.title}</h3>
            <div className="mt-3 space-y-5">
              {groupItems.map((item) => (
                <ScaleInput
                  key={item.key}
                  label={item.text}
                  value={answers[item.key] ?? null}
                  onChange={(value) => setAnswer(item.key, value)}
                />
              ))}
            </div>
          </section>
        )
      })}
    </div>
  )
}

// ---------------------------------------------------------------------------
// How you see yourself today
// ---------------------------------------------------------------------------

interface TraitRatingFieldsProps {
  traits: CatalogTrait[]
  /** The characteristics the person wants to grow in; rated first. */
  desiredTraits: string[]
  ratings: Record<string, number>
  onChange: (ratings: Record<string, number>) => void
}

/** A 1-5 self-rating per characteristic: a few first, the rest behind "Rate more". */
export function TraitRatingFields({ traits, desiredTraits, ratings, onChange }: TraitRatingFieldsProps) {
  const { t } = useTranslation()
  const [showAll, setShowAll] = useState(false)
  const moreId = useId()

  const chosen = traits.filter((trait) => desiredTraits.includes(trait.key))
  const first = chosen.length > 0 ? chosen : traits.slice(0, DEFAULT_RATED_TRAITS)
  const rest = traits.filter((trait) => !first.includes(trait))

  const setRating = (key: string, value: number | null) => {
    const next = { ...ratings }
    if (value == null) delete next[key]
    else next[key] = value
    onChange(next)
  }

  const row = (trait: CatalogTrait) => (
    <ScaleInput
      key={trait.key}
      label={<span className="font-medium">{trait.title}</span>}
      hint={trait.definition}
      value={ratings[trait.key] ?? null}
      onChange={(value) => setRating(trait.key, value)}
    />
  )

  return (
    <div className="space-y-5">
      <p className="rounded-lg border border-border bg-bg-elevated px-3 py-2 text-sm text-text-secondary">
        <span className="font-medium text-text-primary">{t('profile.fields.scaleLabel')} </span>
        {t('profile.fields.traitScale')}
      </p>
      {chosen.length > 0 && <p className="text-sm text-text-secondary">{t('profile.fields.ratingChosenFirst')}</p>}
      {first.map(row)}
      {rest.length > 0 && (
        <div>
          <button
            type="button"
            aria-expanded={showAll}
            aria-controls={moreId}
            onClick={() => setShowAll((open) => !open)}
            className="inline-flex items-center gap-1.5 rounded text-sm font-medium text-accent-primary underline-offset-2 hover:underline focus:outline-none focus-visible:ring-2 focus-visible:ring-accent-primary"
          >
            <ChevronDown className={`h-4 w-4 transition-transform ${showAll ? 'rotate-180' : ''}`} aria-hidden="true" />
            {showAll ? t('profile.fields.rateFewer') : t('profile.fields.rateMore', { count: rest.length })}
          </button>
          <div id={moreId} className={showAll ? 'mt-5 space-y-5' : 'hidden'}>
            {showAll && rest.map(row)}
          </div>
        </div>
      )}
    </div>
  )
}
