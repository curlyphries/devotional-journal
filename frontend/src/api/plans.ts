import client from './client'

export interface ReadingPlan {
  id: string
  title: string
  description: string
  duration_days: number
  category: string
  is_premium: boolean
  is_public: boolean
  is_owned: boolean
}

/** A passage as stored on a plan day: a reference string, or a structured reference. */
export type PlanPassage = string | { book: string; chapter: number; verses?: string }

export interface ReadingPlanDay {
  /** Present on plan detail; today's-reading responses may omit it. */
  id?: string
  day_number: number
  passages: PlanPassage[]
  theme: string
  /** Present on plan detail only. */
  reflection_prompts_seed?: string | null
}

/** Human-readable reference for a plan passage, e.g. "Psalm 23:1-6". */
export function formatPlanPassage(passage: PlanPassage): string {
  if (typeof passage === 'string') return passage
  const verses = passage.verses ? `:${passage.verses}` : ''
  return `${passage.book || ''} ${passage.chapter || ''}${verses}`.trim()
}

export interface ReadingPlanDetail extends ReadingPlan {
  days: ReadingPlanDay[]
}

export interface UserPlanEnrollment {
  id: string
  plan: ReadingPlan
  started_at: string
  current_day: number
  completed_at: string | null
  is_active: boolean
  progress_percentage: number
}

export interface TodayReading {
  enrollment: UserPlanEnrollment
  day: ReadingPlanDay
}

export const getPlans = async (category?: string): Promise<ReadingPlan[]> => {
  const params = category ? { category } : {}
  const response = await client.get('/plans/', { params })
  return response.data
}

export const getPlanDetail = async (planId: string): Promise<ReadingPlanDetail> => {
  const response = await client.get(`/plans/${planId}/`)
  return response.data
}

export const enrollInPlan = async (planId: string): Promise<UserPlanEnrollment> => {
  const response = await client.post(`/plans/${planId}/enroll/`)
  return response.data
}

export const getEnrolledPlans = async (activeOnly?: boolean): Promise<UserPlanEnrollment[]> => {
  const params = activeOnly ? { active: 'true' } : {}
  const response = await client.get('/plans/enrolled/', { params })
  return response.data
}

export const getTodayReading = async (enrollmentId: string): Promise<TodayReading> => {
  const response = await client.get(`/plans/enrolled/${enrollmentId}/today/`)
  return response.data
}

export const advanceDay = async (enrollmentId: string): Promise<{ message: string; enrollment: UserPlanEnrollment }> => {
  const response = await client.post(`/plans/enrolled/${enrollmentId}/advance/`)
  return response.data
}

export const deletePlan = async (planId: string): Promise<void> => {
  await client.delete(`/plans/${planId}/delete/`)
}
