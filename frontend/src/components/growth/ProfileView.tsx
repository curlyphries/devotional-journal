import { useId, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import {
  BookOpenCheck,
  HeartHandshake,
  History,
  Loader2,
  Lock,
  Pencil,
  ShieldCheck,
  Sprout,
  Trash2,
  UserRound,
} from 'lucide-react'
import { guidesKeys, type Catalog } from '../../api/guides'
import {
  eraseGrowthProfile,
  growthKeys,
  submitAssessment,
  updateGrowthProfile,
  type GrowthProfile,
  type MoodKey,
  type TraitScore,
} from '../../api/profile'
import { formatDate } from '../../lib/dates'
import { MOODS, moodLabelKey } from '../../lib/moods'
import ConfirmDialog from '../ConfirmDialog'
import DictationButton from '../DictationButton'
import InlineError from '../InlineError'
import { useToast } from '../Toast'
import ProfileInsights from './ProfileInsights'
import {
  AboutFields,
  InwardFields,
  LookingForFields,
  TraitRatingFields,
  type AboutValues,
  type LookingForValues,
} from './ProfileFields'
import { MeterBar, Notice, RatingDots, ThemeChips } from './primitives'
import { useApplyProfile } from './useGrowthProfile'

const sectionTitle = 'text-lg font-semibold text-text-primary'
const subTitle = 'text-sm font-semibold uppercase tracking-wider text-text-secondary'

function titleOf(list: { key: string; title: string }[], key: string | null): string | null {
  if (!key) return null
  return list.find((item) => item.key === key)?.title ?? key.replace(/[_-]+/g, ' ')
}

interface ProfileViewProps {
  profile: GrowthProfile
  catalog: Catalog
  /** Go through the four setup steps again. */
  onRestartSetup: () => void
  /** Called after the profile has been erased and re-read. */
  onErased: () => void
}

/** The growth profile as calm cards: what the person said, what it adds up to, and how to correct or erase it. */
export default function ProfileView({ profile, catalog, onRestartSetup, onErased }: ProfileViewProps) {
  const { t } = useTranslation()
  const [retaking, setRetaking] = useState(false)

  return (
    <div className="space-y-6">
      {profile.support?.message && (
        <section
          role="note"
          aria-label={t('profile.support.label')}
          className="flex items-start gap-3 rounded-xl border-2 border-accent-secondary bg-accent-secondary/10 p-4 sm:p-5"
        >
          <HeartHandshake className="mt-0.5 h-6 w-6 flex-shrink-0 text-accent-primary" aria-hidden="true" />
          <div className="min-w-0">
            <h2 className="font-semibold text-text-primary">{t('profile.support.title')}</h2>
            <p className="mt-1 whitespace-pre-wrap leading-relaxed text-text-primary">{profile.support.message}</p>
          </div>
        </section>
      )}

      <AboutCard profile={profile} catalog={catalog} onRestartSetup={onRestartSetup} />
      <WalkCard profile={profile} />

      {profile.profiling_enabled ? (
        <>
          <InnerCard profile={profile} />
          <OverTimeCard
            profile={profile}
            catalog={catalog}
            retaking={retaking}
            onRetake={() => setRetaking(true)}
            onClose={() => setRetaking(false)}
          />
          <ProfileInsights profile={profile} />
        </>
      ) : (
        <section className="card space-y-3 p-4 sm:p-6" aria-labelledby="child-profile-heading">
          <div className="flex items-center gap-2">
            <ShieldCheck className="h-5 w-5 flex-shrink-0 text-accent-primary" aria-hidden="true" />
            <h2 id="child-profile-heading" className={sectionTitle}>
              {t('profile.child.title')}
            </h2>
          </div>
          <p className="leading-relaxed text-text-primary">{t('profile.child.body')}</p>
          <p className="text-sm text-text-secondary">{t('profile.child.hidden')}</p>
          {profile.disclaimer && (
            <p className="border-t border-border pt-3 text-sm leading-relaxed text-text-secondary">{profile.disclaimer}</p>
          )}
        </section>
      )}

      <DataCard onErased={onErased} />
    </div>
  )
}

// ---------------------------------------------------------------------------
// About you
// ---------------------------------------------------------------------------

function AboutCard({
  profile,
  catalog,
  onRestartSetup,
}: {
  profile: GrowthProfile
  catalog: Catalog
  onRestartSetup: () => void
}) {
  const { t } = useTranslation()
  const toast = useToast()
  const applyProfile = useApplyProfile()
  const id = useId()
  const aboutMeRef = useRef<HTMLTextAreaElement>(null)

  const [editing, setEditing] = useState(false)
  const [about, setAbout] = useState<AboutValues>({ lifeStage: null, situations: [], faithBackground: null })
  const [lookingFor, setLookingFor] = useState<LookingForValues>({ needs: [], desiredTraits: [] })
  const [aboutMe, setAboutMe] = useState(profile.about_me ?? '')

  const startEditing = () => {
    setAbout({
      lifeStage: profile.life_stage,
      situations: profile.situations ?? [],
      faithBackground: profile.faith_background,
    })
    setLookingFor({ needs: profile.needs ?? [], desiredTraits: profile.desired_traits ?? [] })
    save.reset()
    setEditing(true)
  }

  const save = useMutation({
    mutationFn: () =>
      updateGrowthProfile({
        situations: about.situations,
        needs: lookingFor.needs,
        desired_traits: lookingFor.desiredTraits,
        ...(about.lifeStage ? { life_stage: about.lifeStage } : {}),
        ...(about.faithBackground ? { faith_background: about.faithBackground } : {}),
      }),
    onSuccess: (updated) => {
      applyProfile(updated, { lifeStageChanged: true })
      setEditing(false)
      toast.success(t('profile.about.saved'))
    },
    meta: { silent: true }, // the error is rendered inline in the form
  })

  const saveAboutMe = useMutation({
    mutationFn: () => updateGrowthProfile({ about_me: aboutMe.trim() }),
    onSuccess: (updated) => {
      applyProfile(updated)
      setAboutMe(updated.about_me ?? '')
      toast.success(t('profile.aboutMe.saved'))
    },
    meta: { silent: true }, // the error is rendered inline under the box
  })

  const allTopics = catalog.categories.flatMap((category) => category.topics)
  const stage = catalog.life_stages.find((item) => item.key === profile.life_stage)
  const situations = (profile.situations ?? []).map((key) => titleOf(catalog.situations, key) ?? key)
  const needs = (profile.needs ?? []).map((key) => titleOf(allTopics, key) ?? key)
  const traits = (profile.desired_traits ?? []).map((key) => titleOf(catalog.traits, key) ?? key)
  const mostlyEmpty =
    !profile.assessment && needs.length === 0 && traits.length === 0 && situations.length === 0 && profile.profiling_enabled
  const notSaid = <span className="text-text-secondary">{t('profile.about.notSaid')}</span>

  const chips = (items: string[]) =>
    items.length > 0 ? (
      <ul className="flex flex-wrap gap-1.5">
        {items.map((item) => (
          <li key={item} className="rounded-full border border-border bg-bg-elevated px-2.5 py-0.5 text-sm text-text-primary">
            {item}
          </li>
        ))}
      </ul>
    ) : (
      notSaid
    )

  return (
    <section className="card space-y-5 p-4 sm:p-6" aria-labelledby={`${id}-title`}>
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <UserRound className="h-5 w-5 flex-shrink-0 text-accent-primary" aria-hidden="true" />
          <h2 id={`${id}-title`} className={sectionTitle}>
            {t('profile.about.title')}
          </h2>
        </div>
        {!editing && (
          <button
            type="button"
            className="btn-secondary inline-flex items-center gap-2 text-sm"
            onClick={startEditing}
            aria-label={t('profile.about.editLabel')}
          >
            <Pencil className="h-4 w-4" aria-hidden="true" />
            {t('common.edit')}
          </button>
        )}
      </div>

      {editing ? (
        <form
          className="space-y-6"
          onSubmit={(event) => {
            event.preventDefault()
            save.mutate()
          }}
        >
          <AboutFields catalog={catalog} values={about} onChange={setAbout} />
          <LookingForFields catalog={catalog} values={lookingFor} onChange={setLookingFor} />
          {save.isError && <InlineError error={save.error} title={t('profile.about.saveFailed')} />}
          <div className="flex flex-wrap justify-end gap-3 border-t border-border pt-4">
            <button type="button" className="btn-secondary" disabled={save.isPending} onClick={() => setEditing(false)}>
              {t('common.cancel')}
            </button>
            <button type="submit" className="btn-primary inline-flex items-center gap-2 disabled:opacity-60" disabled={save.isPending}>
              {save.isPending && <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />}
              {t('profile.about.save')}
            </button>
          </div>
        </form>
      ) : (
        <>
          <dl className="grid gap-x-6 gap-y-4 sm:grid-cols-2">
            <div>
              <dt className="text-sm text-text-secondary">{t('profile.fields.lifeStage')}</dt>
              <dd className="mt-1 text-text-primary">{stage?.title ?? titleOf([], profile.life_stage) ?? notSaid}</dd>
            </div>
            <div>
              <dt className="text-sm text-text-secondary">{t('profile.fields.faithBackground')}</dt>
              <dd className="mt-1 text-text-primary">
                {titleOf(catalog.faith_backgrounds, profile.faith_background) ?? notSaid}
              </dd>
            </div>
            <div className="sm:col-span-2">
              <dt className="text-sm text-text-secondary">{t('profile.fields.situations')}</dt>
              <dd className="mt-1">{chips(situations)}</dd>
            </div>
            <div className="sm:col-span-2">
              <dt className="text-sm text-text-secondary">{t('profile.about.needs')}</dt>
              <dd className="mt-1">{chips(needs)}</dd>
            </div>
            <div className="sm:col-span-2">
              <dt className="text-sm text-text-secondary">{t('profile.about.desiredTraits')}</dt>
              <dd className="mt-1">{chips(traits)}</dd>
            </div>
          </dl>
          {mostlyEmpty && (
            <Notice>
              <p className="text-text-primary">{t('profile.about.mostlyEmpty')}</p>
              <button
                type="button"
                className="rounded font-medium text-accent-primary underline-offset-2 hover:underline focus:outline-none focus-visible:ring-2 focus-visible:ring-accent-primary"
                onClick={onRestartSetup}
              >
                {t('profile.about.restartSetup')}
              </button>
            </Notice>
          )}
        </>
      )}

      <form
        className="space-y-2 border-t border-border pt-5"
        onSubmit={(event) => {
          event.preventDefault()
          saveAboutMe.mutate()
        }}
      >
        <label htmlFor={`${id}-about-me`} className="block font-medium text-text-primary">
          {t('profile.aboutMe.label')}
        </label>
        <p id={`${id}-about-me-hint`} className="text-sm text-text-secondary">
          {t('profile.aboutMe.hint')}
        </p>
        <textarea
          id={`${id}-about-me`}
          ref={aboutMeRef}
          aria-describedby={`${id}-about-me-hint`}
          className="input min-h-[6rem] w-full"
          maxLength={2000}
          value={aboutMe}
          onChange={(event) => setAboutMe(event.target.value)}
        />
        {saveAboutMe.isError && <InlineError error={saveAboutMe.error} title={t('profile.aboutMe.saveFailed')} />}
        <div className="flex flex-wrap items-start justify-between gap-3">
          <DictationButton value={aboutMe} onChange={setAboutMe} textareaRef={aboutMeRef} hidePrivacyNote className="min-w-0" />
          <button
            type="submit"
            className="btn-primary inline-flex items-center gap-2 disabled:opacity-60"
            disabled={saveAboutMe.isPending || aboutMe.trim() === (profile.about_me ?? '').trim()}
          >
            {saveAboutMe.isPending && <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />}
            {t('common.save')}
          </button>
        </div>
      </form>
    </section>
  )
}

// ---------------------------------------------------------------------------
// Your walk with God
// ---------------------------------------------------------------------------

function TraitList({ title, hint, items }: { title: string; hint: string; items: TraitScore[] }) {
  const id = useId()
  return (
    <div>
      <h3 id={id} className={subTitle}>
        {title}
      </h3>
      <p className="mt-0.5 text-xs text-text-secondary">{hint}</p>
      <ul aria-labelledby={id} className="mt-2 space-y-1.5">
        {items.map((item) => (
          <li key={item.trait} className="flex items-center justify-between gap-3 text-text-primary">
            <span className="min-w-0 break-words">{item.title}</span>
            <RatingDots rating={item.score} />
          </li>
        ))}
      </ul>
    </div>
  )
}

function WalkCard({ profile }: { profile: GrowthProfile }) {
  const { t } = useTranslation()
  const id = useId()
  const spiritual = profile.spiritual
  const practices = spiritual?.practices ?? []
  const strengths = spiritual?.strengths ?? []
  const growthAreas = spiritual?.growth_areas ?? []
  const themes = spiritual?.top_themes ?? []
  // For a child no assessment is taken, so an all-empty list of bars would only be noise.
  const showPractices = practices.length > 0 && (profile.profiling_enabled || practices.some((item) => item.score != null))

  const counts = [
    { label: t('profile.walk.studiesCompleted'), value: spiritual?.studies_completed ?? 0 },
    { label: t('profile.walk.lessonsCompleted'), value: spiritual?.lessons_completed ?? 0 },
    { label: t('profile.walk.entriesWithFeedback'), value: spiritual?.entries_with_feedback ?? 0 },
  ]

  return (
    <section className="card space-y-5 p-4 sm:p-6" aria-labelledby={`${id}-title`}>
      <div>
        <div className="flex items-center gap-2">
          <BookOpenCheck className="h-5 w-5 flex-shrink-0 text-accent-primary" aria-hidden="true" />
          <h2 id={`${id}-title`} className={sectionTitle}>
            {t('profile.walk.title')}
          </h2>
        </div>
        <p className="mt-1 text-sm text-text-secondary">{t('profile.walk.intro')}</p>
      </div>

      {showPractices && (
        <div>
          <h3 className={subTitle}>{t('profile.walk.practices')}</h3>
          <div className="mt-3 space-y-3">
            {practices.map((item) => (
              <MeterBar key={item.key} label={item.label} value={item.score} />
            ))}
          </div>
        </div>
      )}

      {profile.profiling_enabled &&
        (strengths.length > 0 || growthAreas.length > 0 ? (
          <div className="grid gap-5 sm:grid-cols-2">
            {strengths.length > 0 && (
              <TraitList title={t('profile.walk.strengths')} hint={t('profile.walk.strengthsHint')} items={strengths} />
            )}
            {growthAreas.length > 0 && (
              <TraitList title={t('profile.walk.growthAreas')} hint={t('profile.walk.growthAreasHint')} items={growthAreas} />
            )}
          </div>
        ) : (
          <p className="text-sm text-text-secondary">{t('profile.walk.noRatings')}</p>
        ))}

      <dl className="grid grid-cols-3 gap-3">
        {counts.map((count) => (
          <div
            key={count.label}
            className="flex flex-col-reverse justify-end rounded-lg border border-border bg-bg-elevated/50 p-3 text-center"
          >
            <dt className="mt-1 break-words text-xs leading-snug text-text-secondary">{count.label}</dt>
            <dd className="text-2xl font-semibold text-text-primary">{count.value}</dd>
          </div>
        ))}
      </dl>

      {themes.length > 0 && (
        <div>
          <h3 className={subTitle}>{t('profile.walk.topThemes')}</h3>
          <p className="mb-2 mt-0.5 text-xs text-text-secondary">{t('profile.walk.topThemesHint')}</p>
          <ThemeChips themes={themes} label={t('profile.walk.topThemes')} />
        </div>
      )}
    </section>
  )
}

// ---------------------------------------------------------------------------
// How you are doing inside
// ---------------------------------------------------------------------------

function InnerCard({ profile }: { profile: GrowthProfile }) {
  const { t } = useTranslation()
  const id = useId()
  const inner = profile.inner_life
  const items = inner?.items ?? []
  const themes = inner?.recurring_themes ?? []
  const moodCounts = inner?.mood_counts ?? {}
  const moods = MOODS.map((mood) => ({ id: mood.id, count: moodCounts[mood.id as MoodKey] ?? 0 })).filter(
    (mood) => mood.count > 0,
  )
  const maxMood = Math.max(1, ...moods.map((mood) => mood.count))
  const openThreads = inner?.open_threads ?? 0
  const averages = [
    { label: t('profile.inner.understanding'), hint: t('profile.inner.understandingHint'), value: inner?.understanding_avg ?? null },
    { label: t('profile.inner.resonance'), hint: t('profile.inner.resonanceHint'), value: inner?.resonance_avg ?? null },
  ]

  return (
    <section className="card space-y-5 p-4 sm:p-6" aria-labelledby={`${id}-title`}>
      <div>
        <div className="flex items-center gap-2">
          <Sprout className="h-5 w-5 flex-shrink-0 text-accent-primary" aria-hidden="true" />
          <h2 id={`${id}-title`} className={sectionTitle}>
            {t('profile.inner.title')}
          </h2>
        </div>
        <p className="mt-1 text-sm text-text-secondary">{t('profile.inner.intro')}</p>
      </div>

      {items.length > 0 && (
        <div className="space-y-3">
          {items.map((item) => (
            <MeterBar key={item.key} label={item.label} value={item.score} />
          ))}
        </div>
      )}

      <div>
        <h3 className={subTitle}>{t('profile.inner.moods')}</h3>
        {moods.length > 0 ? (
          <>
            <p className="mt-0.5 text-xs text-text-secondary">{t('profile.inner.moodsHint')}</p>
            <ul className="mt-3 space-y-2">
              {moods.map((mood) => (
                <li key={mood.id} className="grid grid-cols-[6.5rem_1fr_2rem] items-center gap-3 text-sm">
                  <span className="truncate text-text-primary">{t(moodLabelKey(mood.id))}</span>
                  <span aria-hidden="true" className="h-2 overflow-hidden rounded-full bg-bg-elevated">
                    <span
                      className="block h-full rounded-full bg-text-secondary"
                      style={{ width: `${(mood.count / maxMood) * 100}%` }}
                    />
                  </span>
                  <span className="text-right text-text-secondary">
                    {mood.count}
                    <span className="sr-only"> {t('profile.inner.moodEntries', { count: mood.count })}</span>
                  </span>
                </li>
              ))}
            </ul>
          </>
        ) : (
          <p className="mt-1 text-sm text-text-secondary">{t('profile.inner.noMoods')}</p>
        )}
      </div>

      {themes.length > 0 && (
        <div>
          <h3 className={`${subTitle} mb-2`}>{t('profile.inner.recurringThemes')}</h3>
          <ThemeChips themes={themes} label={t('profile.inner.recurringThemes')} />
        </div>
      )}

      <div>
        <h3 className={subTitle}>{t('profile.inner.fromLessons')}</h3>
        <dl className="mt-2 grid gap-3 sm:grid-cols-2">
          {averages.map((average) => (
            <div key={average.label} className="rounded-lg border border-border bg-bg-elevated/50 p-3">
              <dt className="text-sm text-text-primary">{average.label}</dt>
              <dd className="mt-1 text-lg font-semibold text-text-primary">
                {average.value != null ? (
                  t('growth.scale.value', { value: average.value.toFixed(1), max: 5 })
                ) : (
                  <span className="text-sm font-normal text-text-secondary">{t('profile.inner.noLessonsYet')}</span>
                )}
              </dd>
              <dd className="mt-1 text-xs text-text-secondary">{average.hint}</dd>
            </div>
          ))}
        </dl>
      </div>

      <p className="text-sm text-text-primary">
        {t('profile.inner.openThreads', { count: openThreads })}{' '}
        <Link to="/threads" className="text-accent-primary underline-offset-2 hover:underline">
          {t('profile.inner.seeThreads')}
        </Link>
      </p>
    </section>
  )
}

// ---------------------------------------------------------------------------
// Over time
// ---------------------------------------------------------------------------

function OverTimeCard({
  profile,
  catalog,
  retaking,
  onRetake,
  onClose,
}: {
  profile: GrowthProfile
  catalog: Catalog
  retaking: boolean
  onRetake: () => void
  onClose: () => void
}) {
  const { t, i18n } = useTranslation()
  const toast = useToast()
  const applyProfile = useApplyProfile()
  const id = useId()
  const assessment = profile.assessment
  const [answers, setAnswers] = useState<Record<string, number>>({})
  const [ratings, setRatings] = useState<Record<string, number>>({})

  const save = useMutation({
    mutationFn: () => submitAssessment({ answers, trait_ratings: ratings }),
    onSuccess: (updated) => {
      applyProfile(updated)
      onClose()
      toast.success(t('profile.overTime.saved'))
    },
    meta: { silent: true }, // the error is rendered inline in the form
  })

  const open = () => {
    // Start from the last answers so only what has changed needs touching.
    setAnswers(assessment?.answers ?? {})
    setRatings(assessment?.trait_ratings ?? {})
    save.reset()
    onRetake()
  }

  // Newest first reads more naturally in a list; the server sends oldest first.
  const history = [...(assessment?.history ?? [])].reverse()
  const average = (value: number | null) =>
    value != null ? value.toFixed(1) : <span className="text-text-secondary">{t('growth.scale.notAnswered')}</span>
  const nothingToSave = Object.keys(answers).length === 0 && Object.keys(ratings).length === 0

  return (
    <section className="card space-y-4 p-4 sm:p-6" aria-labelledby={`${id}-title`}>
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div className="min-w-0">
          <div className="flex items-center gap-2">
            <History className="h-5 w-5 flex-shrink-0 text-accent-primary" aria-hidden="true" />
            <h2 id={`${id}-title`} className={sectionTitle}>
              {t('profile.overTime.title')}
            </h2>
          </div>
          <p className="mt-1 text-sm text-text-secondary">
            {assessment
              ? t('profile.overTime.lastTaken', { date: formatDate(assessment.taken_at, i18n.language) })
              : t('profile.overTime.neverTaken')}
          </p>
        </div>
        {!retaking && (
          <button type="button" className="btn-secondary text-sm" onClick={open}>
            {assessment ? t('profile.overTime.retake') : t('profile.overTime.take')}
          </button>
        )}
      </div>

      {retaking ? (
        <form
          className="space-y-6"
          onSubmit={(event) => {
            event.preventDefault()
            save.mutate()
          }}
        >
          {assessment && <p className="text-sm text-text-secondary">{t('profile.overTime.prefilled')}</p>}
          <InwardFields
            items={catalog.assessment.items}
            scale={catalog.assessment.scale}
            answers={answers}
            onChange={setAnswers}
          />
          <section aria-label={t('profile.setup.today.title')}>
            <h3 className="mb-3 text-base font-semibold text-text-primary">{t('profile.setup.today.title')}</h3>
            <TraitRatingFields
              traits={catalog.traits}
              desiredTraits={profile.desired_traits ?? []}
              ratings={ratings}
              onChange={setRatings}
            />
          </section>
          {save.isError && <InlineError error={save.error} title={t('profile.overTime.saveFailed')} />}
          <div className="flex flex-wrap justify-end gap-3 border-t border-border pt-4">
            <button type="button" className="btn-secondary" disabled={save.isPending} onClick={onClose}>
              {t('common.cancel')}
            </button>
            <button
              type="submit"
              className="btn-primary inline-flex items-center gap-2 disabled:opacity-60"
              disabled={save.isPending || nothingToSave}
            >
              {save.isPending && <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />}
              {t('profile.overTime.save')}
            </button>
          </div>
        </form>
      ) : history.length > 0 ? (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <caption className="sr-only">{t('profile.overTime.caption')}</caption>
            <thead>
              <tr className="border-b border-border text-text-secondary">
                <th scope="col" className="py-2 pr-3 font-medium">
                  {t('profile.overTime.date')}
                </th>
                <th scope="col" className="px-3 py-2 font-medium">
                  {t('profile.walk.title')}
                </th>
                <th scope="col" className="py-2 pl-3 font-medium">
                  {t('profile.inner.title')}
                </th>
              </tr>
            </thead>
            <tbody>
              {history.map((point, index) => (
                <tr key={`${point.taken_at}-${index}`} className="border-b border-border last:border-0">
                  <th scope="row" className="whitespace-nowrap py-2 pr-3 font-normal text-text-primary">
                    {formatDate(point.taken_at, i18n.language, { year: 'numeric', month: 'short', day: 'numeric' })}
                  </th>
                  <td className="px-3 py-2 text-text-primary">{average(point.practices_avg)}</td>
                  <td className="py-2 pl-3 text-text-primary">{average(point.inner_avg)}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <p className="mt-2 text-xs text-text-secondary">{t('profile.overTime.averagesHint')}</p>
        </div>
      ) : (
        <p className="text-sm text-text-secondary">{t('profile.overTime.empty')}</p>
      )}
    </section>
  )
}

// ---------------------------------------------------------------------------
// Your data
// ---------------------------------------------------------------------------

function DataCard({ onErased }: { onErased: () => void }) {
  const { t, i18n } = useTranslation()
  const toast = useToast()
  const queryClient = useQueryClient()
  const id = useId()
  const [confirming, setConfirming] = useState(false)

  const erase = useMutation({
    mutationFn: eraseGrowthProfile,
    onSuccess: async () => {
      queryClient.invalidateQueries({ queryKey: guidesKeys.profileBasics() })
      queryClient.invalidateQueries({ queryKey: guidesKeys.recommendations(i18n.language) })
      // Wait for the fresh (now empty) profile so the page goes straight back to first run.
      await queryClient.invalidateQueries({ queryKey: growthKeys.profile(i18n.language) })
      setConfirming(false)
      toast.success(t('profile.data.erased'))
      onErased()
    },
    onError: (err) => {
      setConfirming(false)
      toast.fromError(err, t('profile.data.eraseFailed'))
    },
  })

  return (
    <section className="card space-y-4 p-4 sm:p-6" aria-labelledby={`${id}-title`}>
      <div className="flex items-center gap-2">
        <Lock className="h-5 w-5 flex-shrink-0 text-accent-primary" aria-hidden="true" />
        <h2 id={`${id}-title`} className={sectionTitle}>
          {t('profile.data.title')}
        </h2>
      </div>
      <p className="leading-relaxed text-text-secondary">{t('profile.data.stored')}</p>
      <p className="leading-relaxed text-text-secondary">{t('profile.data.control')}</p>
      <div className="flex flex-wrap items-center gap-x-5 gap-y-3">
        <button
          type="button"
          className="btn-secondary inline-flex items-center gap-2"
          onClick={() => setConfirming(true)}
        >
          <Trash2 className="h-4 w-4" aria-hidden="true" />
          {t('profile.data.erase')}
        </button>
        <Link to="/audit" className="text-sm text-accent-primary underline-offset-2 hover:underline">
          {t('profile.data.auditLink')}
        </Link>
        <Link to="/help#study" className="text-sm text-accent-primary underline-offset-2 hover:underline">
          {t('profile.data.helpLink')}
        </Link>
      </div>

      <ConfirmDialog
        open={confirming}
        title={t('profile.data.eraseTitle')}
        message={t('profile.data.eraseBody')}
        confirmLabel={t('profile.data.eraseConfirm')}
        destructive
        busy={erase.isPending}
        onConfirm={() => erase.mutate()}
        onCancel={() => setConfirming(false)}
      />
    </section>
  )
}
