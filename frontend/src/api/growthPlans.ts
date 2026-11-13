/**
 * Growth plans API (`/guides/plans/`): one characteristic a person chose to
 * grow in, with short- and long-term goals and weekly check-ins.
 *
 * Kept apart from `plans.ts`, which is the (unrelated) reading-plans API.
 */
import client, { AI_TIMEOUT_MS } from './client'
import { guidesLang, type TopicCard } from './guides'

export type GrowthPlanStatus = 'active' | 'paused' | 'completed'
export type GoalHorizon = 'short' | 'long'
export type GoalStatus = 'active' | 'done' | 'skipped'
export type GoalKind = 'practice' | 'study' | 'reflection' | 'prayer'

export interface GrowthGoal {
  id: string
  horizon: GoalHorizon
  title: string
  kind: GoalKind
  target_count: number
  progress_count: number
  percent: number
  due_date: string | null
  status: GoalStatus
  overdue: boolean
  /** Counted automatically from completed lessons: no manual "+1". */
  auto: boolean
}

export interface GrowthCheckIn {
  id: string
  date: string
  rating: number
  note: string
}

export interface PlanNotice {
  code: string
  message: string
  suggestion?: string | null
}

export interface GrowthPlanProgress {
  percent: number
  stage: 'starting' | 'building' | 'steady' | 'established'
  stage_label: string
  short_percent: number
  long_percent: number
  goals_done: number
  goals_total: number
  rating_change: number | null
  days_in: number
  days_total: number
  lessons_done: number
  check_in_due: boolean
  summary: string
}

export interface GrowthPlan {
  id: string
  trait: { key: string; title: string; definition: string }
  why: string
  status: GrowthPlanStatus
  started_at: string
  target_date: string | null
  baseline_rating: number | null
  current_rating: number | null
  scripture: { reference: string }[]
  jesus: { reference: string; note: string }
  check_in_question: string
  /** Studies that build this characteristic. */
  topics: TopicCard[]
  goals: GrowthGoal[]
  /** Newest first. */
  checkins: GrowthCheckIn[]
  goal_source: 'catalog' | 'ai'
  /** Why the goals could not be tailored by AI, when that was asked for. A notice, not a failure. */
  personalize_error: PlanNotice | null
  progress: GrowthPlanProgress
}

export interface CreateGrowthPlanPayload {
  trait: string
  why?: string
  baseline_rating?: number
  personalize?: boolean
}

export interface NewGoalPayload {
  title: string
  horizon: GoalHorizon
  target_count: number
  days: number
}

export interface GoalPatch {
  add?: number
  progress_count?: number
  status?: GoalStatus
  title?: string
}

const params = () => ({ lang: guidesLang() })
const planUrl = (planId: string) => `/guides/plans/${encodeURIComponent(planId)}/`
const goalUrl = (planId: string, goalId: string) => `${planUrl(planId)}goals/${encodeURIComponent(goalId)}/`

export async function listGrowthPlans(): Promise<GrowthPlan[]> {
  const response = await client.get('/guides/plans/', { params: params() })
  return response.data
}

export async function createGrowthPlan(payload: CreateGrowthPlanPayload): Promise<GrowthPlan> {
  const response = await client.post('/guides/plans/', payload, {
    params: params(),
    // Tailoring the goals waits on an AI model.
    ...(payload.personalize ? { timeout: AI_TIMEOUT_MS } : {}),
  })
  return response.data
}

export async function getGrowthPlan(planId: string): Promise<GrowthPlan> {
  const response = await client.get(planUrl(planId), { params: params() })
  return response.data
}

export async function updateGrowthPlan(
  planId: string,
  patch: { status?: GrowthPlanStatus; why?: string },
): Promise<GrowthPlan> {
  const response = await client.patch(planUrl(planId), patch, { params: params() })
  return response.data
}

export async function deleteGrowthPlan(planId: string): Promise<void> {
  await client.delete(planUrl(planId))
}

export async function addGrowthGoal(planId: string, goal: NewGoalPayload): Promise<GrowthPlan> {
  const response = await client.post(`${planUrl(planId)}goals/`, goal, { params: params() })
  return response.data
}

export async function updateGrowthGoal(planId: string, goalId: string, patch: GoalPatch): Promise<GrowthPlan> {
  const response = await client.patch(goalUrl(planId, goalId), patch, { params: params() })
  return response.data
}

export async function deleteGrowthGoal(planId: string, goalId: string): Promise<GrowthPlan> {
  const response = await client.delete(goalUrl(planId, goalId), { params: params() })
  return response.data
}

export async function addGrowthCheckIn(
  planId: string,
  checkIn: { rating: number; note?: string },
): Promise<GrowthPlan> {
  const response = await client.post(`${planUrl(planId)}checkins/`, checkIn, { params: params() })
  return response.data
}
