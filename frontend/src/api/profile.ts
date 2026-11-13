/**
 * Growth profile API (`/guides/profile/`): what the person told the app about
 * themselves, their self-assessment, and the reflection the app writes from it.
 *
 * Every call sends `?lang=` so the server answers in the UI language.
 */
import client, { AI_TIMEOUT_MS } from './client'
import { guidesLang, type TopicCard } from './guides'

/**
 * React Query keys. They sit under `['guides']` (see `guidesKeys` in guides.ts)
 * so finishing a lesson, which invalidates everything there, also refreshes
 * the profile and the growth plans.
 */
export const growthKeys = {
  profile: (lang: string) => ['guides', 'profile', lang] as const,
  plans: (lang: string) => ['guides', 'plans', lang] as const,
  plan: (planId: string, lang: string) => ['guides', 'plan', planId, lang] as const,
}

export interface ScoredItem {
  key: string
  label: string
  /** 1-5, or null when the person has not answered it. */
  score: number | null
}

export interface TraitScore {
  trait: string
  title: string
  score: number
}

export interface ThemeCount {
  theme: string
  count: number
}

export interface AssessmentHistoryPoint {
  taken_at: string
  practices_avg: number | null
  inner_avg: number | null
}

export interface ProfileAssessment {
  taken_at: string
  answers: Record<string, number>
  trait_ratings: Record<string, number>
  /** Oldest first. */
  history: AssessmentHistoryPoint[]
}

export interface ProfileInsightItem {
  id: string
  area: 'spiritual' | 'inner'
  title: string
  text: string
  /** What the statement is based on, in plain sentences. */
  evidence: string[]
  /** The person's own verdict: true = "that's right", false = "that's not me". */
  accurate: boolean | null
}

export interface ProfileInsights {
  generated_at: string
  provider: string
  model: string
  local: boolean
  summary: string
  items: ProfileInsightItem[]
  encouragement: string
  suggested_topics: TopicCard[]
  suggested_traits: { key: string; title: string }[]
}

export type MoodKey = 'grateful' | 'struggling' | 'convicted' | 'peaceful' | 'fired_up'

export interface GrowthProfile {
  /** False until the person has saved anything. */
  exists: boolean
  life_stage: string | null
  situations: string[]
  faith_background: string | null
  needs: string[]
  desired_traits: string[]
  about_me: string
  /** False for the "child" life stage: no inner-life profile or AI reflection is built for children. */
  profiling_enabled: boolean
  assessment: ProfileAssessment | null
  spiritual: {
    practices: ScoredItem[]
    strengths: TraitScore[]
    growth_areas: TraitScore[]
    studies_completed: number
    lessons_completed: number
    entries_with_feedback: number
    top_themes: ThemeCount[]
  }
  inner_life: {
    items: ScoredItem[]
    mood_counts: Partial<Record<MoodKey, number>>
    recurring_themes: ThemeCount[]
    understanding_avg: number | null
    resonance_avg: number | null
    open_threads: number
  }
  insights: ProfileInsights | null
  /** A gentle pointer to support, when the server thinks one is warranted. */
  support: { message: string } | null
  /** "Reflection, not diagnosis" wording; always shown next to the insights. */
  disclaimer: string
}

export interface ProfilePatch {
  life_stage?: string | null
  situations?: string[]
  faith_background?: string | null
  needs?: string[]
  /** At most three. */
  desired_traits?: string[]
  about_me?: string
}

export interface AssessmentPayload {
  answers: Record<string, number>
  trait_ratings: Record<string, number>
}

const params = () => ({ lang: guidesLang() })

export async function getGrowthProfile(): Promise<GrowthProfile> {
  const response = await client.get('/guides/profile/', { params: params() })
  return response.data
}

export async function updateGrowthProfile(patch: ProfilePatch): Promise<GrowthProfile> {
  const response = await client.patch('/guides/profile/', patch, { params: params() })
  return response.data
}

/** Save self-assessment answers. Partial answers are fine. */
export async function submitAssessment(payload: AssessmentPayload): Promise<GrowthProfile> {
  const response = await client.post('/guides/profile/assessment/', payload, { params: params() })
  return response.data
}

/** Ask the AI to (re)write the reflection. Can take a couple of minutes on a local model. */
export async function generateProfileInsights(): Promise<GrowthProfile> {
  const response = await client.post('/guides/profile/insights/', null, {
    params: params(),
    timeout: AI_TIMEOUT_MS,
  })
  return response.data
}

/** Tell the app whether one statement is right. `null` clears the answer. */
export async function sendInsightFeedback(insightId: string, accurate: boolean | null): Promise<GrowthProfile> {
  const response = await client.post(
    `/guides/profile/insights/${encodeURIComponent(insightId)}/feedback/`,
    { accurate },
    { params: params() },
  )
  return response.data
}

/** Erase the profile, assessment history and insights. Studies, plans and journal entries are kept. */
export async function eraseGrowthProfile(): Promise<void> {
  await client.delete('/guides/profile/')
}
