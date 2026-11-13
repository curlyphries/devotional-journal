/**
 * Bible study guide API (`/guides/…`): the catalog of studies, what is
 * suggested for this person and why, and the studies they have started.
 *
 * Every call sends `?lang=` so the server answers in the UI language; all text
 * in the responses is already translated.
 */
import i18next from 'i18next'
import client, { AI_TIMEOUT_MS } from './client'

// ---------------------------------------------------------------------------
// Shared vocabulary
// ---------------------------------------------------------------------------

export type LifeStageKey = 'child' | 'teen' | 'young_adult' | 'adult' | 'senior'

/** An error the server folded into a successful response: what happened and what to do. */
export interface GuideNotice {
  code: string
  message: string
  suggestion?: string | null
}

export interface TopicEnrollment {
  /** Id of the person's study of this topic. */
  id: string
  status: 'active' | 'completed'
  current_lesson: number
  completed_lessons: number[]
}

/** One study in the library, as shown on a card. Shared with the profile and growth-plan pages. */
export interface TopicCard {
  key: string
  category: string
  title: string
  summary: string
  lesson_count: number
  /** Life stages this study is written for. */
  stages: string[]
  /** Character traits this study builds. */
  traits: string[]
  /** Touches on painful things (grief, abuse, addiction…): show a gentle care marker. */
  sensitive: boolean
  /** How the topic meets the person's life stage. */
  stage_note: string | null
  /** The person's own study of this topic, if they have one. */
  enrollment: TopicEnrollment | null
}

// ---------------------------------------------------------------------------
// Catalog and recommendations
// ---------------------------------------------------------------------------

export interface LifeStage {
  key: string
  title: string
  note: string
}

export interface CatalogCategory {
  key: string
  title: string
  summary: string
  topics: TopicCard[]
}

export interface CatalogTrait {
  key: string
  title: string
  definition: string
}

export interface AssessmentItem {
  key: string
  area: 'practices' | 'inner'
  text: string
}

export interface Catalog {
  life_stages: LifeStage[]
  situations: { key: string; title: string }[]
  faith_backgrounds: { key: string; title: string }[]
  categories: CatalogCategory[]
  traits: CatalogTrait[]
  assessment: { scale: string; items: AssessmentItem[] }
}

export interface Recommendation {
  topic: TopicCard
  score: number
  /** Human sentences saying why this is suggested. Always shown. */
  reasons: string[]
}

export interface Recommendations {
  based_on: { entries_considered: number; has_profile: boolean }
  results: Recommendation[]
}

/** The little of the growth profile the study pages need. */
export interface ProfileBasics {
  exists: boolean
  life_stage: string | null
}

// ---------------------------------------------------------------------------
// Studies and lessons
// ---------------------------------------------------------------------------

export interface Study {
  id: string
  topic: { key: string; title: string; category: string; sensitive: boolean }
  life_stage: string | null
  status: 'active' | 'completed'
  current_lesson: number
  lesson_count: number
  completed_lessons: number[]
  progress_percent: number
  started_at: string
  completed_at: string | null
}

export interface StudyLessonSummary {
  number: number
  title: string
  reference: string
  completed: boolean
}

export interface StudyDetail extends Study {
  stage_note: string | null
  summary: string
  lessons: StudyLessonSummary[]
}

export interface LessonPassage {
  reference: string
  /** Fetched from the Bible source — never written by the AI. */
  text: string
  translation: string
  translation_name: string
  verified: boolean
  source: string
}

export interface LessonPersonal {
  connection: string
  explanation: string
  questions: string[]
  provider: string
  model: string
  local: boolean
  created_at: string
}

export interface LessonReply {
  text: string
  follow_up: string | null
  /** "built_in" = the AI was unavailable and a prepared reply was used. */
  source: 'ai' | 'built_in'
  fallback_reason: GuideNotice | null
}

export interface LessonAnswer {
  question: string
  answer: string
}

export interface LessonResponse {
  answers: LessonAnswer[]
  stood_out: string
  understanding: number
  resonance: number
  reply: LessonReply | null
  completed_at: string
}

export interface Lesson {
  study_id: string
  /** 1-based. */
  number: number
  lesson_count: number
  title: string
  topic: { key: string; title: string }
  passage: LessonPassage | null
  /** The Bible text could not be fetched; the reference is still shown. */
  passage_error: GuideNotice | null
  reference: string
  explanation: string
  explanation_level: 'standard' | 'simple'
  questions: string[]
  practice: string
  prayer: string
  /** Child stage: meant to be read together with a grown-up. */
  with_grown_up: boolean
  /** Sensitive topics: a gentle "you don't have to carry this alone" note. */
  support_note: string | null
  personal: LessonPersonal | null
  response: LessonResponse | null
  previous: { number: number } | null
  next: { number: number } | null
}

export interface LessonAnswersPayload {
  answers: LessonAnswer[]
  stood_out: string
  understanding: number
  resonance: number
}

export type LessonNextStep =
  | { kind: 'next_lesson'; number: number }
  | { kind: 'study_complete'; suggestions: TopicCard[] }

export interface LessonResult {
  lesson: Lesson
  reply: LessonReply
  study: Study
  next_step: LessonNextStep
}

// ---------------------------------------------------------------------------
// Requests
// ---------------------------------------------------------------------------

/** The `lang` query parameter the guides endpoints expect. */
export function guidesLang(): 'en' | 'es' {
  return i18next.language?.startsWith('es') ? 'es' : 'en'
}

const params = () => ({ lang: guidesLang() })
const studyUrl = (studyId: string) => `/guides/studies/${encodeURIComponent(studyId)}/`
const lessonUrl = (studyId: string, lesson: number) => `${studyUrl(studyId)}lessons/${lesson}/`

/**
 * React Query keys. Everything lives under `['guides']`, so
 * `invalidateQueries({ queryKey: guidesKeys.all })` refreshes all of it after a
 * change that moves suggestions, enrolment and progress at once.
 */
export const guidesKeys = {
  all: ['guides'] as const,
  catalog: (lang: string) => ['guides', 'catalog', lang] as const,
  recommendations: (lang: string) => ['guides', 'recommendations', lang] as const,
  profileBasics: () => ['guides', 'profile-basics'] as const,
  studies: (lang: string) => ['guides', 'studies', lang] as const,
  study: (studyId: string, lang: string) => ['guides', 'study', studyId, lang] as const,
  lesson: (studyId: string, lesson: number, lang: string) => ['guides', 'lesson', studyId, lesson, lang] as const,
}

export const getCatalog = async (): Promise<Catalog> => {
  const response = await client.get('/guides/catalog/', { params: params() })
  return response.data
}

export const getRecommendations = async (): Promise<Recommendations> => {
  const response = await client.get('/guides/recommendations/', { params: params() })
  const body = (response.data ?? {}) as Partial<Recommendations>
  return {
    based_on: body.based_on ?? { entries_considered: 0, has_profile: false },
    results: Array.isArray(body.results) ? body.results : [],
  }
}

/** Whether the person has a growth profile, and their life stage. */
export const getProfileBasics = async (): Promise<ProfileBasics> => {
  const response = await client.get('/guides/profile/', { params: params() })
  const body = (response.data ?? {}) as Partial<ProfileBasics>
  return { exists: !!body.exists, life_stage: body.life_stage ?? null }
}

/** Save who the studies are for. Changes which studies are suggested and shown. */
export const setLifeStage = async (lifeStage: string): Promise<ProfileBasics> => {
  const response = await client.patch('/guides/profile/', { life_stage: lifeStage }, { params: params() })
  const body = (response.data ?? {}) as Partial<ProfileBasics>
  return { exists: body.exists ?? true, life_stage: body.life_stage ?? lifeStage }
}

/** The person's studies, newest first. */
export const getStudies = async (): Promise<Study[]> => {
  const response = await client.get('/guides/studies/', { params: params() })
  const data = response.data
  return Array.isArray(data) ? data : Array.isArray(data?.results) ? data.results : []
}

/** Start a study of a topic. Returns the existing one when it is already in progress. */
export const startStudy = async (topic: string, lifeStage?: string | null): Promise<Study> => {
  const body: { topic: string; life_stage?: string } = { topic }
  if (lifeStage) body.life_stage = lifeStage
  const response = await client.post('/guides/studies/', body, { params: params() })
  return response.data
}

export const getStudy = async (studyId: string): Promise<StudyDetail> => {
  const response = await client.get(studyUrl(studyId), { params: params() })
  return response.data
}

/** Leave a study: removes it and the answers written in it. */
export const leaveStudy = async (studyId: string): Promise<void> => {
  await client.delete(studyUrl(studyId), { params: params() })
}

export const getLesson = async (studyId: string, lesson: number): Promise<Lesson> => {
  const response = await client.get(lessonUrl(studyId, lesson), { params: params() })
  return response.data
}

/** Save the answers to a lesson. The reply may be written by AI, so this can take a while. */
export const respondToLesson = async (
  studyId: string,
  lesson: number,
  payload: LessonAnswersPayload
): Promise<LessonResult> => {
  const response = await client.post(`${lessonUrl(studyId, lesson)}respond/`, payload, {
    params: params(),
    timeout: AI_TIMEOUT_MS,
  })
  return response.data
}

/** Switch the lesson to its simpler explanation (remembered by the server). */
export const simplifyLesson = async (studyId: string, lesson: number): Promise<Lesson> => {
  const response = await client.post(`${lessonUrl(studyId, lesson)}simplify/`, null, { params: params() })
  return response.data
}

/** Ask the AI to connect the lesson to the person's own life. May fail with AI_* codes. */
export const personalizeLesson = async (studyId: string, lesson: number): Promise<Lesson> => {
  const response = await client.post(`${lessonUrl(studyId, lesson)}personalize/`, null, {
    params: params(),
    timeout: AI_TIMEOUT_MS,
  })
  return response.data
}
