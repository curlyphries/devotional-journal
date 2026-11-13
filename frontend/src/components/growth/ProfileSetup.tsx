import { useEffect, useId, useRef, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { ArrowLeft, ArrowRight, Check, Loader2, ShieldCheck } from 'lucide-react'
import type { Catalog } from '../../api/guides'
import { submitAssessment, updateGrowthProfile, type GrowthProfile, type ProfilePatch } from '../../api/profile'
import InlineError from '../InlineError'
import { useApplyProfile } from './useGrowthProfile'
import {
  AboutFields,
  InwardFields,
  LookingForFields,
  TraitRatingFields,
  type AboutValues,
  type LookingForValues,
} from './ProfileFields'
import { Notice } from './primitives'

type StepKey = 'about' | 'looking' | 'inward' | 'today'

const ALL_STEPS: StepKey[] = ['about', 'looking', 'inward', 'today']
/** Children get no inner-life profile, so the two inward-looking steps are left out. */
const CHILD_STEPS: StepKey[] = ['about', 'looking']

interface ProfileSetupProps {
  catalog: Catalog
  profile: GrowthProfile
  /** Called once the person finishes (or skips through) the last step. */
  onDone: () => void
}

/**
 * First-run setup: four short steps, each optional. What is filled in is
 * saved when the person moves on, so nothing is lost by stopping part-way.
 */
export default function ProfileSetup({ catalog, profile, onDone }: ProfileSetupProps) {
  const { t } = useTranslation()
  const applyProfile = useApplyProfile()
  const headingId = useId()
  const headingRef = useRef<HTMLHeadingElement>(null)

  const [stepIndex, setStepIndex] = useState(0)
  const [about, setAbout] = useState<AboutValues>({
    lifeStage: profile.life_stage,
    situations: profile.situations ?? [],
    faithBackground: profile.faith_background,
  })
  const [lookingFor, setLookingFor] = useState<LookingForValues>({
    needs: profile.needs ?? [],
    desiredTraits: profile.desired_traits ?? [],
  })
  const [answers, setAnswers] = useState<Record<string, number>>(profile.assessment?.answers ?? {})
  const [traitRatings, setTraitRatings] = useState<Record<string, number>>(profile.assessment?.trait_ratings ?? {})
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<unknown>(null)
  // Whether anything has reached the server yet (an empty profile is created at the end otherwise).
  const savedSomething = useRef(profile.exists)

  const childMode =
    about.lifeStage === 'child' || (about.lifeStage === profile.life_stage && profile.exists && !profile.profiling_enabled)
  const steps = childMode ? CHILD_STEPS : ALL_STEPS
  const index = Math.min(stepIndex, steps.length - 1)
  const step = steps[index]
  const isLast = index === steps.length - 1

  // Move focus to the new step's heading so keyboard and screen-reader users land on it.
  const firstRender = useRef(true)
  useEffect(() => {
    if (firstRender.current) {
      firstRender.current = false
      return
    }
    headingRef.current?.focus()
  }, [index])

  /** Save the current step. Resolves to the updated profile, or null when there was nothing to save. */
  const persist = async (): Promise<GrowthProfile | null> => {
    if (step === 'about') {
      const patch: ProfilePatch = { situations: about.situations }
      if (about.lifeStage) patch.life_stage = about.lifeStage
      if (about.faithBackground) patch.faith_background = about.faithBackground
      return updateGrowthProfile(patch)
    }
    if (step === 'looking') {
      return updateGrowthProfile({ needs: lookingFor.needs, desired_traits: lookingFor.desiredTraits })
    }
    const hasAnswers = Object.keys(answers).length > 0
    const hasRatings = Object.keys(traitRatings).length > 0
    if (step === 'inward') {
      return hasAnswers ? submitAssessment({ answers, trait_ratings: traitRatings }) : null
    }
    // Send the answers again with the ratings so the latest assessment is complete.
    return hasAnswers || hasRatings ? submitAssessment({ answers, trait_ratings: traitRatings }) : null
  }

  const advance = async () => {
    if (!isLast) {
      setStepIndex(index + 1)
      return
    }
    if (!savedSomething.current) {
      // Everything was skipped: still create the (empty) profile so the person is not asked again.
      const created = await updateGrowthProfile({
        situations: about.situations,
        needs: lookingFor.needs,
        desired_traits: lookingFor.desiredTraits,
      })
      savedSomething.current = true
      applyProfile(created)
    }
    onDone()
  }

  const run = async (save: boolean) => {
    setError(null)
    setSaving(true)
    try {
      if (save) {
        const updated = await persist()
        if (updated) {
          savedSomething.current = true
          applyProfile(updated, { lifeStageChanged: step === 'about' })
        }
      }
      await advance()
    } catch (err) {
      setError(err)
    } finally {
      setSaving(false)
    }
  }

  const childNote = (
    <Notice icon={<ShieldCheck className="h-5 w-5" aria-hidden="true" />} title={t('profile.child.title')}>
      <p className="text-text-primary">{t('profile.child.body')}</p>
    </Notice>
  )

  return (
    <section className="card space-y-6 p-4 sm:p-6" aria-labelledby={headingId}>
      <div>
        <p className="text-sm text-text-secondary">
          {t('profile.setup.stepOf', { current: index + 1, total: steps.length })}
        </p>
        <ol className="mt-2 flex gap-2" aria-label={t('profile.setup.stepsLabel')}>
          {steps.map((key, position) => (
            <li key={key} className="min-w-0 flex-1" aria-current={position === index ? 'step' : undefined}>
              <span
                aria-hidden="true"
                className={`block h-1.5 rounded-full ${position <= index ? 'bg-accent-primary' : 'bg-bg-elevated'}`}
              />
              <span
                className={`sr-only mt-1.5 truncate text-xs sm:not-sr-only sm:block ${
                  position === index ? 'text-text-primary' : 'text-text-secondary'
                }`}
              >
                {t(`profile.setup.${key}.short`)}
              </span>
            </li>
          ))}
        </ol>
      </div>

      <div>
        <h2
          id={headingId}
          ref={headingRef}
          tabIndex={-1}
          className="text-xl font-semibold text-text-primary focus:outline-none"
        >
          {t(`profile.setup.${step}.title`)}
        </h2>
        <p className="mt-1 text-text-secondary">{t(`profile.setup.${step}.intro`)}</p>
      </div>

      {step === 'about' && (
        <>
          <AboutFields catalog={catalog} values={about} onChange={setAbout} />
          {childMode && childNote}
        </>
      )}
      {step === 'looking' && (
        <>
          <LookingForFields catalog={catalog} values={lookingFor} onChange={setLookingFor} />
          {childMode && childNote}
        </>
      )}
      {step === 'inward' && (
        <InwardFields
          items={catalog.assessment.items}
          scale={catalog.assessment.scale}
          answers={answers}
          onChange={setAnswers}
        />
      )}
      {step === 'today' && (
        <TraitRatingFields
          traits={catalog.traits}
          desiredTraits={lookingFor.desiredTraits}
          ratings={traitRatings}
          onChange={setTraitRatings}
        />
      )}

      {error != null && <InlineError error={error} title={t('profile.setup.saveFailed')} />}

      <div className="flex flex-wrap items-center justify-between gap-3 border-t border-border pt-4">
        <button
          type="button"
          className="btn-secondary inline-flex items-center gap-2 disabled:opacity-50"
          disabled={index === 0 || saving}
          onClick={() => {
            setError(null)
            setStepIndex(index - 1)
          }}
        >
          <ArrowLeft className="h-4 w-4" aria-hidden="true" />
          {t('common.back')}
        </button>
        <div className="flex flex-wrap items-center gap-3">
          <button
            type="button"
            className="rounded px-2 py-2 text-sm text-text-secondary underline-offset-2 hover:text-text-primary hover:underline focus:outline-none focus-visible:ring-2 focus-visible:ring-accent-primary disabled:opacity-50"
            disabled={saving}
            onClick={() => run(false)}
          >
            {t('profile.setup.skipStep')}
          </button>
          <button
            type="button"
            className="btn-primary inline-flex items-center gap-2 disabled:opacity-60"
            disabled={saving}
            onClick={() => run(true)}
          >
            {saving ? (
              <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
            ) : isLast ? (
              <Check className="h-4 w-4" aria-hidden="true" />
            ) : null}
            {isLast ? t('profile.setup.finish') : t('common.next')}
            {!isLast && !saving && <ArrowRight className="h-4 w-4" aria-hidden="true" />}
          </button>
        </div>
      </div>
      <p className="text-xs text-text-secondary">{t('profile.setup.savedAsYouGo')}</p>
    </section>
  )
}
