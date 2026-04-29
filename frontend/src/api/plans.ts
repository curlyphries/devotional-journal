import client from './client'

export interface ReadingPlan {
  id: string
  title: string
  description: string
  duration_days: number
  category: string
  is_premium: boolean
}

export interface ReadingPlanDay {
  day_number: number
  passages: string[]
  theme: string
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
