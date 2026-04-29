import client from './client'

// Types
export interface LifeArea {
  code: string
  name: string
  description: string
  icon: string
  scripture_tags: string[]
  reflection_prompts: string[]
  display_order: number
}

export interface UserJourney {
  id: string
  title: string
  goal_statement: string
  success_definition: string
  focus_areas: string[]
  duration_days: number
  current_day: number
  status: 'active' | 'paused' | 'completed' | 'abandoned'
  started_at: string
  completed_at: string | null
  progress_percentage: number
  days_remaining: number
}

export interface CreateJourneyData {
  title: string
  goal_statement: string
  success_definition: string
  focus_areas: string[]
  duration_days: number
  goal_categories?: string[]
  reading_mode?: 'ai_suggested' | 'self_directed' | 'hybrid'
}

export interface DailyReflection {
  id: string
  date: string
  scripture_reference: string
  scripture_themes: string[]
  reflection_content: string
  area_scores: Record<string, number>
  gratitude_note: string
  struggle_note: string
  tomorrow_intention: string
  ai_insight: string
  ai_provider_used: string
  created_at: string
}

export interface CreateReflectionData {
  date: string
  scripture_reference: string
  reflection_content: string
  area_scores: Record<string, number>
  gratitude_note?: string
  struggle_note?: string
  tomorrow_intention?: string
}

export interface AlignmentTrend {
  id: string
  period_type: 'week' | 'month'
  period_start: string
  period_end: string
  area_averages: Record<string, number>
  area_deltas: Record<string, number>
  overall_average: number
  reflection_count: number
}

export interface OpenThread {
  id: string
  thread_type: 'struggle' | 'commitment' | 'question' | 'relationship' | 'decision' | 'confession'
  summary: string
  original_context: string
  related_life_area: string
  status: 'open' | 'following_up' | 'progressing' | 'resolved' | 'deferred' | 'dropped'
  created_at: string
  days_since_mentioned: number
  followup_count: number
  skip_count: number
}

export interface ThreadPrompt {
  thread_id: string
  prompt: string
  thread_type: string
  days_since_mentioned: number
  response_options: string[]
}

export interface TodayContext {
  date: string
  scripture: {
    reference: string
    theme: string
    day: number
  } | null
  existing_reflection: DailyReflection | null
  journey: UserJourney | null
  thread_prompts: ThreadPrompt[]
}

export interface CrewHealth {
  status: 'healthy' | 'unhealthy'
  base_url: string
  model: string
  model_available: boolean
  available_models?: string[]
}

// Life Areas API
export const lifeAreasApi = {
  list: () => client.get<LifeArea[]>('/life-areas/'),
  get: (code: string) => client.get<LifeArea>(`/life-areas/${code}/`),
}

// Journeys API
export const journeysApi = {
  list: () => client.get<UserJourney[]>('/journeys/'),
  get: (id: string) => client.get<UserJourney>(`/journeys/${id}/`),
  create: (data: CreateJourneyData) => client.post<UserJourney>('/journeys/', data),
  getActive: () => client.get<UserJourney>('/journeys/active/'),
  advanceDay: (id: string) => client.post<UserJourney>(`/journeys/${id}/advance_day/`),
  complete: (id: string) => client.post<UserJourney>(`/journeys/${id}/complete/`),
  pause: (id: string) => client.post<UserJourney>(`/journeys/${id}/pause/`),
  resume: (id: string) => client.post<UserJourney>(`/journeys/${id}/resume/`),
}

// Reflections API
export const reflectionsApi = {
  list: () => client.get<DailyReflection[]>('/reflections/'),
  get: (id: string) => client.get<DailyReflection>(`/reflections/${id}/`),
  create: (data: CreateReflectionData) => client.post<DailyReflection>('/reflections/', data),
  update: (id: string, data: Partial<CreateReflectionData>) => 
    client.patch<DailyReflection>(`/reflections/${id}/`, data),
  getToday: () => client.get<TodayContext>('/reflections/today/'),
  getByDate: (date: string) => client.get<DailyReflection>(`/reflections/by-date/${date}/`),
  generateInsight: (id: string) => 
    client.post<{ insight: string; provider: string }>(`/reflections/${id}/generate_insight/`),
}

// Trends API
export const trendsApi = {
  list: () => client.get<AlignmentTrend[]>('/trends/'),
  getWeekly: () => client.get<AlignmentTrend[]>('/trends/weekly/'),
  getMonthly: () => client.get<AlignmentTrend[]>('/trends/monthly/'),
  getByArea: (areaCode: string) => client.get<AlignmentTrend[]>(`/trends/by-area/${areaCode}/`),
}

// Threads API
export const threadsApi = {
  list: () => client.get<OpenThread[]>('/threads/'),
  get: (id: string) => client.get<OpenThread>(`/threads/${id}/`),
  create: (data: { thread_type: string; summary: string; related_life_area?: string }) =>
    client.post<OpenThread>('/threads/', data),
  getActive: () => client.get<OpenThread[]>('/threads/active/'),
  getNeedingFollowup: () => client.get<{ prompts: ThreadPrompt[] }>('/threads/needing_followup/'),
  getStats: () => client.get<Record<string, number>>('/threads/stats/'),
  resolve: (id: string, resolution_note?: string) =>
    client.post<OpenThread>(`/threads/${id}/resolve/`, { resolution_note }),
  defer: (id: string, days?: number) =>
    client.post<OpenThread>(`/threads/${id}/defer/`, { days }),
  drop: (id: string) => client.post<OpenThread>(`/threads/${id}/drop/`),
  respond: (data: { thread_id: string; response: string; expanded_text?: string; reflection_id?: string }) =>
    client.post('/threads/respond/', data),
}

// AI Crew API
export const crewApi = {
  health: () => client.get<CrewHealth>('/crew/health/'),
  weeklyReview: () => client.post<{ review: string; type: string; provider: string }>('/crew/weekly-review/'),
  monthlyRecap: () => client.post<{ recap: string; type: string; provider: string }>('/crew/monthly-recap/'),
  askAgent: (agent: string, prompt: string, context?: Record<string, unknown>) =>
    client.post<{ response: string; agent: string; provider: string }>('/crew/ask-agent/', {
      agent,
      prompt,
      context,
    }),
}
