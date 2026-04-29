import client from './client'

// Types
export interface FocusIntention {
  id: string
  period_type: 'day' | 'week' | 'month'
  period_start: string
  period_end: string
  intention_text: string
  themes: string[]
  related_life_areas: string[]
  status: 'active' | 'completed' | 'expired'
  passages_generated: boolean
  is_active: boolean
  passages_count: number
  created_at: string
  updated_at: string
}

export interface DevotionalPassage {
  id: string
  focus_intention: string
  sequence_number: number
  scheduled_date: string
  scripture_reference: string
  scripture_text: string
  translation: string
  stylized_quote: string
  context_note: string
  connection_to_focus: string
  reflection_prompts: string[]
  application_suggestions: string[]
  is_read: boolean
  read_at: string | null
  user_reflection: string
  reflection_saved_at: string | null
  created_at: string
}

export interface StudyPlanDay {
  day: number
  focus: string
  scripture: string
  practice: string
  journal_prompt: string
}

export interface StudyGuide {
  source_type: string
  source_reference: string
  title: string
  insight_summary: string
  analytical_insights: string[]
  heart_check_questions: string[]
  study_plan: StudyPlanDay[]
  prayer_focus: string
  next_step: string
  study_session_id?: string
  study_progress?: {
    status: 'active' | 'completed' | 'archived'
    total_days: number
    completed_days: number[]
    next_day: number | null
    progress_percentage: number
  }
}

export interface TodayDevotional {
  active_intentions: FocusIntention[]
  todays_passages: DevotionalPassage[]
  has_daily_focus: boolean
  has_weekly_focus: boolean
  has_monthly_focus: boolean
}

export interface CreateFocusIntentionInput {
  period_type: 'day' | 'week' | 'month'
  intention: string
  journey_id?: string
}

// API Functions
export const getFocusIntentions = async (): Promise<FocusIntention[]> => {
  const response = await client.get('/focus/')
  return response.data
}

export const getActiveFocusIntentions = async (): Promise<FocusIntention[]> => {
  const response = await client.get('/focus/active/')
  return response.data
}

export const getTodayDevotional = async (): Promise<TodayDevotional> => {
  const response = await client.get('/focus/today/')
  return response.data
}

export const createFocusIntention = async (data: CreateFocusIntentionInput): Promise<FocusIntention> => {
  const response = await client.post('/focus/', data)
  return response.data
}

export const completeFocusIntention = async (id: string): Promise<FocusIntention> => {
  const response = await client.post(`/focus/${id}/complete/`)
  return response.data
}

export const getFocusIntentionPassages = async (id: string): Promise<DevotionalPassage[]> => {
  const response = await client.get(`/focus/${id}/passages/`)
  return response.data
}

export const getDevotionalPassages = async (): Promise<DevotionalPassage[]> => {
  const response = await client.get('/passages/')
  return response.data
}

export const getTodayPassages = async (): Promise<DevotionalPassage[]> => {
  const response = await client.get('/passages/today/')
  return response.data
}

export const getUpcomingPassages = async (): Promise<DevotionalPassage[]> => {
  const response = await client.get('/passages/upcoming/')
  return response.data
}

export const markPassageRead = async (id: string): Promise<DevotionalPassage> => {
  const response = await client.post(`/passages/${id}/mark_read/`)
  return response.data
}

export const savePassageReflection = async (id: string, reflection: string): Promise<DevotionalPassage> => {
  const response = await client.post(`/passages/${id}/reflect/`, { reflection })
  return response.data
}

export const generatePassageDeepDive = async (id: string, context?: string): Promise<StudyGuide> => {
  const response = await client.post(`/passages/${id}/deep_dive/`, {
    context: context || '',
  })
  return response.data
}
